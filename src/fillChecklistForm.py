#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from urllib.request import urlretrieve
import pytesseract as tess
from PIL import Image
import time

def takeScreens():
    driver=webdriver.Chrome("/Users/chatuu/Downloads/chromedriver")
    driver.set_page_load_timeout(10)
    driver.get("http://novadaq-test-master.fnal.gov:8083/snapshot/ShowImage.jsp?id=4a03190f")
    image=driver.find_element_by_xpath('/html/body/img')
    url=image.get_attribute('src')
    urlretrieve(url,'Screen01.png')

    driver.get("http://novadaq-test-master.fnal.gov:8083/snapshot/ShowImage.jsp?id=4a03190d")
    image=driver.find_element_by_xpath('/html/body/img')
    url=image.get_attribute('src')
    urlretrieve(url,'Screen02.png')

    driver.get("http://novadaq-test-master.fnal.gov:8083/snapshot/ShowImage.jsp?id=4a03190e")
    image=driver.find_element_by_xpath('/html/body/img')
    url=image.get_attribute('src')
    urlretrieve(url,'Screen03.png')

    driver.get("http://novadaq-test-master.fnal.gov:8083/snapshot/ShowImage.jsp?id=4a031910")
    image=driver.find_element_by_xpath('/html/body/img')
    url=image.get_attribute('src')
    urlretrieve(url,'Screen04.png')

    driver.close()

def readImages():
    output={}
    img1=Image.open(r'Screen02.png')
    width,height=img1.size
    imgRun=img1.crop((1890, 442, 1959, 473))
    RunNo=tess.image_to_string(imgRun,config="--psm 13")
    imgSubrun=img1.crop((1920, 480, 1950, 508))
    SubrunNo=tess.image_to_string(imgSubrun,config="--psm 13")
    imgBeamTrig=img1.crop((282, 1611, 331, 1632))
    beamTrig=tess.image_to_string(imgBeamTrig,config="--psm 13")
    imgOneHz=img1.crop((280, 1766, 332, 1784))
    oneHz=tess.image_to_string(imgOneHz,config="--psm 13")
    imgDDActiv=img1.crop((277, 1816, 331, 1836))
    ddActivity=tess.image_to_string(imgDDActiv,config="--psm 13")
    
    img2=Image.open(r'Screen01.png')
    width,height=img2.size
    imgTemp=img2.crop((560, 170, 610, 193))
    temp=tess.image_to_string(imgTemp,config="--psm 13")
    imgDew=img2.crop((560,218,596,234))
    dew=tess.image_to_string(imgDew,config="--psm 13")
    imgGas=img2.crop((2186,1141,2243,1161))
    gas=tess.image_to_string(imgGas,config="--psm 13")
    imgWater=img2.crop((1860, 1244, 1912, 1262))
    water=tess.image_to_string(imgWater,config="--psm 13")
    imgCurrent=img2.crop((2246, 1970, 2300, 1990))
    current=tess.image_to_string(imgCurrent,config="--psm 13")
    
    output['run']=RunNo
    output['subrun']=SubrunNo
    output['temp']=temp
    output['dew']=dew
    output['gas']=gas
    output['water']=water
    output['current']=current
    output['beamTrig']=beamTrig
    output['oneHz']=oneHz
    output['ddActiv']=ddActivity

    return output

def fillChecklist(output):
    run=output['run']
    subrun=output['subrun']
    temp=output['temp']
    dew=output['dew']
    gas=output['gas']
    water=output['water']
    current=output['current']
    beamTrig=output['beamTrig']
    oneHz=output['oneHz']
    ddActiv=output['ddActiv']
    runSubrun=str(run)+'/'+str(subrun)

    driver=webdriver.Chrome("/Users/chatuu/Downloads/chromedriver")
    driver.set_page_load_timeout(10)

    driver.get("http://dbweb5.fnal.gov:8080/ECL/novatestbeam/E/create_entry?f=Shift+Checklist")
    driver.find_element_by_name("username").send_keys("ckuruppu")
    driver.find_element_by_name("password").send_keys("USCChatuu123!")
    submit_button = driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/table/tbody/tr/td[2]/div[2]/form/table/tbody/tr[3]/td[2]/input")
    submit_button.submit()

    driver.find_element_by_name("DetectorDAQRun").send_keys(runSubrun)
    driver.find_element_by_name("BeamlineTriggersDetector").send_keys(beamTrig)
    driver.find_element_by_name("DDTTriggers").send_keys(ddActiv)
    driver.find_element_by_name("1HzTriggers").send_keys(oneHz)
    driver.find_element_by_name("MagnetCurrent").send_keys(current)
    driver.find_element_by_name("MC7bTemperature").send_keys(temp)
    driver.find_element_by_name("MC7bDewPoint").send_keys(dew)
    driver.find_element_by_name("DryerDewPoint").send_keys(dew)
    driver.find_element_by_name("WaterInletTemp").send_keys(water)

    driver.find_element_by_name("DAQComments").send_keys("All OK..!")
    driver.find_element_by_name("DetectorDQMComments").send_keys("All OK..!")
    driver.find_element_by_name("DetectorEVDComments").send_keys("All OK..!")
    driver.find_element_by_name("BeamlineDQMComments").send_keys("All OK..!")
    driver.find_element_by_name("DetectorDAQ").click()
    driver.find_element_by_name("MagnetCurrentPolarity").click()
    driver.find_element_by_name("BeamlineDAQ").click()
    driver.find_element_by_name("BeamlineDQM").click()
    driver.find_element_by_name("DetectorDQM").click()
    driver.find_element_by_name("DetectorEVD").click()
    driver.find_element_by_name("DAQAppManager").click()
    driver.find_element_by_name("SpillServer").click()
    driver.find_element_by_name("TimingStatus").click()
    driver.find_element_by_name("BeamlineTriggers").send_keys("0")
    driver.find_element_by_name("AttachScreenshots").click()

    upload1=driver.find_element_by_name("__image__0")
    upload2=driver.find_element_by_name("__image__1")
    upload3=driver.find_element_by_name("__image__2")

    upload1.send_keys("/Users/chatuu/Documents/learning/python selenium/Screen01.png")
    upload2.send_keys("/Users/chatuu/Documents/learning/python selenium/Screen02.png")
    upload3.send_keys("/Users/chatuu/Documents/learning/python selenium/Screen03.png")

    moreImg=driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr/td/div[2]/form[2]/table[3]/tbody/tr[6]/td/a')
    moreImg.click()

    upload4=driver.find_element_by_name("__image__3")
    upload4.send_keys("/Users/chatuu/Documents/learning/python selenium/Screen04.png")

    time.sleep(1000)
    driver.quit()

def main():
    takeScreens()
    fillChecklist(readImages())

if __name__=='__main__':
    main()