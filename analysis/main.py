from bs4 import BeautifulSoup;
import csv;
import pandas as pd;
import time;
from selenium import webdriver;
import gc;
import os;
from selenium.webdriver.common.keys import Keys



def getImageLink(tags):
    links=[];
    for x in tags:
        for y in x:
            beam = y.attrs['data-bem']
            start = beam.find('{"url":"');
            start = start + 8
            end = beam.find('","fileSizeInBytes', start);
            links.append(beam[start:end]);
            break;
    return links;



def getTitle(tags):
    title=[];
    for x in tags:
        for y in x:
            beam = y.attrs['data-bem']
            start = beam.find('title":"');
            start = start + 8;
            end = beam.find('","hasTitle', start);
            title.append(beam[start:end]);
            break;
    return title;

def getDescription(tags):
    description=[];
    for x in tags:
        for y in x:
            for j in y.findAll('img'):
                description.append(j.attrs['alt']);
                break;
    return description;

def getAllFiles(dir):
    files_list=[];
    for root, dirs, files in os.walk(dir):
        for filename in files:
            files_list.append(filename)
    return files_list;

def findWhetherCSVContains50Data(filename):
    split_filename=filename.split('.')
    file=pd.read_csv(filename);
    count=len(file.Title)
    if(count>=50):
        return True;
    else:
        return False;

def getAllDirec(dir):
    files_list=[];
    for root, dirs, files in os.walk(dir):
        for filename in dirs:
            files_list.append(filename)
    return files_list;

root_folder_name="indoor";
root_child_name="train";

data_root_dir_name='data_indoor';
#print(getAllFiles(root_folder_name+"\\"+root_child_name+"\\"+"airport_inside"))

dirs_list=getAllDirec(root_folder_name+"\\"+root_child_name);

if(os.path.exists(data_root_dir_name)):
    if(os.path.exists(data_root_dir_name+"\\"+root_child_name)):
        for i,direc in enumerate(dirs_list):
            if(os.path.exists(data_root_dir_name+"\\"+root_child_name+"\\"+direc)):
                filename=getAllFiles(root_folder_name+"\\"+root_child_name+"\\"+direc)
                for i, file in enumerate(filename):
                    data_front=file.split('.')[0];
                    if(os.path.exists(data_root_dir_name+"\\"+root_child_name+"\\"+direc+"\\"+data_front+".csv")):
                        if (findWhetherCSVContains50Data(
                                data_root_dir_name + "\\" + root_child_name + "\\" + direc + "\\" + data_front + ".csv")):
                            pass;
                        else:
                            data_front = file.split('.')[0];
                            print(data_front)
                            encoded_url = 'https%3A%2F%2Fsolmolandra.000webhostapp.com%2F' + root_folder_name + '%2F' + root_child_name + '%2F' + direc + '%2F' + data_front + '.jpg'
                            search_query = 'https://yandex.com/images/search?img_url=' + encoded_url + '&rpt=imagelike';

                            driver = webdriver.Chrome("chromedriver.exe");
                            driver.get(search_query);
                            elem = driver.find_element_by_tag_name("body");
                            no_of_pagedown = 20;
                            while (no_of_pagedown):
                                elem.send_keys(Keys.PAGE_DOWN)
                                time.sleep(0.2);
                                no_of_pagedown -= 1;
                            page = driver.execute_script('return document.documentElement.outerHTML')
                            driver.close()
                            tags = []
                            if (True):
                                soup = BeautifulSoup(page, "html5lib");
                                count = 0;
                                for j in range(500):
                                    val = soup.findAll("div", {
                                        "class": "serp-item serp-item_type_search serp-item_group_search serp-item_pos_" + str(
                                            j) + " serp-item_scale_yes justifier__item i-bem"})
                                    if (val != []):
                                        tags.append(val);
                                        count += 1;
                                        if (count >= 50):
                                            break;

                                dataframe_data = {
                                    'Title': getTitle(tags),
                                    'Description': getDescription(tags),
                                    'Link': getImageLink(tags),
                                }
                                df = pd.DataFrame(dataframe_data);
                                df.to_csv(
                                    data_root_dir_name + "\\" + root_child_name + "\\" + direc + "\\" + data_front + ".csv");
                                gc.collect();
                                print("Successfull");
                    else:
                        data_part  = file.split('.');
                        data_front = data_part[0];
                        extension = data_part[1];
                        print(data_front, extension);
                        encoded_url = 'https%3A%2F%2Fsolmolandra.000webhostapp.com%2F' + root_folder_name + '%2F' + root_child_name + '%2F' + direc + '%2F' + data_front + '.' + extension;
                        search_query = 'https://yandex.com/images/search?img_url=' + encoded_url + '&rpt=imagelike';

                        driver = webdriver.Chrome("chromedriver.exe");
                        driver.get(search_query);
                        elem = driver.find_element_by_tag_name("body");
                        no_of_pagedown = 20;
                        while (no_of_pagedown):
                            elem.send_keys(Keys.PAGE_DOWN)
                            time.sleep(0.2);
                            no_of_pagedown -= 1;
                        page = driver.execute_script('return document.documentElement.outerHTML')
                        driver.close()
                        tags = []
                        if (True):
                            soup = BeautifulSoup(page, "html5lib");
                            count = 0;
                            for j in range(500):
                                val = soup.findAll("div", {
                                    "class": "serp-item serp-item_type_search serp-item_group_search serp-item_pos_" + str(
                                        j) + " serp-item_scale_yes justifier__item i-bem"})
                                if (val != []):
                                    tags.append(val);
                                    count += 1;
                                    if (count >= 50):
                                        break;

                            dataframe_data = {
                                'Title': getTitle(tags),
                                'Description': getDescription(tags),
                                'Link': getImageLink(tags),
                            }
                            df = pd.DataFrame(dataframe_data);
                            df.to_csv(
                                data_root_dir_name + "\\" + root_child_name + "\\" + direc + "\\" + data_front + ".csv");
                            gc.collect();
                            print("Successfull");

            else:
                try:
                    os.makedirs(data_root_dir_name + "\\" + root_child_name+"\\"+direc);
                except FileExistsError:
                    pass;

                filename = getAllFiles(root_folder_name + "\\" + root_child_name + "\\" + direc)
                for i, file in enumerate(filename):
                    data_part=data_front=file.split('.');
                    data_front=data_part[0];
                    extension=data_part[1];
                    print(data_front,extension);
                    encoded_url = 'https%3A%2F%2Fsolmolandra.000webhostapp.com%2F' + root_folder_name + '%2F' + root_child_name + '%2F' + direc + '%2F' + data_front + '.'+extension;
                    search_query = 'https://yandex.com/images/search?img_url=' + encoded_url + '&rpt=imagelike';

                    driver = webdriver.Chrome("chromedriver.exe");
                    driver.get(search_query);
                    elem = driver.find_element_by_tag_name("body");
                    no_of_pagedown = 20;
                    while (no_of_pagedown):
                        elem.send_keys(Keys.PAGE_DOWN)
                        time.sleep(0.2);
                        no_of_pagedown -= 1;
                    page = driver.execute_script('return document.documentElement.outerHTML')
                    driver.close()
                    tags = []
                    if (True):
                        soup = BeautifulSoup(page, "html5lib");
                        count = 0;
                        for j in range(500):
                            val = soup.findAll("div", {
                                "class": "serp-item serp-item_type_search serp-item_group_search serp-item_pos_" + str(
                                    j) + " serp-item_scale_yes justifier__item i-bem"})
                            if (val != []):
                                tags.append(val);
                                count += 1;
                                if (count >= 50):
                                    break;

                        dataframe_data = {
                            'Title': getTitle(tags),
                            'Description': getDescription(tags),
                            'Link': getImageLink(tags),
                        }
                        df = pd.DataFrame(dataframe_data);
                        df.to_csv(data_root_dir_name + "\\" + root_child_name + "\\" + direc + "\\" + data_front+".csv");
                        gc.collect();

                        print("Successfull");

                #previous else content should be written
    else:
        try:
            os.makedirs(data_root_dir_name+"\\"+root_child_name);
        except FileExistsError:
            pass;
else:
    try:
        os.makedirs(data_root_dir_name);
    except FileExistsError:
        pass;

