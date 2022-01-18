import os 
import csv
import copy
file_path = 'C:\\Users\\Boom NB\\Downloads\\APK'
csv_name = 'APKinfo2.csv'
dir_set = set()
csv_set = set()
dir_dic = {}
cat_list = []

def add_dir_file():
    for e in os.listdir(file_path):
        for f in os.listdir(file_path + '\\' + e):
            dir_set.add(f.strip())
            if f.strip() not in dir_dic:
                dir_dic[f.strip()] = e 

def add_csv_file():
    with open(csv_name, 'r' ,encoding = 'utf-8-sig') as csvfile:
            writer = csv.reader(csvfile)
            for row in writer:
                if row[-2] not in cat_list:
                    cat_list.append(row[-2])
                if row[-1] == 'TRUE' or row[-1] == 'True':
                    csv_set.add(row[1].strip())
                    if row[1].strip() not in dir_dic:
                        dir_dic[row[1].strip()] = row[-2]

def show_err():
    dir_set.symmetric_difference_update(csv_set)
    for g in cat_list:
        for e in dir_set:
            if dir_dic[e] == g:
                print(e , dir_dic[e])
        print('---------------------')

def re(s):
    return '_'.join(s.split('_')[:-2])

def find():
    i = 0
    with open(csv_name, 'r' ,encoding = 'utf-8-sig') as csvfile:
            writer = csv.reader(csvfile)
            for row in writer:
                if row[-1] == 'TRUE' or row[-1] == 'True':
                    found = False
                    for cat in os.listdir(file_path):
                        for f in os.listdir(file_path + '\\' + cat):
                            if re(row[1]) == re(f):  
                                found = True
                                break
                    if not found :
                        print(row[-2] , row[1] ,row[4])
                        i += 1
    print(i)
def version(s1):
    return s1.split('_')[-2]
def find2():
    os_set = set()
    for e1 in os.listdir(file_path):
        for e2 in os.listdir(file_path + '\\' + e1): 
            os_set.add(e2)
    D = []
    with open(csv_name, 'r' ,encoding = 'utf-8-sig') as csvfile:
            writer = csv.reader(csvfile)
            for row in writer:
                d = copy.deepcopy(row)
                if row[-1] == 'TRUE' or row[-1] == 'True':
                    for fname in os_set:
                        if re(row[1]) == re(fname) and version(row[1]) != version(fname):
                            d[3] = version(fname)
                            d[1] = fname
                            print(d[3] , d[1])
                D.append(d)
                            
        
    # header = ['Apps name' , 'Files name' , 'Download time' , 'version' , 'download link' , 'rank' , 'category' , 'is-Downloaded' ]
    # with open('APKinfo2.csv', 'w', encoding='utf-8-sig' ,newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(header)
    #     writer.writerows(D)

    #                 found = False
    #                 for cat in os.listdir(file_path):
    #                     for f in os.listdir(file_path + '\\' + cat):
    #                         if re(row[1]) == re(f):  
    #                             found = True
    #                             break
    #                 if not found :
    #                     print(row[-2] , row[1] ,row[4])
    #                     i += 1
    
    
# add_csv_file()
# add_dir_file()
# show_err()
find2()





