# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 07:24:36 2018

@author: Trace
"""
import time
import math
from .bike import Bike

tss_dict = {'Olympic': 
                {'swim': {'min': 30, 'max': 40},
                 'bike': {'min': 90, 'max': 110},
                 'run': {'min': 50, 'max': 70}},
            'Half-iron':
                {'swim': {'min': 50, 'max': 70},
                 'bike': {'min': 160, 'max': 190},
                 'run': {'min': 110, 'max': 130}},
            'Iron':
                {'swim': {'min': 100, 'max': 130},
                 'bike': {'min': 280, 'max': 360},
                 'run': {'min': 200, 'max': 250}}}

dist_dict = {'Olympic': 
                {'swim': 0.93,
                'bike': 24.85,
                'run': 6.21},
            'Half-iron':
                {'swim': 1.2,
                'bike': 56,
                'run': 13.1},
            'Iron':
                {'swim': 2.4,
                'bike': 112,
                'run': 26.2}}

def swim_calc(swim_css, swim_if, race_type):
    
    swim_if = float(swim_if)
    
    css_yd_min = 100 / (time.strptime(swim_css, '%H:%M:%S')[4] + time.strptime(swim_css, '%H:%M:%S')[5]/60)
    swim_speed_yd_min = css_yd_min * swim_if
    
    swim_time = (dist_dict[race_type]['swim'] * 1760) / (swim_speed_yd_min * 60)
    swim_tss = round(swim_if**3 * 100 * swim_time, 2)
    swim_pace = 100 / swim_speed_yd_min
    
    swim_time_str = time.strftime("%H:%M:%S", time.gmtime(swim_time*60*60))
    swim_pace = time.strftime("%H:%M:%S", time.gmtime(swim_pace*60))
    
    swim_dict = {'swim_time': swim_time,
                 'swim_time_str': swim_time_str,
                 'swim_tss': swim_tss,
                 'swim_pace': swim_pace}
    
# =============================================================================
#     swim_dict = {'swim_time': type(swim_css),
#                   'swim_tss': type(swim_if),
#                   'swim_pace': type(race_type)}
# =============================================================================
    
    return swim_dict

def bike_calc(bike_ftp, mass):
    bike_ftp = int(bike_ftp)
    mass = int(mass)

    bike_course = 'utils/GPX-Route_6863_340.gpx'
    intensities = [0.25, 0.43, .8, .85, 1]
    grades = [-0.05, -0.02, 0.02, 0.05]

    bk = Bike(bike_course, bike_ftp, mass, intensities, grades)
    print(bk.bike_gpx)
    bk.predict()

    bike_time_str = time.strftime("%H:%M:%S", time.gmtime(bk.total_time*60*60))

    bike_dict = {'bike_time': bk.total_time,
                 'bike_time_str': bike_time_str,
                 'bike_tss': round(bk.tss, 2),
                 'bike_pace': round(bk.avg_velocity) * 0.62}

    return bike_dict

def run_calc(run_ftpa, run_if, race_type):

    run_if = float(run_if)

    run_pace_min_mi = (time.strptime(run_ftpa, '%H:%M:%S')[4] + time.strptime(run_ftpa, '%H:%M:%S')[5]/60) / run_if
    run_speed_mph = 60 / run_pace_min_mi

    run_time = dist_dict[race_type]['run'] / run_speed_mph
    run_tss = round(run_if**2 * 110 * run_time, 2)

    run_time_str = time.strftime("%H:%M:%S", time.gmtime(run_time*60*60))
    run_pace = time.strftime("%H:%M:%S", time.gmtime(run_pace_min_mi*60))

    run_dict = {'run_time': run_time,
                'run_time_str': run_time_str,
                'run_tss': run_tss,
                'run_pace': run_pace}

    return run_dict

def predict_race(inputs):

    race_type = inputs['race_type']

    results = swim_calc(inputs['swim_css'], inputs['swim_if'], race_type)
    results.update(bike_calc(inputs['bike_ftp'], inputs['mass']))
    results.update(run_calc(inputs['run_ftpa'], inputs['run_if'], race_type))

    race_time = results['swim_time'] + results['bike_time'] + results['run_time'] + (3/60)
    race_time_str = time.strftime("%H:%M:%S", time.gmtime(race_time*60*60))
    race_tss = round(results['swim_tss'] + results['bike_tss'] + results['run_tss'], 2)

    results['race_time'] = race_time
    results['race_time_str'] = race_time_str
    results['race_tss'] = race_tss

    return results