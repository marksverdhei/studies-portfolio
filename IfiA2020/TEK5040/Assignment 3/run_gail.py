#!/usr/bin/env python



import gym
import numpy as np

import tensorflow as tf
import tensorflow.keras.layers as klayers
import tensorflow.keras.losses as klosses
import tensorflow.keras.optimizers as koptimizers

import matplotlib.pyplot as plt

from common.multiprocessing_env import SubprocVecEnv


###############################################
# Create the Pendulum-v0 environment with gym
#################################################
num_envs = 16
env_name = "Pendulum-v0"

def make_env():
    def _thunk():
        env = gym.make(env_name)
        return env

    return _thunk

envs = [make_env() for i in range(num_envs)]
envs = SubprocVecEnv(envs)

env = gym.make(env_name)


#######################################################
# Define a layer of normal distribution
##########################################################
class ProbabilityDistribution(tf.keras.layers.Layer):
    def __init__(self, name):
        super(ProbabilityDistribution, self).__init__(name=name)
        self.log_std=self.add_weight(name='std', shape=(1,1), trainable=True)


    def call(self, inputs):
        action_mean = inputs[0]
        action=inputs[1]
        self_std=tf.math.exp(self.log_std)
        #log probability for the action for given action mean
        log_prob=-(tf.square(tf.subtract(action,action_mean)))/(2*self_std**2) -tf.math.log(self_std) -0.5*np.log(2*np.pi)

        #Calculate the entropy of normal distribution
        k = np.sqrt(2 * np.pi)
        entropy=0.5 + tf.math.log(k * self_std)
        ones_= tf.ones_like(log_prob)

        return log_prob, entropy*ones_


    def get_std(self):
        return self.log_std


##########################################################################
# Define an actor-critic architecture containing policy and value networks
# as well as  sampling operation from a normal distribution and the surrogate
# loss for the PPO algorithm
##########################################################################
class ActorCritic:
    def __init__(self,ob_shape, ac_shape, hidden_size,eps,ent_coeff,name):
        self.hidden_size=hidden_size
        self.eps=eps
        self.ent_coeff=ent_coeff

        #define inputs
        ob_input=klayers.Input(shape=ob_shape, name='ob_input')
        ac_input = klayers.Input(shape=ac_shape,name='ac_input')
        logpi_old_input=klayers.Input(shape=ac_shape, name='logpi_old_input')
        advs_input=klayers.Input(shape=(1,), name='advs_input')

        #define custom layers
        self.dist=ProbabilityDistribution(name='normal_distribution')
        self.comp_loss =klayers.Lambda(self.comp_actor_loss)
        self.random_normal=klayers.Lambda(self.comp_random_normal)

        #Define the base model
        v_h1= klayers.Dense(self.hidden_size, activation='relu')(ob_input)
        value= klayers.Dense(1, activation=None)(v_h1)
        a_h1= klayers.Dense(self.hidden_size, activation='relu')(ob_input)
        a_out= klayers.Dense(1, activation=None)(a_h1)
        action_sample=self.random_normal(a_out)
        self.model_base=tf.keras.Model(inputs=ob_input, outputs=[a_out, action_sample, value], name=name+'_base')


        #define the probability model
        [a_out, _, value_out] = self.model_base(ob_input)
        log_prob, entropy = self.dist([a_out, ac_input])
        self.model_prob=tf.keras.Model(inputs=[ob_input,ac_input], outputs=[log_prob, entropy, value_out], name=name+'_prob')

        #define the  final model
        ac_input_ = klayers.Input(shape=ac_shape, name='ac_input_')
        ob_input_ = klayers.Input(shape=ob_shape, name='ob_input_')
        [logpi, entropy_, value_] = self.model_prob([ob_input_, ac_input_])
        actor_loss_=self.comp_loss([logpi,logpi_old_input,advs_input,entropy_])

        self.model_final=tf.keras.Model(inputs=[ob_input_,ac_input_,logpi_old_input, advs_input],outputs=[actor_loss_,value_], name=name+'_final')

    def comp_actor_loss(self,tensor):
        logpi=tensor[0]
        logpi_old_input=tensor[1]
        advs_input=tensor[2]
        entropy_=tensor[3]
        ratio = tf.exp(logpi - logpi_old_input)
        surr = ratio * advs_input
        actor_loss = tf.minimum(surr, tf.clip_by_value(ratio, 1 - self.eps, 1 + self.eps) * advs_input)
        actor_loss_=-actor_loss - self.ent_coeff * tf.reduce_mean(entropy_)
        return actor_loss_

    def comp_random_normal(self, a_out):
        action_sample = tf.random.normal(shape=(1, 1), mean=a_out, stddev=tf.math.exp(self.dist.get_std()))
        return action_sample

    def get_models(self):
        return(self.model_base, self.model_prob, self.model_final)



########################################################################
# Implements generalized advantage estimate (GAE).
# This is better version of advantage
########################################################################
def compute_gae(next_value, rewards, masks, values, gamma=0.99, tau=0.95):
    values = values + [next_value]
    gae = 0
    returns = []
    for step in reversed(range(len(rewards))):
        delta = rewards[step] + gamma * values[step + 1] * masks[step] - values[step]
        gae = delta + gamma * tau * masks[step] * gae
        returns.insert(0, gae + values[step])
    return returns



#################################################################################
# Proximal Policy Optimization algorithm, on top of the Actor-Critic architecture
#
############################################################################
class PPO:
    def __init__(self,  ob_shape, ac_shape, lr, hidden_size, eps=0.2, v_coeff=0.5, ent_coeff=0.01):

        self.ob_shape = ob_shape
        self.ac_shape = ac_shape
        self.lr = lr
        self.hidden_size = hidden_size
        self.eps = eps
        self.v_coeff = v_coeff
        self.ent_coeff = ent_coeff

        # current actor critic
        actor_critic=ActorCritic(self.ob_shape, self.ac_shape, self.hidden_size,self.eps, self.ent_coeff, name='pi')
        self.pi_base, self.pi_prob, self.pi_final=actor_critic.get_models()

        # Non trainable old actor critic
        actor_critic_old = ActorCritic(self.ob_shape, self.ac_shape, self.hidden_size,self.eps, self.ent_coeff, name='pi_old')
        self.pi_base_old, self.pi_prob_old, _ = actor_critic_old.get_models()

        self.pi_base.summary()
        self.pi_prob.summary()
        self.pi_final.summary()

        #compile the model
        self.pi_final.compile(
            optimizer=koptimizers.Adam(learning_rate=self.lr),
            # define separate losses for policy logits and value estimate
            loss=[self._action_loss, self._value_loss]
        )


    def _action_loss(self,true_val, pred_val ):
        return tf.reduce_mean(pred_val)

    def _value_loss(self, returns, value):
        return self.v_coeff*klosses.mean_squared_error(returns, value)

    def get_action(self, obs):
        _,action_sample,_= self.pi_base.predict(obs)
        return action_sample

    def get_value(self, obs):
        _, _, value = self.pi_base.predict(obs)
        return value

    def assign_old_pi(self):
        self.pi_prob_old.set_weights(self.pi_prob.get_weights())

    # Train the  PPO actor critic network with a single batch
    def update(self, obs, acs, returns, advs):
        old_pi_prob,_,_=self.pi_prob_old.predict([obs,acs])
        self.pi_final.train_on_batch(x=[obs,acs,old_pi_prob, advs],y=[np.ones_like(returns), returns])



############################################################
#  Generates data for the PPO iterations
###########################################################
def ppo_iter(mini_batch_size, obs, acs, returns, advantage):
    batch_size = obs.shape[0]
    for _ in range(batch_size // mini_batch_size):
        rand_ids = np.random.randint(0, batch_size, mini_batch_size)
        yield (obs[rand_ids, :], acs[rand_ids, :],
               returns[rand_ids, :], advantage[rand_ids, :])




###############################################################
# Test run the model with a random starting point
# and generates state action pairs and the corresponding rewards
################################################################
def test_env(model, vis=False):
    ob = env.reset()
    done = False
    total_reward = 0
    while not done:
        if vis:
            env.render()
        ac = model.get_action(np.expand_dims(ob, axis=0))
        next_ob, reward, done, _ = env.step(ac)
        ob = np.squeeze(next_ob)
        total_reward += reward
    return total_reward



#######################################################
# Load the expert trajectories.
# Expert trajectories are the state-action pairs recorded when a human performs the control task.
# In this task  state is 3 dimensional vector (sin_theta, cos_theta and theta_dot)
# while action is a scalar (
#########################################################
try:
    expert_traj = np.load("expert_traj.npy")
except:
    print("Train, generate and save expert trajectories using ppo algorithm first")
    assert False



###############################################################
# Implements the discriminator class
#
#############################################################
class Discriminator:
    def __init__(self, ob_shape, ac_shape, hidden_size,batch_size,  lr, name='discriminator'):
        super(Discriminator, self).__init__()
        self.ob_shape = ob_shape
        self.ac_shape = ac_shape
        self.hidden_size = hidden_size
        self.batch_size=batch_size
        self.lr = lr
        self.name = name

        self.ones=tf.ones([self.batch_size,1])
        self.zeros=tf.zeros([self.batch_size,1])

        # Defined the combined observation-action input. i.e. first ob_shape[0] elements of each row is the observation
        # vector and the rest (ac_shape[0] elements) is the action vector.
        ob_ac=klayers.Input(shape=[ ob_shape[0] + ac_shape[0]])

        # Base part of the discrimator network,
        d_h1=klayers.Dense(self.hidden_size, activation='tanh', name='dense1')(ob_ac)
        d_h2 = klayers.Dense(self.hidden_size, activation='tanh', name='dense2')(d_h1)
        d_out = klayers.Dense(1, activation=None, name='dense3')(d_h2)

        # discriminator network outputs a reward which is the log probability of the network output
        # for a trajectory input (ie. policy observation-action input)
        reward = - tf.squeeze(tf.math.log(tf.sigmoid(d_out)))

        # Discriminator can output the logits for all observation-action inputs
        expert_out, policy_out = tf.split(d_out, num_or_size_splits=2, axis=0)

        self.model_reward=tf.keras.Model(inputs=ob_ac, outputs=reward)

        self.model_prob=tf.keras.Model(inputs=ob_ac, outputs=[expert_out,policy_out])

        self.model_prob.compile(optimizer=koptimizers.Adam(learning_rate=self.lr),
                                loss=[klosses.BinaryCrossentropy(from_logits=True), klosses.BinaryCrossentropy(from_logits=True)])


    def get_reward(self, _ob_ac):
        reward=self.model_reward.predict(_ob_ac)
        return reward


    def update(self, all_ob_ac):
        # The model outputs [expert_out,policy_out], meaning that we label experts as one and policy as zero
        self.model_prob.train_on_batch(all_ob_ac, [self.ones, self.zeros])



#######################################################
# Gail training procedure starts from here
# First define the training hyper-parameters and then the
# training procedure itself.
#######################################################


############# Hyper parameters ########################
ppo_hidden_size           = 256
discriminator_hidden_size = 128
lr                        = 3e-4
num_steps                 = 20
mini_batch_size           = 5
ppo_epochs                = 4
threshold_reward          = -200

max_frames = 20000
frame_idx  = 0
plot_interval=1000
test_rewards = []



############# Training procedure ###########################
ob_shape = list(envs.observation_space.shape)
ac_shape = list(envs.action_space.shape)

ob = envs.reset()
early_stop = False

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
tf.compat.v1.keras.backend.set_session(tf.compat.v1.Session(config=config))


ppo = PPO( ob_shape, ac_shape, lr, ppo_hidden_size)
discriminator = Discriminator( ob_shape, ac_shape, discriminator_hidden_size, num_envs*num_steps, lr,)



i_update = 0
state = envs.reset()
early_stop = False

fig,ax = plt.subplots(1,1)
ax.set_xlabel('frame_index/plot_interval') ; ax.set_ylabel('reward')

while frame_idx < max_frames and not early_stop:
    i_update += 1

    values    = []
    obs    = []
    acs   = []
    rewards   = []
    masks     = []
    entropy = 0

    for _ in range(num_steps):

        ac = ppo.get_action(ob)
        next_ob, _, done, _ = envs.step(ac)
        reward = discriminator.get_reward(np.concatenate([ob, ac], axis=1))

        value = ppo.get_value(ob)
        values.append(value)
        rewards.append(reward[:, np.newaxis])
        masks.append((1-done)[:, np.newaxis])

        obs.append(ob)
        acs.append(ac)

        ob = next_ob
        frame_idx += 1

        if frame_idx % plot_interval == 0:
            test_reward = np.mean([test_env(ppo) for _ in range(10)])
            test_rewards.append(test_reward)

            ax.plot(range(int(frame_idx / plot_interval)), test_rewards)
            fig.canvas.draw()
            fig.canvas.flush_events()
            plt.pause(0.1)


            if test_reward > threshold_reward: early_stop = True


    next_value = ppo.get_value(next_ob)
    returns = compute_gae(next_value, rewards, masks, values)

    returns = np.concatenate(returns)
    values = np.concatenate(values)
    obs = np.concatenate(obs)
    acs = np.concatenate(acs)
    advantages = returns - values


    # Policy Update
    if i_update % 3 == 0:
        ppo.assign_old_pi()
        for _ in range(ppo_epochs):
            for ob_batch, ac_batch, return_batch, adv_batch in ppo_iter(mini_batch_size, obs, acs, returns, advantages):
                ppo.update(ob_batch, ac_batch, return_batch, adv_batch)

    # Discriminator Update
    expert_ob_ac = expert_traj[np.random.randint(0, expert_traj.shape[0], num_steps * num_envs), :]
    policy_ob_ac = np.concatenate([obs, acs], 1)
    discriminator.update(np.concatenate([expert_ob_ac, policy_ob_ac], axis=0))
print(test_rewards)
