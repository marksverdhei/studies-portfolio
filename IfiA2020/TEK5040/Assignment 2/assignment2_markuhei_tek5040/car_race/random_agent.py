import gym

env = gym.make('CarRacing-v0')
observation = env.reset()

for t in range(10000):
    env.render()

    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)

    if done:
        print("Episode finished after {} timesteps".format(t+1))
        break

env.close()
