"""
@authors: Nikolaos Siomos (nikolaos.siomos@lmu.de)

================
General:
    Parses the command line arguments provided when calling __main_ 
    The information is stored in a python dictionary
    
Returns:
    
    args:
        A dictionary with all the information provided as command line arguments
        
"""

import argparse
import os
from pdb import set_trace

def call_parser():
        
    """Collects the information included as commandline arguments. 
    """
    
    print('Parsing SCC_Converter arguments...')    
    
    parser = argparse.ArgumentParser(
    	description='arguments ')
    

    parser.add_argument('-f', '--parent_folder', metavar='parent_folder', 
                        type=str, nargs='?',  default = None,
                        help='The path to the parent folder that contains the normal folder and all other optional input folders (dark, atmosphere, overlap). If no results folder is provided, it will be exported here by default')

    parser.add_argument('--dark_folder', metavar='dark_folder', 
                        type=str, nargs='?', default = None,
                        help='The path to the dark folder. Defaults to a drk folder inside the parent folder')

    parser.add_argument('--rayleigh_folder', metavar='rayleigh_folder', 
                        type=str, nargs='?', default = None,
                        help='The path to the rayleigh fit measurement folder. Defaults to a nrm folder inside the parent folder')
    
    parser.add_argument('--telecover_sectors_folder', metavar='telecover_sectors_folder', 
                        type=str, nargs='?', default = None,
                        help='The path to the telecover folder that contains the sector files. Defaults to a tlc/sectors folder inside the parent folder')

    parser.add_argument('--telecover_rings_folder', metavar='telecover_rings_folder', 
                        type=str, nargs='?', default = None,
                        help='The path to the telecover folder that contains the ring (inner/outer) files. Defaults to a tlc/rings folder inside the parent folder')
        
    parser.add_argument('--pcb_cal_p45_folder', metavar='pcb_cal_p45_folder', 
                        type=str, nargs='?', default = None,
                        help='The path to the polarization calibration +45 folder. Defaults to a pcb/+45 folder inside the parent folder')

    parser.add_argument('--pcb_cal_m45_folder', metavar='pcb_cal_m45_folder', 
                        type=str, nargs='?', default = None,
                        help='The path to the polarization calibration -45 folder. Defaults to a pcb/-45 folder inside the parent folder')

    parser.add_argument('--pcb_cal_stc_folder', metavar='pcb_cal_stc_folder', 
                        type=str, nargs='?', default = None,
                        help='The path to the polarization calibration folder for a calibration with a single calibrator position. Defaults to a pcb/stc folder inside the parent folder')

    parser.add_argument('--radiosonde_folder', metavar='radiosonde_folder', 
                        type=str, nargs='?', default = None,
                        help='The path to the radiosonde folder. The radiosonde file that is closest to the measurement within 12h will be selected if more than 1 files are provided inside')    
    
    parser.add_argument('-o', '--output_folder', metavar='scc_converter', 
                        type=str, nargs='?', default = None,
                        help='The path to the results folder. This optional argument can be used if the results folder must be placed out of the parent_folder. Defaults to parent_folder/scc_converter ')

    parser.add_argument('-d', '--debug', metavar = 'debug',
                        type = bool, default = False, 
                        action = argparse.BooleanOptionalAction,
                        help = 'If called then debugging files will be generated in ./results/debug folder. These included the metadata gathered from the configuration file, the licel header, and the combination of the two. Default to False ')

    parser.add_argument('-c', '--config_file', metavar='config_file', 
                        type=str, nargs='?', default = None,
                        help='The absolute path to the configuration file that contains the necessary lidar/channel metadata. This optional argument can be used if the settings folder must be placed out of the parent_folder (defaults to ./<parent_folder>/config_file.ini)')            

    parser.add_argument('--radiosonde_filename', metavar='radiosonde_filename', 
                        type=str, nargs='?', default = None, 
                        help='Corresponding radiosonde filename. Use mode A in order to automatically include it by processing both rayleigh and radiosonde folders. Providing it as an argument will override the automatic detection with mode A')            

    parser.add_argument('--rayleigh_filename', metavar='rayleigh_filename', 
                        type=str, nargs='?', default = None,
                        help='Corresponding rayleigh filename. Mandatory to provid when processing a depolarization calibration measurement. Use mode A in order to automatically include it by processing both rayleigh and calibration folders. Providing it as an argument will override the automatic detection with mode A')          

    parser.add_argument('-P', '--ground_pressure', metavar='ground_pressure', 
                        type=str, nargs='?', default = 1013.25,
                        help='The atmospheric pressure in the lidar station in hPa. Defaults to 1013hPa')            

    parser.add_argument('-T', '--ground_temperature', metavar='ground_temperature', 
                        type=str, nargs='?', default = 273.15,
                        help='The atmospheric temperature in the lidar station in K. Defaults to 293.15 K')            

    parser.add_argument('--files_per_sector', metavar='files_per_sector', 
                        type=int, nargs='?', default = None,
                        help='The number of telecover files per sector. If called, an automated assignment of the telecover files in different sectors will be attempted serially')            
    
    parser.add_argument('--files_per_ring', metavar='files_per_ring', 
                        type=int, nargs='?', default = None,
                        help='The number of telecover files per ring. If called, an automated assignment of the telecover files in different rings will be attempted serially')            

    parser.add_argument('--file_format', metavar='file_format', 
                        type=str, nargs='?', default = 'licel',
                        help="Raw file format.  Currently only licel is supported and polly_xt is being prepared. Defaults to 'licel'.")   
         
    parser.add_argument('-M', '--mode', metavar='mode', 
                        type=str, nargs='?', default = 'A',
                        help="The processing mode. Select between A: Automated, R: Rayleigh, T: Telecover, C: Polarization Calibration, D: Standalone Dark. Defaults to A. By using A the algorithm will process all available measurements. Use an option other than A to process only measurements of the specific type!")   

    parser.add_argument('--rsonde_skip_header', metavar='rsonde_skip_header', 
                        type=int, nargs='?', default = 1,
                        help="Number of lines to skip at the beginning of the radiosonde file. Defaults to 1 (1 line reserved for header info)")   
                  
    parser.add_argument('--rsonde_skip_footer', metavar='rsonde_skip_footer', 
                        type=int, nargs='?', default = 0,
                        help="Number of lines to skip at the end of the radiosonde file. Defaults to 0 (no footer assumed)")   

    parser.add_argument('--rsonde_delimiter', metavar='rsonde_delimiter', 
                        type=str, nargs='?', default = 'S',
                        help="The dilimiter that separates columns in the radiosonde file choose one of S: space, C: comma. Defaults to S!")   
    
    parser.add_argument('--rsonde_column_index', metavar='rsonde_column_index', 
                        type=int, nargs='+', default = [2, 1, 3, None], 
                        help="The column number of Height, Pressure, Temperature, and Relative Humidity (optional) columns in the radiosonde file. For example: --rsonde_columns 1 3 2 6 means height: 1st column, temperature: 3rd column, pressure: 2nd column, relative humidity: 6th column. The relative humidity column is OPTIONAL and can be omitted! Defaults to 1 2 3")   

    parser.add_argument('--rsonde_column_units', metavar='rsonde_column_units', 
                        type=str, nargs='+', default = ['m', 'hPa', 'K', 'percent'], 
                        help="The units of Height, Pressure, Temperature, and Relative Humidity (optional) columns in the radiosonde file. Supported units for height: m (default), Km | for pressure: Pa, hPa (default) | for temperature: C, K (default) | for relative humidity: fraction, percent (default). For example: --rsonde_column_units Km Pa C fraction ")   
                            
    parser.add_argument('--rsonde_station_name', metavar='rsonde_station_name', 
                        type=str, nargs='?', default = None, 
                        help="The station name of where the radiosonde measurement was performed. Defaults to None ")   

    parser.add_argument('--rsonde_wmo_number', metavar='rsonde_wmo_number', 
                        type=str, nargs='?', default = None, 
                        help="The WMO number of the radiosounding station. Defaults to None ")   

    parser.add_argument('--rsonde_wban_number', metavar='rsonde_wban_number', 
                        type=str, nargs='?', default = None, 
                        help="The WBAN number of the radiosounding station. Defaults to None ")   
                                                                                                                                              
    parser.add_argument('--rsonde_geodata', metavar='rsonde_geodata', 
                        type=float, nargs=3, default = [None, None, None], 
                        help="The radiosonde station latitude, longitude, and altitude. Mandatory if the mode is set to S. For example: --rsonde_geodata 40.5 22.9 60.0 ")   

    parser.add_argument('--trim_overflows', metavar='trim_overflows', 
                        type=int, nargs='?', default = 0, 
                        help="This options determines how overflow values will be treated. If set to 0 (default), no action will be taken, if set to 1 the files containing at least one overflow value will be screened out. If set to 2, overflow will be interpolated (use with care and only for a few bins per profile). If set to 3 then overflows will be included, use this only for debuging purposes")   
                
    args = vars(parser.parse_args())
    
    return(args)

def check_parser(args):
    
    if args['parent_folder'] == None and \
        args['dark_folder'] == None and \
            args['telecover_sectors_folder'] == None and \
                args['telecover_rings_folder'] == None and \
                    (args['pcb_cal_p45_folder'] == None or \
                     args['pcb_cal_m45_folder'] == None) and \
                        args['pcb_cal_stc_folder'] == None:
        raise Exception("-- Error: Neither a parent folder nor individual folders for the dark, rayleigh_fit, telecover, nor polarization_calibration tests where provided. Please either provide the parent_folder and use the default folder structure within or define each test folder explicitly! ")          
                

    if args['parent_folder'] == None and args['output_folder'] == None:
        raise Exception("Neither a parent nor an output folder were provided. Please provide at least one of the two! ")
                    
    if args['parent_folder'] != None and not os.path.exists(args['parent_folder']):
        raise Exception(f"The provided parent folder {args['parent_folder']} does not exist! Please use an existing folder or specify the measurement folders explicitly ")

    if args['output_folder'] == None:
        out_path = os.path.join(args['parent_folder'],'netcdf','converter')
        args['output_folder'] = out_path
        os.makedirs(args['output_folder'], exist_ok = True)
    elif not os.path.exists(args['output_folder'] ):
        raise Exception(f"The provided output folder {args['output_folder']} does not exist! Please use an existing folder or don't provide one and let the the parser create the default output folder ") 

    if args['config_file'] == None:
        args['config_file'] = os.path.join(args['parent_folder'],'config_file.ini')  

    if len(args['rsonde_column_index']) == 3:
        rsonde_column_index = args['rsonde_column_index']
        rsonde_column_index.extend([None])
        args['rsonde_column_index'] = rsonde_column_index

    if len(args['rsonde_column_units']) == 3:
        rsonde_column_units = args['rsonde_column_units']
        rsonde_column_units.extend([None])
        args['rsonde_column_units'] = rsonde_column_units

    if args['file_format'] not in ['licel', 'polly_xt']:
        raise Exception(f"-- Error: file_format field not recognized. Please use one of {['licel', 'polly_xt']} with: -F <file_format>")
            
    fld = ['dark_folder', 'rayleigh_folder', 'telecover_sectors_folder', 
           'telecover_rings_folder', 'pcb_cal_p45_folder', 
           'pcb_cal_m45_folder', 'pcb_cal_stc_folder']
    
    if args['file_format'] == 'licel':
        default_loc = ['drk', 'nrm', 'tlc', 
                       'tlc_rin', os.path.join('pcb','+45'),
                       os.path.join('pcb','-45'), os.path.join('pcb','stc')]
    elif args['file_format'] == 'polly_xt':
        default_loc = ['drk', 'nrm', 'tlc', 
                       'tlc_rin', 'nrm',
                       'nrm',  os.path.join('pcb','stc')]
    else:
        raise Exception(f"Provided file format '{args['file_format']}' not recognized. Please provide a supported file format.")
    
    for i in range(len(fld)):
        if args[fld[i]] == None:
            args[fld[i]] = os.path.join(args['parent_folder'], default_loc[i])
            
    # if args['radiosonde_folder'] != None and not os.path.exists(args['radiosonde_folder']):
    #     raise Exception(f"The provided radiosonde folder {args['radiosonde_folder']} does not exist! Please use an existing folder or specify the radiosonde file explicitly ")

    if args['radiosonde_folder'] == None and args['radiosonde_filename'] == None:
        raise Exception("Neither the radiosonde folder nor the radiosonde filename were provided. Please provide at least one of them ")
    
    if not os.path.exists(args['config_file']):
        raise Exception(f"-- Error: Path to the configuration file does not exists (defaults to <parent_folder>/config_file.ini). Path: {args['config_file']}!")  

    if args['debug'] not in [True, False]:
        raise Exception(f"-- Error: debug field should be boolean. Please use one of {[True, False]} with: -d <debug>")
        
    if not os.path.exists(os.path.join(args['output_folder'],'debug')) and args['debug']:
        os.makedirs(os.path.join(args['output_folder'],'debug'), exist_ok = True)

    if args['mode'] not in ['A', 'R', 'T', 'C', 'D']:
        raise Exception(f"-- Error: mode field not recognized. Please revise the settings file and use one of {['A', 'R', 'T', 'C', 'D']} with: -M <mode>")

    if len(args['rsonde_column_index']) != 4:
        raise Exception("-- Error: rsonde_column_index field has less or more elements than expected. Please provide 3 or 4 integer eg: --rsonde_column_index 1 2 3")

    if len(args['rsonde_column_units']) != 4:
        raise Exception("-- Error: rsonde_column_unit field has less or more elements than expected. Please provide 3 or 4 strings eg: --rsonde_column_units Km Pa C ")

    if args['rsonde_column_units'][0] not in ['m_asl', 'km_asl', 'm_agl', 'km_agl', 'm_geo', 'Km_geo', 'm'] or \
        args['rsonde_column_units'][1] not in ['Pa', 'hPa', 'atm'] or \
            args['rsonde_column_units'][2] not in ['C', 'Cx10', 'K'] or \
                args['rsonde_column_units'][3] not in ['fraction', 'percent', None] :
                    raise Exception(f"-- Error: rsonde_column_unit field values were not recognized ({args['rsonde_column_units']}). Please provide on of [m, Km] for height, [Pa, hPa] for pressure, [C, K] for temperature, and [fraction, percent] for relative humidity (optional)")

    if len(args['rsonde_geodata']) != 3:
        raise Exception("-- Error: rsonde_geodata field has less or more elements than expected. Please provide 3 floats that correspond to the radiosonde station latitude, longitude, and altitude eg: --rsonde_geodata 40.5 22.9 60.0")
            
    if any([not geodata_i for geodata_i in args['rsonde_geodata']]) and args['mode'] == 'S':
        raise Exception("-- Error: The rsonde_geodata field is mandatory when processing a radiosonde file (mode = S). Please provide 3 floats that correspond to the radiosonde station latitude, longitude, and altitude eg: --rsonde_geodata 40.5 22.9 60.0")
    
    return(args)

def view_parser(args):
    
    print(" ")
    print("-- Converter arguments!")
    print("-------------------------------------------------------------------")
    for key in args.keys():
        print(f"{key} = {args[key]}")
    print("-------------------------------------------------------------------")
    print("")

    return()