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
"""

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

# variables
name = input("Enter Name:")
UID = input("Enter Telnyx UUID:").strip()
print('Pulling PCAP with UID of ' + UID)

#functions
def PCAP_RTP():
    # Firefox Driver + PCAP Site + Make sure we get to it
    # headless operation
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
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

    time.sleep(1.8)

    # Name
    elem = driver.find_element_by_xpath("//*[@id='inputUsername']")
    elem.clear()
    elem.send_keys(name.strip() + "RTP")

    # Submit
    elem = driver.find_element_by_xpath("/html/body/div/main/div[2]/form/button")
    elem.click()

    time.sleep(1.8)

    #Grab the output message
    messageRTP = driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div/div/div[2]/table/tbody/tr[1]/td[2]/span/span")
    print("RTP " + messageRTP.text)

    driver.close()

def PCAP_SIP():
    # Firefox Driver + PCAP Site + Make sure we get to it
    # headless operation
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
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

    time.sleep(1.8)

    # Host to CH1
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

    time.sleep(1.8)

    #Grab the output message
    messageSIP = driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div/div/div[2]/table/tbody/tr[1]/td[2]/span/span")
    print("SIP " + messageSIP.text)

    driver.close()

PCAP_RTP()
PCAP_SIP()

print("Congrats! You are lazy.")
# elem.send_keys(Keys.RETURN)
