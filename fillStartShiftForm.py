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
    driver1 = webdriver.Chrome("/Users/chatuu/Downloads/chromedriver")
    driver1.set_page_load_timeout(10)
    driver1.get(
        "http://novadaq-test-master.fnal.gov:8083/snapshot/ShowImage.jsp?id=4a03190f")
    image = driver1.find_element_by_xpath('/html/body/img')
    url = image.get_attribute('src')
    urlretrieve(url, 'Screen01.png')

    driver1.get(
        "http://novadaq-test-master.fnal.gov:8083/snapshot/ShowImage.jsp?id=4a03190d")
    image = driver1.find_element_by_xpath('/html/body/img')
    url = image.get_attribute('src')
    urlretrieve(url, 'Screen02.png')

    driver1.close()


def readImages():
    output = {}
    img1 = Image.open(r'Screen02.png')
    width, height = img1.size
    imgRun = img1.crop((1889, 251, 1960, 274))
    imgRun.show()
    RunNo = tess.image_to_string(imgRun, config="--psm 13")
    imgSubrun = img1.crop((1918, 285, 1947, 309))
    SubrunNo = tess.image_to_string(imgSubrun, config="--psm 13")

    img2 = Image.open(r'Screen01.png')
    width, height = img2.size

    imgPOT = img2.crop((1227, 1916, 1472, 1947))
    imgPOT.show()
    POT = tess.image_to_string(imgPOT, config="--psm 13")

    imgCurrent = img2.crop((2245, 1949, 2334, 1970))
    imgCurrent.show()
    current = tess.image_to_string(imgCurrent, config="--psm 13")

    return [RunNo, SubrunNo, current, POT]


def fillStartShift():
    driver = webdriver.Chrome("/Users/chatuu/Downloads/chromedriver")
    driver.set_page_load_timeout(10)
    driver.get(
        "http://dbweb5.fnal.gov:8080/ECL/novatestbeam/E/create_entry?f=Start+Shift")
    driver.find_element_by_name("username").send_keys("ckuruppu")
    driver.find_element_by_name("password").send_keys("USCChatuu123!")
    submit_button = driver.find_element_by_xpath(
        "/html/body/div[2]/div/div[2]/table/tbody/tr/td[2]/div[2]/form/table/tbody/tr[3]/td[2]/input")
    submit_button.submit()

    driver.find_element_by_name("MCenterBeam").click()
    driver.find_element_by_name("ReviewedECL").click()
    driver.find_element_by_name("ReviewBulletinBoard").click()
    driver.find_element_by_name("VNC").click()
    driver.find_element_by_name("Zoom").click()
    driver.find_element_by_name("Kerberos").click()
    driver.find_element_by_name("RunControl").click()

    magnetPPolarity = driver.find_element_by_xpath(
        "/html/body/div[2]/table/tbody/tr/td/div[2]/form[2]/table[2]/tbody/tr[4]/td[1]/input[1]")
    magnetPPolarity.click()

    runInfo = readImages()

    detectorRun = "Detector/"+runInfo[0]+"/"+runInfo[1]

    driver.find_element_by_name("Runs").send_keys(detectorRun)

    driver.find_element_by_name("MagnetCurrent").send_keys(runInfo[2])

    driver.find_element_by_name("CurrentConditions").send_keys(runInfo[3])

    time.sleep(1000)
    driver.quit()


def main():
    fillStartShift()


if __name__ == '__main__':
    main()
