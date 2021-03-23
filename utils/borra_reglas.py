'''
Application for removing rules on Alfresco
'''

import time
import secrets
import json
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import alflib

HOST='10.42.25.237'
URL_API=':8080/alfresco/api/-default-/public/alfresco/versions/1/'

class AlfrescoBot():
    '''
    Selenium Bot for Alfresco.
    Logs in, erases rules, etc.
    '''
    def __init__(self):
        '''
        Inits the selenium driver. TODO: Share login session.
        '''
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(30)
        self.driver.get("http://" + HOST + ":8080/share")

    def login(self):
        '''
        Logs into Alfresco by using the form.
        '''
        elem = self.driver.find_element_by_name("username")
        #print(elem)
        elem.clear()
        elem.send_keys(secrets.username)
        elem = self.driver.find_element_by_name("password")
        elem.clear()
        elem.send_keys(secrets.password)
        elem.send_keys(Keys.RETURN)

    def borra_r(self):
        # pylint: disable=W0702
        '''
        Erases rules. You have to be inside the folder-rules page.
        '''
        try:
            elem = self.driver.find_element_by_partial_link_text("R-")
        except:
            return False
        elem.click()
        time.sleep(6)
        button = '/html/body/div[4]/div[1]/div[2]/div[4]/div[2]/div/div/div/div/div[1]/span[2]/span'
        elem = self.driver.find_element_by_xpath(button)
        elem.click()
        time.sleep(2)
        elem = self.driver.find_element_by_xpath('//*[@id="yui-gen7-button"]')
        elem.click()
        return True

    def goto_rules(self, dir_id):
        '''
        Receive a dir_id from Alfresco, and it generates the url and goes to it.
        '''
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(30)
        folder_url = ':8080/share/page/site/rncr/folder-rules?nodeRef=workspace://SpacesStore/'
        url = "http://" + HOST + folder_url + dir_id
        self.driver.get(url)

    def reload(self):
        # pylint: disable=W0612
        '''
        Web page reload.
        '''
        time.sleep(6)
        elem = self.driver.refresh()

    def close(self):
        '''
        Closes the web page
        '''
        self.driver.close()

def recursive_search(search_data):
    '''
    Recursively searches inside alfresco, with the objetive of finding specific names,
    and erasing the rules that match a certain name from them.
    '''
    for dir_item in search_data['list']['entries']:
        #print(dir_item)
        if dir_item['entry']['isFolder']:
            dir_id = dir_item['entry']['id']
            dir_name = dir_item['entry']['name']
            if dir_name in ['04 - GESTIONAR DOCUMENTO','DOCUMENTOS POR FIRMAR']:
                print(dir_id, dir_name)
                bot.goto_rules(dir_id)
                bot.login()
                borrado=True
                while borrado:
                    time.sleep(5)
                    borrado=bot.borra_r()
                    bot.reload()
                bot.close()
            url = 'http://' + HOST + URL_API + 'nodes/' + dir_id + '/children'
            new_response = requests.get(url,headers=alflib.headers)
            subsearch = json.loads(new_response.text)
            recursive_search(subsearch)

bot = AlfrescoBot()

ROOTID='345185be-f20f-474f-b23f-9768ae70e851'

URL = 'http://' + HOST + URL_API + 'nodes/' + ROOTID + '/children'
print(URL)
response = requests.get(URL,headers=alflib.headers)
search = json.loads(response.text)

recursive_search(search)

bot.close()
