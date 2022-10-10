"""
Main  GUI module of Load Profile Creator (LPC)

@author: Paul Bohn
@contributor: Paul Bohn
"""

__version__ = '0.1'
__author__ = 'pdb-94'


import sys
import os
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import datetime as dt
# Import Gui Modules
from gui.project_setup import Project_Setup
from gui.hospital import Hospital
from gui.department import Department
from gui.room import Room
from gui.load import Consumer
from gui.load_profile import Load_profile
from gui.plot import Plot
from gui.popup_dialog import DeleteDialog, Load_Dialog
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

        # Set up Main Window
        self.setGeometry(200, 200, 1200, 750)
        self.setWindowTitle('Load Profile Creator')
        self.show()

        # Assign functions to Widgets
        self.tabs.currentChanged.connect(self.tab_changed)
        self.delete_btn.clicked.connect(self.delete)
        self.save_btn.clicked.connect(self.save)
        self.return_btn.clicked.connect(self.previous_tab)
        self.next_btn.clicked.connect(self.next_tab)
        self.tabs.widget(3).department_combo.currentIndexChanged.connect(self.add_room_combo)
        self.tabs.widget(4).department_combo.currentIndexChanged.connect(self.add_room_combo)
        self.tabs.widget(4).room_combo.currentIndexChanged.connect(self.add_consumer_combo)
        self.tabs.widget(5).level_1_combo.currentIndexChanged.connect(self.change_load_profile)
        self.tabs.widget(5).level_2_combo.currentIndexChanged.connect(self.level_2_combo)
        self.tabs.widget(5).level_3_combo.currentIndexChanged.connect(self.level_3_combo)

    def next_tab(self):
        """
        Show next tab
        :return:
        """
        # Get current Index from TabWidget and set current Index -=1
        index = self.tabs.currentIndex()
        if index < len(self.tab_classes):
            self.tabs.setCurrentIndex(index + 1)

    def previous_tab(self):
        """
        Show previous Tt
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
            gui_func.show_widget(widget=[self.delete_btn], show=False)
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
        elif index == 5:
            # Tab Load profile
            print('Exporting Data')

    def create_env(self):
        """
        Create Environment from User Input in hospital tab
        :return: None
        """
        tab = self.tabs.widget
        name = tab(1).name_edit.text()
        start_str = tab(1).start_time_edit.text()
        start = dt.datetime.strptime(start_str, '%d.%m.%Y %H:%M')
        end_str = tab(1).end_time_edit.text()
        end = dt.datetime.strptime(end_str, '%d.%m.%Y %H:%M')
        step_str = tab(1).time_step_edit.text()
        step_time = dt.datetime.strptime(step_str, '%H:%M')
        help_time = dt.datetime(year=1900, month=1, day=1, hour=0, minute=0)
        step = step_time - help_time
        if end < start:
            print('End time < Start Time. Please choose valid time frame.')
        else:
            self.env[0] = Environment(name=name,
                                      time_data=[start, end, step])
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
        start = gui_func.convert_time(string=start_str)
        end_str = tab(2).end_time_edit.text()
        end = gui_func.convert_time(string=end_str)
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
        :return:
        """
        tab = self.tabs.widget(3)
        # Time data
        name = tab.name_edit.text()
        # Time data
        start_str = tab.start_time_edit.text()
        start = gui_func.convert_time(string=start_str)
        end_str = tab.end_time_edit.text()
        end = gui_func.convert_time(string=end_str)
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
        root = sys.path[1]
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
        for i in range(len(load)):
            for k in range(load_quantity[i]):
                if load_quantity[i] == 1:
                    load_name = load[i]
                else:
                    load_name = load[i] + ' ' + str(k + 1)
                self.env[0].department[dep_index].room[-1].load.append(md.Load(env=self.env[0],
                                                                               name=load_name,
                                                                               data=None))
                self.env[0].department[dep_index].room[-1].load_names.append(load_name)

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
        print(data)
        self.env[0].department[dep_index].room[room_index].create_load(name=name,
                                                                       data=data)
        # Add name to viewer
        gui_func.add_to_viewer(widget=tab, item=[name])
        # Clear User Inputs
        gui_func.change_combo_index(combo=[tab.type_combo])

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
                # Open Warning Dialog before deleting hospital
                self.warning_dialog = DeleteDialog()
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
                tab(6).department.pop(item_index)
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
                self.env[0].department[dep_index].room[room_index].load.pop(load_index)
                self.env[0].department[dep_index].room[room_index].load_names.pop(load_index)

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
        :return:
        """
        tab = self.tabs.widget(6)
        # Clear and load profile ComboBox
        gui_func.clear_widget(widget=[tab.level_2_combo, tab.level_3_combo, tab.level_4_combo])
        level = tab.level_1_combo.currentIndex()
        gui_func.show_widget(widget=[tab.level_2_combo, tab.level_2,
                                     tab.level_3_combo, tab.level_3,
                                     tab.level_4_combo, tab.level_4],
                             show=False)
        # Add Items to load profile ComboBox based on selection in level ComboBox
        if isinstance(self.env[0], Environment):
            gui_func.enable_widget(widget=[tab.level_1_combo], enable=True)
            if level == 0:
                # Hospital
                tab.adjust_plot(time_series=self.env[0].time_series,
                                df=self.env[0].load_df['Total Load [W]'])
            elif level == 1:
                # Show, enable and add department names to level_2_combo
                gui_func.clear_widget(widget=[tab.level_2_combo])
                gui_func.show_widget(widget=[tab.level_2_combo, tab.level_2], show=True)
                gui_func.enable_widget(widget=[tab.level_2_combo], enable=True)
                tab.department = self.env[0].department_names
                gui_func.add_combo(widget=tab.level_2_combo, name=tab.department)
            elif level == 2:
                gui_func.clear_widget(widget=[tab.level_2_combo])
                tab.department = self.env[0].department_names
                gui_func.add_combo(widget=tab.level_2_combo, name=tab.department)
                # Show and enable level_2 and level_3_combo
                gui_func.enable_widget(widget=[tab.level_2_combo, tab.level_3_combo], enable=True)
                gui_func.show_widget(widget=[tab.level_2_combo, tab.level_2,
                                             tab.level_3_combo, tab.level_3],
                                     show=True)
            elif level == 3:
                tab.department = self.env[0].department_names
                gui_func.add_combo(widget=tab.level_2_combo, name=tab.department)
                gui_func.enable_widget(widget=[tab.level_2_combo, tab.level_3_combo, tab.level_4_combo], enable=True)
                gui_func.show_widget(widget=[tab.level_2_combo, tab.level_2,
                                             tab.level_3_combo, tab.level_3,
                                             tab.level_4_combo, tab.level_4],
                                     show=True)

    def level_2_combo(self):
        """

        :return:
        """
        tab = self.tabs.widget(5)
        dep_index = tab.level_2_combo.currentIndex()
        dep = self.env[0].department[dep_index]
        name = dep.name
        if tab.level_1_combo.currentIndex() == 1:
            tab.adjust_plot(time_series=self.env[0].time_series,
                            df=dep.load_df[name + ' Total Load [W]'])
        else:
            gui_func.clear_widget(widget=[tab.level_3_combo])
            tab.room = dep.room_names
            gui_func.add_combo(widget=tab.level_3_combo, name=tab.room)

    def level_3_combo(self):
        """

        :return:
        """
        tab = self.tabs.widget(5)
        dep_index = tab.level_2_combo.currentIndex()
        room_index = tab.level_3_combo.currentIndex()
        room = self.env[0].department[dep_index].room[room_index]
        name = room.name
        if tab.level_1_combo.currentIndex() == 2:
            tab.adjust_plot(time_series=self.env[0].time_series,
                            df=room.load_df[name + ' Total Load [W]'])
        else:
            gui_func.clear_widget(widget=[tab.level_4_combo])
            tab.consumer = room.load_names
            gui_func.add_combo(widget=tab.level_4_combo, name=tab.consumer)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TabWidget()
    sys.exit(app.exec())
