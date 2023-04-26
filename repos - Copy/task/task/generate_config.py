import configparser
import pandas as pd
config_file = configparser.ConfigParser()
start_date=pd.to_datetime(input('Enter Start Date in "YYYY-MM-DD" format: ' ),format='%Y-%m-%d %H:%M:%S')
last_date=pd.to_datetime(input('Enter Start Date in "YYYY-MM-DD" format: ' ),format='%Y-%m-%d %H:%M:%S')
