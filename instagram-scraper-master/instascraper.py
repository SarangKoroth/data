import re
import csv
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


# Creating a class
class Insta_Info_Scraper:
    def login(self):
        inp= input("Please enter the phone no., email, or username: ")
        password = input("Please enter the password: ")
        
        

        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")   
        #options.add_argument("--disable-web-security")
        #options.add_argument("--allow-running-insecure-content")
        #options.add_argument("--allow-insecure-localhost")
        #options.add_argument("--no-sandbox")
        #options.add_argument("--disable-gpu")
        #options.add_argument("window-size=1920,1080")

        #In case the website blocks headless chrome
        #user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        #options.add_argument(f'user-agent={user_agent}')
        
        options.add_argument("--test-type")
        #options.add_argument("--disable-info-bars")
        options.add_argument('--ignore-certificate-errors')
        self.driver=webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",options=options)
        driver=self.driver
        # to load a given URL in browser window
        self.driver.get("https://www.instagram.com/accounts/login/")

        self.driver.implicitly_wait(15)
        
        
        usrname=self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        usrname.send_keys(inp)

        time.sleep(10)
        
        pswrd = self.driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')
        pswrd.send_keys(password)
        time.sleep(10)

        pswrd.send_keys(Keys.RETURN)
        time.sleep(5)

        if(self.driver.current_url=='https://www.instagram.com/accounts/login/two_factor?next=%2F'):
            otp = int(input("Please enter the OTP recieved at registered mobile number: "))
            self.driver.current_url
            submit_otp.send_keys(otp)
            submit_otp.send_keys(Keys.RETURN)


        print("Scraping in progress")
 
    def getinfo(self,hashtag):

        url='https://www.instagram.com/explore/tags/'+hashtag[1:]
        self.driver.get(url)
        time.sleep(2)
        
        print("--------------Top Posters in "+hashtag+"-----------------")

        try:
            for i in range(1,4):
                for j in range(1,4):
                    xpath='//*[@id="react-root"]/section/main/article/div[1]/div/div/div['
                    xpath += str(i)
                    xpath += ']/div['
                    xpath+=str(j)
                    xpath+=']'
                    self.driver.find_element_by_xpath(xpath).click()
                    pxpath='//span/a[@tabindex="0"]'
                    self.driver.find_element_by_xpath(pxpath).click()
                    time.sleep(10)


                    self.driver.get(self.driver.current_url)
                    html=self.driver.page_source
                    time.sleep(2)
                    #print(html)

                    title1=html.find('<title>')
                    title2=html.find('</title>')

                    content1=html.find('<meta content="')
                    content2=html.find('See Instagram')
                    content=html[content1+15:content2-2].split(', ')

                    followers=content[0]
                    following=content[1]
                    posts=content[2]

                    email = re.findall(r'[\w\.-]+@[\w\.-]+', html)
                    print('User:',html[title1+7:title2-29])
                    print(followers)
                    print(following)
                    print(posts)
                    print('Email:',list(set(email)))
                    print ('--------------Scraping completed!-----------------')
                    print("")

                    self.email.append(email)
                    self.driver.get(url)
                    time.sleep(2)
                    
        except:
            print("Error! Check your internet")

        print("--------------Top Posters Completed!-----------------")
        print("")

        print("--------------Recent Posters in "+hashtag+"-----------------")

        try:
            for i in range(1,11):
                for j in range(1,4):
                    xpath='//*[@id="react-root"]/section/main/article/div[2]/div/div['
                    xpath += str(i)
                    xpath += ']/div['
                    xpath+=str(j)
                    xpath+=']'
                    self.driver.find_element_by_xpath(xpath).click()
                    pxpath='//span/a[@tabindex="0"]'
                    self.driver.find_element_by_xpath(pxpath).click()
                    time.sleep(10)


                    self.driver.get(self.driver.current_url)
                    html=self.driver.page_source
                    time.sleep(2)
                    #print(html)

                    title1=html.find('<title>')
                    title2=html.find('</title>')

                    content1=html.find('<meta content="')
                    content2=html.find('See Instagram')
                    content=html[content1+15:content2-2].split(', ')

                    followers=content[0]
                    following=content[1]
                    posts=content[2]

                    email = re.findall(r'[\w\.-]+@[\w\.-]+', html)
                    print('User:',html[title1+7:title2-29])
                    print(followers)
                    print(following)
                    print(posts)
                    print('Email:',list(set(email)))
                    print ('--------------Scraping completed!-----------------')

                    self.email.append(email)
                    self.driver.get(url)
                    time.sleep(2)

                    if i>4:
                        div = self.driver.find_element_by_xpath(xpath)
                        actions = ActionChains(self.driver)
                        actions.move_to_element(div).perform()
        except:
            print("Error! Check your internet")

        div = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[11][1]')
        actions = ActionChains(self.driver)
        actions.move_to_element(div).perform()

        try:
            for i in range(11,21):
                for j in range(1,4):

                    xpath='//*[@id="react-root"]/section/main/article/div[2]/div/div['
                    xpath += str(i)
                    xpath += ']/div['
                    xpath+=str(j)
                    xpath+=']'
                    self.driver.find_element_by_xpath(xpath).click()
                    pxpath='//span/a[@tabindex="0"]'
                    self.driver.find_element_by_xpath(pxpath).click()
                    time.sleep(10)


                    self.driver.get(self.driver.current_url)
                    html=self.driver.page_source
                    time.sleep(2)
                    #print(html)

                    title1=html.find('<title>')
                    title2=html.find('</title>')

                    content1=html.find('<meta content="')
                    content2=html.find('See Instagram')
                    content=html[content1+15:content2-2].split(', ')

                    followers=content[0]
                    following=content[1]
                    posts=content[2]

                    email = re.findall(r'[\w\.-]+@[\w\.-]+', html)
                    print('User:',html[title1+7:title2-29])
                    print(followers)
                    print(following)
                    print(posts)
                    print('Email:',list(set(email)))
                    print ('--------------Scraping completed!-----------------')

                    self.email.append(email)
                    self.driver.get(url)
                    time.sleep(2)

                    if i>14:
                        div = self.driver.find_element_by_xpath(xpath)
                        actions = ActionChains(self.driver)
                        actions.move_to_element(div).perform()
        except:
            print("Error! Check your internet")

        div = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[21][1]')
        actions = ActionChains(self.driver)
        actions.move_to_element(div).perform()

        try:
            for i in range(21,31):
                for j in range(1,4):
                    xpath='//*[@id="react-root"]/section/main/article/div[2]/div/div['
                    xpath += str(i)
                    xpath += ']/div['
                    xpath+=str(j)
                    xpath+=']'
                    self.driver.find_element_by_xpath(xpath).click()
                    pxpath='//span/a[@tabindex="0"]'
                    self.driver.find_element_by_xpath(pxpath).click()
                    time.sleep(10)


                    self.driver.get(self.driver.current_url)
                    html=self.driver.page_source
                    time.sleep(2)
                    #print(html)

                    title1=html.find('<title>')
                    title2=html.find('</title>')

                    content1=html.find('<meta content="')
                    content2=html.find('See Instagram')
                    content=html[content1+15:content2-2].split(', ')

                    followers=content[0]
                    following=content[1]
                    posts=content[2]

                    email = re.findall(r'[\w\.-]+@[\w\.-]+', html)
                    print('User:',html[title1+7:title2-29])
                    print(followers)
                    print(following)
                    print(posts)
                    print('Email:',list(set(email)))
                    print ('--------------Scraping completed!-----------------')

                    self.email.append(email)
                    self.driver.get(url)
                    time.sleep(2)

                    if i>24:
                        div = self.driver.find_element_by_xpath(xpath)
                        actions = ActionChains(self.driver)
                        actions.move_to_element(div).perform()
        except:
            print("Error! Check your internet")

        div = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[31][1]')
        actions = ActionChains(self.driver)
        actions.move_to_element(div).perform()

        try:
            for i in range(31,34):
                for j in range(1,4):
                    xpath='//*[@id="react-root"]/section/main/article/div[2]/div/div['
                    xpath += str(i)
                    xpath += ']/div['
                    xpath+=str(j)
                    xpath+=']'
                    self.driver.find_element_by_xpath(xpath).click()
                    pxpath='//span/a[@tabindex="0"]'
                    self.driver.find_element_by_xpath(pxpath).click()
                    time.sleep(10)


                    self.driver.get(self.driver.current_url)
                    html=self.driver.page_source
                    time.sleep(2)
                    #print(html)

                    title1=html.find('<title>')
                    title2=html.find('</title>')

                    content1=html.find('<meta content="')
                    content2=html.find('See Instagram')
                    content=html[content1+15:content2-2].split(', ')

                    followers=content[0]
                    following=content[1]
                    posts=content[2]

                    email = re.findall(r'[\w\.-]+@[\w\.-]+', html)
                    print('User:',html[title1+7:title2-29])
                    print(followers)
                    print(following)
                    print(posts)
                    print('Email:',list(set(email)))
                    print ('--------------Scraping completed!-----------------')

                    self.email.append(email)
                    self.driver.get(url)
                    time.sleep(2)

        except:
            print("Error! Check your internet")




        print("--------------Recent Posters Completed!-----------------")


    def main(self):
        self.email = []
        hashtag=input("Enter the relevant hashtags (separated by commas): ")
        try:
            hashtag=hashtag.split(',')
        except:
            ('Error! You have entered the hashtags incorrectly')
        if type(hashtag)==str:
            print('string found')
            hashtag=[hashtag]
        for i in hashtag:
            self.getinfo(i)
        self.generate_csv()
        

# collecting all the mails id into csv file
    def generate_csv(self):
        with open('email.csv', 'w', newline='') as file:
            file_write = csv.writer(file)
            file_write.writerow(["e-mails"])
            for email in self.email:
                file_write.writerow(email)
            


if __name__ == '__main__':
    obj = Insta_Info_Scraper()
    obj.login()
    obj.main()
