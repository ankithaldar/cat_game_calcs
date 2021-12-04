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
import numpy as np
import tensorflow as tf
from tf_agents.environments import py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as timeStep
#   script imports
from dog_maze import DogMaze, ActionResult
# imports


# classes
class DogAdventureEnvironment(py_environment.PyEnvironment):

    def __init__(self, game):
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(),
            dtype=np.int32,
            minimum=0,
            maximum=3,
            name='action'
        )
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(36,),
            dtype=np.int32,
            minimum=0,
            maximum=3,
            name='observation'
        )

        # 0=>Left, 1=>Right, 2=>Down, 3=>Up
        self._action_values = {0: -1, 1: 1, 2: -6, 3: 6}
        self._game = game

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        self._game.reset()
        return timeStep.restart(self._game.game_state())

    def _step(self, action):

        if self._game.game_ended():
            return self.reset()

        action = action.item()

        next_agent_position_direction = self._action_values.get(action)
        current_agent_position = np.where(self._game.game_state() == 1)[0]\
            .item()
        new_agent_position = current_agent_position + \
            next_agent_position_direction

        response = self._game.move_dog(
            current_agent_position,
            new_agent_position
        )

        if response == ActionResult.GAME_COMPLETE:
            return timeStep.termination(self._game.game_state(), 10)

        elif response == ActionResult.ILLEGAL_MOVE:
            return timeStep.termination(self._game.game_state(), -0.3)

        elif response == ActionResult.FOUND_ROBOT:
            return timeStep.termination(self._game.game_state(), -0.3)

        elif response == ActionResult.FOUND_BONE:
            return timeStep.transition(
                self._game.game_state(),
                reward=1,
                discount=1.0
            )

        return timeStep.transition(
            self._game.game_state(),
            reward=-0.3,
            discount=1.0
        )


# functions
def function():
    pass


# main
def main():
    dogEnvironemt = DogAdventureEnvironment(DogMaze())
    utils.validate_py_environment(dogEnvironemt, episodes=5)


# if main script
if __name__ == '__main__':
    main()
    print(f'\n\nCoded by {__author__}')
