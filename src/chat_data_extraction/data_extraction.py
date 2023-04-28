from pathlib import Path
from datetime import datetime
import numpy as np
import pandas as pd
from util.main.dict_util import combine_dict
from util.main.database import create_connection

def first_capture_time(content):
    """
    Detection of the first completion of an objective (flag, wool, core and monument)
    :param content: Content of a log file
    :return:
    """
    last_line=""
    map_playing =""
    first_capture_track = False
    time_match=0

    dict_values=dict()

    for line in content.readlines():

        #Tracking map start
        if line.__contains__('§9§o') and not first_capture_track:
            try :
                map_playing=[s for s in last_line.split("  ") if s != ''][-2]

                #Remove space at the beginning of string if detected
                if map_playing[0]==" ":
                    map_playing = map_playing[1:]

                first_capture_track = True
                subdate = line.split('[')[1].split(']')[0].split(':')
                time_match = datetime(year=2000,month=1,day=1,hour=int(subdate[0]),minute=int(subdate[1]),second=int(subdate[2]))
            except:
                a=0

        #Objective completion in order : (flag and wool), monument, core
        elif (line.__contains__('captured by') or line.__contains__('was destroyed by') or line.__contains__('was leaked by') ) and first_capture_track:
            first_capture_track=False
            time_for_capture = line.split('[')[1].split(']')[0].split(':')
            time_capture= datetime(year=2000,month=1,day=1,hour=int(time_for_capture[0]),minute=int(time_for_capture[1]),second=int(time_for_capture[2]))
            diff_time = time_capture-time_match

            try:
                dict_values[map_playing].append(diff_time.total_seconds())
            except:
                dict_values[map_playing]=[diff_time.total_seconds()]


        last_line = line

    return dict_values


compact_logs_directory = './logs_data/compact_logs'
files = Path(compact_logs_directory).glob('*.txt')
dict_total={}

#First capture times
for f in files:
    content_file = open(f,"r",encoding='unicode_escape')
    dict_file = first_capture_time(content=content_file)
    dict_total = combine_dict(dict1=dict_total,dict2=dict_file)

for items in dict_total.items():
    dict_total[items[0]] = np.mean(items[1])

df_first_capture = pd.DataFrame.from_dict(dict_total, orient='index')




