from bs4 import BeautifulSoup;
import requests;
import pandas as pd;
import os;


num=input("How many data file are there?\n");

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

for i in range(int(num)):
    encoded_url='https%3A%2F%2Fsolmolandra.000webhostapp.com%2Fdata%2Fdata'+str(i+1)+'.jpg';
    search_query='https://yandex.com/images/search?img_url='+encoded_url+'&rpt=imagelike';
    page=requests.get(search_query);
    tags=[]
    if(page.status_code == 200):
        soup=BeautifulSoup(page.text,"html.parser");
        for j in range(200):
            val=soup.findAll("div",{"class":"serp-item serp-item_type_search serp-item_group_search serp-item_pos_"+str(j)+" serp-item_scale_yes justifier__item i-bem"})
            if(val!=[]):
                tags.append(val);


        dataframe_data={
            'Title':getTitle(tags),
            'Description':getDescription(tags),
            'Link':getImageLink(tags),
        }
        df=pd.DataFrame(dataframe_data);
        try:
            os.makedirs('data');
        except FileExistsError:
            pass;
        df.to_csv("data\\data"+str(i));
        print("Successfull");