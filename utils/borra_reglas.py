from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import secrets
import requests
import json
import alflib

HOST='10.42.25.237'


class AlfrescoBot():
  def __init__(self):
    self.driver = webdriver.Firefox()
    self.driver.set_page_load_timeout(30)
    self.driver.get("http://" + HOST + ":8080/share")


  def login(self):
    elem = self.driver.find_element_by_name("username")
    #print(elem)
    elem.clear()
    elem.send_keys(secrets.username)
    elem = self.driver.find_element_by_name("password")
    elem.clear()
    elem.send_keys(secrets.password)
    elem.send_keys(Keys.RETURN)

  def goto_docs_por_firmar(self):
      time.sleep(3)
      elem = self.driver.find_element_by_id('HEADER_SITES_MENU_text')
      elem.click()
      time.sleep(1)
      elem = self.driver.find_element_by_xpath('/html/body/div[13]/div/div[1]/div[2]/table/tbody/tr/td[2]/a')
      elem.click()
      time.sleep(2)
      elem = self.driver.find_element_by_id('HEADER_SITE_DOCUMENTLIBRARY')
      elem.click()
      time.sleep(5)
      elem = self.driver.find_element_by_link_text('10 - DIRECCIÓN BIENES MUEBLES')
      elem.click()
      time.sleep(1)
      elem = self.driver.find_element_by_link_text('10.00 - JEFATURA')
      elem.click()
      time.sleep(1)
      elem = self.driver.find_element_by_link_text('04 - GESTIONAR DOCUMENTO')
      elem.click()
      time.sleep(5)
      elem = self.driver.find_element_by_link_text('Manage Rules')
      elem.click()
      time.sleep(5)

  def borra_r(self):
      elem = self.driver.find_element_by_partial_link_text("R-")
      elem.click()
      time.sleep(6)
      elem = self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/div[2]/div[4]/div[2]/div/div/div/div/div[1]/span[2]/span")
      elem.click()
      time.sleep(2)
      elem = self.driver.find_element_by_xpath('//*[@id="yui-gen7-button"]')
      elem.click()

  def goto_rules(self, dir_id):
    self.driver = webdriver.Firefox()
    self.driver.set_page_load_timeout(30)
    self.driver.get("http://" + HOST +":8080/share/page/site/rncr/folder-rules?nodeRef=workspace://SpacesStore/" + dir_id)

  def reload(self):
    time.sleep(6)
    elem = self.driver.refresh()

  def close(self):
    self.driver.close()

def recursive_search(search_data):
    for dir_item in search_data['list']['entries']:
        #print(dir_item)
        if dir_item['entry']['isFolder']:
            dir_id = dir_item['entry']['id']
            dir_name = dir_item['entry']['name']
            if dir_name == '04 - GESTIONAR DOCUMENTO' or dir_name == 'DOCUMENTOS POR FIRMAR':
                print(dir_id, dir_name)
                bot.goto_rules(dir_id)
                bot.login()
                while True:
                    time.sleep(5)
                    bot.borra_r()
                    bot.reload()
            URL = 'http://' + HOST + ':8080/alfresco/api/-default-/public/alfresco/versions/1/nodes/' + dir_id + '/children'
            response = requests.get(URL,headers=alflib.headers)
            subsearch = json.loads(response.text)
            recursive_search(subsearch)
#    for subdir in search['list']['entries']:
#        curdir_id = subdir['entry']['id']
#        curdir_name = subdir['entry']['name']
#        print(curdir_id, curdir_name)

bot = AlfrescoBot()
#bot.login()

ROOTID='345185be-f20f-474f-b23f-9768ae70e851'

URL = 'http://' + HOST + ':8080/alfresco/api/-default-/public/alfresco/versions/1/nodes/' + ROOTID + '/children'
response = requests.get(URL,headers=alflib.headers)
search = json.loads(response.text)
#print(search)

recursive_search(search)

#time.sleep(5)
#bot.goto_docs_por_firmar()
#bot.borra_r()
#bot.reload()
#bot.borra_r()
#time.sleep(10)
#
#bot.close()
