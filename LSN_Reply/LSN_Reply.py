#Repository: 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import sys
import time
import random
import traceback
from time import sleep
import urllib.parse
import pymongo
import ast

#Uisng Chrome browser
chrome_options = Options()
chrome_options.add_argument(" — incognito")
chrome_options.add_argument("--window-size=1920,1200");
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(r'/usr/local/bin/chromedriver', options=chrome_options)
# driver = webdriver.Chrome(options=chrome_options)

#Taking Input
EmailId = sys.argv[1]

Password = sys.argv[2]

LastMsg = sys.argv[3]

ReplyMsg = sys.argv[4]

Limit = int(sys.argv[5])

#DB connection
client = pymongo.MongoClient('mongodb+srv://sumi:'+urllib.parse.quote_plus('sumi@123')+'@codemarket-staging.k16z7.mongodb.net/codemarket_shiraz?retryWrites=true&w=majority')
db = client.codemarket_shiraz #db
otp_collection = db.OTP_linkedin #collection

#OTP 
def otp():
    print("Linkedin sent you an OTP to your email.")
    otp_collection.insert({"linkedin_login_url": EmailId, "Status":"OTP sent"})
    while True:
        data = otp_collection.find({"linkedin_login_url": EmailId, "Status":"OTP updated"})
        data = list(data)
        # print(data)
        # print(len(data))
        if len(data) == 1:
            # print(data[0]['OTP'])
            otpget = data[0]['OTP']
            # print("otp is: ",otp)
            otp_collection.update_many( 
            {"linkedin_login_url":EmailId, "Status":"OTP updated"}, 
            { "$set":{ "Status":"Login complete" }},)
            print("Found OTP")
            break
        print("Waiting for correct OTP...")
        sleep(15)
    submit_otp = driver.find_element_by_name("pin")
    submit_otp.send_keys(otpget)
    submit_otp.send_keys(Keys.RETURN)

    if driver.current_url == 'https://www.linkedin.com/checkpoint/challenge/verify':
        print("Dropping collection")
        sleep(2)
        otp_collection.drop()
        print("Incorrect OTP. Enter correct otp.")
        print(driver.current_url)
        #otp_collection.drop()
        otp()

    if 'https://www.linkedin.com/feed' in driver.current_url:
        print("Dropping collection")
        sleep(2)
        otp_collection.drop()
        print("Login from Otp...")
        return True
    else:
        print("Session Expired try login again...")
        LSN_Reply()
    print("No return...")

def chat_scroll():
    try:
        ul = driver.find_element_by_xpath("//*[@class='infinite-scroller is-scrollable ember-view overflow-y-auto overflow-hidden flex-grow-1']/ul")
        chat_len = len(ul.find_elements_by_xpath('./li'))
        for l in ul.find_elements_by_xpath('./li')  :
            driver.execute_script("arguments[0].scrollIntoView();", l)
            time.sleep(1)
            # chat_check = chat_list.find_elements_by_xpath("//div[@class='msg-conversation-listitem__link msg-overlay-list-bubble__convo-item   msg-overlay-list-bubble__convo-item--v3']")
            ul2 = driver.find_element_by_xpath("//*[@class='infinite-scroller is-scrollable ember-view overflow-y-auto overflow-hidden flex-grow-1']/ul")
            # print(len(chat_check))
        print(len(ul2.find_elements_by_xpath('./li')), chat_len)
        if len(ul2.find_elements_by_xpath('./li')) > chat_len:
            chat_scroll()
        print("Scrolling chat...")
    except:
        print("No chat scroll...")


def LSN_Reply():
    
    #Sign in into linked account
    driver.get("https://www.linkedin.com/login")
    driver.find_element_by_id("username").send_keys(EmailId)
    password = driver.find_element_by_id("password")
    sleep(2)
    password.send_keys(Password)
    password.send_keys(Keys.RETURN)

    if driver.current_url == 'https://www.linkedin.com/checkpoint/lg/login-submit' or "login-submit" in driver.current_url:
        print("Incorrect login details")

    if 'https://www.linkedin.com/checkpoint/lg/login?errorKey=challenge_global_internal_error' in driver.current_url:
        print("Sorry something went wrong. Please try again later")

    print("Current Url : " + driver.current_url)
    if "https://www.linkedin.com/checkpoint" in driver.current_url:
        print("OTP...")
        value = otp()
        if value == True:
            print("Redirected to Feed Page after login.")
        else:
            print("Something went wrong!!")

    if 'https://www.linkedin.com/feed' in driver.current_url:
        print("Login...")
    else:
        print("Something is wrong!! Try again!! Network Problem!!")
        print(driver.current_url)

    #Finding 
    try: 
        #Redirected to LSN Inbox Page
        print("Redirected to Linkedin Sales Navigator Inbox Page.")
        driver.get("https://www.linkedin.com/sales/inbox")
        
        sleep(20) #Longer wait for page load

        chat_scroll()

        #Connection list 
        ul = driver.find_element_by_xpath("//*[@class='infinite-scroller is-scrollable ember-view overflow-y-auto overflow-hidden flex-grow-1']/ul")
        count = 1

        flag = 0

        #Going through each connection
        for x in ul.find_elements_by_xpath("./li"):

            #Selection 1 connection 
            sleep(2)
            a = x.find_element_by_tag_name('a')
            # print(a)
            a.click()
            sleep(2)

            #Chat Inbox
            inbox = driver.find_element_by_xpath("//*[@class='flex flex-column flex-grow-1 flex-shrink-zero justify-flex-end ember-view']/ul")
            # print(len(inbox.find_elements_by_xpath("./li")))

            #Going through each chat message
            for i in reversed(inbox.find_elements_by_xpath("./li")):
                #print(i.text)
                try:
                    #Checking for inmail message - if found then break the loop and moving to next connection - else Normal message
                    try:
                        inputdiv = driver.find_element_by_xpath("//*[@placeholder='Subject (required)']")
                        print("--Not Connected--")
                        sleep(2)
                        break
                    except:
                        sleep(2)
                        pass
                    
                    # userName = i.find_element_by_tag_name("address")
                    #print(userName.text, len(userName.text))
                    # if userName.text == "You":
                    #print("--Some Message Sent By You, Searching Invitation Message... Wait...--")
                    
                    #Retriving 1 msg
                    sleep(2)
                    article = i.find_element_by_tag_name("article")
                    sleep(2)

                    yourMsgName = article.find_element_by_xpath("./div[1]").text.strip()
                    yourMsgName = yourMsgName.split(" ")[0]

                    #Finding your sent messsage if you sent some message then it will compare LastMsg(input) with msg.text(already sent msg )
                    if yourMsgName == "You":

                        msg = article.find_element_by_xpath("./div[2]")
                        # print(msg.text)
                        #Checking msg is equal to LastMsg or not 
                        # if "I have a great job offer for you" in msg.text:
                        if LastMsg in msg.text:
                            print("--Invitation Message Found--")

                            #Name retrieve
                            name = x.find_element_by_xpath('./a/div/div[2]/div/div[1]')
                            #print(name.text)
                            
                            name = name.text.strip()
                            
                            first_name = name.split(' ')[0]
                            last_name = name.split( ' ')[1]
                            
                            #Save the window opener (current window)
                            main_window = driver.current_window_handle

                            profile = driver.find_element_by_xpath("//*[@data-control-name='view_profile']")
                            profile.click()

                            # Switch tab to the new tab, which we will assume is the next one on the right
                            driver.switch_to.window(driver.window_handles[1])
                            sleep(4)

                            #view profile dots 
                            viewProfileDots = driver.find_element_by_xpath("(//*[@class='profile-topcard-actions flex align-items-center mt2']/div)[last()]")
                            viewProfileDots.click()
                            sleep(2)

                            #view profile list options
                            viewProfileConnect = viewProfileDots.find_element_by_xpath("div/div/div/div/ul")
                            for x in viewProfileConnect.find_elements_by_xpath("./li"):
                                try:
                                    # print(x.text)
                                    #For connect
                                    if x.text == "View on LinkedIn.com":
                                        print("Clicking on view on linkedin.com")
                                        x.click()
                                        driver.close()
                                        driver.switch_to.window(driver.window_handles[1])
                                        sleep(4)
                                        profile_link = driver.current_url
                                        #Close the new tab
                                        driver.close()
                                        sleep(2)
                                        #Switch back to old tab
                                        driver.switch_to.window(main_window)
                                        break
                                except:
                                    pass
                                    # driver.close()
                                    # driver.switch_to.window(main_window)

                            #If Msg found enter Reply msg
                            textArea = driver.find_element_by_xpath("//*[@class='flex-grow-1 overflow-y-auto']")
                            textArea = textArea.find_element_by_tag_name("textarea")
                            textArea.click()
                            sleep(2)
                            textArea.send_keys(ReplyMsg)
                            
                            #Click on send
                            sleep(2)
                            send = driver.find_element_by_xpath("//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml4']")
                            send.click()

                            if first_name and last_name and profile_link:
                                message = f"https://www.soojji.com/interview_form?linkedinurl={profile_link}&firstname={first_name}&lastname={last_name}"
                                textArea.click()
                                sleep(2)
                                textArea.send_keys(message)
                                
                                #Click on send
                                sleep(2)
                                send = driver.find_element_by_xpath("//button[@class='artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml4']")
                                send.click()

                            print("--Reply Message sent successfully--")
                            
                            print("Count : ", count)
                            if count < Limit:
                                count += 1
                            else:
                                flag = 1
                                print("Limit is reached...")
                                break
                            break
                        break
                except:
                    #For ignoring 1 element of ul - li
                    sleep(2)
                    print("--Invitation message is searching.--")
                    #traceback.print_exc()
            #break
            if flag == 1:
                print("Flag : ", flag)
                print("--Reply Message Stopped--")
                break
            
    except:
        print("Error Occured...")
        traceback.print_exc()

LSN_Reply()
