import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        self.verbose = verbose
        self.s = 0
        self.a = 0
        self.q_table = np.zeros((num_states, num_actions))
        self.T_c = np.zeros((num_states, num_actions, num_states)) + 1e-5
        self.T = np.zeros((num_states, num_actions, num_states))
        self.R = np.zeros((num_states, num_actions))


    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        random = np.random.random_sample()

        if random < self.rar:
            action = rand.randint(0, self.num_actions-1)
        else:
            # pick action with best Q value
            action = np.argmax(self.q_table[s])

        self.a = action
        self.s = s

        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The reward
        @returns: The selected action
        """
        # update Q table
        self.q_table[self.s, self.a] += \
        self.alpha *(r + self.gamma * np.amax(self.q_table[s_prime]) - self.q_table[self.s, self.a])

        random = np.random.random_sample()

        # increment T_c, update T, update R
        self.T_c[self.s, self.a, s_prime] += 1
        self.R[self.s, self.a] = (1-self.alpha) * self.R[self.s, self.a] + self.alpha * r

        # do some Dyna
        for i in range(self.dyna):
            s_rand = rand.randint(0, self.num_states-1)
            a_rand = rand.randint(0, self.num_actions-1)
            # infer next state from T
            next_state = np.argmax(self.T_c[s_rand, a_rand])
            # get reward
            r_dyna = self.R[s_rand, a_rand]
            # update Q table
            self.q_table[s_rand, a_rand] += \
            self.alpha *(r_dyna + self.gamma * np.amax(self.q_table[next_state]) - self.q_table[s_rand, a_rand])

        if random < self.rar:
            action = rand.randint(0, self.num_actions-1)
        else:
            # pick action with best Q value
            action = np.argmax(self.q_table[s_prime])

        self.rar *= self.radr
        self.a = action
        self.s = s_prime

        return action

    def author(self):
        return 'kkc3'

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
