#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  Copyright (c) 2021, Ankit Haldar
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree. An additional grant
#  of patent rights can be found in the PATENTS file in the same directory.
#

__author__ = "Ankit 'Helder' Haldar"
__version__ = '0.1'


# Imports
import numpy as np

# Script Imports
from items import CraftItems, read_config_yaml

# Imports


# Constants
CRAFT_BATCH = CraftItems(loader='csv')
CONST_TIME = read_config_yaml()['CONST_TIME']

# Constants


class State(object):
    """docstring for State."""

    def __init__(self, coins):
        super(State, self).__init__()
        self.current_coin_balance = coins


class Action(object):
    """docstring for Action."""

    def __init__(self):
        super(Action, self).__init__()
        self.batch_size = CraftItems(loader='reset')


class CatGameCraftEnv:
    """
    final_demand: Final counts of items required for the level
    """

    def __init__(self):
        super(CatGameCraftEnv, self).__init__()
        self.final_demand = CraftItems(loader='demand')
        self.reset()

    def reset(self):
        self.lapsed_time = 0
        self.rewards = 0
        self.coins = read_config_yaml()['INIT_COINS']
        self.craftable = CraftItems(loader='craftable')
        self.have_basket = CraftItems(loader='reset')
        self.in_progress = CraftItems(loader='reset')
        self.in_progress_time = CraftItems(loader='reset')
        self.coins_present_stash = [0] * read_config_yaml()['CURRENT_LEVEL']

    def get_coin_presents(self) -> None:
        def watch_ad():
            return np.random.choice((0, 1), 1, p=[0.6, 0.4])[0]

        def collect_now():
            if self.coins >= 100_000:
                return np.random.choice((0, 1), 1, p=[0.7, 0.3])[0]
            else:
                return 1

        total_coins_present = sum(self.coins_present_stash)
        if total_coins_present <= 2000:
            watch_ad_coins = total_coins_present * 0.5
        else:
            watch_ad_coins = 1000

        collect_now = collect_now()
        if collect_now:
            self.coins += (total_coins_present + watch_ad_coins * watch_ad())
            self.coins_present_stash = [0] * \
                read_config_yaml()['CURRENT_LEVEL']

    # change this function for 1 Min game
    def assign_coins_present(self) -> None:
        if self.lapsed_time % 5 == 0 and self.lapsed_time >= 5:
            for i in range(read_config_yaml()['CURRENT_LEVEL']):
                if self.coins_present_stash[i] == 0:
                    self.coins_present_stash[i] = 210
                    break

    def required_coins(self):
        pass

    def check_base_items(self, item):
        pass

    def base_item_present(self):
        pass

    def get_base_items(self):
        pass

    def step(self):
        self.assign_coins_present()
        self.get_coin_presents()

        # Check if base Item is present
        for fd_item, fd_qntty in self.final_demand.__dict__:
            if fd_qntty > 0:
                pass


def main():
    CatGameCraftEnv().step()


if __name__ == '__main__':
    main()
