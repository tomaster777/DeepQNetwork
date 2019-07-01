import gym
import keras
import matplotlib
import matplotlib.pyplot as plt
from agent import Agent
from itertools import count
import numpy as np

# constants
# ENVIRONMENT = 'Pendulum-v0'
ENVIRONMENT = 'CartPole-v1'
EPISODES = 200
EPSILON_MAX = 1.0
EPSILON_MIN = 0.01
EPSILON_DECAY = 0.0005
DISCOUNT_RATE = 0.999
EXPERIENCE_REPLAY_SIZE = 2000
EXPERIENCE_REPLAY_TRAIN = 20


# build env and get observation and action space size
env = gym.make(ENVIRONMENT)
state = env.reset()
OBSERVATION_SPACE = env.observation_space.shape[0]
ACTION_SPACE = env.action_space.n


def pre_process(state: np.array) -> np.array:
    """parses state so the network can understand it
    
    Arguments:
        state {np.array} -- state to parse
    
    Returns:
        np.array -- parsed state
    """
    processed_state = state
    processed_state = np.array([processed_state])
    return processed_state


# create agent
agent = Agent(OBSERVATION_SPACE, ACTION_SPACE, EPSILON_MAX, EPSILON_MIN, EPSILON_DECAY, 
              DISCOUNT_RATE, EXPERIENCE_REPLAY_SIZE, EXPERIENCE_REPLAY_TRAIN)


# train agent
rewards = []
epsilons = []
for epoch in range(EPISODES):

    # play episode
    episode_reward = 0
    for frame in count():
        
        # let agent take action
        action = agent.choose_action(pre_process(state))
        next_state, reward, done, info = env.step(action)

        # add replay frame to agents memory
        agent.remember(pre_process(state), action, reward, pre_process(next_state), done)

        # update state
        state = next_state

        episode_reward += reward

        # update agent's Q-network
        agent.experience_replay()

        # reset env if done
        if done:
            state = env.reset()
            rewards.append(episode_reward)
            epsilons.append(agent.epsilon * 100)
            print(epoch, episode_reward)
            episode_reward = 0
            break
env.close()

# plot rewards
fig, ax = plt.subplots()
ax.plot(rewards)
ax.plot(epsilons)

ax.set(xlabel='epoch', ylabel='reward')
ax.grid()
plt.show()