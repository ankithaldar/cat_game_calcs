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
__version__ = "0.1"


# imports
import csv
import os
import random
import sys
from dataclasses import dataclass
from typing import Any, Optional

import yaml
from yaml.cyaml import CLoader

#   script imports
# imports


# Error Classes
# Error Classes


RANDOM_MAX = 20


# classes
@dataclass
class ItemDetails(object):
    name: str
    price: int
    time: int
    base_item_1: str
    count_item_1: int
    base_item_2: Optional[str]
    count_item_2: Optional[int]
    base_item_3: Optional[str]
    count_item_3: Optional[int]


@dataclass(init=False)
class CraftItems(object):
    string: Any
    wood: Any
    ribbon: Any
    metal: Any
    needles: Any
    sparkles: Any
    bronze: Any
    silver: Any
    gold: Any
    amethyst: Any
    pendant: Any
    necklace: Any
    orb: Any
    water: Any
    fire: Any
    waterstone: Any
    firestone: Any
    elementstone: Any
    artifact: Any

    def __init__(self, loader='csv'):
        if loader == 'csv':
            self.load_from_csv()
        elif loader == 'reset':
            self.reset_to_zero()
        elif loader == 'reset_one':
            self.reset_to_one()
        elif loader == 'random':
            self.set_random_sets()
        elif loader == 'demand':
            self.set_demand()
        elif loader == 'craftable':
            self.set_craftable()

    def reset_to_zero(self):
        for each in self.__dataclass_fields__:
            self.set_attribute_value(each, 0)

    def reset_to_one(self):
        for each in self.__dataclass_fields__:
            self.set_attribute_value(each, 1)

    def set_random_sets(self):
        for each in self.__dataclass_fields__:
            self.set_attribute_value(each, random.randint(1, RANDOM_MAX + 1))

    def set_demand(self):
        for each in self.__dataclass_fields__:
            for item_demands in read_config_yaml()["CRAFT_PIECES"]:
                for item, quantity in item_demands.items():
                    if each == item:
                        self.set_attribute_value(each, quantity)

    def set_craftable(self):
        for each in self.__dataclass_fields__:
            self.set_attribute_value(each, False)

    def load_from_csv(self):
        for row in file_reader(read_config_yaml()["COUNTS"]):
            for each in self.__dataclass_fields__:
                if each == row["name"]:
                    self.set_attribute_value(each, ItemDetails(**row))

    def set_attribute_value(self, name, value):
        self.__setattr__(name, value)


# functions
def file_reader(filename):
    try:
        with open(filename, "r") as f:

            if filename.endswith(".csv"):
                return [row for row in csv.DictReader(f)]

            elif filename.endswith(".yaml"):
                return yaml.load(f, Loader=CLoader)
    except Exception as e:
        print(f"Missing file {filename}. Please check path.")
        sys.exit(1)


def read_config_yaml():
    return file_reader("run_config.yaml")


# main
def main():
    craft_items = CraftItems(loader="reset")
    craft_items.set_attribute_value("string", "10")
    [print(k, v) for k, v in craft_items.__dict__.items()]


# if main script
if __name__ == "__main__":
    main()
    print("\n\nCoded by {0}".format(__author__))
