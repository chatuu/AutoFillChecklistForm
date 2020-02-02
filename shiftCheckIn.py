#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from urllib.request import urlretrieve
import pytesseract as tess
from PIL import Image
import time


def GetCoordinators():
    driver1 = webdriver.Chrome("/Users/chatuu/Downloads/chromedriver")
    driver1.set_page_load_timeout(10)
    driver1.get(
        "https://cdcvs.fnal.gov/redmine/projects/novatestbeam/wiki/Test_Beam_Shift_Bulletin_Board")
    html_list = driver1.find_element_by_xpath(
        "/html/body/div/div[2]/div[1]/div[3]/div[2]/div[2]/ul[1]")
    items = html_list.find_elements_by_tag_name("li")
    for item in items:
        line = item.text
        words = line.split()

        if (words[0] == "Run" and words[1] == "Coordinator:"):
            runCoord = words[2] + " " + words[3]
            print("Found Run Coordinator: " + runCoord)

        if (words[0] == "Deputy" and words[1] == "Run" and words[2] == "Coordinator:"):
            deputy = words[3]+" "+words[4]
            print("Found Deputy Run Coordinator: " + deputy)
    Coordinators = [runCoord, deputy]

    return Coordinators


def fillCheckIn():
    driver = webdriver.Chrome("/Users/chatuu/Downloads/chromedriver")
    driver.set_page_load_timeout(10)
    driver.get(
        "http://dbweb5.fnal.gov:8080/ECL/novatestbeam/E/create_entry?f=Shift+Check+In")
    driver.find_element_by_name("username").send_keys("ckuruppu")
    driver.find_element_by_name("password").send_keys("USCChatuu123!")
    submit_button = driver.find_element_by_xpath(
        "/html/body/div[2]/div/div[2]/table/tbody/tr/td[2]/div[2]/form/table/tbody/tr[3]/td[2]/input")
    submit_button.submit()

    driver.find_element_by_name("ShifterName").send_keys("Chatura Kuruppu")
    driver.find_element_by_name("Shift").send_keys("Swing")
    driver.find_element_by_name("ControlRoom").send_keys("ROC-West-TB")
    driver.find_element_by_name("Debrief").click()
    driver.find_element_by_name("CalledMCR").click()
    Coords = GetCoordinators()
    driver.find_element_by_name(
        "RunCoordinator").send_keys(Coords[0])
    driver.find_element_by_name(
        "DeputyRunCoordinator").send_keys(Coords[1])

    time.sleep(1000)
    driver.quit()


def main():
    fillCheckIn()


if __name__ == '__main__':
    main()
