from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 
import unittest
from pynput.keyboard import Key, Controller

class Processes(unittest.TestCase):
    def __init__(self):
        self.messages = [] #holds messages
        self.subjects = [] #holds all interest topics
        self.waitTime = 0.0 #wait time between messages
        self.repeat = 0
    
    def getPath(self):
        while True:
            x = input("Copy and paste the path to the chromedriver her(exclude '\chromedriver.exe') ")
            print(x)
            if x is "":
                continue
            break
        self.path = x+"\chromedriver"


    def setUp(self): #requirement of unittest.TestCase. Creates webdriver object
        while True:
            try:
                self.getPath()
                self.driver = webdriver.Chrome(self.path)
                break
            except:
                print("Incorrect path to the chromedriver. Chromedriver not found")
        return super().setUp()

    def retrieveMessages(self):#receives input messages and stores them
        while True:
            try:
                numMessages = int(input("Enter the total number of messages you want to send: "))
                print(" ")
            except ValueError:
                print("Enter a number please")
                continue
            break
        for i in range(numMessages):
            tempMessage = input("Enter message "+str(i+1)+": ")
            self.messages.append(tempMessage)
        print(" ")
    
    def wait(self): #receives input for wait time between messages
        while True:
            try:
                self.waitTime = float(input("Type in how long you want the bot to wait before sending each message (in seconds): "))
            except ValueError:
                print("Enter a number please")
                continue
            break
        print(" ")

    def topics(self):#makes interests inputted as list
        print("List interests to try and find people with similar ones (optional)")
        print("If typing more than one interest, seperate each interest with one space")
        self.subjects = input("Type multi-word interests as one word - Ex: MountainClimbing: ").split()
        print(" ")

    def test_start(self): #finds website, inputs interests, and navigates to chat
        print("Browser is opening. Please wait a moment")
        self.driver.get("https://www.omegle.com/")
        interests = self.driver.find_element_by_class_name("newtopicinput")
        for i in range(len(self.subjects)):
            interests.send_keys(self.subjects[i])
            interests.send_keys(Keys.RETURN)
        search = self.driver.find_element_by_id("textbtn")
        search.click()
        time.sleep(2)
    
    def test_chat_is_disconnected(self):
        element = self.driver.find_element_by_class_name("inconversation")
        x = element.get_attribute("class")
        if x is "inconversation":
            return True
        else:
            return False

    
    def test_send_messages(self): #sends messages
        keyboard = Controller()
        for i in range(len(self.messages)):
            if self.test_chat_is_disconnected():
                break  
            time.sleep(self.waitTime)
            keyboard.type(self.messages[i])
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
    
    def test_to_next_chat(self): #navigates to next chat
        button = self.driver.find_element_by_class_name("disconnectbtn")
        for i in range(3):
            button.click()
    
    def timesRepeated(self):
        while True:
            try:
                self.repeat = int(input("Enter how many times do you want the bot to run: "))
            except ValueError:
                print("Enter a number please")
                continue
            break
        
print("Welcome to the Omegle Bot")
while True:
    print(" ")
    while True:
        try:
            flow = int(input("Enter 1 to proceed with use || Enter 0 to exit software: "))
        except ValueError:
            print("Enter 1 or 0 please")
            continue
        print(" ")
        break

    if flow is 1: 
        browser = Processes()
        browser.retrieveMessages()
        browser.timesRepeated()
        browser.wait()
        browser.topics()
        browser.setUp() #sets up webdriver object
        browser.test_start() #opens website
        for i in range(browser.repeat):
            browser.test_send_messages()
            browser.test_to_next_chat()
        print("Bot has finished running")
        browser.driver.quit()

    else:
        break
    



