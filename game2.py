#!/usr/bin/python3

import random as r
import numpy as np

'''
This code is a simulation of infinitely repeated Stag Hunt with discount factor beta.
Strategic form of the played game (agent 1 on the left, agent 2 on the top):
             a     b
        A | x,x | w,y |
        B | y,w | z,z |
            x>y>=z>w
The game is played infinitely yet there is a possibility of it ending in any given round equal to (1-beta).
Game is symmetrical, so agents are interchangeable (via changing the case of the strategy names).

The aim is to illustrate the benifits of escaping equilibruim _Bb via making sacrifice changing from _b to _a.
It is not a complete simulation featuring actual agents since there is no complex strategic interaction needed:
    -agent 1 plays _B K+S times and then changes to _A until the end of the game;
    -agent 2 plays _b K times and then changes to _a until the end of the game.

In order to prove that this move is worthy, agent 2 must get more than the player remaining in _Bb: during K they get z, during S - w, during N - x.
The only special case is playing with the mixed Nash equilibrium player: during K - y with probability p or z with (1-p),
during S,N - x with p or w with (1-p). Probability p depends on payoffs as p/(1-p)=(x-y)/(z-w) or p=(z-w)/(z-w+x-y).

Player remaining in Bb gets j*z, where j is the number of the last round.
'''

(x, y, z, w) = (3, 2, 1, 0)
betas_rounds = {}


def true_with_prob(prob):
    return r.random() < prob


def test_prob(prob):
    j = 1
    while True:
        if true_with_prob(1 - prob):
            return j
        j += 1


def play_normal(beta, K, S):
    (k, s) = (K, S)
    j = 1
    sum_util = 0
    while True:
        if k > 0:
            sum_util += z
            k -= 1
        elif s > 0:
            sum_util += w
            s -= 1
        else:
            sum_util += x

        if true_with_prob(1 - beta):
            return sum_util >= j * z
        j += 1


def play_vs_MNE(beta, K, S):
    p = (z - w) / (x - y + z - w)
    (k, s) = (K, S)
    sum_util = 0
    b_sum_util = 0
    while True:
        if k > 0:
            if true_with_prob(p):
                sum_util += y
                b_sum_util += y
            else:
                sum_util += z
                b_sum_util += z
            k -= 1
        else:
            if true_with_prob(p):
                sum_util += x
                b_sum_util += y
            else:
                sum_util += w
                b_sum_util += z

        if true_with_prob(1 - beta):
            return sum_util >= b_sum_util


def rounds_from_beta(beta):
    T = 10000
    if beta not in betas_rounds:
        a = 0
        for i in range(T):
            a += test_prob(beta)
        betas_rounds[beta] = a / T
    return int(np.round(betas_rounds[beta], 0))


def sum_condition(K, S, beta):
    N = rounds_from_beta(beta) - (K + S)
    if N <= 0:
        return False

    # inclusive ranges
    left = (x - z) * sum([beta ** j for j in range(K + S + 1, K + S + N + 1)])
    right = (z - w) * sum([beta ** j for j in range(K + 1, K + S + 1)])
    return left >= right


def simulate(beta, times, play):
    total_rounds = rounds_from_beta(beta)
    K_S_winrates = {}

    # both min for unsure is 2, rational - 1
    (k, s) = (2, 2)
    for K in range(k, total_rounds - s):
        for S in range(s, total_rounds - k):
            if sum_condition(K, S, beta):
                wins = 0
                for i in range(times):
                    if play(beta, K, S):
                        wins += 1
                K_S_winrates[(K, S)] = wins / times
            else:
                break
    if not K_S_winrates:
        return None
    return K_S_winrates


def calculate_winrates_for_beta_range(start, stop, step, TIMES, play):
    beta_winrates = {}
    for beta in np.arange(start, stop, step):
        beta_winrates[beta] = simulate(beta, TIMES, play)
    return dict(filter(lambda elem: elem[1] is not None, beta_winrates.items()))


def main():
    TIMES = 10000

    beta_winrates = calculate_winrates_for_beta_range(0.001, 0.999, 0.001, TIMES, play_normal)
    print(beta_winrates)

    # beta_winrates_unsure=calculate_winrates_for_beta_range(0.7,0.999,0.001, TIMES, play_normal) #in simulate k,s=2,2
    # beta_winrates_MNE=calculate_winrates_for_beta_range(0.7,0.999,0.001, TIMES, play_vs_MNE)
    # beta_winrates_rational=calculate_winrates_for_beta_range(0.7,0.999,0.001, TIMES, play_normal) #in simulate k,s=1,1

    return 0


if __name__ == '__main__':
    main()
