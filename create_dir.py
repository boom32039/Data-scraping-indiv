import os 
import pandas as pd
dir_path =  'C:\\Users\\Boom NB\\Downloads\\APK'
category_list = pd.read_json("top_chart_categories.json")
for e in category_list['categories']:
    os.mkdir(dir_path+e['name'])


    
