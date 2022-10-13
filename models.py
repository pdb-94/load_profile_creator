"""
Module including Classes Department, Room and Load

@author: Paul Bohn
@contributor: Paul Bohn
"""

import numpy as np
import pandas as pd
import datetime as dt
import random


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
        self.load_profile = pd.DataFrame(index=self.time_series, columns=columns)

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
        self.load_profile = pd.DataFrame(index=self.time_series, columns=columns)

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
        # self.load_profile[name + ' power [W]'] = self.load[-1].load_profile[name + ' power [W]']


class Load:

    # TODO: Create load profiles from data
    #   - how to deal with profile (pd.Series with True/False)

    def __init__(self,
                 env=None,
                 name: str = None,
                 data: dict = None):
        self.env = env
        self.name = name
        self.data = data
        # Collect parameters from data
        self.load_type = self.data['load_type']
        self.power = float(self.data['power [W]'])
        self.standby = float(self.data['standby [W]'])
        if self.load_type == 'constant':
            self.on = self.data['on']
            self.off = self.data['off']
            self.t_start = dt.datetime.combine(self.env.time_series.iloc[0].date(), self.on)
            self.t_end = dt.datetime.combine(self.env.time_series.iloc[-1].date(), self.off)
        elif self.load_type == 'sequential':
            self.on = self.data['on']
            self.off = self.data['off']
            self.t_start = dt.datetime.combine(self.env.time_series.iloc[0].date(), self.on)
            self.t_end = dt.datetime.combine(self.env.time_series.iloc[-1].date(), self.off)
            self.cycle_length = self.data['cycle_length']
            self.interval_open = self.data['interval_open']
            self.interval_close = self.data['interval_close']
        elif self.load_type == 'cycle':
            self.cycle_length = self.data['cycle_length']
            self.cycle = pd.read_csv(self.data['cycle'])
            self.profile = pd.read_csv(self.data['profile'])
        # Create time_series and load_df
        self.time_series = self.env.time_series
        columns = [name + ' power [W]']
        self.load_profile = pd.DataFrame(index=self.time_series, columns=columns)
        self.create_profile()

    def create_profile(self):
        """
        Call functions based on load_type
        :return:
        """
        if self.load_type == 'constant':
            self.constant_load_profile()
        elif self.load_type == 'sequential':
            self.sequential_load_profile()
        elif self.load_type == 'cycle':
            self.cycle_load_profile()

    def constant_load_profile(self):
        """
        Create load profile for constant loads
        :return: None
        """
        start_diff = dt.timedelta(minutes=random.randrange(-15, 15, 1))
        end_diff = dt.timedelta(minutes=random.randrange(-15, 15, 1))
        env_start = self.env.time_series.iloc[0]
        env_end = self.env.time_series.iloc[-1]
        # Add random start/end time (max. +- 15 min)
        if self.t_start + start_diff < env_start:
            load_start = self.t_start
        else:
            load_start = self.t_start + start_diff
        if self.t_end + end_diff > env_end:
            load_end = self.t_end
        else:
            load_end = self.t_end + end_diff
        # Build load profile using power/standby and load_start/load_end
        self.load_profile.loc[env_start:load_start - dt.timedelta(minutes=1), self.name + ' power [W]'] = self.standby
        self.load_profile.loc[load_start:load_end, self.name + ' power [W]'] = self.power
        self.load_profile.loc[load_end + dt.timedelta(minutes=1):env_end, self.name + ' power [W]'] = self.standby

    def sequential_load_profile(self):
        """
        Create load profile for sequential loads
        :return: None
        """
        i_start = self.on.hour * 60 + self.on.minute
        i_end = self.off.hour * 60 + self.off.minute
        time_diff = dt.timedelta(minutes=random.randrange(0, self.interval_open, 1))
        # close sequences
        for i in range(0, len(self.load_profile.index), self.interval_close):
            if len(self.load_profile.index) - i < self.cycle_length:
                pass
            else:
                for k in range(self.cycle_length):
                    index = self.load_profile.index
                    self.load_profile.loc[index[i] + time_diff:index[i + k] + time_diff,
                    self.name + ' power [W]'] = self.power
        # Overwrite open sequences with standby
        self.load_profile.loc[self.t_start:self.t_end, self.name + ' power [W]'] = self.standby
        # open sequence
        for i in range(i_start, i_end, self.interval_open):
            if len(self.load_profile.index) - i < self.cycle_length:
                pass
            else:
                for k in range(self.cycle_length):
                    self.load_profile.loc[self.load_profile.index[i + k], self.name + ' power [W]'] = self.power

        # Fill nan values with standby
        self.load_profile[self.name + ' power [W]'] = self.load_profile[self.name + ' power [W]'].fillna(self.standby)

    def cycle_load_profile(self):
        pass
