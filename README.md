# Create top-charts apps as json file 
1. open 42mattersAPI.ipynb in Google Colab 
2. import top_chart_categories.json file in '/content/' (from https://data.42matters.com/api/meta/android/apps/app_categories.json and save into .json file)
3. you have to edit some lines 
```
api_url = 'https://data.42matters.com/api/v3.0/android/apps/top_google_charts.json'
category_list = pd.read_json("/content/top_chart_categories.json")
access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
country = "TH"
date = '24-12-2021'
dic = {}
```
- access_token 
  - you have to get the access token from 42matters.com by use free-trial 14 days or subscribe some packages 
- date 
  - date should be date that you want to get info at that time
4. clicking run all in Runtime tab and wait until top_chart_apps.json appears
# Files 
- apps_date.json 
  - use to contain the file that has been downloaded and its time  
  - key : APP_ID , value : downloaded time
  - if you never downloaded before , please create an empty file and named it as apps_dates.json 
- APKinfo.csv 
  - it will appear after run download_file.py  
- checking.py 
  - use to check what the difference of information between files in APKinfo.csv and files in directory (TO DEBUG) 
- create_dir.py 
  - create all folder (named by all categories in top_chart_apps.json) 
- download_file.py 
  - main file to download files 
# Libraries
- libraries that needed for downloading and getting information 
```
time
datetime
pytz
json
csv 
os
selenium 
pandas
```
Can install by (if don't have) 
```
pip install <LIBRARY NAME> 
```
# Preparing before download
1. upload top_chart_apps.json to your work's directory 
2. In create_dir.py 
Change dir_path to your folder path that use to all .APK files 
```
dir_path =  'C:\\Users\\Boom NB\\Downloads\\APK' ==> dir_path =  <YOUR PATH>
```
3. run create_dir.py 
4. if you never run download_file.py it before , create apps_date.json as empty json file
5. In download_file.py line 16 , change dir_path to your folder path that will use to store APK files
```
dir_path =  'C:\\Users\\Boom NB\\Downloads\\APK' ==> dir_path =  <YOUR PATH>
```
6. In download_file.py line 23 to 28
```
cat_key_list = [] ; i = 0 
for cat in cat_dict:
    if i == len(cat_dict) :break
    if i >= 0:
        cat_key_list.append(cat)
    i += 1
```
   - I do not download all files in one runtime but I download some parts and continue to download other parts in another runtime.
   - variable i is refered to categories's order that will be downloaded based on top_charts_apps.json  
   - Ex.if you want to download the first categories to 20th categories you might change "len(cat_dict)" to 10
   - Ex.if you want to download the 1st categories to 15th categories you might change "if i >= 0" to "if i >= 1 " and "len(cat_dict)" to 15
# Downloading process
1. run download_file.py
2. apps_date.json and top_chart_apps.json will change to dict
3. using app ID in top_chart_apps.json to check file existence in apps_date dict
4. if it not download it and contain info in app_date dict 
5. if exists do nothing but 
6. After downloading all files that selected , apps_date dict will be dumped to json file again and csv is written 
# Problem while downloading 
- sometimes you must click resume on some file in chrome://downloads/ to continue downloading 
- you have to kill the terminal when internet error occured on browser. 
# Problem after downloading 
- use checking.py to find what file has a problem by run checking.py (it will print those files that have problem)
  -  you have to change file_path to your folder path that stores the downloaded file
     ```
     file_path = 'C:\\Users\\Boom NB\\Downloads\\APK' ==> file_path = <YOUR PATH>
     ```
- file name in csv and file name in your folder may not be the same because I just observe the pattern of real file name and named in python
- some file exists in csv but not in the folder