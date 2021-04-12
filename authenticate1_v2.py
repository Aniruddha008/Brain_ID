# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 00:33:27 2019

@author: Aniruddha Tarodekar
"""

#import tkinter.mesagebox
from datetime import datetime
import json
import ssl
import time
from tkinter import *
# install with pip install websocket-client
import websocket
import mysql.connector

class Cortex1():
  
  def __init__(self, url, user):
    self.ws =  websocket.create_connection(url, sslopt={"cert_reqs": ssl.CERT_NONE})
    self.user = user
  
  
  
  def query_headset(self):
    queryheadset_request = {
    'id' : 2,
    "jsonrpc": "2.0",
			"method": "queryHeadsets", 
			"params": { }
            }
    self.ws.send(json.dumps(queryheadset_request))
    result = self.ws.recv()
    result_dic = json.loads(result)
    print('query headset result', json.dumps(result_dic, indent=4))
    self.headset_id = result_dic['result'][0]['id']
    print('headset_id', self.headset_id)
    
    

  def connect_headset(self):
    connect_headset_request = {
			"jsonrpc": "2.0", 
			"id": 111,
			"method": "controlDevice",
			"params": {
				"command": "connect",
	    		"headset": self.headset_id
			}
		}
    self.ws.send(json.dumps(connect_headset_request))
    result = self.ws.recv()
    result_dic = json.loads(result)
    print('connect headset result', json.dumps(result_dic, indent=4))        


  def request_access(self):
    request_access_request = {
            "jsonrpc": "2.0", 
            "method": "requestAccess",
            "params": {
                   'clientId':'7qMdFUjo8jXXN2dXrhqUMgjL6jdn2Y2p38hSM3Vv', 
    'clientSecret': 'dsHNx4LxxJCkOHYijsHXBBtvMquvuRVqcuwacsxc4kAaVypwVqdWmc3UFoVbk6vEhirPp96GdgbrUQKhdvQLfESgMTvSWlHVhu9CAKHh6PIeL3rIzlM6kWXp6Jq6epzw'
    },
			"id": 1
		}
    self.ws.send(json.dumps(request_access_request))
    result = self.ws.recv()
    result_dic = json.loads(result)



  def authorize(self):
    authorize_request = {
			"jsonrpc": "2.0",
			"method": "authorize", 
			"params": { 
				'clientId':'7qMdFUjo8jXXN2dXrhqUMgjL6jdn2Y2p38hSM3Vv', 
    'clientSecret': 'dsHNx4LxxJCkOHYijsHXBBtvMquvuRVqcuwacsxc4kAaVypwVqdWmc3UFoVbk6vEhirPp96GdgbrUQKhdvQLfESgMTvSWlHVhu9CAKHh6PIeL3rIzlM6kWXp6Jq6epzw',
     			},
			"id": 4
		}
#        print('json.dumps(authorize_request)', json.dumps(authorize_request))
    self.ws.send(json.dumps(authorize_request))
    result = self.ws.recv()
    result_dic = json.loads(result)
    print('auth_result', json.dumps(result_dic, indent=4))
    self.auth = result_dic['result']['cortexToken']
    print('\ncortexToken', self.auth)

  def create_session(self, token, headset_id):
     create_session_request = { 
			"jsonrpc": "2.0",
			"id": 5,
			"method": "createSession",
			"params": {
				"cortexToken": self.auth,
				"headset": self.headset_id,
				"status": "open"
			}
		}
     self.ws.send(json.dumps(create_session_request))
     result = self.ws.recv()
     result_dic = json.loads(result)
     print('create session result ', json.dumps(result_dic, indent=4))
     self.session_id = result_dic['result']['id']
     print(self.session_id)
  
  
  def load_profile(self, name):
    load_request = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "setupProfile",
    "params": {
        "cortexToken": self.auth,
        'headset' : 'INSIGHT-5A688FB1',
        "profile": name,
        'status' : 'load'
    }}
    self.ws.send(json.dumps(load_request))
    result = self.ws.recv()
    result_dic = json.loads(result)
    print('loading up profile', json.dumps(result_dic, indent=4))
    return result_dic

  def unload_profile(self, name):
    unload_request = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "setupProfile",
    "params": {
        "cortexToken": self.auth,
        'headset' : 'INSIGHT-5A688FB1',
        "profile": name,
        'status' : 'unload'
    }}
    self.ws.send(json.dumps(unload_request))
    result = self.ws.recv()
    result_dic = json.loads(result)
    print('unloading up profile', json.dumps(result_dic, indent=4))

  
  

  
  def close_session(self):
    close_session_request = { 
			"jsonrpc": "2.0",
			"id": 5,
			"method": "updateSession",
			"params": {
				"cortexToken": self.auth,
				"session": self.session_id,
				"status": "close"
			}
		}
    self.ws.send(json.dumps(close_session_request))
    result = self.ws.recv()
    result_dic = json.loads(result)
    print('close session result ', json.dumps(result_dic, indent=4))
  
  def get_cortex_info(self):
    get_cortex_info_request = {
			"jsonrpc": "2.0",
			"method": "getCortexInfo",
			"id":100
        }
    self.ws.send(json.dumps(get_cortex_info_request))
    result = self.ws.recv()
    print(json.dumps(json.loads(result), indent=4))

  
  def has_access_right(self):
    has_access_right_request = {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "hasAccessRight",
            "params": {
               'clientId':'7qMdFUjo8jXXN2dXrhqUMgjL6jdn2Y2p38hSM3Vv', 
    'clientSecret': 'dsHNx4LxxJCkOHYijsHXBBtvMquvuRVqcuwacsxc4kAaVypwVqdWmc3UFoVbk6vEhirPp96GdgbrUQKhdvQLfESgMTvSWlHVhu9CAKHh6PIeL3rIzlM6kWXp6Jq6epzw'
     }
        }
    self.ws.send(json.dumps(has_access_right_request))
    result = self.ws.recv()
    print(json.dumps(json.loads(result), indent=4))
  
  def grant_access_and_session_info(self):
    self.query_headset()
    self.connect_headset()
    self.request_access()
    self.authorize()
    self.create_session(self.auth, self.headset_id)
    
  def subRequest(self, stream):
    subRequest = { 
			"jsonrpc": "2.0", 
			"method": "subscribe", 
			"params": { 
				"cortexToken": self.auth,
				"session": self.session_id,
				"streams": stream
			}, 
			"id": 6
		}

    self.ws.send(json.dumps(subRequest))
    
    
    print('\n')
    print('subscribe result')
    #time.sleep(1)
    self.login_attempts = 0
    self.successful_login_attempts = 0

    for i in range(1, self.user['number_row_data']):                    # Modify for loop to run however many times   
      new_data = self.ws.recv()
      result_dic = json.loads(new_data)
      w1 = self.extractKeyValue(result_dic)
      
  def subscribe(self, stream):
    
    self.grant_access_and_session_info()
    self.subRequest(stream)
                                             # calling function to get mental command info
    
  def extractKeyValue(self, result_dic):
    
    first_response = { 
			"id": 6,
            "jsonrpc":"2.0", 
			"result":{
                    "failure":[],
				    "success":[{
                            "cols": ["act","pow"],
				            "sid": self.session_id,
				            "streamName":"com"
                            }]
                }
        }
#    neutral = ['neutral', 0.0]
    
#    self.login_attempts = 0
#    self.successful_login_attempts = 0
#    self.participant_name = self.getUserName()  # remove later, this is just in case the get function does not work
    self.l = ''
    
    if result_dic != first_response:
      self.get_mental_command = result_dic['com']
      
      if (self.get_mental_command[0] == 'lift') and (self.get_mental_command[1] > 0.85):
        
        #print('login successfull'+ '\naction', self.get_mental_command[0] + '\nscore', self.get_mental_command[1] )                    
        action = self.get_mental_command[0]
        score = str(self.get_mental_command[1])
        print('action', action + ' score:', score)
       
        
        self.login_attempts += 1
        self.successful_login_attempts += 1
        print('+ve' ,self.login_attempts)
        print('+ve',self.successful_login_attempts)
        
        
        self.storeDatabase_PerformanceTable(self.get_mental_command[0], self.get_mental_command[1])
        self.storeDatabase_AttemptsTable(self.getUserName(), self.login_attempts, self.successful_login_attempts)
        self.l = 'login successful'
      else:
        
        self.login_attempts += 1
        self.successful_login_attempts += 0
        print('-ve' ,self.login_attempts)
        print('-ve',self.successful_login_attempts)
        
        
        self.storeDatabase_AttemptsTable(self.getUserName(), self.login_attempts, self.successful_login_attempts)
        self.l = 'login unsuccessful'
        
    return self.l
  
  """ 
  You need to have the database and tables created before running this
  """
  def storeDatabase_PerformanceTable(self, action, score):
        print("Connecting to Database...")
        
        db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Aniruddha",
                database="DATAS" # This database name is the same for both storeDatabase functions
        )
        print(db_connection)
        
        # creating database_cursor to perform SQL operation
        db_cursor = db_connection.cursor()
        
        """ 
        TODO: Important note: INSERT INTO -string- needs to be updated manually for every participant 
        """
        
        db_cursor.execute(f"INSERT INTO {self.entered_name}_Performance VALUES (%s, %s)", (action, score))
        print(self.entered_name)
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        print("Stored in the database")  
  
  """ 
  You need to have the database and tables created before running this
  """
  def storeDatabase_AttemptsTable(self, username, login_attempts, successful_login_attempts):
        print("Connecting to Database...")
        
        db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Aniruddha",
                database="DATAS"
        )
        print(db_connection)
        
        # creating database_cursor to perform SQL operation
        db_cursor = db_connection.cursor()
        
        """ 
        TODO: Important note: INSERT INTO -string- needs to be updated manually for every participant 
        """
        
        db_cursor.execute(f"INSERT INTO {self.entered_name}_Attempts VALUES (%s, %s, %s)", (username, login_attempts, successful_login_attempts))
        
        db_connection.commit()
        print(db_cursor.rowcount, "Record Inserted")
        print("Stored in the database") 
    
  """
  TODO: Need to test this get function, it should return the username entered by the user. It should work, because we are getting the user name before subscribe is called
  """
  def getUserName(self):
     return self.entered_name
  
  def attempts(self, l):
      db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Aniruddha",
                database="DATAS"
        )
      print(db_connection)
        
        # creating database_cursor to perform SQL operation
      db_cursor = db_connection.cursor()
        
       
      """ 
      TODO: Important note: INSERT INTO -string- needs to be updated manually for every participant 
      """
      db_cursor.execute(f"INSERT INTO {self.entered_name}_LOGINS VALUES (%s, %s)", (self.getUserName(), self.l))
        
      db_connection.commit()
      print(db_cursor.rowcount, "Record Inserted")
      print("Stored in the database") 
        
      
          
    
  def ui(self):
    
    self.root = Tk()
    self.root.configure(background = 'green')
    self.root.title('BCI authentication')

    Label(self.root, text='Name').grid(row=0) 
    
    e1 = Entry(self.root) 
    e1.grid(row=0, column=1)
   
  

    def click():
      
      self.subscribe(['com'])
      
      
      Label(self.root, text= self.l ).grid(row=2)
      self.attempts(self.l)
    
    def loading():
      invalid_profile =  {
          "error": {
          "code": -32031,
          "message": "Invalid Profile Name."
          },
              "id": 1,
              "jsonrpc": "2.0"
      }
      
      self.entered_name = e1.get()
      
#      self.load_profile(self.entered_name)
      if self.load_profile(self.entered_name) == invalid_profile:
        Label(self.root, text= 'Invalid Profile Name' ).grid(row=2, column = 5)
      else:
        Label(self.root, text= 'Profile is successfully loaded' ).grid(row=2, column = 5)
        
    def unloading():
      self.unload_profile('')
      Label(self.root, text= 'Profile is successfully unloaded' ).grid(row=6, column = 10)
    
    def refresh():
        Label.grid_forget(self.root)
        e1.delete(first=0,last=100)
    
    def creating():
        self.name = e1.get()
        print('name : ', self.name)
        self.db = mysql.connector.connect(
   host="localhost",
  user="root",
  passwd="Aniruddha",     
  database = 'DATAS'
       )
        self.mycursor = self.db.cursor()
        try:
            self.mycursor.execute(f"CREATE TABLE {self.name}_PERFORMANCE (action VARCHAR(50), score FLOAT )")
            self.mycursor.execute(f"CREATE TABLE {self.name}_attempts (name VARCHAR(50) , total_login_attempts INT, successful_login_attempts INT)")
            self.mycursor.execute(f"CREATE TABLE {self.name}_LOGINS (name VARCHAR(50), message VARCHAR(50))")
            Label(self.root, text= 'tables created!').grid(row=6, column = 10)
        except  Exception:
             Label(self.root, text= 'tables already created!').grid(row=6, column = 10)
            
    load = Button(self.root, text = 'load', width = 10, command = loading).place(x = 300, y = 20)
    unload = Button(self.root, text = 'unload', width = 10, command = unloading).place(x = 300, y = 50)
    create = Button(self.root, text = 'create', width = 10, command = creating).place(x = 300, y = 80) 
    clear = Button(self.root, text = 'clear', width = 10, command = refresh).place(x = 300, y = 110)
    b = Button(self.root, text = 'password', width = 10, command = click).place(x = 100, y = 50)


    self.root.mainloop()



