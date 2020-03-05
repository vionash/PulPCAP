# PulPCAP

Version 0.81

by Vlad

Headlessly pull PCAPs from extractor!

### Setup:
  You will need these dependencies to run this properly:
- Time
- OS
- Selenium
    
Selenium is a webdriver, which basically acts like a browser that you can automate to do stuff.
  Can be installed using <pip install selenium>
  
This code here is based on using geckodriver (firefox). You can download the latest release here: 

[Firefox WebDriver](https://github.com/mozilla/geckodriver/releases)    

Add this file to your PATH (so you can call the driver from anywhere) or just edit the python code to where you have it listed. Inside the code there will be a comment on where you can change this.

**NOTE:** You can use chrome for this as well, just have to configure it yourself but should be practically the same.
  
  This script can also reference the KIBP if you run the .sh file instead! It will traceroute, then just run the python script on top. Quite handy!

### Usage:
  
  You will have the following inputs:
- "Enter Name": This references how you can discern which PCAP is yours in the PCAPExtractor channel. It also adds the TUID at the end.
- "Enter Telnyx Call Leg ID": TUID Input. This is the Call-Leg ID that you can find in CDR Search/Call Session. You can add more than 1 even! Just simply add a space.
- "Enter SIP KIBP Location..": Choose between CH1 and DC2! CH1 references ch1.001 tanker and DC2 references dc.020 tanker.
    
 That's it! You should then see the requested PCAPs in the slack channel, processing. 
