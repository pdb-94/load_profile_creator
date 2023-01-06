"""
Main module to run the Load Profile Creator (LPC) without GUI

@author: Paul Bohn
@contributor: Paul Bohn (TH Köln), Moritz End (TH Köln)
"""

__version__ = '0.1'
__author__ = 'pdb-94'


import datetime as dt
from environment import Environment

env = Environment(name='St. Dominics_3', time_data=[dt.datetime(year=2023, month=1, day=6, hour=0, minute=0),
                                                    dt.datetime(year=2023, month=1, day=6, hour=23, minute=59),
                                                    dt.timedelta(minutes=1)])
env.create_department(name='Administration',
                      t_start=dt.time(hour=7, minute=0),
                      t_end=dt.time(hour=20, minute=0))
names = ['Accounts Office', 'Administration Office', 'Administrator', 'Biostars/Account', 'Consulting Room 1',
         'Consulting Room 2', 'Consulting Room 3', 'Consulting Room 4', 'Consulting Room 5', 'Consulting Room 6',
         'Consulting Room 7', 'Consulting Room 8', 'Dispensary', 'Doctors Room', 'Emergency Consulting',
         'Emergency Ward',
         'Financial Controller', 'Head Finance', 'HR', 'Insurance Office', 'Internal Audit', 'Manufacturing Room',
         'Medical Director', 'Nursing Administration', 'Office', 'OPD Screening', 'Pay Office', 'Pharmacy Office',
         'Pharmacy Store', 'Records Department', 'Work Shop']
start = [dt.time(hour=7, minute=30), dt.time(hour=7, minute=0), dt.time(hour=7, minute=30), dt.time(hour=7, minute=30),
         dt.time(hour=7, minute=30), dt.time(hour=7, minute=30), dt.time(hour=7, minute=30), dt.time(hour=7, minute=30),
         dt.time(hour=7, minute=30), dt.time(hour=7, minute=30), dt.time(hour=7, minute=30), dt.time(hour=7, minute=30),
         dt.time(hour=0, minute=0), dt.time(hour=7, minute=30), dt.time(hour=7, minute=0), dt.time(hour=7, minute=0),
         dt.time(hour=7, minute=0), dt.time(hour=7, minute=30), dt.time(hour=7, minute=30), dt.time(hour=7, minute=30),
         dt.time(hour=7, minute=30), dt.time(hour=7, minute=0), dt.time(hour=7, minute=0), dt.time(hour=7, minute=30),
         dt.time(hour=7, minute=30), dt.time(hour=7, minute=0), dt.time(hour=7, minute=0), dt.time(hour=7, minute=30),
         dt.time(hour=7, minute=30), dt.time(hour=7, minute=30), dt.time(hour=7, minute=30), dt.time(hour=8, minute=0)]
end = [dt.time(hour=17, minute=00), dt.time(hour=18, minute=0), dt.time(hour=17, minute=30), dt.time(hour=18, minute=0),
       dt.time(hour=17, minute=30), dt.time(hour=17, minute=30), dt.time(hour=17, minute=30),
       dt.time(hour=17, minute=30),
       dt.time(hour=17, minute=30), dt.time(hour=17, minute=30), dt.time(hour=17, minute=30),
       dt.time(hour=17, minute=30),
       dt.time(hour=23, minute=59), dt.time(hour=18, minute=0), dt.time(hour=20, minute=0), dt.time(hour=19, minute=0),
       dt.time(hour=20, minute=0), dt.time(hour=17, minute=0), dt.time(hour=17, minute=0), dt.time(hour=7, minute=30),
       dt.time(hour=18, minute=30), dt.time(hour=18, minute=0), dt.time(hour=20, minute=0), dt.time(hour=18, minute=0),
       dt.time(hour=19, minute=0), dt.time(hour=20, minute=0), dt.time(hour=19, minute=0), dt.time(hour=18, minute=0),
       dt.time(hour=17, minute=30), dt.time(hour=17, minute=30), dt.time(hour=18, minute=0), dt.time(hour=16, minute=0)]
file = ['accounts_office.csv', 'administration_office.csv', 'administrator.csv', 'biostars_account.csv', 'consulting_r1.csv',
        'consulting_r2.csv', 'consulting_r3.csv', 'consulting_r4.csv', 'consulting_r5.csv', 'consulting_r6.csv', 'consulting_r7.csv',
        'consulting_r8.csv', 'corridor.csv', 'dispensary.csv', 'doctors_room.csv', 'emergency_consulting.csv', 'emergency_ward.csv',
        'financial_controller.csv', 'head_finance.csv', 'human_resources.csv', 'insurance_office.csv', 'internal_audit.csv',
        'manufacturing_room.csv', 'medical_director.csv', 'nursing_administration.csv', 'office.csv', 'opd_screening_room.csv',
        'pharmacy_office.csv', 'pharmacy_store.csv', 'records_department.csv', 'work_shop.csv']
for i in range(len(names)):
    env.department[0].create_room(standard=True, name=names[i],
                                  t_start=start[i],
                                  t_end=end[i],
                                  path='/data/room/Masterarbeit/',
                                  file=file[i])
env.build_load_profiles()
env.create_export_dir()
