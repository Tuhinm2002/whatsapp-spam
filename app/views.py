from ast import expr_context
from django.shortcuts import render
from matplotlib import transforms
import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from django.http import HttpResponseRedirect
import torch.nn as nn
import torch
import os
import torchvision.transforms as transforms
from app.myclass import ClassificationBase,CNN
from PIL import Image
import pickle
import numpy as np
import torch.functional as F

# Create your views here.





def result_func(request):
    if request.method=="GET":
        output=request.GET.get('result')
        if output=='1':
            res="spam"
        elif output=='0':
            res="not-spam"
        else:
            res="connection error or messages could not be load properly try again"
    return render(request,"result.html",{'result':res})



def selenium_func(data,parser):
    options=webdriver.ChromeOptions()
    # options.add_argument('user-data-dir=/home/<usernaem>/.config/google-chrome/default')

    chrome=webdriver.Chrome(executable_path="/<chromewebdriver_folder_name>/chromedriver_linux64/chromedriver",options=options)
    chrome.get("https://web.whatsapp.com/")
    time.sleep(30)

    user_name=[data]

    for name in user_name:
        try:
            user=chrome.find_element(By.XPATH,value='//span[@title="{}"]'.format(name))
            user.click()
        except:
            return "user not found or retry again"
    
    
    if parser=="text":
            time.sleep(50)
            vec=pickle.load(open("CountVect.pkl","rb"))
            model=pickle.load(open("model.pkl","rb"))
            text=[]
            for elem in chrome.find_elements(By.XPATH,value='.//div[@class="_22Msk"]'):
                text.append(elem.text) 
            dt=vec.transform(text)
            pred=model.predict(dt)[0]
            return pred
    
    elif parser=="img":
            MODEL1=ClassificationBase()
            model=CNN()
            model.load_state_dict(torch.load("model.pth"))   #jciay5ix tvf2evcx oq44ahr5 lb5m6g5c
            time.sleep(50)
            finder=chrome.find_element(By.XPATH,value='//img[@class="jciay5ix tvf2evcx oq44ahr5 lb5m6g5c"]')
            finder.click()
            time.sleep(5)
            finder.screenshot('images_folder//ss.png')
            
            composer=transforms.Compose([transforms.Resize((32,32)),transforms.ToTensor()])
            testing=[]
            pred=[]
            for i in os.listdir("images_folder/"):
                img=Image.open(os.path.join("images_folder/",i))
                j=composer(img)
                j=j[:3]
                print(j.shape)
                xb=torch.unsqueeze(j,0)
                # print(xb.shape)
                yb=model(xb)
                _, preds  = torch.max(yb, dim=1)
                pred.append(preds[0].item())
                time.sleep(10)
            for i in os.listdir("images_folder/"):
                os.remove(os.path.join("images_folder/",i))
            return pred[0]
        

    time.sleep(10)
    chrome.close()

def project(request):
    return render(request,"index.html")

def pred(request):
    return render(request,"home.html")

def image_add(request):
    if request.method=='POST':
            data=request.POST.get('field')
            print(data)
            val=selenium_func(data,parser="img")
            url="result/?result={}".format(val)
            return HttpResponseRedirect(url)
            
        
    return render(request,"add.html")

def text_add(request):
    if request.method=='POST':
            data=request.POST.get('field')
            print(data)
            val=selenium_func(data,parser="text")
            url="result/?result={}".format(val)
            return HttpResponseRedirect(url)

    return render(request,"add.html")
