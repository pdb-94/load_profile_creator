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


# TODO: Create function create_directory


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
                        gui_func.add_combo(widget=tab.room_combo, name=self.env[0].department[0].room_names)
        elif index == 5:
            # Tab Load profile
            tab = self.tabs.widget(index)
            # Change widget text, show and enable/disable widgets
            gui_func.change_widget_text(widget=[self.next_btn], text=['Export Data'])
            gui_func.show_widget(widget=[self.delete_btn, self.save_btn], show=False)
            gui_func.enable_widget(widget=[self.save_btn, self.return_btn], enable=True)
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
                # Create operator from user Input
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
        # Name
        name = tab.name_edit.text()
        # Time data
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
        # Get load data
        load = list(standard_room['device'])
        load_quantity = list(standard_room['quantity'])
        # Create load objects from standard room
        # TODO: cycle and profile
        for i in range(len(load)):
            load_type = standard_room.loc[i, 'type']
            power = standard_room.loc[i, 'power [W]']
            standby = standard_room.loc[i, 'standby [W]']
            cycle_length = standard_room.loc[i, 'cycle length']
            interval_open = standard_room.loc[i, 'interval (open)']
            interval_close = standard_room.loc[i, 'interval (closed)']
            on = self.env[0].department[dep_index].t_start
            off = self.env[0].department[dep_index].t_end
            if load_type == 'constant':
                cycle = ''
                profile = ''
            else:
                cycle = ''
                profile = ''
            for k in range(load_quantity[i]):
                if load_quantity[i] == 1:
                    load_name = load[i]
                else:
                    load_name = load[i] + ' ' + str(k + 1)
                data = {'load_type': load_type, 'power [W]': power, 'standby [W]': standby, 'on': on, 'off': off,
                        'cycle_length': cycle_length, 'interval open': interval_open, 'interval close': interval_close,
                        'cycle': cycle, 'profile': profile}
                room = self.env[0].department[dep_index].room[-1]
                # Create load object in room.load
                room.load.append(md.Load(env=self.env[0],
                                         name=load_name,
                                         data=data))
                room.load_names.append(load_name)
                # Create columns for load in room load profile
                room.load_profile[load_name + ' power [W]'] = room.load[-1].load_profile[load_name + ' power [W]']

    def create_load(self):
        """
        Get room parameters and create Load object in selected Department/Room
        :return: None
        """
        tab = self.tabs.widget(4)
        dep_index = tab.department_combo.currentIndex()
        room_index = tab.room_combo.currentIndex()
        # Basic parameters (name, power, standby)
        name = tab.name_edit.text()
        load_type = str(tab.type_combo.currentText())
        load_type = load_type.lower()
        power = tab.power_edit.text()
        standby = tab.standby_edit.text()
        # Build dictionary with load parameters and clear widget
        if load_type == 'constant':
            # Constant load
            on = self.env[0].department[dep_index].room[room_index].t_start
            off = self.env[0].department[dep_index].room[room_index].t_end
            data = {'load_type': load_type, 'power [W]': power, 'standby [W]': standby, 'on': on, 'off': off}
            gui_func.clear_widget(widget=[tab.name_edit, tab.power_edit, tab.standby_edit])
        else:
            # Sequential load
            cycle_length = tab.cycle_edit.text()
            cycle = tab.cycle_profile_edit.text()
            profile = tab.profile_edit.text()
            data = {'load_type': load_type, 'power [W]': power, 'standby [W]': standby, 'cycle_length': cycle_length,
                    'cycle': cycle, 'profile': profile}
            gui_func.clear_widget(widget=[tab.name_edit, tab.power_edit, tab.standby_edit,
                                          tab.cycle_edit, tab.cycle_profile_edit, tab.profile_edit])

        # Create Load object in selected Department & Room in Environment
        self.env[0].department[dep_index].room[room_index].create_load(name=name,
                                                                       data=data)
        # Add name to viewer
        gui_func.add_to_viewer(widget=tab, item=[name])
        # Clear User Inputs
        gui_func.change_combo_index(combo=[tab.type_combo])

    def create_directory(self):
        """
        Create export directory
        :return: None
        """
        # root = sys.path[1]
        root = 'C:/Users/Rummeny/PycharmProjects/hospital_load_model'
        # Top Level
        directory = '/load_profiles'
        folder = root + directory
        if not os.path.exists(folder):
            os.makedirs(folder)
        # Sub level
        sub_directory = ['/hospital', '/department', '/room', '/consumer']
        for sub_dir in sub_directory:
            if not os.path.exists(folder+sub_dir):
                os.makedirs(folder+sub_dir)
        self.export_data(load=self.env[0],
                         path=root+directory+sub_directory[0])
        for i in range(len(self.env[0].department)):
            self.export_data(load=self.env[0].department[i],
                             path=root + directory + sub_directory[1])
            for k in range(len(self.env[0].department[i].room)):
                self.export_data(load=self.env[0].department[i].room[k],
                                 path=root + directory + sub_directory[2])
                for j in range(len(self.env[0].department[i].room[k].load)):
                    self.export_data(load=self.env[0].department[i].room[k].load[j],
                                     path=root + directory + sub_directory[3])

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
                self.env[0].department.pop(item_index)
                self.env[0].department_names.pop(item_index)
                gui_func.delete_from_combo(combo=tab(3).department_combo, index=item_index)
                gui_func.delete_from_combo(combo=tab(4).department_combo, index=item_index)
                tab(5).department.pop(item_index)
            elif index == 3:
                # Tab Room: Delete Item based on selected department in dep_combo and room_viewer
                gui_func.delete_from_viewer(widget=tab(index), item=item_index)
                dep_index = tab(index).department_combo.currentIndex()
                room_index = tab(index).viewer.currentRow()
                gui_func.delete_from_combo(combo=tab(4).room_combo, index=item_index)
                self.env[0].department[dep_index].room.pop(room_index)
                self.env[0].department[dep_index].room_names.pop(room_index)
            elif index == 4:
                # Tab Consumer
                gui_func.delete_from_viewer(widget=tab(index), item=item_index)
                dep_index = tab(index).department_combo.currentIndex()
                room_index = tab(index).room_combo.currentIndex()
                load_index = tab(index).viewer.currentRow()
                room = self.env[0].department[dep_index].room[room_index]
                # Delete load
                if load_index == tab(index).viewer.count() - 1:
                    load_index = tab(index).viewer.count()
                name = self.env[0].department[dep_index].room[room_index].load_names[load_index]
                room.load.pop(load_index)
                room.load_names.pop(load_index)
                room.load_profile = room.load_profile.drop([name + ' power [W]'], axis=1)

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
        if len(self.env[0].department[dep_index].room) > 0:
            room_index = tab.room_combo.currentIndex()
            if len(self.env[0].department[dep_index].room[room_index].load) > 0:
                consumer_names = self.env[0].department[dep_index].room[room_index].load_names
                gui_func.add_to_viewer(widget=tab, item=consumer_names)

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
                tab.adjust_plot(time_series=self.env[0].time_series,
                                df=self.env[0].load_profile['Total Load [W]'])
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
        dep = self.env[0].department[dep_index]
        name = dep.name
        if tab.level_1_combo.currentIndex() == 1:
            tab.adjust_plot(time_series=self.env[0].time_series,
                            df=dep.load_profile[name + ' Total Load [W]'])
        else:
            gui_func.clear_widget(widget=[tab.level_3_combo])
            tab.room = dep.room_names
            gui_func.add_combo(widget=tab.level_3_combo, name=tab.room)

    def room_load_profile(self):
        """
        Show room load profile in tab load profile
        :return:
        """
        tab = self.tabs.widget(5)
        dep_index = tab.level_2_combo.currentIndex()
        room_index = tab.level_3_combo.currentIndex()
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
        load = self.env[0].department[dep_index].room[room_index].load[load_index]
        name = load.name
        tab.adjust_plot(time_series=self.env[0].time_series,
                        df=load.load_profile[name + ' power [W]'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TabWidget()
    sys.exit(app.exec())
