import requests
import json
import urllib.parse
from time import sleep
import pymongo
from bson.objectid import ObjectId
import pandas as pd

print("--Script Started--")
client = pymongo.MongoClient('mongodb+srv://sumi:'+urllib.parse.quote_plus('sumi@123')+'@codemarket-staging.k16z7.mongodb.net/dreamjobpal?retryWrites=true&w=majority')
db = client.dreamjobpal
collection = db.interviewforms
whatsappData = list(collection.find({"status": "Form Submitted"}))
print(len(whatsappData))
if len(whatsappData):
    # print('iff')

    # Creating the group
    for y in whatsappData:
        try: 
            print("--------------------------------------------------------------------- ")
            allskills = y['skill_set'].split(" ")
            skill = allskills[0].split(',')
            GroupName = y['firstname'] + " " + y['lastname'][0] + "(" + skill[0] + ")"
            
            AdminNumber = '18053007217'
            
            participant = [y['whatsapp'].replace('+', ''), '18059055170', AdminNumber]
            
            message = f"FirstName : {y['firstname']}\nLastname : {y['lastname']}\nLinkedinUrl : {y['linkedinurl']}\nJoining Timeline : {y['joining_timeline']}\nCurrent_salary : {y['current_salary']}\nExpected_salary : {y['expected_salary']}\nSkill set : {y['skill_set']}\nWhatsapp No : {y['whatsapp']}"

            url1 = 'https://api.maytapi.com/api/e7fc0a51-09c8-48fe-b689-412d7f533ce4/10236/createGroup'
            headers = {'x-maytapi-key': 'fc6434c6-fc38-4eaa-87f1-b928f2ecdc84','Content-Type':'application/json','accept':'application/json'}
            
            #adminNo = input("Please enter the group admin's number (country code at front, Ex: 91xxxxxxxxxx):\n")
            adminNo = AdminNumber

            #membersNos = input("Please enter the numbers of group members separated by commas (country code at front, Ex: 91xxxxxxxxxx,91xxxxxxxxxx):\n")

            #groupName = input('Please enter the group name:\n')
            groupName = GroupName

            #phoneNos = membersNos.split(',')
            phoneNos = participant

            #print(phoneNos)
            dataDict = {'name': groupName, 'numbers': phoneNos}
            #print(dataDict)
            #print(json.dumps(dataDict))
            sleep(2)
            createGroup = requests.post(url1, headers = headers, data = json.dumps(dataDict))
            #print(createGroup)
            sleep(2)
            createGroupJson = createGroup.json()
            print(createGroupJson)
            
            if createGroupJson['success'] == False:
                collection.update_one({"_id":y['_id']}, {'$set':{"status": "Whatsapp number not available"}})
                print("--Wrong no in database or Country code in number not found--")

            groupId = createGroupJson['data']['id']
            #print(groupId)

            #Checking number is in createGroupJson participant present or not
            numbernotadded = y['whatsapp'].replace('+', '')
            groupParticipants = createGroupJson['data']['participants']
            flag = 0
            for x in groupParticipants:
                if numbernotadded not in x:
                    continue
                else:
                    flag = 1
            if flag == 0:
                print("--Not added in group--")
                message = message + f"\nNot added in group, sent private group invitation to {y['whatsapp']}"
            

            url2 = 'https://api.maytapi.com/api/e7fc0a51-09c8-48fe-b689-412d7f533ce4/10236/sendMessage'
            headers = {'x-maytapi-key': 'fc6434c6-fc38-4eaa-87f1-b928f2ecdc84','Content-Type':'application/json','accept':'application/json'}

            #message = input('Please enter the message you want to send on the group:\n')
            #message = y['Message']

            dataDict = {"to_number": groupId,"type": "text","message": message}
            sendMsg = requests.post(url2, headers = headers, data = json.dumps(dataDict))
            sendMsgJson = sendMsg.json()
            print(sendMsgJson)

            # url3 = 'https://api.maytapi.com/api/e7fc0a51-09c8-48fe-b689-412d7f533ce4/10236/group/promote'
            # headers = {'x-maytapi-key': 'fc6434c6-fc38-4eaa-87f1-b928f2ecdc84','Content-Type':'application/json','accept':'application/json'}
            # adminNo = adminNo + '@c.us'
            # data_Dict = {"conversation_id": groupId,"number": adminNo}
            # #print(json.dumps(dataDict))
            # promoteMember = requests.post(url3, headers = headers, data = json.dumps(data_Dict))
            # promoteMemberJson = promoteMember.json()
            #print(promoteMemberJson)
            
            print("----1 group created----")
            print("GroupName : ", GroupName)
            print("AdminNumber : ", AdminNumber)
            print("Participant : ", participant)
            print("Message : ", message)
            print("-----------------------")
            
            if flag == 0:
                collection.update_one({"_id":y['_id']}, {'$set':{"status": "Whatsapp group created, Sent private group invitation"}})
                print("Whatsapp group created, Sent private group invitation")
            else:
                collection.update_one({"_id":y['_id']}, {'$set':{"status": "Whatsapp group created"}}) #Update
            sleep(2)
            # break
        except:
            print("Wrong no in database or Country code in number not found or Mobile is not connected in maytapi")
else:
    print("All groups are alredy created.")

print("--Script Stopped--")