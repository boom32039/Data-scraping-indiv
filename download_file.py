import time
import datetime
import pytz
import json
import csv 
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#CSV_list = {'file_name' : [] , 'app_name' : [] , 'date' : [] , 'version' : [] , 'url' : [] , 'rank' : [] , 'genre' : []}
CSV_list = []
dir_path = 'C:\\Users\\Boom NB\\Downloads\\APK\\'
# cat_dict = {cat1 : [app1, app2] , cat2 : [] ,...}
# cat_key_list = [cat1 ,cat2 ,cat3 , cat4 ,...]
with open('top_chart_apps.json') as json_file:
    cat_dict = json.load(json_file)

# How many cat want to download ? 
cat_key_list = [] ; i = 0 
for cat in cat_dict:
    if i == len(cat_dict) :break
    if i >= 0:
        cat_key_list.append(cat)
    i += 1

#date of each app
with open('apps_date.json') as json_file:
    apps_date = json.load(json_file)
    
def getCurrentTime():
    current_time = datetime.datetime.now(pytz.timezone('Asia/Bangkok')) 
    date = str(current_time.day)  + '/' + str(current_time.month) + '/' + str(current_time.year) 
    hour = str(current_time.hour) ; minute = str(current_time.minute) ; second = str(current_time.second);
    if len(hour) == 1 :
        hour = '0' + hour
    if len(minute) == 1 :
        minute = '0' + minute
    if len(second) == 1 :
        second = '0' + second
    time = hour  + ':' + minute + ':' + second
    return  date +' ' +  time 

def isAllfileDownload(d):
    for e in d:
        if e.split('.')[-1] == 'crdownload': 
            return False
    return True

def fillInGenre(genre):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-infobars")
    prefs = {'download.default_directory' : dir_path + genre}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome( 'chromedriver', options=chrome_options)
    i = 1 
    for app_dict in cat_dict[genre]:
        try:
            download(app_dict['package_name'] , i , genre , driver )
        except:
            dic = getCSVdict(app_dict['name'] , '-' , '-' , '-', '-' , i , genre, False , {} )
            CSV_list.append(dic)
            pass
        finally:
            i += 1 
    # all files are in folder ? 
    download_dir = dir_path + genre
    while(not isAllfileDownload(os.listdir(download_dir))):
        time.sleep(10)
        
def getCSVdict(app_name , file_name , date , version, url , rank , category ,isDownloaded ,dic):
    dic['version'] = version 
    dic['app_name'] = app_name
    dic['date'] = date
    dic['url'] = url
    dic['file_name'] = file_name
    dic['rank'] = rank
    dic['category'] = category
    dic['isDownloaded'] = isDownloaded
    return dic

def rename(name):
    new_name = ''
    for e in name:
        if e in '/?:|':
            new_name += '_'
        else:
            new_name += e
    return new_name

def download(app_id , rank , cat , driver ):
    dic = {'app_name' : '' , 'file_name' : '' , 'date' : '' , 'version' : '' , 'url' : '' , 'rank' : '' , 'category' : '' , 'isDownloaded' : False}
    driver.get('https://www.apkcombo.com/')
    time.sleep(0.5)
    search_bar = driver.find_element(By.CLASS_NAME , 'ainput')
    search_bar.send_keys(app_id)
    search_bar.submit()
    app_name = driver.find_element(By.CLASS_NAME , 'app_name').find_element(By.TAG_NAME , 'h1').text
    version = driver.find_element(By.CLASS_NAME , 'version').text
    url = driver.current_url + 'download/apk/'
    time.sleep(0.5)
    driver.get(url)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "variant")) #This is a dummy element
    )
    if driver.find_element(By.CLASS_NAME , 'vtype').text != 'APK':
        apk_variant = driver.find_elements(By.CLASS_NAME , 'tab ')
        found = False
        if app_id in apps_date:
            found = True
        for e in apk_variant:
            if 'APK' in e.text and app_id not in apps_date:
                driver.execute_script("arguments[0].click();", e)
                time.sleep(5)
                found = True
                break
            
        APKfiles = driver.find_elements(By.CLASS_NAME  , 'variant')
        for e in APKfiles:
            if 'APK' in e.text.split() and app_id not in apps_date:
                driver.execute_script("arguments[0].click();", e)
                time.sleep(5)
                found = True
                break
        if not found:
            dic = getCSVdict(app_name , '-' , '-' , '-', '-' , rank , cat, False , {} )
            CSV_list.append(dic)
            return 
    else:
        link = driver.find_element(By.CLASS_NAME , 'variant')
        if app_id not in apps_date:
            driver.execute_script("arguments[0].click();", link)
            time.sleep(5)
            if ('#google_vignette' in driver.current_url):
                url += '#google_vignette'
                driver.get(url)
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "variant")) #This is a dummy element
                )
                link = driver.find_element(By.CLASS_NAME , 'variant')
                driver.execute_script("arguments[0].click();", link)
                time.sleep(5)
    try:
        n = driver.find_element(By.CLASS_NAME , 'vername').text
        r_version = n.split()[-1]
        if r_version != version :
            version = r_version 
    except:
        pass
    
    file_name = rename(app_name) + '_' + version + '_apkcombo.com.apk'
    if app_id not in apps_date:
        download_date = getCurrentTime()
        apps_date[app_id] = download_date
    else:
        download_date = apps_date[app_id]
    dic = getCSVdict(app_name , file_name , download_date , version, url , rank , cat ,True ,dic)
    CSV_list.append(dic)

def delete_files(d):
    for cat in d:
        dir = dir_path + cat
        for file in os.listdir(dir):
            os.remove(dir + '\\' + file)
    
def create_csv_and_json():
    csv_columns = ['app_name','file_name','date' ,'version' , 'url' , 'rank' , 'category', 'isDownloaded']
    csv_file = "APKinfo.csv"

    # apps_date dic to json
    with open('apps_date.json','w',encoding="utf-8") as json_file:
        json.dump(apps_date, json_file, indent=4, separators=(',', ': '), sort_keys=True)
    json_file.close()
    
    # write CSV_list to csv 
    try:
        with open(csv_file, 'a'  ,newline="",encoding = 'utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writerows(CSV_list)
    except IOError:
        print("I/O error")
        
# ---------MAIN--------------
def main():
    for cat in cat_key_list:
        fillInGenre(cat)
        print('finished' , cat)

main()

create_csv_and_json()


        
        
        
        
        
        

