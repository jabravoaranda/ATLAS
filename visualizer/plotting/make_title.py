#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 22:34:11 2022

@author: nick
"""

import numpy as np

def quicklook(start_date, start_time, end_time, lidar, channel, 
              zan, loc, smooth, sm_lims, sm_hwin, sm_expo):
    
    zan = np.round(float(zan), decimals = 1)
    
    sm_llim = np.round(float(sm_lims[0]), decimals = 1)

    sm_ulim = np.round(float(sm_lims[-1]), decimals = 1)

    #FIXME: check if this is correct
    if isinstance(sm_hwin, list):
        sm_lhwin = np.round(float(sm_hwin[0]), decimals = 0)
        sm_uhwin = np.round(float(sm_hwin[-1]), decimals = 0)
    else:
        sm_lhwin = sm_uhwin = np.round(float(sm_hwin), decimals = 0)
            
    if sm_expo == True:
        sm_type = 'Exponential'
    else:
        sm_type = 'Linear'

    if sm_lhwin > sm_uhwin:
        change = 'Decrease'
    else:
        change = 'Increase'
        
    date = f'{start_date[6:]}.{start_date[4:6]}.{start_date[:4]}'
    
    start = f'{start_time[:2]}:{start_time[2:4]}:{start_time[4:6]}'

    end = f'{end_time[:2]}:{end_time[2:4]}:{end_time[4:6]}'
    
    if smooth == True:
        if sm_lhwin == sm_uhwin:
            title = f'{lidar} {loc} {channel} - Quicklook - Smoothing: {sm_llim} to {sm_ulim} Km, Half Win.: {sm_uhwin}m\n'+\
                        f'On {date} from {start} to {end} UTC, '+r'$\nearrow$'+f'{zan}'+r'$^{o}$ off-zenith'
        else:
            title = f'{lidar} {loc} {channel} - Quicklook - Smoothing: {sm_llim} to {sm_ulim} Km, Half Win.: {sm_lhwin}m to {sm_uhwin}m, {change}: {sm_type}\n'+\
                        f'On {date} from {start} to {end} UTC, '+r'$\nearrow$'+f'{zan}'+r'$^{o}$ off-zenith'
    else:
        title = f'{lidar} {loc} {channel} - Quicklook - No Smoothing'+'\n'+\
                f'On {date} from {start} to {end} UTC, '+r'$\nearrow$'+f'{zan}'+r'$^{o}$ off-zenith'
                        
    return(title)

def rayleigh(start_date, start_time, end_time, lidar, channel, 
             zan, loc, ewl, dwl, bdw, smooth, sm_lims, sm_hwin, sm_expo,
             mol_method, st_name, rs_start_date, rs_start_time, wmo_id, wban_id):
    
    zan = np.round(float(zan), decimals = 1)
    
    ewl = np.round(float(ewl), decimals = 2)

    dwl = np.round(float(dwl), decimals = 2)
    
    bdw = np.round(float(bdw), decimals = 2)
    
    sm_llim = np.round(float(sm_lims[0]), decimals = 1)

    sm_ulim = np.round(float(sm_lims[-1]), decimals = 1)

    sm_lhwin = np.round(float(sm_hwin[0]), decimals = 0)

    sm_uhwin = np.round(float(sm_hwin[-1]), decimals = 0)
    
    if sm_expo == True:
        sm_type = 'Exponential'
    else:
        sm_type = 'Linear'
        
    if sm_lhwin > sm_uhwin:
        change = 'Decrease'
    else:
        change = 'Increase'
        
    # lat = np.round(float(lat), decimals = 3)

    # lon = np.round(float(lon), decimals = 3)

    # elv = np.round(float(elv), decimals = 0)
    
    # loc = f'lat: {lat}$^o$, lon: {lon}$^o$, alt: {elv} m'
        
    date = f'{start_date[6:]}.{start_date[4:6]}.{start_date[:4]}'
    
    start = f'{start_time[:2]}:{start_time[2:4]}:{start_time[4:6]}'

    end = f'{end_time[:2]}:{end_time[2:4]}:{end_time[4:6]}'

    rs_date = f'{rs_start_date[6:]}.{rs_start_date[4:6]}.{rs_start_date[:4]}'
    
    rs_start = f'{rs_start_time[:2]}:{rs_start_time[2:4]}'
    
    if mol_method == 'Radiosonde': 
        mol_part = f' - {mol_method} {st_name} {wmo_id} {wban_id} {rs_date} {rs_start}UT'
    else: mol_part = f' - {mol_method}'
    
    if smooth == True:
        if sm_lhwin == sm_uhwin:
            title = f'{lidar} {loc} {channel} - Rayleigh Fit - Smoothing: {sm_llim} to {sm_ulim} Km, Half Win.: {sm_uhwin}m\n'+\
                        f'On {date} from {start} to {end} UTC, '+r'$\nearrow$'+f'{zan}'+r'$^{o}$ off-zenith' + mol_part + '\n'+\
                            f'{mol_method} {st_name} {wmo_id} {wban_id} - Emitted WL: {ewl}nm, Received WL: {dwl}nm, Bandwidth: {bdw}nm'
        else:
            title = f'{lidar} {loc} {channel} - Rayleigh Fit - Smoothing: {sm_llim} to {sm_ulim} Km, Half Win.: {sm_lhwin}m to {sm_uhwin}m, {change}: {sm_type}\n'+\
                        f'On {date} from {start} to {end} UTC, '+r'$\nearrow$'+f'{zan}'+r'$^{o}$ off-zenith'+f' - {mol_method} {st_name} {wmo_id} {wban_id}'+'\n'+\
                            f'Emitted WL: {ewl}nm, Received WL: {dwl}nm, Bandwidth: {bdw}nm'     
    else:
        title = f'{lidar} {loc} {channel} - Rayleigh Fit - No Smoothing'+'\n'+\
                    f'On {date} from {start} to {end} UTC, '+r'$\nearrow$'+f'{zan}'+r'$^{o}$ off-zenith'+f' - {mol_method} {st_name} {wmo_id} {wban_id}'+'\n'+\
                        f'Emitted WL: {ewl}nm, Received WL: {dwl}nm, Bandwidth: {bdw}nm'   
                     
    
    return(title)

def telecover(start_date, start_time, end_time, lidar, channel, 
              zan, loc, iters, sampling, smooth, sm_lims, sm_hwin, sm_expo):
    
    zan = np.round(float(zan), decimals = 1)
    
    sm_llim = np.round(float(sm_lims[0]), decimals = 1)

    sm_ulim = np.round(float(sm_lims[-1]), decimals = 1)

    sm_lhwin = np.round(float(sm_hwin[0]), decimals = 0)

    sm_uhwin = np.round(float(sm_hwin[-1]), decimals = 0)
    
    if sm_expo == True:
        sm_type = 'Exponential'
    else:
        sm_type = 'Linear'

    if sm_lhwin > sm_uhwin:
        change = 'Decrease'
    else:
        change = 'Increase'
        
    date = f'{start_date[6:]}.{start_date[4:6]}.{start_date[:4]}'
    
    start = f'{start_time[:2]}:{start_time[2:4]}:{start_time[4:6]}'

    end = f'{end_time[:2]}:{end_time[2:4]}:{end_time[4:6]}'
        
    
    if smooth == True:
        if sm_lhwin == sm_uhwin:
            sm_text = f' - Smoothing: {sm_llim} to {sm_ulim} Km, Half Win.: {sm_uhwin}m'

        else:
            sm_text = f' - Smoothing: {sm_llim} to {sm_ulim} Km, Half Win.: {sm_uhwin}m, {change}: {sm_type}'

    else:
        sm_text = ''
        
    title = f'{lidar} {loc} {channel} - Telecover Test{sm_text}\n'+\
                f'On {date} from {start} to {end} UTC, '+r'$\nearrow$'+f'{zan}'+r'$^{o}$ off-zenith' + f' - Iterations: {iters}, Sampling Time per Iteration: {sampling}s'
                
    return(title)

def polarization_calibration(start_date_cal, start_time_cal, end_time_cal,
                             start_date_ray, start_time_ray, end_time_ray,  
                             lidar, channel_r, channel_t, zan, loc, 
                             ewl, dwl, bdw, smooth, sm_lims, sm_hwin, sm_expo,
                             mol_method, st_name, wmo_id, wban_id):
    
    zan = np.round(float(zan), decimals = 1)
    
    ewl = np.round(float(ewl), decimals = 2)

    dwl = np.round(float(dwl), decimals = 2)
    
    bdw = np.round(float(bdw), decimals = 2)
    
    sm_llim = np.round(float(sm_lims[0]), decimals = 1)

    sm_ulim = np.round(float(sm_lims[-1]), decimals = 1)

    sm_lhwin = np.round(float(sm_hwin[0]), decimals = 0)

    sm_uhwin = np.round(float(sm_hwin[-1]), decimals = 0)
            
    if sm_expo == True:
        sm_type = 'Exponential'
    else:
        sm_type = 'Linear'

    if sm_lhwin > sm_uhwin:
        change = 'Decrease'
    else:
        change = 'Increase'
        
    date_cal = f'{start_date_cal[6:]}.{start_date_cal[4:6]}.{start_date_cal[:4]}'
    
    start_cal = f'{start_time_cal[:2]}:{start_time_cal[2:4]}:{start_time_cal[4:6]}'

    end_cal = f'{end_time_cal[:2]}:{end_time_cal[2:4]}:{end_time_cal[4:6]}'

    date_ray = f'{start_date_ray[6:]}.{start_date_ray[4:6]}.{start_date_ray[:4]}'
    
    start_ray = f'{start_time_ray[:2]}:{start_time_ray[2:4]}:{start_time_ray[4:6]}'

    end_ray = f'{end_time_ray[:2]}:{end_time_ray[2:4]}:{end_time_ray[4:6]}'
               
    # title = f'Ratio {channel_r} to {channel_t}: {lidar} at {loc}\n '+\
    #             f'Calibration on {date_cal} from {start_cal} to {end_cal} UTC, '+\
    #                 r'$\nearrow$' + f' {zan}' + r'$^{o}$ off-zenith'+ f'\n'+\
    #                     f'Rayleigh on {date_ray} from {start_ray} to {end_ray} UTC, '+\
    #                         r'$\nearrow$' + f' {zan}' + r'$^{o}$ off-zenith'
    if smooth == True:
        if sm_lhwin == sm_uhwin:
            title = f'{lidar} {loc} {channel_r} to {channel_t} - Pol. Calibration - Smoothing: {sm_llim} to {sm_ulim} Km, Half Win.: {sm_uhwin}m\n'+\
                        f'Calibration on {date_cal} from {start_cal} to {end_cal} UTC, '+\
                            r'$\nearrow$' + f' {zan}' + r'$^{o}$ off-zenith'+ '\n'+\
                                f'Rayleigh on {date_ray} from {start_ray} to {end_ray} UTC, '+\
                                    r'$\nearrow$' + f' {zan}' + r'$^{o}$ off-zenith'+f' - {mol_method} {st_name} {wmo_id} {wban_id}'+'\n'+\
                                        f'Emitted WL: {ewl}nm, Received WL: {dwl}nm, Bandwidth: {bdw}nm'   
        else:
            title = f'{lidar} {loc} {channel_r} to {channel_t} - Pol. Calibration - Smoothing: {sm_llim} to {sm_ulim} Km, Half Win.: {sm_lhwin}m to {sm_uhwin}m, {change}: {sm_type}\n'+\
                        f'Calibration on {date_cal} from {start_cal} to {end_cal} UTC, '+\
                            r'$\nearrow$' + f' {zan}' + r'$^{o}$ off-zenith'+ '\n'+\
                                f'Rayleigh on {date_ray} from {start_ray} to {end_ray} UTC, '+\
                                    r'$\nearrow$' + f' {zan}' + r'$^{o}$ off-zenith'+f' - {mol_method} {st_name} {wmo_id} {wban_id}'+'\n'+\
                                        f'Emitted WL: {ewl}nm, Received WL: {dwl}nm, Bandwidth: {bdw}nm'   
    else:
        title = f'{lidar} {loc} {channel_r} to {channel_t} - Pol. Calibration - No Smoothing'+'\n'+\
                    f'Calibration on {date_cal} from {start_cal} to {end_cal} UTC, '+\
                        r'$\nearrow$' + f' {zan}' + r'$^{o}$ off-zenith'+ '\n'+\
                            f'Rayleigh on {date_ray} from {start_ray} to {end_ray} UTC, '+\
                                r'$\nearrow$' + f' {zan}' + r'$^{o}$ off-zenith'+f' - {mol_method} {st_name} {wmo_id} {wban_id}'+'\n'+\
                                    f'Emitted WL: {ewl}nm, Received WL: {dwl}nm, Bandwidth: {bdw}nm'  

    return(title)

def intercomparison(start_date, start_time, end_time, lidar_1, lidar_2, 
                    channel_1, channel_2, zan, lat, lon, elv):
    
    zan = np.round(float(zan), decimals = 1)
    
    lat = np.round(float(lat), decimals = 3)

    lon = np.round(float(lon), decimals = 3)

    elv = np.round(float(elv), decimals = 0)
    
    loc = f'lat: {lat}$^o$, lon: {lon}$^o$, alt: {elv} m'
        
    date = f'{start_date[6:]}.{start_date[4:6]}.{start_date[:4]}'
    
    start = f'{start_time[:2]}:{start_time[2:4]}:{start_time[4:6]}'

    end = f'{end_time[:2]}:{end_time[2:4]}:{end_time[4:6]}'
        
    title = f'{lidar_1} {channel_1} vs {lidar_2} {channel_2} at {loc}\n'+\
                f'On {date} from {start} to {end} UTC, '+r'$\nearrow$'+\
                    f' {zan}'+r'$^{o}$ off-zenith' 
    
    return(title)