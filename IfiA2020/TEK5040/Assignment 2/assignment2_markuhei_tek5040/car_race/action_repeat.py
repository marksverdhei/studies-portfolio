import gym

env = gym.make('CarRacing-v0')
observation = env.reset()

for t in range(10000):
    env.render()

    action_repeat = 4
    reward = 0
    for _ in range(action_repeat):
        observation, r, done, info = env.step(action)
        reward = reward + r

        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break

env.close()
