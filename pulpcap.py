#PulPCAP
#Vladi

#Version 0.1

"""
To Do:
    -Find method to add new tab: <driver.execute_script("window.open('<URL>','_blank')")>
    -Find a way to actually focus on the tab for commands
    -Instead of sleeps, implement check for state change to make it work more consistently
    -If statements for breaking RTP/SIP search if not valid formats were used
    -Some fun responses for different things
    -Add setting up path to your own webdriver
    -KIBP for SIP configuration based on user input
"""

import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from progress.spinner import Spinner

# variables
KIBPList = ["CH1", "DC2"]
name = input("Enter Name:")
UID = input("Enter Telnyx UUID:").strip()
print("List of SIP Tankers" + str(KIBPList) + ":")
KIBP = input("Enter SIP KIBP Location from list above! (If left blank, defaults to CH1):")
KIBP = KIBP.lower()
print('Pulling PCAP with UID of ' + UID)

options = Options()
#options.add_argument("--headless")
driver = webdriver.Firefox(options=options)

#functions
def PCAP_RTP():
    # Firefox Driver + PCAP Site + Make sure we get to it

    driver.get('http://10.255.0.21:1968/')
    assert "PCAP" in driver.title

    # AutoFillButton
    elem = driver.find_element_by_xpath("/html/body/div/main/div[2]/div[1]/button")
    elem.click()

    # UID Box
    elem = driver.find_element_by_xpath("//*[@id='inputID']")
    elem.clear()
    elem.send_keys(UID.strip())

    # Submit Button
    elem = driver.find_element_by_xpath("//*[@id='fillButton']")
    elem.click()

    time.sleep(2)

    # Name
    elem = driver.find_element_by_xpath("//*[@id='inputUsername']")
    elem.clear()
    elem.send_keys(name.strip() + "RTP")

    # Submit
    elem = driver.find_element_by_xpath("/html/body/div/main/div[2]/form/button")
    elem.click()

    time.sleep(2)

    #Grab the output message
    messageRTP = driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div/div/div[2]/table/tbody/tr[1]/td[2]/span/span")
    firstTenMessageRTP = messageRTP.text[1:14]

    if firstTenMessageRTP == "start_time or":
        print("Hmmm...either wrong filter or doesn't exist! Double check ID")
    else:
        print("RTP " + messageRTP.text)

def PCAP_SIP():
    # Firefox Driver + PCAP Site + Make sure we get to it
    driver.get('http://10.255.0.21:1968/')
    assert "PCAP" in driver.title

    # AutoFillButton
    elem = driver.find_element_by_xpath("/html/body/div/main/div[2]/div[1]/button")
    elem.click()

    # UID Box
    elem = driver.find_element_by_xpath("//*[@id='inputID']")
    elem.clear()
    elem.send_keys(UID.strip())

    # Signaling Button
    elem = driver.find_element_by_xpath("/html/body/div[1]/main/div[2]/div[2]/div/div/div[2]/div/div[2]/div/label[2]/input")
    elem.click()

    # Submit Button
    elem = driver.find_element_by_xpath("//*[@id='fillButton']")
    elem.click()

    time.sleep(2)

    # Host to CH1
    if KIBP == "ch1":
        elem = driver.find_element_by_xpath("/html/body/div/main/div[2]/form/div[2]/select/option[4]").click()
    elif KIBP == "dc2":
        elem = driver.find_element_by_xpath("/html/body/div/main/div[2]/form/div[2]/select/option[22]").click()
    else:
        elem = driver.find_element_by_xpath("/html/body/div/main/div[2]/form/div[2]/select/option[4]").click()

    # Source
    elem = driver.find_element_by_xpath("/html/body/div/main/div[2]/form/div[3]/select/option[2]").click()

    # Name
    elem = driver.find_element_by_xpath("//*[@id='inputUsername']")
    elem.clear()
    elem.send_keys(name.strip() + "SIP")

    # Submit
    elem = driver.find_element_by_xpath("/html/body/div/main/div[2]/form/button")
    elem.click()

    time.sleep(2)

    #Grab the output message
    messageSIP = driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div/div/div[2]/table/tbody/tr[1]/td[2]/span/span")
    firstTenMessageSIP = messageSIP.text[1:14]

    if firstTenMessageSIP == "start_time or":
        print("Hmmm...either wrong filter or doesn't exist! Double check ID")
    else:
        print("SIP " + messageSIP.text)

PCAP_SIP()
#PCAP_RTP()

driver.close()

print("Congrats! You are lazy.")
# elem.send_keys(Keys.RETURN)
