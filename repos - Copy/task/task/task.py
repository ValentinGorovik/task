# -*- coding: utf-8 -*-
import pandas as pd
import os
import generate_config as cfg
##start_date=pd.to_datetime(input('Enter Start Date in "YYYY-MM-DD" format: ' ),format='%Y-%m-%d %H:%M:%S')#'%Y-%m-%d %H:%M:%S'
##last_date=pd.to_datetime(input('Enter Start Date in "YYYY-MM-DD" format: ' ),format='%Y-%m-%d %H:%M:%S')
start_date=cfg.start_date
last_date=cfg.last_date
a=os.listdir('files')
results = 'results'
if not os.path.exists(results): ## Проверяю, есть ли папка result. Если нет, то создаём.
    os.makedirs(results)
csv_list=[]
for file in a:
    csv_list.append(pd.read_csv('files\\'+file).reindex(columns=['Duration','Start date',
                                                                                           'End date',
                                                                                           'Start station','End station number',
                                                                                           'End station','Bike number','Member type']))


csv_merged = pd.DataFrame()
csv_merged = pd.concat(csv_list, ignore_index=True)
csv_merged[['Start date','End date']] = csv_merged[['Start date','End date']].apply(pd.to_datetime)##всех к одному date формату
csv_merged['Start date']=pd.to_datetime(csv_merged['Start date'],format='%Y-%m-%d').dt.date
csv_merged['End date']=pd.to_datetime(csv_merged['End date'],format='%Y-%m-%d').dt.date
demo_df=csv_merged[csv_merged['Start date']>=start_date]
demo_df=demo_df[demo_df['End date']<=last_date]
errors=demo_df["Duration"].astype(str).str.isdigit().value_counts().reset_index()##количество ошибок в duration
errors_count=errors['Duration'][0]-demo_df['Duration'].count()
unique_count_bike_all=csv_merged['Bike number'].nunique() ##количество уникальных байков всего
unique_count_bike_demo=demo_df['Bike number'].nunique() ##количество уникальных байков за даты
unique_count_rides_demo=demo_df['Duration'].nunique()##количество поездок за даты
max_duration_demo=demo_df['Duration'].max()##количество поездок за даты
general_stats=pd.DataFrame({'Indicator': ['Total current',
                                     'Time of the longest trip',
                                     'Number of bikes that were discovered during the specified period, number of entries',
                                     'Unprocessable'
                                     ],
                            'Result': [unique_count_rides_demo,
                                     max_duration_demo, 
                                     unique_count_bike_all, errors_count]})

general_stats.to_csv('results\\general-stats.csv')##вывод 1 файла
df_group_count_rides=demo_df[['Duration','Start date']].reset_index(drop=True)
df_group_count_rides['By month']=df_group_count_rides['Start date'].astype(str).str[0:7]
df_group_count_rides=df_group_count_rides.groupby('By month')['Duration'].count().reset_index()## 4 задание
df_group_count_rides=df_group_count_rides.rename(columns={'Duration':'Count'})
df_group_count_rides.to_csv('results\\df_group_count_rides.csv')
bike_stats=demo_df.groupby(['Bike number']).agg({'Member type':'count', 'Duration': 'sum'}).sort_values(by=['Member type','Duration'],ascending=False).reset_index() ## 4 задание кол-во поездок каждого велика
bike_stats.to_csv('results\\bike_stats.csv')

