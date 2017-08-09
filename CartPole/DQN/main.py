import gym
import AI
MAX_EPISODE = 10000
MAX_STEP = 500
ENV_NAME = 'CartPole-v0'
TEST_EPISODE = 10
EXPECT_REWARD = 500

env = gym.make(ENV_NAME)
agent = AI.AI(env)

def test():
    global MAX
    total_reward = 0
    for episode in range(TEST_EPISODE):
        state = env.reset()
        while True:
            action = agent.greedy_action(state)
            env.render()
            new_state, reward, done, info = env.step(action)
            total_reward += reward
            if done:
                break
            state = new_state
    print('test result:', total_reward/TEST_EPISODE, ' per episode')

def main():
    for episode in range(MAX_EPISODE):
        print(episode)
        if episode % 500 == 0 and episode > 2000:
            test()
        state = env.reset()
        while True:
            action = agent.egreedy_action(state)
            new_state, reward, done, info = env.step(action)
            agent.update(state, action, reward, new_state, done)
            if done:
                break
            state = new_state

if __name__ == '__main__':
    main()
