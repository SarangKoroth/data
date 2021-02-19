#Repository : bilal_linkedin_reply
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time
import random
import sys
import pymongo
import urllib.parse
import dns
from mongoengine import *
from mongoengine.context_managers import switch_collection
import traceback
from selenium.common.exceptions import TimeoutException
from time import sleep


Email_id = sys.argv[1]
Password = sys.argv[2]
OldMessage = sys.argv[3]
input_message = sys.argv[4]
dateLimit = sys.argv[5] #dateFormat = 2020-12-15
# print(input_message)

sleeps = [2,3,4]
def otp():
    client = pymongo.MongoClient('mongodb+srv://bilalm:' + urllib.parse.quote_plus('Codemarket.123') + '@codemarket-staging.k16z7.mongodb.net/codemarket_shiraz?retryWrites=true&w=majority')
    my_db = client['codemarket_shiraz']
    time.sleep(random.choice(sleeps))
    print("Linkedin sent you an OTP to your email.")
    otp_db = my_db.OTP_linkedin
    otp_db.insert({"linkedin_login_url": Email_id, "Status":"OTP sent"})
# execute "python otp.py <email> <otp>" in another terminal
    flag = True
    while flag:
        data = otp_db.find({"linkedin_login_url": Email_id, "Status":"OTP updated"})
        data = list(data)
        # print(data)
        # print(len(data))
        if len(data) == 1:
            # print(data[0]['OTP'])
            otp = data[0]['OTP']
            # print("otp is: ",otp)
            otp_db.update_many( 
            {"linkedin_login_url":Email_id, "Status":"OTP updated"}, 
            { "$set":{ "Status":"Login complete" }},)
            break
        time.sleep(5)
    # otp = int(input("Please enter the OTP recieved at registered mobile number: "))
    # driver.current_url
    submit_otp = driver.find_element_by_name("pin")
    submit_otp.send_keys(otp)
    submit_otp.send_keys(Keys.RETURN)
    my_db.OTP_linkedin.drop()
        
# def chat_scroll():
#     try:
#         chats = driver.find_element_by_xpath("//*[@class='msg-conversations-container__conversations-list msg-overlay-list-bubble__conversations-list']")
#         # chats = driver.find_elements_by_xpath("//div[@class='msg-conversation-listitem__link msg-overlay-list-bubble__convo-item   msg-overlay-list-bubble__convo-item--v3']")
#         chat_len = len(chats.find_elements_by_xpath('./div'))
#         l = driver.find_element_by_xpath("//*[@class='msg-conversations-container__conversations-list msg-overlay-list-bubble__conversations-list']/div[last()]") #last Element
#         # for l in chats.find_elements_by_xpath('./div')  :
#         # print(l)
#         driver.execute_script("arguments[0].scrollIntoView();", l)
#         sleep(4)
#         #time.sleep(1)
#         # chat_check = chat_list.find_elements_by_xpath("//div[@class='msg-conversation-listitem__link msg-overlay-list-bubble__convo-item   msg-overlay-list-bubble__convo-item--v3']")
#         chat_check = driver.find_element_by_xpath("//*[@class='msg-conversations-container__conversations-list msg-overlay-list-bubble__conversations-list']")
#         # print(len(chat_check))
#         print(len(chat_check.find_elements_by_xpath('./div') ), chat_len)
#         if len(chat_check.find_elements_by_xpath('./div') ) > chat_len:
#             chat_scroll()
#         print("Scrolling chat...")
#         return True
#     except:
#         print("No chat scroll...")

def chat_scroll():
    try:
        #Chat scrolling
        chats = driver.find_element_by_xpath("//*[@class='msg-conversations-container__conversations-list msg-overlay-list-bubble__conversations-list']")
        chat_len = len(chats.find_elements_by_xpath('./div'))
        l = driver.find_element_by_xpath("//*[@class='msg-conversations-container__conversations-list msg-overlay-list-bubble__conversations-list']/div[last()]")
        driver.execute_script("arguments[0].scrollIntoView();", l)
        
        #Incoming Entered Date and converting into ( 202-02-12 to Feb 12, 2020 format)
        sleep(4)
        print(dateLimit)
        incomingdate = dateLimit
        incomingdate = incomingdate.split('-')
        if int(incomingdate[1]) < 10:
            incomingdate[1] = incomingdate[1].replace('0','')
        month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthCheck = month[int(incomingdate[1])-1]
        sleep(2)
        
        #Retreiving date
        timetext = driver.find_element_by_xpath("//*[@class='msg-conversations-container__conversations-list msg-overlay-list-bubble__conversations-list']/div[last()]/div/div[2]/div/div[1]/time")
        timetext = timetext.text.split()
        timeDate = timetext[1].replace(',', '')
        flag = 0
        print("Enterd date :", incomingdate)
        print("Retrive date :",timetext)
        
        #Comparing both date
        if int(incomingdate[0]) < 2021: #for Dec 12, 2020
            try:
                if int(timetext[2]) == int(incomingdate[0]):
                    if timetext[0] == monthCheck:
                        if int(timeDate) <= int(incomingdate[2]):
                            flag = 1
                            print("Found Date. Stop Scrolling")
            except:
                pass
        else: #for Feb 15 (2021 year)
            if timetext[0] == monthCheck:
                if int(timeDate) <= int(incomingdate[2]):
                    flag = 1
                    print("Found Date. Stop Scrolling")
                    
        sleep(2)
        
        #Retreiving latest chatlist
        chat_check = driver.find_element_by_xpath("//*[@class='msg-conversations-container__conversations-list msg-overlay-list-bubble__conversations-list']")
        print(len(chat_check.find_elements_by_xpath('./div') ), chat_len)
        
        #flag is updated to 1 means entered date found. if its 0 means it will find next date and call fundtion again
        if len(chat_check.find_elements_by_xpath('./div') ) > chat_len and flag == 0:
            chat_scroll()
        print("Scrolling chat...")
        return True
    except:
        print("No chat scroll...")
        # traceback.print_exc()

try: 
    chrome_options = Options()
    chrome_options.add_argument(" — incognito")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--disable-dev-shm-usage')
    PATH= r"/usr/local/bin/chromedriver"
    # PATH = r"C:\Users\BILAL\Projects\LinkedInScraper\chromedriver.exe"
    driver = webdriver.Chrome(PATH,options=chrome_options)
    # driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.linkedin.com/login")

except TimeoutException as exception:
    print("Chrome failed to start... Please Restart Script...")

driver.find_element_by_id("username").send_keys(Email_id)
password = driver.find_element_by_id("password")
time.sleep(random.choice(sleeps))
password.send_keys(Password)
password.send_keys(Keys.RETURN)

if driver.current_url == 'https://www.linkedin.com/checkpoint/lg/login-submit' or "login-submit" in driver.current_url:
    print("--Incorrect login details--")

if 'https://www.linkedin.com/checkpoint/lg/login?errorKey=challenge_global_internal_error' in driver.current_url:
    print("Sorry something went wrong. Please try again later")

if 'https://www.linkedin.com/checkpoint' in driver.current_url:
    print("Current URL : ", driver.current_url)
    otp()
print("Current URL : ", driver.current_url)
print('Login...')
    
# chat_list = driver.find_element_by_xpath("//div[@class='msg-conversations-container__conversations-list msg-overlay-list-bubble__conversations-list']")
# chat_list
# chat_container = chat_scroll()
chat_scroll()

chat_check = driver.find_elements_by_xpath("//div[@class='msg-conversation-listitem__link msg-overlay-list-bubble__convo-item  msg-overlay-list-bubble__convo-item--v2 ']")
if len(chat_check) == 0: 
    chat_check = driver.find_elements_by_xpath("//div[@class='msg-conversation-listitem__link msg-overlay-list-bubble__convo-item   ']")   

chat_container = chat_check
# print("Chat Container: ", len(chat_container))
soup1 = BeautifulSoup(driver.page_source, 'html.parser')
# print(soup1)

# chatDIv = soup1.find_all('div', attrs={"class": "msg-conversations-container__conversations-list msg-overlay-list-bubble__conversations-list"})
# chats = chatDIv[0].find_all('div', attrs={"class": "msg-conversation-listitem__link msg-overlay-list-bubble__convo-item msg-overlay-list-bubble__convo-item--v2 "})
sleep(2)
chats = soup1.find_all('div', attrs={"class": "msg-conversation-listitem__link msg-overlay-list-bubble__convo-item msg-overlay-list-bubble__convo-item--v2 "})
if len(chats) == 0: 
    # print("Iff")
    chats = soup1.find_all('div', attrs={"class": "msg-conversation-listitem__link msg-overlay-list-bubble__convo-item"})
if len(chats) == 0: 
    print("Iff")
    chats = soup1.find_all('div', attrs={"class": "msg-conversation-listitem__link msg-overlay-list-bubble__convo-item msg-overlay-list-bubble__convo-item--v2"})
if len(chats) == 0: 
    print("Iff")
    chats = soup1.find_all('div', attrs={"class": "msg-conversation-listitem__link msg-overlay-list-bubble__convo-item  msg-overlay-list-bubble__convo-item--v2"})


print("Chats:", len(chats))
for enu,chat in enumerate(chats):
    # print(enu, chat)
    print("-------------------")
    # chat = chats[enu].find('mark', attrs={"class":"msg-conversation-card__unread-count"})
    # if chat:
    try:
        # print("New Message")
        chat_container[enu].send_keys(Keys.RETURN)
        time.sleep(random.choice(sleeps))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # chat_box = soup.find('div', {"class":"msg-overlay-conversation-bubble"})
        chat_box = soup.find('div', {"class":"msg-s-message-list-container relative display-flex mtA ember-view"})
        # print("chatbox", len(chat_box))
        # conversation_list = chat_box.find('ul', {"class":"msg-s-message-list-content  list-style-none full-width"})
        conversation_list = chat_box.find('ul')
        time.sleep(random.choice(sleeps))
        conversation = conversation_list.find_all('li')
        time.sleep(random.choice(sleeps))
        # container = chat_box.find('h4')
        container = soup.find('h4', {'class':"msg-overlay-bubble-header__title truncate t-14 t-bold t-black pr1"})
        name = container.find('a').text.strip()
        # print(name)
        first_name = name.split(' ')[0]
        last_name = name.split( ' ')[1]
        if len(conversation) < 4:
            link = conversation[0].find_all('a')
            link = link[1]['href']

            profile_link= "https://www.linkedin.com"+link
            # print(profile_link)
        # print("Before for loop")
        conversation.reverse()
        for num,messages in enumerate(conversation):
            # print("ATTEMPT",num)
            if messages.p is None:
                # print("NO message")
                continue
            if messages.find('a')is None:
                # print("NO LINK")
                continue
            name_ = messages.find_all('a')
            name1 = name_[1].text.strip()
            link = messages.find('a')['href']
            msg = messages.p.text
            # print("1111")
            # print("Professional Link",profile_link)
            if name1 == name:
                link = messages.find('a')['href']
                profile_link= "https://www.linkedin.com"+link
            #     print(profile_link)
            # print("22222", name1, name)
            if name1 != name: 
                # print("3333")
                my_link = messages.find('a')['href']
                link = messages.find('a')['href']
                msg = messages.p.text
#                 print(name1)
#                 print(my_link)
                print(msg)
                # if msg == 'I have a great job opportunity for you' or msg == 'I have a great job opportunity for you.' or 'I have a great job' in msg:
                if OldMessage in msg:
                    print("Replying")

                    # message = f"https://www.soojji.com/profile_edit?linkedinurl={profile_link}&firstname={first_name}&lastname={last_name}"
                    message = f"https://www.soojji.com/interview_form?linkedinurl={profile_link}&firstname={first_name}&lastname={last_name}"
                    reply = driver.find_element_by_xpath("//div[@aria-label='Write a message…']")
                    time.sleep(random.choice(sleeps))
                    reply.send_keys(input_message)
                    send_reply = driver.find_element_by_xpath("//button[@type='submit']")
                    time.sleep(random.choice(sleeps))
                    send_reply.send_keys(Keys.RETURN)

                    reply.send_keys(message)
                    # send_reply = driver.find_element_by_xpath("//button[@type='submit']")
                    time.sleep(random.choice(sleeps))
                    send_reply.send_keys(Keys.RETURN)

                    close_chat = driver.find_element_by_xpath("//button[@data-control-name='overlay.close_conversation_window']")
                    time.sleep(random.choice(sleeps))
                    close_chat.send_keys(Keys.RETURN)
                    print("Replied")
                    time.sleep(random.choice(sleeps))
#                     break
                else: 
#                     print("ELSE")
                    close_chat = driver.find_element_by_xpath("//button[@data-control-name='overlay.close_conversation_window']")
                    time.sleep(random.choice(sleeps))
                    close_chat.send_keys(Keys.RETURN)
                    time.sleep(random.choice(sleeps))
                    print("Different Message... Closing ChatBox...")
                break
                    # print("ELSE")
        try:
            close_chat = driver.find_element_by_xpath("//button[@data-control-name='overlay.close_conversation_window']")
            time.sleep(random.choice(sleeps))
            if close_chat:
                
                close_chat = driver.find_element_by_xpath("//button[@data-control-name='overlay.close_conversation_window']")
                time.sleep(random.choice(sleeps))
                close_chat.send_keys(Keys.RETURN)
                time.sleep(random.choice(sleeps)) 
        except:
            # print("Error something")
            # traceback.print_exc()
            pass
    except:
        close_chat = driver.find_element_by_xpath("//button[@data-control-name='overlay.close_conversation_window']")
        time.sleep(random.choice(sleeps))
        if close_chat:                
            time.sleep(random.choice(sleeps))
            close_chat.send_keys(Keys.RETURN)
            time.sleep(random.choice(sleeps))
        print("Something error")
        traceback.print_exc()     
#         break