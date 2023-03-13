import argparse

import numpy as np
import pandas as pd


'''
Change length of match into standard time
Return : List[hour : String ,minute : String, second : String]
'''
def length_to_standart_time(length,cloudy_ver):
    list = []

    #Cloudy Version 1 format
    if cloudy_ver ==1:
        carl = length.split(" ")

        for i,element in enumerate(carl):
            if (i%2==0):
                list.append(carl[i])
        for i in range (3-len(list)):
            list.insert(0,'0')

    #Cloudy Version 2 and 3
    else:
        next = ''

        #Hour split
        first_split = length.split('h')
        if len(first_split)==1:
            list.append('0')
            next=first_split[0]
        else:
            list.append(first_split[0])
            next = first_split[1]

        #Minute split
        second_split = next.split('m')
        if len(second_split)==1:
            list.append('0')
            next = second_split[0]
        else:
            list.append(second_split[0])
            next=second_split[1]

        #Second split
        third_split = next.split('.')
        if len(third_split)==1:
            if third_split[0]=='':
                list.append('0')
            else:
                list.append(third_split[0].split('s')[0])

        else:
            list.append(third_split[0])

    return list



def date_mutation(date):

    year_hour_separator = date.split(" ")
    ymd_date = year_hour_separator[0].split("-")
    hm_date = year_hour_separator[1].split(":")

    constructor_date=np.concatenate((ymd_date,hm_date))

    switch={
        'Jan':1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }

    constructor_date[1] = switch.get(constructor_date[1])
    if (year_hour_separator[2] == 'PM' and constructor_date[3] != '12'):
        constructor_date[3] = str(int(constructor_date[3]) + 12)

    elif(year_hour_separator[2] == 'AM' and constructor_date[3] == '12'):
        constructor_date[3] = '0'

    return constructor_date



'''
Extract data from CSV into a new CSV
New csv name : new_data.csv

Return : None
'''
def extract_data_to_newdf(cfg):
    #Read file
    df = pd.read_csv(cfg.origin)

    #New dataframe for new csv
    new_df = pd.DataFrame(columns=['date_day','date_months','date_year','date_hour','date_minute','map_name','length_hour','length_minute','length_second','participants','winner','cloudy_ver'])
    new_df.to_csv('new_data.csv', index=False,sep=";")
    #Loop for every row of dataframe
    for i, row in df.iterrows():

        #Print progress
        if i%1000==0:
            print('Item number ',i,' done ...')

            #Clean RAM to speed up
            new_df.to_csv('new_data.csv', mode='a',index=False,header=False,sep=";")
            new_df = pd.DataFrame(
                columns=['date_day', 'date_months', 'date_year', 'date_hour', 'date_minute', 'map_name', 'length_hour',
                         'length_minute', 'length_second', 'participants', 'winner', 'cloudy_ver'])

        #Standardization function
        new_date=date_mutation(row['end_date'])
        new_length=length_to_standart_time(row['length'],row['cloudy-ver'])


        data= [[new_date[0],new_date[1],new_date[2],new_date[3],new_date[4],row['map_name'],new_length[0],new_length[1],new_length[2],row['participants'],row['winner'],row['cloudy-ver']]]

        df2 = pd.DataFrame(data,
            columns=['date_day','date_months','date_year','date_hour','date_minute','map_name','length_hour','length_minute','length_second','participants','winner','cloudy_ver'])

        new_df = pd.concat([new_df,df2],axis=0)


    new_df.to_csv(cfg.new,mode='a',index=False,header=False,sep=";")






parser = argparse.ArgumentParser()
parser.add_argument('--origin', type=str, default="data.csv", help='Origin data file name')
parser.add_argument('--new', type=str, default="new_data.csv",help='New data file name')
cfg = parser.parse_args()

extract_data_to_newdf(cfg)


#Tests
#print(length_to_standart_time('32m',3))
#print(length_to_standart_time('4 seconds',1))
#print(date_mutation("27-Dec-20 10:14 PM"))