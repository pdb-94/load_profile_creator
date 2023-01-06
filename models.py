"""
Module including Classes Department, Room and Load

@author: Paul Bohn
@contributor: Paul Bohn
"""

import sys
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

    def create_room(self, standard: bool, name: str, t_start: dt.time, t_end: dt.time, path: str = None,
                    file: str = None):
        """
        Create room object in department
        :param standard: bool
            Standard or individual room
        :param name: str
            room name
        :param t_end: dt.time
            room opening tim
        :param t_start: dt.time
            room closing time
        :param path: str
            file dirctory
        :param file: str
            file name
        :return: None
        """
        if standard is True:
            self.create_standard_room(name=name, t_start=t_start, t_end=t_end, path=path, file=file)
        else:
            self.create_individual_room(name=name, t_start=t_start, t_end=t_end)

    def create_standard_room(self, name: str, t_start: dt.time, t_end: dt.time, path: str, file: str):
        """
        Create standard room
        :param name: str
            room name
        :param t_start: dt.time
            opening hours
        :param t_end: dt.time
            closing hours
        :param path: str
            file directory
        :param file: str
            file name
        :return: None
        """
        self.room.append(Room(env=self.env, name=name, t_start=t_start, t_end=t_end))
        self.room_names.append(name)
        root = sys.path[1]
        root = 'C:/Users/Rummeny/PycharmProjects/hospital_load_model'
        file_path = root + path + file
        standard_room = pd.read_csv(file_path, sep=';', decimal=',')
        load = list(standard_room['device'])
        load_quantity = list(standard_room['quantity'])
        for i in range(len(load)):
            load_type = standard_room.loc[i, 'type']
            power = standard_room.loc[i, 'power [W]']
            standby = standard_room.loc[i, 'standby [W]']
            cycle_length = standard_room.loc[i, 'cycle length']
            interval_open = standard_room.loc[i, 'interval (open)']
            interval_close = standard_room.loc[i, 'interval (closed)']
            operating_hour = standard_room.loc[i, 'operating hour']
            on = self.room[-1].t_start
            off = self.room[-1].t_end
            # Build data dictionary depending on load_type
            if load_type == 'constant':
                data = {'load_type': load_type, 'power [W]': power, 'standby [W]': standby, 'on': on, 'off': off,
                        'room': 'standard', 'operating_hour': operating_hour}
            elif load_type == 'sequential':
                data = {'load_type': load_type, 'power [W]': power, 'standby [W]': standby,
                        'cycle_length': cycle_length, 'interval_open': interval_open,
                        'interval_close': interval_close, 'on': on, 'off': off, 'room': 'standard'}
            else:
                load[i] = load[i].replace(' ', '_')
                cycle = root + '/data/load/cycle/' + load[i].lower() + '_cycle.csv'
                profile = root + '/data/load/profile/' + load[i].lower() + '_profile.csv'
                data = {'load_type': load_type, 'power [W]': power, 'standby [W]': standby,
                        'cycle_length': cycle_length, 'profile': profile, 'cycle': cycle, 'room': 'standard'}
            # Rename loads if quantity > 1
            for k in range(load_quantity[i]):
                if load_quantity[i] == 1:
                    load_name = load[i]
                else:
                    load_name = load[i] + ' ' + str(k + 1)
                room = self.room[-1]
                # Create load object in room.load
                room.load.append(Load(env=self.env,
                                      name=load_name,
                                      data=data))
                room.load_names.append(load_name)

    def create_individual_room(self, name: str, t_start: dt.time, t_end: dt.time):
        """
        Create individual room
        :param name: str
            room name
        :param t_start: dt.time
            opening hours
        :param t_end: dt.time
            closing hours
        :return: None
        """
        self.room.append(Room(env=self.env, name=name, t_start=t_start, t_end=t_end))
        self.room_names.append(name)

    def summarize_load_profile(self):
        """
        Calculate total power [W]
        :return: None
        """
        self.load_profile[self.name + ' Total Load [W]'] = np.nan
        for i in range(len(self.room)):
            name = self.room[i].name
            self.load_profile[name + ' power [W]'] = self.room[i].load_profile[name + ' Total Load [W]']
        self.load_profile[self.name + ' Total Load [W]'] = self.load_profile.sum(axis=1)

    def clear_load_profile(self):
        for col in self.load_profile.columns:
            col.drop()


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
        columns = [self.name + ' Total Load [W]']
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

    def summarize_load_profile(self):
        """
        Calculate total power [W]
        :return: None
        """
        self.load_profile[self.name + ' Total Load [W]'] = np.nan
        for i in range(len(self.load)):
            name = self.load[i].name
            self.load_profile[name + ' power [W]'] = self.load[i].load_profile[name + ' power [W]']
        self.load_profile[self.name + ' Total Load [W]'] = self.load_profile.sum(axis=1)

    def clear_load_profile(self):
        for col in self.load_profile.columns:
            col.drop()


class Load:
    """
    Class to create load objects
    """

    def __init__(self,
                 env=None,
                 name: str = None,
                 data: dict = None):
        self.env = env
        self.name = name
        self.data = data
        # Collect parameters from data
        self.load_type = self.data.get('load_type')
        self.power = float(self.data.get('power [W]'))
        self.standby = float(self.data.get('standby [W]'))
        if self.load_type == 'constant':
            self.on = self.data.get('on')
            self.off = self.data.get('off')
            self.t_start = dt.datetime.combine(self.env.time_series.iloc[0].date(), self.on)
            self.t_end = dt.datetime.combine(self.env.time_series.iloc[-1].date(), self.off)
            self.operating_hour = self.data.get('operating_hour')
        elif self.load_type == 'sequential':
            self.on = self.data.get('on')
            self.off = self.data.get('off')
            self.t_start = dt.datetime.combine(self.env.time_series.iloc[0].date(), self.on)
            self.t_end = dt.datetime.combine(self.env.time_series.iloc[-1].date(), self.off)
            self.cycle_length = int(self.data.get('cycle_length'))
            self.interval_open = int(self.data.get('interval_open'))
            self.interval_close = int(self.data.get('interval_close'))
        elif self.load_type == 'cycle':
            self.room = self.data.get('room')
            self.cycle_length = self.data.get('cycle_length')
            self.cycle = pd.read_csv(self.data.get('cycle'))
            self.profile = pd.read_csv(self.data.get('profile'))
        # Create time_series and load_df
        self.time_series = self.env.time_series
        columns = [name + ' power [W]']
        self.load_profile = pd.DataFrame(index=self.time_series, columns=columns)
        self.create_profile()
        self.drop()

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
        start_diff = dt.timedelta(minutes=random.randrange(-30, 30, 1))
        end_diff = dt.timedelta(minutes=random.randrange(-30, 30, 1))
        env_start = self.env.time_series.iloc[0]
        env_end = self.env.time_series.iloc[-1]
        if self.operating_hour == False:
            self.load_profile[self.name + ' power [W]'] = self.power
        else:
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
            self.load_profile[self.name + ' power [W]'] = self.standby
            self.load_profile.loc[load_start:load_end, self.name + ' power [W]'] = self.power

    def sequential_load_profile(self):
        """
        Create load profile for sequential loads
        :return: None
        """
        i_start = self.on.hour * 60 + self.on.minute
        i_end = self.off.hour * 60 + self.off.minute
        time_diff = dt.timedelta(minutes=random.randrange(0, self.interval_close, 1))
        # close sequence
        for i in range(0, len(self.load_profile.index),
                       int(np.random.normal(loc=self.interval_close, scale=5, size=None)) + self.cycle_length):
            # Change interval_close and cycle_length with normal deviation
            normal_cycle_length = int(np.random.normal(loc=self.cycle_length, scale=2, size=None))
            normal_interval_close = int(np.random.normal(loc=self.interval_close, scale=5, size=None))
            # Vary i by replacing standard cycle length and interval with normalized cycle_length and interval
            i = i - self.cycle_length - self.interval_close + normal_interval_close + normal_cycle_length
            if len(self.load_profile.index) - i < normal_cycle_length:
                pass
            else:
                for k in range(normal_cycle_length):
                    # Change power with normal deviation
                    power = int(np.random.normal(loc=self.power, scale=self.power * 0.2, size=None))
                    if power > self.power:
                        power = self.power
                    index = self.load_profile.index
                    self.load_profile.loc[index[i + k] + time_diff, self.name + ' power [W]'] = power
        # Overwrite open sequences with standby
        self.load_profile.loc[self.t_start:self.t_end, self.name + ' power [W]'] = self.standby
        # open sequence
        i_time_diff = random.randrange(0, self.interval_open, 1)
        for i in range(i_start, i_end, self.interval_open + self.cycle_length):
            # Change interval_open and cycle_length with normal deviation
            normal_interval_open = int(np.random.normal(loc=self.interval_open, scale=5, size=None))
            normal_cycle_length = int(np.random.normal(loc=self.cycle_length, scale=2, size=None))
            # Vary i by replacing standard cycle length and interval with normalized cycle_length and interval
            i = i - self.cycle_length - self.interval_open + normal_interval_open + normal_cycle_length
            if len(self.load_profile.index) - i - i_time_diff < normal_cycle_length:
                pass
            else:
                for k in range(normal_cycle_length):
                    # Change power with normal deviation
                    power = int(np.random.normal(loc=self.power, scale=self.power * 0.2, size=None))
                    if power > self.power:
                        power = self.power
                    index = self.load_profile.index
                    self.load_profile.loc[index[i + k + i_time_diff], self.name + ' power [W]'] = power
        # Fill nan values with standby
        self.load_profile[self.name + ' power [W]'] = self.load_profile[self.name + ' power [W]'].fillna(self.standby)

    def cycle_load_profile(self):
        """
        Create load profile for cycle loads
        :return: None
        """
        cycle_length = len(self.cycle.index)
        self.load_profile[self.name + ' power [W]'] = self.profile.values
        for i in range(len(self.load_profile.index)):
            index = self.load_profile.index
            if self.room == 'standard':
                # randomize start time for standard room load
                time = i + random.randrange(-15, 15, 1)
            else:
                time = i
            # Check if Status is turned on
            if self.load_profile.loc[index[i], self.name + ' power [W]'] == True:
                # Check if cycle is longer than index
                if time + cycle_length < len(index):
                    self.load_profile.loc[index[time]:index[time + cycle_length - 1]] = self.cycle.values
        # Replace False values with standby
        self.load_profile[self.name + ' power [W]'] = self.load_profile[self.name + ' power [W]'].replace(False,
                                                                                                          self.standby)

    def drop(self):
        """
        Drop if index is to long
        :return: None
        """
        index = self.load_profile.index
        self.load_profile = self.load_profile[index[0]:index[1439]]
