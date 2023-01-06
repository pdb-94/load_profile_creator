"""
Main module to run Load Profile Creator (LPC)

@author: Paul Bohn
@contributor: Paul Bohn (TH Köln), Moritz End (TH Köln)
"""

__version__ = '0.1'
__author__ = 'pdb-94'

import sys
import datetime as dt
from PyQt5.QtWidgets import *
from gui.tab_widget import TabWidget
from environment import Environment
from models import Department, Room, Load

app = QApplication(sys.argv)
lpc = TabWidget()
sys.exit(app.exec())

# env = Environment(name='St. Dominics_3', time_data=[dt.datetime(year=2023, month=1, day=6, hour=0, minute=0),
#                                                     dt.datetime(year=2023, month=1, day=6, hour=23, minute=59),
#                                                     dt.timedelta(minutes=1)])
# env.create_department(name='Administration',
#                       t_start=dt.time(hour=7, minute=0),
#                       t_end=dt.time(hour=20, minute=0))
# names = ['Accounts Office', 'Administration Office', 'Administrator', 'Biostars/Account', 'Consulting Room 1',
#          'Consulting Room 2', 'Consulting Room 3', 'Consulting Room 4', 'Consulting Room 5', 'Consulting Room 6',
#          'Consulting Room 7', 'Consulting Room 8', 'Dispensary', 'Doctors Room', 'Emergency Consulting',
#          'Emergency Ward',
#          'Financial Controller', 'Head Finance', 'HR', 'Insurance Office', 'Internal Audit', 'Manufacturing Room',
#          'Medical Director', 'Nursing Administration', 'Office', 'OPD Screening', 'Pay Office', 'Pharmacy Office',
#          'Pharmacy Store', 'Records Department', 'Work Shop']
# start = [dt.time(hour=7, minute=30), dt.time(hour=7, minute=0), dt.time(hour=7, minute=30), dt.time(hour=7, minute=30),
#          dt.time(hour=7, minute=30), dt.time(hour=7, minute=30), dt.time(hour=7, minute=30), dt.time(hour=7, minute=30),
#          dt.time(hour=7, minute=30), dt.time(hour=7, minute=30), dt.time(hour=7, minute=30), dt.time(hour=7, minute=30),
#          dt.time(hour=0, minute=0), dt.time(hour=7, minute=30), dt.time(hour=7, minute=0), dt.time(hour=7, minute=0),
#          dt.time(hour=7, minute=0), dt.time(hour=7, minute=30), dt.time(hour=7, minute=30), dt.time(hour=7, minute=30),
#          dt.time(hour=7, minute=30), dt.time(hour=7, minute=0), dt.time(hour=7, minute=0), dt.time(hour=7, minute=30),
#          dt.time(hour=7, minute=30), dt.time(hour=7, minute=0), dt.time(hour=7, minute=0), dt.time(hour=7, minute=30),
#          dt.time(hour=7, minute=30), dt.time(hour=7, minute=30), dt.time(hour=7, minute=30), dt.time(hour=8, minute=0)]
# end = [dt.time(hour=17, minute=00), dt.time(hour=18, minute=0), dt.time(hour=17, minute=30), dt.time(hour=18, minute=0),
#        dt.time(hour=17, minute=30), dt.time(hour=17, minute=30), dt.time(hour=17, minute=30),
#        dt.time(hour=17, minute=30),
#        dt.time(hour=17, minute=30), dt.time(hour=17, minute=30), dt.time(hour=17, minute=30),
#        dt.time(hour=17, minute=30),
#        dt.time(hour=23, minute=59), dt.time(hour=18, minute=0), dt.time(hour=20, minute=0), dt.time(hour=19, minute=0),
#        dt.time(hour=20, minute=0), dt.time(hour=17, minute=0), dt.time(hour=17, minute=0), dt.time(hour=7, minute=30),
#        dt.time(hour=18, minute=30), dt.time(hour=18, minute=0), dt.time(hour=20, minute=0), dt.time(hour=18, minute=0),
#        dt.time(hour=19, minute=0), dt.time(hour=20, minute=0), dt.time(hour=19, minute=0), dt.time(hour=18, minute=0),
#        dt.time(hour=17, minute=30), dt.time(hour=17, minute=30), dt.time(hour=18, minute=0), dt.time(hour=16, minute=0)]
# file = ['accounts_office', 'administration_office', 'administrator', 'biostars_account', 'consulting_r1',
#         'consulting_r2', 'consulting_r3', 'consulting_r4', 'consulting_r5', 'consulting_r6', 'consulting_r7',
#         'consulting_r8', 'corridor', 'dispensary', 'doctors_room', 'emergency_consulting', 'emergency_ward',
#         'financial_controller', 'head_finance', 'human_resources', 'insurance_office', 'internal_audit',
#         'manufacturing_room', 'medical_director', 'nursing_administration', 'office', 'opd_screening_room',
#         'pharmacy_office', 'pharmacy_store', 'records_department', 'work_shop']
# for i in range(len(names)):
#     env.department[0].create_room(standard=True, name=names[i],
#                                   t_start=start[i],
#                                   t_end=end[i],
#                                   path='/data/room/Masterarbeit/',
#                                   file=file[i])
# env.build_load_profiles()
# env.create_export_dir()
