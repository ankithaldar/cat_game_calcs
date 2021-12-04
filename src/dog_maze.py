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
#   script imports
# imports


# classes
class ActionResult(Enum):
    VALID_MOVE = 1
    ILLEGAL_MOVE = 2
    FOUND_BONE = 3
    FOUND_ROBOT = 4
    GAME_COMPLETE = 5


class DogMaze():
    """base class for dog maze game"""

    def __init__(self):
        self._robot_locations = [6, 10, 14, 25, 33]
        self._bone_locations = [5, 7, 9, 16, 19, 26, 30]
        self.reset()
        self.check()

    def reset(self):
        self._state = np.zeros((36,), dtype=np.int32)
        self._state[self._robot_locations] = 2
        self._state[self._bone_locations] = 3
        self._state[0] = 1
        self._game_ended = False

    def __is_spot_last(self, position):
        return position == 35

    def move_dog(self, current_position, next_position):

        if self.__is_spot_last(next_position):
            self._state[current_position] = 0
            self._state[next_position] = 1

            self._game_ended = True
            return ActionResult.GAME_COMPLETE

        if next_position < 0 or next_position > (len(self._state) - 1):
            self._game_ended = True
            return ActionResult.ILLEGAL_MOVE

        if self._state[next_position] == 2:
            self._game_ended = True
            return ActionResult.FOUND_ROBOT

        if self._state[next_position] == 3:
            self._state[current_position] = 0
            self._state[next_position] = 1
            return ActionResult.FOUND_BONE

        self._state[current_position] = 0
        self._state[next_position] = 1

        return ActionResult.VALID_MOVE

    def game_ended(self):
        return self._game_ended

    def game_state(self):
        return self._state

    def check(self):
        print(self._state.reshape(6, 6))


# main
def main():
    DogMaze()


# if main script
if __name__ == '__main__':
    main()
    print(f'\n\nCoded by {__author__}')
