from pathlib import Path

def first_capture_time(content):
    """
    Detection of a new
    :param content: Content of a log file
    :return:
    """

    last_line=""
    map_playing =""
    for line in content_file.readlines():

        #Tracking map start
        if line.__contains__('§9§o'):
            print(last_line)
            try :
                map_playing=[s for s in last_line.split("  ") if s != ''][-2]
            finally:
                a=0




        last_line = line



compact_logs_directory = './logs_data/compact_logs'

files = Path(compact_logs_directory).glob('*.txt')
for f in files:
    content_file = open(f,"r",encoding='unicode_escape')
    first_capture_time(content=content_file)


