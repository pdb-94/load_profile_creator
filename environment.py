"""
Module including class Environment

@author: Paul Bohn
@contributor: Paul Bohn
"""

import os
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
# HEyDU Libraries
import models as md


class Environment:
    """

    """
    def __init__(self,
                 name: str = None,
                 time_data: list = None):
        self.name = name
        self.time_data = time_data

        self.department = []
        self.department_names = []
        self.load = []
        self.data_base = []
        self.standard_room = []
        # Create time series and load DataFrame
        self.time_series = self.create_df()
        columns = ['Total Load [W]']
        self.load_df = pd.DataFrame(index=self.time_series, columns=columns)
        self.load_df['Total Load [W]'] = 100

        self.import_database()
        self.import_standard_room()

    def create_df(self):
        """
        Create load_df based on time_input
        :return: pd.DataFrame
            self.df
        """
        if self.time_data is None:
            date = dt.date.today()
            start = dt.time(hour=0, minute=0)
            end = dt.time(hour=23, minute=59)
            step = dt.timedelta(minutes=1)
            t_start = dt.datetime.combine(date, start)
            t_end = dt.datetime.combine(date, end)
        else:
            t_start = self.time_data[0]
            t_end = self.time_data[1]
            step = self.time_data[2]
        time = pd.date_range(start=t_start, end=t_end, freq=step)
        df = pd.Series(time)

        return df

    def create_department(self, name, t_start, t_end):
        """
        Create department in self.department
        :param t_end:
        :param t_start:
        :param name:
        :return:
        """
        self.department.append(md.Department(env=self, name=name, t_start=t_start, t_end=t_end))
        self.department_names.append(name)

    def import_database(self):
        """
        Import load data base
        :return:
        """
        path = os.getcwd()
        dir = 'data/load'
        files = next(os.walk(path+dir), (None, None, []))[2]
        csv_files = [file for file in files if file.endswith('.csv')]
        header = [0, 1, 2, 3, 4, 5, 6]
        for file in csv_files:
            self.data_base.append(pd.read_csv(path + dir + '/' + file, sep=';', decimal=',', header=header))

    def import_standard_room(self):
        """
        Import default rooms
        :return:
        """
        path = os.getcwd()
        dir = '/data/room'
        files = next(os.walk(path+dir), (None, None, []))[2]
        csv_files = [file for file in files if file.endswith('.csv')]
        for file in csv_files:
            self.standard_room.append(pd.read_csv(path + dir + '/' + file, sep=';', decimal=','))


if __name__ == '__main__':
    # Create hospital & departments
    today = dt.date.today()
    environment = Environment('Hospital', time_data=[dt.datetime(year=2022, month=9, day=29, hour=0, minute=0),
                                                     dt.datetime(year=2022, month=9, day=29, hour=23, minute=59),
                                                     dt.timedelta(minutes=1)])
    environment.create_department(name='Administration')
    environment.department[0].create_room('Emergency Consulting')

