#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 15:00:07 2022

@author: nick
"""

from pdb import set_trace
import numpy as np
import os

def rayleigh(dir_out, fname, header, alt, atb, rcs):
    

    body = np.vstack((alt, atb, rcs)).T

    mask = np.any(np.isnan(body), axis = 1)
    body = body[~mask,:]
    
    fpath = os.path.join(dir_out, 'ascii', fname)
    
    np.savetxt(fpath, body, header = header, comments = '')
    
    return()

def telecover(dir_out, fname, header, iters, 
              alt, sectors, sectors_e):

    sectors_l = np.array([sectors[key] for key in sectors_e.keys() 
                          if isinstance(sectors[key], list) == False])
    
    extra_sector_l = np.array([sectors_e[key] for key in sectors_e.keys() 
                               if isinstance(sectors_e[key], list) == False])
    
    body = np.concatenate((np.array([alt]), sectors_l, extra_sector_l), axis = 0).T
    
    mask = np.any(np.isnan(body), axis = 1)
    body = body[~mask,:]
 
    fpath = os.path.join(dir_out, 'ascii', fname)
    
    np.savetxt(fpath, body, header = header, comments = '')
    
    return()

def polarisation_calibration(dir_out, fname, alt_cal, alt_ray,
                             r_p45, t_p45, r_m45, t_m45, ray_r, ray_t, header):
    
    if (np.abs(alt_cal - alt_ray) < 1E-3).all():
        alt = alt_cal
        
    body = np.vstack((alt, r_p45, t_p45, r_m45, t_m45, ray_r, ray_t)).T

    mask = np.any(np.isnan(body), axis = 1)
    body = body[~mask,:]
    
    fpath = os.path.join(dir_out, 'ascii', fname)
    
    np.savetxt(fpath, body, header = header, comments = '')
    
    return()