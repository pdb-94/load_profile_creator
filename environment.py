"""
Module including class Environment

@author: Paul Bohn
@contributor: Paul Bohn
"""

import os
import sys
import pandas as pd
import datetime as dt
import numpy as np
# LPC Libraries
import models as md


class Environment:
    """
    Top level class of LPC
    """
    def __init__(self,
                 name: str = None,
                 time_data: list = None):
        self.name = name
        self.time_data = time_data

        self.department = []
        self.department_names = []
        self.load = []
        self.standard_room = []
        # Create time series and load DataFrame
        self.time_series = self.create_df()
        columns = [self.name + ' Total Load [W]']
        self.load_profile = pd.DataFrame(index=self.time_series, columns=columns)
        # DataBase
        self.database = self.import_database()
        self.import_standard_room()

    def create_df(self):
        """
        Create load_df based on time_input
        :return: pd.DataFrame
            self.df
        """
        t_start = self.time_data[0]
        t_end = self.time_data[1]
        step = self.time_data[2]
        time = pd.date_range(start=t_start, end=t_end, freq=step)
        df = pd.Series(time)

        return df

    def create_department(self, name: str, t_start: dt.time, t_end: dt.time):
        """
        Create department in self.department
        :param name: str
        :param t_end: dt.time
        :param t_start: dt.time
        :return:
        """
        self.department.append(md.Department(env=self, name=name, t_start=t_start, t_end=t_end))
        self.department_names.append(name)

    def summarize_load_profile(self):
        """
        Calculate total power [W]
        :return: None
        """
        self.load_profile[self.name + ' Total Load [W]'] = np.nan
        for i in range(len(self.department)):
            name = self.department[i].name
            self.load_profile[name + ' power [W]'] = self.department[i].load_profile[name + ' Total Load [W]']
        self.load_profile[self.name + ' Total Load [W]'] = self.load_profile.sum(axis=1)

    def import_database(self):
        """
        Import load data base
        :return: df

        """
        root = sys.path[1]
        root = 'C:/Users/Rummeny/PycharmProjects/hospital_load_model'
        df = pd.read_csv(root + '/data/database.csv', sep=';', decimal=',')

        return df

    def import_standard_room(self):
        """
        Import default rooms
        :return:
        """
        root = sys.path[1]
        directory = '/data/room'
        files = next(os.walk(root+directory), (None, None, []))[2]
        csv_files = [file for file in files if file.endswith('.csv')]
        for file in csv_files:
            self.standard_room.append(pd.read_csv(root + directory + '/' + file, sep=';', decimal=','))

    def clear_load_profile(self):
        for col in self.load_profile.columns:
            col.drop()


if __name__ == '__main__':
    # Create hospital & departments
    today = dt.date.today()
    environment = Environment('Hospital', time_data=[dt.datetime(year=2022, month=9, day=29, hour=0, minute=0),
                                                     dt.datetime(year=2022, month=9, day=29, hour=23, minute=59),
                                                     dt.timedelta(minutes=1)])
