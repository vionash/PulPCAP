# PulPCAP
# Vladi

# Version 0.8

import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import threading
from progress.spinner import PixelSpinner
from selenium.webdriver.common.keys import Keys
from progress.spinner import Spinner

# List to show
KIBPListShow = ["CH1", "DC2"]

# List to reference in code
KIBPList = [x.lower() for x in KIBPListShow]

name = input("Enter Name:")

UID = [str(x).strip() for x in input(
            "Enter Telnyx Call Leg ID (Note: If you'd like to do more than 1, simply separate them with a space!):").split()]

# Enviro Variable from bash script ^^^ import OS
try:
    KIBPLoc = (os.environ['KIBPLoc'])
    print("Reference: Current KIBP Tanker is: " + KIBPLoc)
except:
    print("Hmmm...Looks like we couldn't get the current KIBP from the traceroute, hope you know it!")

print("List of SIP Tankers" + str(KIBPListShow) + ":")

while True:
    try:
        KIBP = input("Enter SIP KIBP Location from list above! (If left blank, defaults to CH1):").strip()
        KIBP = KIBP.lower()
    except ValueError:
        print("Try again!")
        continue
    if KIBP in KIBPList or KIBP == "":
        break
    else:
        print(KIBPListShow)
        print("Not a valid input! Choose from above or leave blank!")
        continue

KIBP = KIBP.upper()
if KIBP == "":
    print("Using CH1 location!")
else:
    print("Using " + KIBP + " location!")

#Start webdriver! Using GeckoDriver(Firefox), run headleslly
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

"""
# If you want to specify driver location, simply append the above driver with (executable_path=r'<Your.path.here.exe')
# Example:
# driver = webdriver.Firefox(options=options, executable_path=r'C:\WebDriver\bin\geckodriver.exe')
"""

# functions
def PCAP_RTP(UID):
    # Firefox Driver + PCAP Site + Make sure we get to it
    driver.get('http://10.255.0.21:1968/')
    assert "PCAP" in driver.title

    # AutoFillButton
    elem = driver.find_element_by_xpath(
        "/html/body/div/main/div[2]/div[1]/button")
    elem.click()

    # UID Box
    elem = driver.find_element_by_xpath(
        "//*[@id='inputID']")
    elem.clear()
    elem.send_keys(UID.strip())

    # Submit Button
    elem = driver.find_element_by_xpath(
        "//*[@id='fillButton']")
    elem.click()

    time.sleep(2)

    # Name
    elem = driver.find_element_by_xpath(
        "//*[@id='inputUsername']")
    elem.clear()
    elem.send_keys(name.strip() + "RTP_" + UID.strip())

    # Submit
    elem = driver.find_element_by_xpath(
        "/html/body/div/main/div[2]/form/button")
    elem.click()

    time.sleep(2)

    # Grab the output message
    messageRTP = driver.find_element_by_xpath(
        "/html/body/div/div/div/div[1]/div/div/div[2]/table/tbody/tr[1]/td[2]/span/span")
    firstTenMessageRTP = messageRTP.text[1:14]

    if firstTenMessageRTP == "start_time or":
        print("Hmmm...For the RTP portion, either wrong filter or doesn't exist! Double check ID")
    else:
        print("RTP " + messageRTP.text)

def PCAP_SIP(UID):
    # Firefox Driver + PCAP Site + Make sure we get to it
    driver.get('http://10.255.0.21:1968/')
    assert "PCAP" in driver.title

    # AutoFillButton
    elem = driver.find_element_by_xpath(
        "/html/body/div/main/div[2]/div[1]/button")
    elem.click()

    # UID Box
    elem = driver.find_element_by_xpath(
        "//*[@id='inputID']")
    elem.clear()
    elem.send_keys(UID.strip())

    # Signaling Button
    elem = driver.find_element_by_xpath(
        "/html/body/div[1]/main/div[2]/div[2]/div/div/div[2]/div/div[2]/div/label[2]/input")
    elem.click()

    # Submit Button
    elem = driver.find_element_by_xpath(
        "//*[@id='fillButton']")
    elem.click()

    time.sleep(2)

    # Host to CH1
    if KIBP == "ch1":
        elem = driver.find_element_by_xpath(
            "/html/body/div/main/div[2]/form/div[2]/select/option[4]").click()
    elif KIBP == "dc2":
        elem = driver.find_element_by_xpath(
            "/html/body/div/main/div[2]/form/div[2]/select/option[22]").click()
    else:
        elem = driver.find_element_by_xpath(
            "/html/body/div/main/div[2]/form/div[2]/select/option[4]").click()

    # Source
    elem = driver.find_element_by_xpath(
        "/html/body/div/main/div[2]/form/div[3]/select/option[2]").click()

    # Name
    elem = driver.find_element_by_xpath(
        "//*[@id='inputUsername']")
    elem.clear()
    elem.send_keys(name.strip() + "SIP_" + UID.strip())

    # Submit
    elem = driver.find_element_by_xpath(
        "/html/body/div/main/div[2]/form/button")
    elem.click()

    time.sleep(2)

    # Grab the output message
    messageSIP = driver.find_element_by_xpath(
        "/html/body/div/div/div/div[1]/div/div/div[2]/table/tbody/tr[1]/td[2]/span/span")
    firstTenMessageSIP = messageSIP.text[1:14]

    if firstTenMessageSIP == "start_time or":
        print("Hmmm...For the SIP portion, either wrong filter or doesn't exist! Double check ID")
    else:
        print("SIP " + messageSIP.text)

for X in UID:
    print("------Pulling PCAPs for: " + X + "------")
    PCAP_SIP(X)
    PCAP_RTP(X)

driver.close()

print("Congrats! You are lazy. Or attempted to be.")
# elem.send_keys(Keys.RETURN)