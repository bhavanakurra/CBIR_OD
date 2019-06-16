from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import os
import json
import urllib.request as urllib2
from past.builtins import xrange
import sys
from PIL import Image
import requests
from io import BytesIO
from io import StringIO
from imageai.Detection import ObjectDetection
import os



def Scraping(x):
    binary = FirefoxBinary('/usr/bin/firefox')
    driver = webdriver.Firefox(firefox_binary=binary)

    url = "https://www.google.com/imghp?hl=en"
    driver.get(url)
    searchtext = x
    
    search_field = driver.find_element_by_name("q").send_keys(searchtext)
    time.sleep(1)


    search_field_02 = driver.find_element_by_xpath("//*[@id='sbtc']/button/div/span")
    search_field_02.click()


    
    images = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
    print(len(images))
    number_of_images_needed = 3
    extensions = {"jpg", "jpeg", "png", "gif"}
    os.environ["PATH"] += os.pathsep + os.getcwd()
    download_path = "../bhavana/Desktop/Result/"
    img_count = 0
    downloaded_img_count = 0
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

    if not os.path.exists(download_path + searchtext.replace(" ", "_")):
        os.makedirs(download_path + searchtext.replace(" ", "_"))

    for img in images:
        img_count += 1
        img_url = json.loads(img.get_attribute('innerHTML'))["ou"]
        img_type = json.loads(img.get_attribute('innerHTML'))["ity"]
        print("Downloading image", img_count, ": ", img_url)
        try:
            if img_type not in extensions:
                img_type = "jpg"
                
            req = urllib2.Request(img_url, headers=headers)
            
            
            raw_img = urllib2.urlopen(req).read()
            f = open(download_path+searchtext.replace(" ", "_")+"/"+str(downloaded_img_count)+"."+img_type, "wb")
            f.write(raw_img)
            f.close
            downloaded_img_count += 1
        except Exception as e:
            print("Download failed:", e)
        if downloaded_img_count >= number_of_images_needed:
            break

    print("Total downloaded: ", downloaded_img_count, "/", img_count)
    driver.quit()

def detection_object(image_path):

	execution_path = os.getcwd()

	detector = ObjectDetection()
	detector.setModelTypeAsRetinaNet()
	detector.setModelPath( os.path.join(execution_path , "../bhavana/Downloads/resnet50_coco_best_v2.0.1.h5"))
	detector.loadModel()

	detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , image_path), output_image_path=os.path.join(execution_path , "../bhavana/Desktop/imagenew.jpeg"))

	for eachObject in detections:
    		print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
    		Scraping(eachObject["name"])

	return "just"
    

