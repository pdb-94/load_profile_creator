"""
Module including GUI functions

@author: Paul Bohn
@contributor: Paul Bohn
"""

__version__ = '0.1'
__author__ = 'pdb-94'


def convert_time(string: str):
    """
    Convert text into int
    :param string: str
        time string
    :return: hour, minute: int
    """
    time_list = string.split(':')
    hour = int(time_list[0])
    minute = int(time_list[1])

    return hour, minute


def show_widget(widget: list, show: bool = True):
    """
    Show buttons
    :param widget: list
        buttons to show
    :param show: bool
        boolean value to show widgets
    :return: None
    """
    if show is True:
        for i in range(len(widget)):
            widget[i].show()
    elif show is False:
        for i in range(len(widget)):
            widget[i].hide()


def enable_widget(widget: list, enable: bool = True):
    """
    Show widgets
    :param widget: list
        buttons to show
    :param enable: bool
        boolean value to enable widgets
    :return: None
    """
    for i in range(len(widget)):
        widget[i].setEnabled(enable)


def delete_from_viewer(widget, item: int):
    """
    Delete Item from ListWidget
    :param widget: PyQt5 ListWidget()
        ListWidget from tab
    :param item: list
        strings to delete from ListWidget
    :return:
    """
    viewer = widget.viewer
    viewer.takeItem(item)


def add_to_viewer(widget, item: list):
    """
    Add Item to ListWidget
    :param widget: PyQt5 ListWidget
        ListWidget from tab
    :param item: list
        strings to add to ListWidget
    :return: None
    """
    viewer = widget.viewer
    viewer.addItems(item)


def add_to_room_viewer(widget, item: list):
    """
    Add Item to Room ListWidget
    :param widget: PyQt5 ListWidget
        ListWidget from tab
    :param item: list
        strings to add to ListWidget
    :return: None
    """
    viewer = widget.viewer
    if viewer.count() == 0:
        viewer.addItems(item)


def add_combo(widget, name: list):
    """
    Add Item to department_ComboBox in Tab Room
    :param widget: PyQt5 ComboBox
        QComboBox
    :param name: list
        items to add to ComboBox
    :return: None
    """
    combo_box = widget
    combo_box.addItems(name)


def change_combo_index(combo: list):
    """
    Show first item in ComboBox
    :param combo: list
    :return: None
    """
    for combobox in combo:
        if combobox.count() == 0:
            pass
        else:
            combobox.setCurrentIndex(0)


def delete_from_combo(combo, index):
    """
    :param combo: PyQt5 QComboBox
        QComboBox
    :param index: int
        row to delete
    :return: None
    """
    combo.removeItem(index)


def clear_widget(widget: list):
    """
    Clear widgets
    :param widget: PyQt5 Widget
        Widget to clear
    :return: None
    """
    for i in range(len(widget)):
        widget[i].clear()


def change_widget_text(widget: list, text: list):
    """
    Change widget text
    :param widget: PyQt5 Widget
        Widget to change text
    :param text: str
        new text
    :return: NOne
    """
    for i in range(len(widget)):
        widget[i].setText(text[i])
