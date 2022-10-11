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
            # Combine start time and date
            on = self.data['on']
            off = self.data['off']
            start_date = self.env.time_series.iloc[0].date()
            end_date = self.env.time_series.iloc[-1].date()
            self.t_start = dt.datetime.combine(start_date, on)
            self.t_end = dt.datetime.combine(end_date, off)
        else:
            if self.data['cycle_length'] == '':
                pass
            else:
                self.cycle_length = int(self.data['cycle_length'])
            if self.data['cycle'] == '':
                pass
            else:
                self.cycle = pd.read_csv(self.data['cycle'])
            if self.data['profile'] == '':
                pass
            else:
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
        print(self.load_profile)

    def constant_load_profile(self):
        """
        Create load profile for constant loads
        :return:
        """
        env_start = self.env.time_series.iloc[0]
        env_end = self.env.time_series.iloc[-1]
        self.load_profile.loc[env_start:self.t_start, self.name + ' power [W]'] = self.standby
        self.load_profile.loc[self.t_start:self.t_end, self.name + ' power [W]'] = self.power
        self.load_profile.loc[self.t_end:env_end, self.name + ' power [W]'] = self.standby

    def sequential_load_profile(self):
        pass

    def cycle_load_profile(self):
        pass



