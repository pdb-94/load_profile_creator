"""
Module including Classes Department, Room and Load

@author: Paul Bohn
@contributor: Paul Bohn
"""

import os
import numpy as np
import pandas as pd
import datetime as dt


class Department:
    """
    Class to create department objects
    """

    def __init__(self,
                 env=None,
                 name: str = None,
                 t_start: dt.time = None,
                 t_end: dt.time = None):
        self.env = env
        self.name = name
        self.t_start = t_start
        self.t_end = t_end

        self.room = []
        self.room_names = []

        # Create time_series and load_df
        self.time_series = self.env.time_series
        columns = [name + ' Total Load [W]']
        self.load_df = pd.DataFrame(index=self.time_series, columns=columns)

    def create_room(self, name: str, t_start: dt.time, t_end: dt.time):
        """
        Create room object in department
        :param name: str
            room name
        :param t_end: dt.time
            room opening tim
        :param t_start: dt.time
            room closing time
        :return:
        """
        self.room.append(Room(env=self.env, name=name, t_start=t_start, t_end=t_end))
        self.room_names.append(name)


class Room:
    """
    Class to create room objects
    """

    def __init__(self,
                 env=None,
                 name: str = None,
                 t_start: dt.time = None,
                 t_end: dt.time = None):
        self.env = env
        self.name = name
        self.t_start = t_start
        self.t_end = t_end

        self.load = []
        self.load_names = []

        self.time_series = self.env.time_series
        columns = [name + ' Total Load [W]']
        self.load_df = pd.DataFrame(index=self.time_series, columns=columns)

    def create_load(self, name: str, data: dict):
        """
        Create load object in self.load
        :param name: str
            load names
        :param data: dict
            load parameters
        :return:
        """
        self.load.append(Load(env=self.env,
                              name=name,
                              data=data))
        self.load_names.append(name)


class Load:
    def __init__(self,
                 env=None,
                 name: str = None,
                 data: dict = None):
        self.env = env
        self.name = name
        self.data = data
        # self.l_type = self.data.get('load_type')

        # Create time_series and load_df
        self.time_series = self.env.time_series
        columns = ['power [W]']
        self.load_profile = pd.DataFrame(index=self.time_series, columns=columns)

    def create_profile(self):
        if self.profile is not None:
            self.load_profile['power [W]'] = self.profile['Status'] * self.power
