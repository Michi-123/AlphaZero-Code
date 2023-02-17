#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @title Agent

import random
import copy 
from .Util import Util
from .MCTS import MCTS
from .Node import Node

class Agent:

    def __init__(self, env):
        self.env = env
    
    def reset():
        pass
    
    def step(a):
        pass
    
    
class AlphaZero:
    def __init__(self, CFG, env, model, train=True):
        self.mcts = MCTS(env, model, CFG, train)
        # self.input_features = None

    def __call__(self, node):
        next_node = self.mcts(node)
        # self.input_features = self.mcts.input_features
        return next_node

class Human:
    def __init__(self, env):
        self.env = env

    def __call__(self, legal_actions):

        print([(a//self.env.lines, a%self.env.lines) for a in legal_actions])
        while True:
            x = input('縦, 横 ')
            action = self._coordinate2action(x)
            if action in legal_actions:
                break

        # next_node = self.util.get_next_node(node, action)

        return action

    def _coordinate2action(self, x):
        x1, x2 = x.split(' ')
        x1, x2 = int(x1), int(x2)
        action = x1 * self.env.lines + x2
        return action


class RandomPlayer:
    def __init__(self, env):
        self.env = env

    def __call__(self, legal_actions):
        action = random.choice(legal_actions)
        return action

""" 
Minimaxプレーヤーで最善の手を取得 
"""
class MiniMax:

    def __init__(self, env):
        self.env = env

    def __call__(self, node, player):

        """ 
        Minimax アルゴリズム 
        """
        def minimax(env, player):

            """ ゲーム終了の場合 """
            if env.done:
                # print('reward', env.reward)
                return env.reward # 報酬: -1, 0, 1
        
            """ 合法手の取得 """
            legal_actions = env.get_legal_actions(env.state)

            """
            先手にとっては最大となる価値（報酬）を選ばせ、
            後手にとっては最小となる価値（報酬）を選ばせる。
            """
            if player == 1:
                """ 先手プレーヤー """
                value = -float('inf') # 状態価値に−∞を設定 float('inf')

                """ 合法手で最大値を取得 """
                for action in legal_actions: 
                    child = copy.deepcopy(env) # 環境のコピー
                    child.step(action) # 実行
                    value = max(value, minimax(child, -player)) # 現在の価値とminimaxの価値のうち大きい方を取得
                # return value # 最大値を返却
                return value / 2 

            else:
                """ 後手プレーヤー """
                value = float('inf') # ∞
        
                """ 合法手で最小値を取得 """
                for action in legal_actions:
                    child = copy.deepcopy(env)
                    child.step(action)
                    value = min(value, minimax(child, -player))
                # return value # 最小値を返却
                return value / 2


        """ 最善手と状態価値を初期化 """
        best_action = 0 # 行動インデックスの初期化
        best_value = -float('inf') # 最善の手を-∞で初期化

        """ 合法手の取得 """
        legal_actions = env.get_legal_actions(env.state)
        # print('legal_actions', legal_actions)

        """ 合法手でループ """
        for action in legal_actions:

            child = copy.deepcopy(env) # 環境のコピー
            child.step(action) # 実行

            """ 
            mini-maxアルゴリズムで探索して、状態価値を取得。
            後手の価値を先手にとってはマイナスの価値とする。
            """
            value = -minimax(child, -player) 

            """ 取得した価値が最善の場合よりも大きい場合は値を交換 """
            if value > best_value:
                best_value = value # 取得した価値を最善の価値に設定
                best_action = action # その場合の行動を最善の行動とする 

            # print('action: ', action ,value)

        # print('best_action', best_action)
        return best_action # 最善の行動インデックスを返却


class AlphaBeta:
    def __init__(self, env):
        self.env = env
    """
    Alpha-betaプレーヤーで最善の手を取得 
    """
    def __call__(self, node, player):

        """ 
        Alpha–beta pruning
        """
        def alphabeta(env, α, β, player):

            """ ゲーム終了の場合 """
            if env.done:
                # print('reward', env.reward)
                return env.reward # 報酬: -1, 0, 1
        
            """ 合法手の取得 """
            legal_actions = env.get_legal_actions(env.state)

            """
            先手にとっては最大となる価値（報酬）を選ばせ、
            後手にとっては最小となる価値（報酬）を選ばせる。
            """
            if player == 1:

                value = -float('inf') # 状態価値に−∞を設定 float('inf')

                """ 合法手で最大値を取得 """
                for action in legal_actions: 
                    child = copy.deepcopy(env) # 環境のコピー
                    child.step(action) # コピーで実行
                    value = max(value, alphabeta(child, α, β, -player)) # 現在の価値とalphabetaの価値のうち大きい方を取得
                    if value >= β:
                        # print('β cutoff')
                        break
                    α = max(α, value)  # 最大値を返却

                # return value 
                return value / 2

            else:

                value = float('inf') # ∞

                for action in legal_actions: 
                    child = copy.deepcopy(env) # 環境のコピー
                    child.step(action) # コピーで実行
                    value = min(value, alphabeta(child, α, β, -player))
                    if value <= α:
                        # print('α cutoff')
                        break
                    β = min(β, value)
                # return value  
                return value / 2


        """ 最善手と状態価値を初期化 """
        best_action = 0
        best_value = -float('inf')

        """ αとβを初期化 """ 
        α = -float('inf')
        β = float('inf')

        """ 合法手でループ """
        legal_actions = env.get_legal_actions(env.state)
        # print('legal_actions', legal_actions)

        for action in legal_actions:

            child = copy.deepcopy(env)
            child.step(action)

            """ 
            Alpha-betaアルゴリズムで探索して、状態価値を取得。
            後手の価値を先手にとってはマイナスの価値とする。
            """
            value = -alphabeta(child, α, β, -player) 

            """ 取得した価値が最善の場合よりも大きい場合は値を交換 """
            if value > best_value:
                best_value = value   # 取得した価値を最善の価値に設定
                best_action = action # その場合の行動を最善の行動とする 

            # print('action: ', action, value)

        # print('best_action', best_action)
        return best_action # 最善の行動インデックスを返却
