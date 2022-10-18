"""
Main  GUI module of Load Profile Creator (LPC)

@author: Paul Bohn
@contributor: Paul Bohn
"""

__version__ = '0.1'
__author__ = 'pdb-94'

import sys
import os
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import datetime as dt
# Import Gui Modules
from gui.project_setup import Project_Setup
from gui.hospital import Hospital
from gui.department import Department
from gui.room import Room
from gui.load import Consumer
from gui.load_profile import Load_profile
from gui.popup_dialog import DeleteDialog
import gui.gui_function as gui_func
# Import HEyDU Modules
from environment import Environment
import models as md


class TabWidget(QWidget):
    """
    Class to create the main Window Frame of the LPC GUI
    """

    def __init__(self):
        super().__init__()

        # Environment Container
        self.env = [None]

        # Set up TabWidget
        self.tabs = QTabWidget()
        self.tab_title = ['Project Setup',
                          'Hospital',
                          'Department',
                          'Room',
                          'Consumer',
                          'Load profile']
        self.tab_classes = [Project_Setup,
                            Hospital,
                            Department,
                            Room,
                            Consumer,
                            Load_profile]
        for i in range(len(self.tab_classes)):
            self.tabs.addTab(self.tab_classes[i](), self.tab_title[i])
        gui_func.enable_widget(widget=[self.tabs.widget(2),
                                       self.tabs.widget(3),
                                       self.tabs.widget(4),
                                       self.tabs.widget(5)],
                               enable=False)

        # Set up Pushbutton
        self.delete_btn = QPushButton('Delete')
        self.save_btn = QPushButton('Save')
        self.return_btn = QPushButton('Return')
        self.next_btn = QPushButton('Start')
        self.next_btn.setFixedSize(QSize(150, 40))
        gui_func.enable_widget(widget=[self.save_btn, self.return_btn], enable=False)
        gui_func.show_widget(widget=[self.save_btn, self.return_btn, self.delete_btn], show=False)

        # Set up Layout
        self.layout = QGridLayout()
        self.layout.addWidget(self.tabs, 0, 0, 4, 1)
        self.layout.addWidget(self.delete_btn, 0, 1, Qt.AlignBottom)
        self.layout.addWidget(self.save_btn, 1, 1)
        self.layout.addWidget(self.return_btn, 2, 1)
        self.layout.addWidget(self.next_btn, 3, 1)
        self.setLayout(self.layout)

        # Warning Dialog
        self.warning_dialog = DeleteDialog()

        # Set up Main Window
        self.setGeometry(200, 200, 1200, 750)
        self.setWindowTitle('Load Profile Creator')
        self.show()

        # Assign functions to Tabs an PushButtons
        self.tabs.currentChanged.connect(self.tab_changed)
        self.delete_btn.clicked.connect(self.delete)
        self.save_btn.clicked.connect(self.save)
        self.return_btn.clicked.connect(self.previous_tab)
        self.next_btn.clicked.connect(self.next_tab)
        # Assign Functions to widgets in tabs
        tab = self.tabs.widget
        tab(3).department_combo.currentIndexChanged.connect(self.add_room_combo)
        tab(4).department_combo.currentIndexChanged.connect(self.add_room_combo)
        tab(4).room_combo.currentIndexChanged.connect(self.add_consumer_combo)
        tab(5).level_1_combo.currentIndexChanged.connect(self.change_load_profile)
        tab(5).level_2_combo.currentIndexChanged.connect(self.department_load_profile)
        tab(5).level_3_combo.currentIndexChanged.connect(self.room_load_profile)
        tab(5).level_4_combo.currentIndexChanged.connect(self.consumer_load_profile)

    # Button Functions
    def next_tab(self):
        """
        Show next tab
        :return:
        """
        # Get current Index from TabWidget and set current Index -=1
        index = self.tabs.currentIndex()
        if index == len(self.tab_classes) - 1:
            self.create_directory()
        elif index < len(self.tab_classes):
            self.tabs.setCurrentIndex(index + 1)

    def previous_tab(self):
        """
        Show previous tab
        :return: None
        """
        # Get current Index from TabWidget and set current Index -=1
        index = self.tabs.currentIndex()
        self.tabs.setCurrentIndex(index - 1)

    def tab_changed(self):
        """
        Prepare tabs to default look (change texts, show/hide/enable/disable/clear widgets, reset ComboBox)
        :return: None
        """
        index = self.tabs.currentIndex()
        if index == 0:
            # Tab Start
            # Change widget text, show and enable widgets
            gui_func.change_widget_text(widget=[self.next_btn], text=['Start'])
            gui_func.show_widget(widget=[self.save_btn, self.return_btn, self.delete_btn], show=False)
            gui_func.enable_widget(widget=[self.next_btn], enable=True)
        elif index == 1:
            # Tab Hospital
            # Change widget text, show and enable/disable widgets
            gui_func.change_widget_text(widget=[self.next_btn], text=['Next'])
            if isinstance(self.env[0], Environment):
                # Show and enable/disable widgets
                gui_func.show_widget(widget=[self.delete_btn, self.save_btn, self.return_btn], show=True)
                gui_func.enable_widget(widget=[self.return_btn], enable=True)
                gui_func.enable_widget(widget=[self.save_btn], enable=False)
            else:
                # show and enable/disable widgets
                gui_func.show_widget(widget=[self.delete_btn, self.save_btn, self.return_btn], show=True)
                gui_func.enable_widget(widget=[self.save_btn, self.return_btn], enable=True)
                gui_func.enable_widget(widget=[self.next_btn], enable=False)
        elif index == 2:
            # Tab Department
            # Change widget text, show and enable widgets
            gui_func.change_widget_text(widget=[self.next_btn], text=['Next'])
            gui_func.show_widget(widget=[self.delete_btn, self.save_btn, self.return_btn], show=True)
            gui_func.enable_widget(widget=[self.save_btn, self.return_btn], enable=True)
        elif index == 3:
            # Tab Room
            tab = self.tabs.widget(index)
            # Change widget text, show, clear and enable/disable widgets
            gui_func.change_widget_text(widget=[self.next_btn], text=['Next'])
            gui_func.show_widget(widget=[self.delete_btn, self.save_btn, self.return_btn], show=True)
            gui_func.enable_widget(widget=[self.save_btn, self.return_btn], enable=True)
            gui_func.clear_widget(widget=[self.tabs.widget(index).viewer])
            # Change ComboBox index to 0
            gui_func.change_combo_index(combo=[tab.room_type, tab.department_combo])
            if isinstance(self.env[0], Environment):
                if len(self.env[0].department) > 0:
                    if len(self.env[0].department[0].room) > 0:
                        # Add selected items to viewer
                        gui_func.add_to_room_viewer(widget=tab, item=self.env[0].department[0].room_names)
        elif index == 4:
            # Tab Consumer
            tab = self.tabs.widget(index)
            # Change widget text, show, clear and enable/disable widgets
            gui_func.change_widget_text(widget=[self.next_btn], text=['Next'])
            gui_func.show_widget(widget=[self.delete_btn, self.save_btn, self.return_btn], show=True)
            gui_func.enable_widget(widget=[self.save_btn, self.return_btn], enable=True)
            gui_func.clear_widget(widget=[tab.room_combo])
            # Change ComboBox index to 0
            gui_func.change_combo_index(combo=[tab.department_combo])
            self.add_room_combo()
            if isinstance(self.env[0], Environment):
                if len(self.env[0].department) > 0:
                    if len(self.env[0].department[0].room) > 0:
                        pass
                    else:
                        # Add selected items to ComboBox
                        gui_func.add_combo(widget=tab.room_combo, name=self.env[0].room[0].load_names)
        elif index == 5:
            # Tab Load profile
            tab = self.tabs.widget(index)
            # Change widget text, show and enable/disable widgets
            gui_func.change_widget_text(widget=[self.next_btn], text=['Export Data'])
            gui_func.show_widget(widget=[self.delete_btn, self.save_btn], show=False)
            gui_func.enable_widget(widget=[self.save_btn, self.return_btn], enable=True)
            self.build_load_profiles()
            if isinstance(self.env[0], Environment):
                gui_func.enable_widget(widget=[tab.level_1_combo], enable=True)
            else:
                gui_func.enable_widget(widget=[tab.level_1_combo], enable=False)
            # Change ComboBox index to 0
            gui_func.change_combo_index(combo=[tab.level_1_combo])

    def save(self):
        """
        Function executed by self.next_btn
        """
        index = self.tabs.currentIndex()
        if index == 1:
            # Tab Hospital
            self.create_env()
            gui_func.enable_widget(widget=[self.save_btn], enable=False)
        elif index == 2:
            # Tab Department
            if isinstance(self.env[0], Environment):
                # Run function create department
                self.create_department()
            else:
                print('Setup Hospital data before creating department.')
        elif index == 3:
            # Tab Room
            if len(self.env[0].department) == 0:
                print('Create department before creating rooms')
            else:
                self.create_room()
        elif index == 4:
            # Tab Consumer
            dep_index = self.tabs.widget(4).department_combo.currentIndex()
            if len(self.env[0].department[dep_index].room) == 0:
                print('Create rooms before creating consumers')
            else:
                self.create_load()

    # Create Hospital
    def create_env(self):
        """
        Create Environment from User Input in hospital tab
        :return: None
        """
        tab = self.tabs.widget
        name = tab(1).name_edit.text()
        start_time = tab(1).start_time_edit.text()
        end_time = tab(1).end_time_edit.text()
        time_step = tab(1).time_step_edit.text()
        time_data = gui_func.convert_datetime(start=start_time, end=end_time, step=time_step)
        if time_data[1] < time_data[0]:
            print('End time < Start Time. Please choose valid time frame.')
        else:
            # Create Environment object in self.env[0]
            self.env[0] = Environment(name=name,
                                      time_data=time_data)
            # Add Hospital to viewer
            if isinstance(self.env[0], Environment):
                gui_func.delete_from_viewer(widget=tab(self.tabs.currentIndex()), item=0)
                gui_func.add_to_viewer(widget=tab(self.tabs.currentIndex()), item=[name])
            else:
                gui_func.add_to_viewer(widget=tab(self.tabs.currentIndex()), item=[name])
            # Clear Input
            gui_func.clear_widget(widget=[tab(1).name_edit])
            gui_func.enable_widget(widget=[self.next_btn], enable=True)
            gui_func.enable_widget(widget=[self.tabs.widget(2), self.tabs.widget(5)], enable=True)

    # Create Department
    def create_department(self):
        """
        Get parameters and run create_department from Environment obj
        :return: None
        """
        tab = self.tabs.widget
        # Name
        name = tab(2).name_edit.text()
        # Time Data
        start_str = tab(2).start_time_edit.text()
        end_str = tab(2).end_time_edit.text()
        start = gui_func.convert_time(text=start_str)
        end = gui_func.convert_time(text=end_str)
        # Create department object in Environment
        self.env[0].create_department(name=name,
                                      t_start=dt.time(hour=start[0], minute=start[1]),
                                      t_end=dt.time(hour=end[0], minute=end[1]))
        # Add Department to Viewer
        gui_func.add_to_viewer(widget=tab(self.tabs.currentIndex()), item=[name])
        # Add Department to department ComboBox in Tab Room
        gui_func.add_combo(widget=tab(3).department_combo, name=[self.env[0].department[-1].name])
        gui_func.add_combo(widget=tab(4).department_combo, name=[self.env[0].department[-1].name])
        # Clear Input
        gui_func.clear_widget(widget=[tab(2).name_edit])
        gui_func.enable_widget(widget=[self.tabs.widget(3)], enable=True)

    # Create Room
    def create_room(self):
        """
        Run function individual/standard room based on selection in room type combobox
        :return: None
        """
        tab = self.tabs.widget(3)
        # Basic parameters
        dep_index = tab.department_combo.currentIndex()
        if tab.room_type.currentIndex() == 0:
            # Individual room
            self.create_individual_room(dep_index=dep_index)
        elif tab.room_type.currentIndex() == 1:
            # Standard room
            self.create_standard_room(dep_index=dep_index)

    def create_individual_room(self, dep_index):
        """
        Get individual room parameters and create room object in selected Department
        :param dep_index: int
            department index
        :return: None
        """
        tab = self.tabs.widget(3)
        # Parameters
        name = tab.name_edit.text()
        start_str = tab.start_time_edit.text()
        end_str = tab.end_time_edit.text()
        start = gui_func.convert_time(text=start_str)
        end = gui_func.convert_time(text=end_str)
        t_start = dt.time(hour=start[0], minute=start[1])
        t_end = dt.time(hour=end[0], minute=end[1])
        # Create room object in selected Department in Environment
        self.env[0].department[dep_index].create_room(name=name,
                                                      t_start=t_start,
                                                      t_end=t_end)
        # Add name to viewer
        gui_func.add_to_viewer(widget=tab, item=[name])
        # Clear Input
        gui_func.clear_widget(widget=[tab.name_edit])
        gui_func.enable_widget(widget=[self.tabs.widget(4)], enable=True)

    def create_standard_room(self, dep_index):
        # TODO: Complete Rooms
        """
        Get standard room parameters and create room object in selected Department
        :param dep_index: int
            department index
        :return: None
        """
        tab = self.tabs.widget(3)
        # Name
        name = tab.name_edit.text()
        # Time data from department
        dep = self.env[0].department[dep_index]
        t_start = dep.t_start
        t_end = dep.t_end
        # Find standard csv-file
        # root = sys.path[1]
        root = 'C:/Users/Rummeny/PycharmProjects/hospital_load_model'  # TODO: Remove Statement (just to be able to run debugger)
        room_name = tab.standard_combo.currentText()
        room_name = room_name.lower()
        room_name = room_name.replace(' ', '_')
        file = room_name + '.csv'
        path = root + '/data/room/' + file
        standard_room = pd.read_csv(path, sep=';', decimal=',')
        # Create room object in selected Department in Environment
        self.env[0].department[dep_index].create_room(name=name,
                                                      t_start=t_start,
                                                      t_end=t_end)
        # Add name to viewer
        gui_func.add_to_viewer(widget=tab, item=[name])
        # Clear Input
        gui_func.clear_widget(widget=[tab.name_edit])
        gui_func.enable_widget(widget=[self.tabs.widget(4)], enable=True)
        # Create Loads in Standard room
        self.create_standard_room_load(dep_index=dep_index, root=root, standard_room=standard_room)

    # Create Load
    def create_load(self):
        """
        Get room parameters and create Load object in selected Department/Room
        :return: None
        """
        tab = self.tabs.widget(4)
        # Basic parameters
        dep_index = tab.department_combo.currentIndex()
        room_index = tab.room_combo.currentIndex()
        load_type = str(tab.type_combo.currentText())
        load_type = load_type.lower()
        # Build dictionary with load parameters and clear widget
        if load_type == 'constant':
            # Constant load
            data = self.create_constant_load_data(dep_index=dep_index, room_index=room_index)
        elif load_type == 'sequential':
            # Sequential load
            data = self.create_sequential_load_data(dep_index=dep_index, room_index=room_index)
        elif load_type == 'cycle':
            data = self.create_cycle_load_data()
        if data is None:
            return
        # Create Load object in selected Department & Room in Environment
        self.env[0].department[dep_index].room[room_index].create_load(name=data['name'],
                                                                       data=data)
        # Run gui function (add load to viewer, change ComoboBox Index, clear widgets)
        gui_func.add_to_viewer(widget=tab, item=[data['name']])
        gui_func.change_combo_index(combo=[tab.type_combo])
        gui_func.clear_widget(widget=[tab.name_edit, tab.power_edit, tab.standby_edit,
                                      tab.cycle_length_edit, tab.cycle_edit, tab.profile_edit,
                                      tab.interval_open_edit, tab.interval_closed_edit])

    def create_standard_room_load(self, dep_index: int, root: str, standard_room: pd.DataFrame):
        """
        Create load objects in standard room
        :param dep_index: int
            department index
        :param root: str
            path of directory
        :param standard_room: pd.DataFrame
            csv-file of selected standard room
        :return: None
        """
        # Get load name and quantity from standard room
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
            on = self.env[0].department[dep_index].t_start
            off = self.env[0].department[dep_index].t_end
            # Build data dictionary depending on load_type
            if load_type == 'constant':
                data = {'load_type': load_type, 'power [W]': power, 'standby [W]': standby, 'on': on, 'off': off,
                        'room': 'standard', 'operating_hour': operating_hour}
            elif load_type == 'sequential':
                data = {'load_type': load_type, 'power [W]': power, 'standby [W]': standby,
                        'cycle_length': cycle_length, 'interval_open': interval_open,
                        'interval_close': interval_close, 'on': on, 'off': off, 'room': 'standard'}
            else:
                cycle = root + '/data/load/' + load[i].lower() + '_cycle.csv'
                profile = root + '/data/load/' + load[i].lower() + '_profile.csv'
                data = {'load_type': load_type, 'power [W]': power, 'standby [W]': standby,
                        'cycle_length': cycle_length, 'profile': profile, 'cycle': cycle, 'room': 'standard'}
            # Rename loads if quantity > 1
            for k in range(load_quantity[i]):
                if load_quantity[i] == 1:
                    load_name = load[i]
                else:
                    load_name = load[i] + ' ' + str(k + 1)
                room = self.env[0].department[dep_index].room[-1]
                # Create load object in room.load
                room.load.append(md.Load(env=self.env[0],
                                         name=load_name,
                                         data=data))
                room.load_names.append(load_name)

    def create_constant_load_data(self, dep_index: int, room_index: int):
        """
        :param dep_index: int
            index of selected department
        :param room_index: int
            index of selected room
        :return: dict
            load data
        """
        tab = self.tabs.widget(4)
        name = tab.name_edit.text()
        load_type = str(tab.type_combo.currentText())
        load_type = load_type.lower()
        power = tab.power_edit.text()
        standby = tab.standby_edit.text()
        on = self.env[0].department[dep_index].room[room_index].t_start
        off = self.env[0].department[dep_index].room[room_index].t_end
        data = {'name': name, 'load_type': load_type, 'power [W]': power, 'standby [W]': standby, 'on': on, 'off': off}

        return data

    def create_sequential_load_data(self, dep_index: int, room_index: int):
        """
        :param dep_index: int
            index of selected department
        :param room_index: int
            index of selected room
        :return: dict
            load data
        """
        tab = self.tabs.widget(4)
        name = tab.name_edit.text()
        load_type = str(tab.type_combo.currentText())
        load_type = load_type.lower()
        power = tab.power_edit.text()
        standby = tab.standby_edit.text()
        on = self.env[0].department[dep_index].room[room_index].t_start
        off = self.env[0].department[dep_index].room[room_index].t_end
        cycle_length = tab.cycle_length_edit.text()
        interval_open = tab.interval_open_edit.text()
        interval_closed = tab.interval_closed_edit.text()
        if cycle_length == '':
            print('Please type in cycle length [min].')
            return
        else:
            cycle_length = int(cycle_length)
        if interval_open == '':
            print('Please type in interval (open) [min].')
            return
        else:
            interval_open = int(interval_open)
        if interval_closed == '':
            print('Please type in interval (closed) [min].')
            return
        else:
            interval_closed = int(interval_closed)
        data = {'name': name, 'load_type': load_type, 'power [W]': power, 'standby [W]': standby,
                'cycle_length': cycle_length,
                'interval_open': interval_open, 'interval_close': interval_closed, 'on': on, 'off': off}

        return data

    def create_cycle_load_data(self):
        """
        :return: dict
            load data
        """
        tab = self.tabs.widget(4)
        name = tab.name_edit.text()
        load_type = str(tab.type_combo.currentText())
        load_type = load_type.lower()
        power = tab.power_edit.text()
        standby = tab.standby_edit.text()
        cycle_length = tab.cycle_length_edit.text()
        cycle = tab.cycle_edit.text()
        profile = tab.profile_edit.text()
        if cycle_length == '':
            print('Please type in cycle length [min].')
            return
        else:
            cycle_length = int(cycle_length)
        if os.path.exists(cycle):
            pass
        else:
            print('File cycle: ' + str(cycle) + ' does not exist.')
            gui_func.clear_widget(widget=[tab.name_edit, tab.power_edit, tab.standby_edit,
                                          tab.cycle_length_edit, tab.cycle_edit, tab.profile_edit])
            return
        if os.path.exists(profile):
            pass
        else:
            print('File cycle: ' + str(profile) + ' does not exist.')
            gui_func.clear_widget(widget=[tab.name_edit, tab.power_edit, tab.standby_edit,
                                          tab.cycle_length_edit, tab.cycle_edit, tab.profile_edit])
            return

        data = {'name': name, 'load_type': load_type, 'power [W]': power, 'standby [W]': standby,
                'cycle_length': cycle_length,
                'profile': profile, 'cycle': cycle}

        return data

    # Export data
    def create_directory(self):
        """
        Create export directory
        :return: None
        """
        # root = sys.path[1]
        root = 'C:/Users/Rummeny/PycharmProjects/hospital_load_model'  # TODO: Remove Statement
        env = self.env[0]
        # Hospital directory
        hospital_directory = '/' + str(env.name + '_load_profile')
        directory = root + hospital_directory
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Export environment load profile
        self.export_data(load=env, path=directory)
        for i in range(len(env.department)):
            dep = env.department[i]
            dep_dir = '/' + dep.name + '_load_profile'
            directory = root + hospital_directory + dep_dir
            if not os.path.exists(directory):
                os.makedirs(directory)
            # Export department load profile
            self.export_data(load=dep, path=directory)
            for k in range(len(dep.room)):
                room = dep.room[k]
                room_dir = '/' + room.name + '_load_profile'
                directory = root + hospital_directory + dep_dir + room_dir
                if not os.path.exists(directory):
                    os.makedirs(directory)
                # Export room load profile
                self.export_data(load=room, path=directory)
                for j in range(len(room.load)):
                    load = room.load[j]
                    load_dir = '/' + load.name + '_load_profile'
                    directory = root + hospital_directory + dep_dir + room_dir + load_dir
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    # Export load load profile
                    self.export_data(load=load, path=directory)

    def export_data(self, load=None, path: str = None):
        """
        Export data
        :param load: object
            Environment; Department; Room; Load
        :param path: str
            export_path
        :return: None
        """
        load.load_profile.to_csv(path + '/' + load.name + '.csv', sep=';', decimal=',')

    # Delete objects
    def delete(self):
        """
        Delete Objects from env an display Widgets
        :return: None
        """
        tab = self.tabs.widget
        index = self.tabs.currentIndex()
        # Get index of Item to delete
        item_index = self.tabs.widget(index).viewer.currentRow()
        if tab(index).viewer.count() > 0:
            if index == 1:
                # Tab Hospital: Delete Item based on selected item in hospital_viewer
                # Open warning Dialog
                option = self.warning_dialog.execute()
                if option is True:
                    # Delete Item
                    gui_func.delete_from_viewer(self.tabs.widget(index), item_index)
                    self.env[0] = None
                    gui_func.enable_widget(widget=[self.save_btn], enable=True)
                elif option is False:
                    # Do not delete Item
                    pass
            elif index == 2:
                # Tab Department: Delete Item based on selected department in department_viewer
                gui_func.delete_from_viewer(widget=self.tabs.widget(index), item=item_index)
                dep = self.env[0].department[item_index]
                name = self.env[0].department_names[item_index]
                self.env[0].department.remove(dep)
                self.env[0].department_names.remove(name)
                gui_func.delete_from_combo(combo=tab(3).department_combo, index=item_index)
                gui_func.delete_from_combo(combo=tab(4).department_combo, index=item_index)
            elif index == 3:
                # Tab Room: Delete Item based on selected department in dep_combo and room_viewer
                gui_func.delete_from_viewer(widget=tab(index), item=item_index)
                dep_index = tab(index).department_combo.currentIndex()
                gui_func.delete_from_combo(combo=tab(4).room_combo, index=item_index)
                room = self.env[0].department[dep_index].room[item_index]
                name = self.env[0].department[dep_index].room_names[item_index]
                self.env[0].department[dep_index].room.remove(room)
                self.env[0].department[dep_index].room_names.remove(name)
            elif index == 4:
                # Tab Consumer
                gui_func.delete_from_viewer(widget=tab(index), item=item_index)
                dep_index = tab(index).department_combo.currentIndex()
                room_index = tab(index).room_combo.currentIndex()
                room = self.env[0].department[dep_index].room[room_index]
                load = room.load[item_index]
                name = room.load_names[item_index]
                room.load.remove(load)
                room.load_names.remove(name)

    # Add to ComboBoxes
    def add_room_combo(self):
        """
        Show rooms in ComboBox/Viewer based on selected department
        :return: None
        """
        tab = self.tabs.widget
        # Clear Room combo, viewer and room_list
        gui_func.clear_widget(widget=[tab(3).viewer, tab(4).room_combo])
        index = self.tabs.currentIndex()
        if isinstance(self.env[0], Environment):
            if index == 2:
                pass
            else:
                if index == 3:
                    # Tab Room
                    dep_index = tab(index).department_combo.currentIndex()
                    if len(self.env[0].department[dep_index].room) > 0:
                        # Add Rooms based on selection in department combo
                        room_names = self.env[0].department[dep_index].room_names
                        gui_func.add_to_viewer(widget=tab(index), item=room_names)
                elif index == 4:
                    # Tab Consumer
                    dep_index = tab(index).department_combo.currentIndex()
                    if len(self.env[0].department) > 0:
                        if len(self.env[0].department[dep_index].room) > 0:
                            # Add Rooms based on selection in department combo
                            room_names = self.env[0].department[dep_index].room_names
                            gui_func.add_combo(widget=tab(index).room_combo, name=room_names)

    def add_consumer_combo(self):
        """
        Show consumers in ComboBox/Viewer based on selected department/room
        :return: None
        """
        tab = self.tabs.widget(4)
        gui_func.clear_widget(widget=[tab.viewer])
        dep_index = tab.department_combo.currentIndex()
        if len(self.env[0].department) == 0:
            gui_func.add_to_viewer(widget=tab, item=[])
        else:
            if len(self.env[0].department[dep_index].room) > 0:
                room_index = tab.room_combo.currentIndex()
                if len(self.env[0].department[dep_index].room[room_index].load) > 0:
                    consumer_names = self.env[0].department[dep_index].room[room_index].load_names
                    gui_func.add_to_viewer(widget=tab, item=consumer_names)

    # Summarize and plot load profiles
    def change_load_profile(self):
        """
        Change load profile level in tab load_profile
        :return: None
        """
        tab = self.tabs.widget(5)
        # Clear and load profile ComboBox
        gui_func.clear_widget(widget=[tab.level_2_combo, tab.level_3_combo, tab.level_4_combo])
        level = tab.level_1_combo.currentIndex()
        gui_func.show_widget(widget=[tab.level_2_combo, tab.level_2,
                                     tab.level_3_combo, tab.level_3,
                                     tab.level_4_combo, tab.level_4],
                             show=False)
        # Add Items to load profile ComboBox based on selection in level ComboBox
        tab.department = self.env[0].department_names
        if isinstance(self.env[0], Environment):
            gui_func.enable_widget(widget=[tab.level_1_combo], enable=True)
            if level == 0:
                # Hospital
                # Show hospital load profile
                name = self.env[0].name
                tab.adjust_plot(time_series=self.env[0].time_series,
                                df=self.env[0].load_profile[name + ' Total Load [W]'])
            elif level == 1:
                # Show, enable and add department names to level_2_combo
                gui_func.clear_widget(widget=[tab.level_2_combo])
                gui_func.show_widget(widget=[tab.level_2_combo, tab.level_2], show=True)
                gui_func.enable_widget(widget=[tab.level_2_combo], enable=True)
                gui_func.add_combo(widget=tab.level_2_combo, name=tab.department)
            elif level == 2:
                gui_func.clear_widget(widget=[tab.level_2_combo])
                gui_func.add_combo(widget=tab.level_2_combo, name=tab.department)
                # Show and enable level_2 and level_3_combo
                gui_func.enable_widget(widget=[tab.level_2_combo, tab.level_3_combo], enable=True)
                gui_func.show_widget(widget=[tab.level_2_combo, tab.level_2,
                                             tab.level_3_combo, tab.level_3],
                                     show=True)
            elif level == 3:
                gui_func.add_combo(widget=tab.level_2_combo, name=tab.department)
                gui_func.enable_widget(widget=[tab.level_2_combo, tab.level_3_combo, tab.level_4_combo], enable=True)
                gui_func.show_widget(widget=[tab.level_2_combo, tab.level_2,
                                             tab.level_3_combo, tab.level_3,
                                             tab.level_4_combo, tab.level_4],
                                     show=True)

    def department_load_profile(self):
        """
        Show department load profile in tab load profile
        :return:
        """
        tab = self.tabs.widget(5)
        dep_index = tab.level_2_combo.currentIndex()
        if dep_index == -1:
            tab.clear_plot()
            return
        dep = self.env[0].department[dep_index]
        name = dep.name
        if tab.level_1_combo.currentIndex() == 1:
            tab.adjust_plot(time_series=self.env[0].time_series,
                            df=dep.load_profile[name + ' Total Load [W]'])
        else:
            gui_func.clear_widget(widget=[tab.level_3_combo, tab.level_4_combo])
            tab.department = dep.room_names
            gui_func.add_combo(widget=tab.level_3_combo, name=tab.department)

    def room_load_profile(self):
        """
        Show room load profile in tab load profile
        :return:
        """
        tab = self.tabs.widget(5)
        dep_index = tab.level_2_combo.currentIndex()
        room_index = tab.level_3_combo.currentIndex()
        indexes = [dep_index, room_index]
        if -1 in indexes:
            tab.clear_plot()
            return
        room = self.env[0].department[dep_index].room[room_index]
        name = room.name
        if tab.level_1_combo.currentIndex() == 2:
            room.load_profile[name + ' Total Load [W]'] = np.nan
            room.load_profile[name + ' Total Load [W]'] = room.load_profile.sum(axis=1)
            tab.adjust_plot(time_series=self.env[0].time_series,
                            df=room.load_profile[name + ' Total Load [W]'])
        else:
            gui_func.clear_widget(widget=[tab.level_4_combo])
            tab.consumer = room.load_names
            gui_func.add_combo(widget=tab.level_4_combo, name=tab.consumer)

    def consumer_load_profile(self):
        """
        Show consumer load profile in tab load profile
        :return:
        """
        tab = self.tabs.widget(5)
        dep_index = tab.level_2_combo.currentIndex()
        room_index = tab.level_3_combo.currentIndex()
        load_index = tab.level_4_combo.currentIndex()
        indexes = [dep_index, room_index, load_index]
        if -1 in indexes:
            tab.clear_plot()
            return
        load = self.env[0].department[dep_index].room[room_index].load[load_index]
        name = load.name
        tab.adjust_plot(time_series=self.env[0].time_series,
                        df=load.load_profile[name + ' power [W]'])

    def build_load_profiles(self):
        """
        Call functions to summarize load profiles
        :return: None
        """
        tab = self.tabs.widget(5)
        if isinstance(self.env[0], Environment):
            env = self.env[0]
            if len(env.department) == 0:
                tab.clear_plot()
                return
            for i in range(len(env.department)):
                dep = env.department[i]
                if len(dep.room) == 0:
                    tab.clear_plot()
                    return
                for k in range(len(dep.room)):
                    room = dep.room[k]
                    # Summarize room profile
                    room.summarize_load_profile()
                # Summarize department profile
                dep.summarize_load_profile()
            # Summarize hospital profile
            env.summarize_load_profile()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TabWidget()
    sys.exit(app.exec())
