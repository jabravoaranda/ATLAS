#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  3 13:34:47 2022

@author: nick
"""

import sys
import numpy as np


def region(sig, x_vals, region, axis, squeeze = False):

    avg_height = (region[1] + region[0]) / 2.
    
    hwin = (region[1] - region[0]) / 2.
    
    # Get the reference height bin    
    avg_bin = get_avg_bin(x_vals = x_vals, avg_height = avg_height)

    # Get the reference window in bins    
    hwin_bin = get_hwin_bin(x_vals = x_vals, hwin = hwin)
        
    sig_sel = choose_from_axis(sig, axis, 
                               avg_bin - hwin_bin, 
                               avg_bin + hwin_bin + 1)

    if squeeze:
        avg = np.nanmean(sig_sel, axis = axis)
        std = np.nanstd(sig_sel, axis = axis)
        sem = std/np.sqrt(sig_sel.size)
    else:
        avg = np.nanmean(sig_sel, axis = axis, keepdims = True)
        std = np.nanstd(sig_sel, axis = axis, keepdims = True)
        sem = std/np.sqrt(sig_sel.size)
        
    return(avg, std, sem)

def get_avg_bin(x_vals, avg_height):

    if avg_height < x_vals[0]:
        raise Exception('-- Error: The height/distance provided for averaging is too low '+\
                        f'({avg_height}km) while the signal starts at {x_vals[0]}km')
        
    elif avg_height > x_vals[-1]:
        raise Exception('-- Error: Calibration height/distance provided for averaging is too high ' +
                        f'({avg_height}km) while the signal ends at {x_vals[-1]}km')
    else:
        avg_bin = np.where(x_vals >= avg_height)[0][0] 
        
    return(avg_bin)

def get_hwin_bin(x_vals, hwin):

    if hwin < (x_vals[1] - x_vals[0]):
        raise Exception('-- Error: The half calibration window provided '+\
                        f'({hwin}m) is smaller than the signal vertical step')
        
    else:
        hwin_bin = int(hwin / (x_vals[1] - x_vals[0]))
        
    return(hwin_bin)

def choose_from_axis(a, axis, start, stop):

    if axis <= a.ndim - 1:
    
        s = [slice(None) for i in range(a.ndim)]
        
        s[axis] = slice(start, stop)

    else:
        raise Exception('-- Error: The provided axis index is larger than '+
                        'the number of the axises of the array')
    
    return a[tuple(s)]