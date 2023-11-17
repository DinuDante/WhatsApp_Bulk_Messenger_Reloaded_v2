
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib.parse import quote
import os
import pandas as pd
import re
#customize and configure the behavior of a browser when controlled by the WebDriver
options = Options()
# exclude the logging feature during ChromeDriver execution.
options.add_experimental_option("excludeSwitches", ["enable-logging"])
#to create user prifile Directory when launching the Chrome browser.
options.add_argument("--profile-directory=Default")
#directory path where the user data for the Chrome browser should be stored.
options.add_argument("--user-data-dir=d:\\userdata")

os.system("")
#logging level of WebDriver Manager.
os.environ["WDM_LOG_LEVEL"] = "0"
#control the color of text when printed to the console
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

print(style.BLUE)
print("**********************************************************")
print("**********************************************************")
print("*****                                               ******")
print("*****  Initiating Mass Messenger >WhatsApp<         ******")
print("*****                                               ******")
print("**********************************************************")
print("**********************************************************")
print(style.RESET)

# read the message from text file
f = open("message.txt", "r")
message = f.read()
f.close()

print(style.YELLOW + '\nThis is your message-')
print(style.GREEN + message)
print("\n" + style.RESET)
message = quote(message)

#Read the excel sheet
df=pd.read_excel('C:\\Users\\HP\\Documents\\Whatsapp_Data.xlsx')

numbers=df['phone'].tolist()
#converting list to string
list_to_str = list(map(str, numbers))

# Add '91' prefix to numbers that don't have it
mobile_numbers = ['91' + num if not num.startswith('91') else num for num in list_to_str]

#length of phone number
total_number=len(mobile_numbers)

print(style.RED + 'We found ' + str(total_number) + ' numbers in the file' + style.RESET)
#maximum amount of time web driver wait
delay = 20
#open the drive in chrome with customize behaviour of chrome driver
driver=webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
print('Once your browser opens up sign in to web whatsapp')
#open the whatapp 
driver.get('https://web.whatsapp.com/')
input(style.MAGENTA + "AFTER logging into Whatsapp Web is complete and your chats are visible, press ENTER..." + style.RESET)
#iterating loop for all numbers
for idx, number in enumerate(mobile_numbers):
	#remove the whitespace from number
	number = number.strip()
	if number == "":
		continue
	print(style.YELLOW + '{}/{} => Sending message to {}.'.format((idx+1), total_number, number) + style.RESET)
	try:
		#url for specific number
		url = 'https://web.whatsapp.com/send?phone=' + number + '&text=' + message
		sent = False
		#how many times url will execute
		for i in range(1):
			if not sent:
				#open the whatsapp for specific number
				driver.get(url)
				try:
					#WebDriver to wait for a certain amount of time until an expected condition is true. 
					wait=WebDriverWait(driver, delay)
					#save the sender button path
					click_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Send']")))
					#click the sender button
					click_btn.click()
					sleep(3)
					print(style.GREEN + 'Message sent to: ' + number + style.RESET)
				except Exception as e:
					print(style.RED + f"\nFailed to send message to: {number}, retry ({i+1}/1)")
					print("Make sure your phone and computer is connected to the internet.")
					print("If there is an alert, please dismiss it." + style.RESET)					
	except Exception as e:
		print(style.RED + 'Failed to send message to ' + number + str(e) + style.RESET)
driver.close()
