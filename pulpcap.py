# PulPCAP
# __Author__ = Vlad Ionash
# Version 0.95

import time
import os
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# classes TODO In reference to the check/wait, safely ignore for now
class wait_for_text_to_start_with(object):
    def __init__(self, locator, text_):
        self.locator = locator
        self.text = text_

    def __call__(self, driver):
        try:
            element_text = EC._find_element(driver, self.locator).text
            return element_text.startswith(self.text)
        except StaleElementReferenceException:
            return False

KIBPListShow = ["CH1", "DC2"]
KIBPList = [x.lower() for x in KIBPListShow]
name = input("Enter Name:")
UID = [str(x).strip() for x in input(
    "Enter Telnyx Call Leg ID (Note: If you'd like to do more than 1, simply separate them with a space!):").split()]

# Enviro Variable from bash script ^^^ import OS
try:
    KIBPLocation = (os.environ['KIBPLocation'])
    print("\n" + "Reference: Current KIBP Tanker is: " + KIBPLocation)
except:
    print("\n" + "Hmmm...Looks like we couldn't get the current KIBP from the traceroute, hope you know it!")

print("\n" + "List of SIP Tankers" + str(KIBPListShow) + ":")

#KIBP Input
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
        print("")
        print(KIBPListShow)
        print("Not a valid input! Choose from above or leave blank!")
        continue

KIBP = KIBP.upper()
if KIBP == "":
    print("\n" + "Using CH1 location!")
else:
    print("\n" + "Using " + KIBP + " location!")

# Start webdriver! Using GeckoDriver(Firefox), run headlessly
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

"""
############################IF YOU"RE LOOKING FOR PATH TO WEBDRIVER, IT IS HERE!!!######################################
# If you want to specify driver location, simply append the above driver with (executable_path=r'<Your.path.here.exe')
# Example:
#         driver = webdriver.Firefox(options=options, executable_path=r'C:\WebDriver\bin\geckodriver.exe')
########################################################################################################################
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
    # TODO Program check instead of wait... don't think this is possible

    # Name
    elem = driver.find_element_by_xpath(
        "//*[@id='inputUsername']")
    elem.clear()
    elem.send_keys(name.strip() + "RTP_" + UID.strip())

    # Submit
    elem = driver.find_element_by_xpath(
        "/html/body/div/main/div[2]/form/button")
    elem.click()

    # Wait for output message and grab it
    try:
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[1]/div/div/div[2]/table/tbody/tr[1]/td[2]/span/span"))
        )
    except ValueError:
        print("Error 532: We Will Not Submit!!!")

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
    # TODO 2nd Wait

    # Host to KIBP, if blank defaults to CH1. Add elifs to add more KIBPs. More KIBP
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

    # Wait for output message and grab it
    try:
        elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div/div[1]/div/div/div[2]/table/tbody/tr[1]/td[2]/span/span"))
        )
    except ValueError:
        print("Error 532: We Will Not Submit!!!")

    messageSIP = driver.find_element_by_xpath(
        "/html/body/div/div/div/div[1]/div/div/div[2]/table/tbody/tr[1]/td[2]/span/span")
    firstTenMessageSIP = messageSIP.text[1:14]

    if firstTenMessageSIP == "start_time or":
        print("Hmmm...For the SIP portion, either wrong filter or doesn't exist! Double check ID")
    elif firstTenMessageSIP == "invalid_filter":
        print("Call doesn't look like it exists, isn't populated yet, or just an invalid filter. "
              "I would try doing it manually if you believe this is a mistake.")
    else:
        print("SIP " + messageSIP.text)

for X in UID:
    print("------Pulling PCAPs for: " + X + "------")
    PCAP_SIP(X)
    PCAP_RTP(X)

driver.close()
print("Congrats! You are lazy. Or attempted to be.")