#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  Copyright (c) 2021, Ankit Haldar
#  All rights reserved.
#
#  This source code is licensed under the MIT license found in the
#  LICENSE file in the root directory of this source tree. An additional grant
#  of patent rights can be found in the PATENTS file in the same directory.
#

__author__ = "Ankit 'Helder' Haldar"
__version__ = "0.1"


# imports
from enum import Enum
import numpy as np
import pandas as pd
from tf_agents.environments import tf_py_environment
from tf_agents.networks import q_network
import tensorflow as tf
#   script imports
from tf_env import DogAdventureEnvironment
from dog_maze import DogMaze
# imports

FC_LAYER_PARAMS = [32, 64, 128]


# classes
class DQN():
    """define dqn for training the model"""

    def __init__(self):
        # create environment
        dogEnvironemt = self._initialize_env()

        self.train_env = tf_py_environment.TFPyEnvironment(dogEnvironemt)
        self.eval_env = tf_py_environment.TFPyEnvironment(dogEnvironemt)

        self.q_net = self._define_q_network()

    def _initialize_env(self):
        return DogAdventureEnvironment(DogMaze())

    def _define_q_network(self):
        return q_network.QNetwork(
            input_tensor_spec=self.train_env.observation_spec(),
            action_spec=self.train_env.action_spec(),
            fc_layer_params=FC_LAYER_PARAMS
        )
