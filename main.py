# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 00:31:50 2019

@author: Aniruddha Tarodekar
"""

from authenticate1_v2 import Cortex1


def start(cortex):
  
    
  print('get cortex info')
  cortex.get_cortex_info()
  
  print('has_access_right')
  cortex.has_access_right()
  
  print('request access')
  cortex.request_access()
  
  print('authorize')
  cortex.authorize()
  
  print('query headsets')
  cortex.query_headset()
  
  
#  print('session create')
#  cortex.create_session("open","INSIGHT-5A688FB1")
  
  
  print('gui')
  cortex.ui()
  
  print('disconnect headset')
  #cortex.
  
  print('close session')
  cortex.close_session()
  
  







url = "wss://localhost:6868"
user = {
	'clientId':'7qMdFUjo8jXXN2dXrhqUMgjL6jdn2Y2p38hSM3Vv', 
    
    'clientSecret': 'dsHNx4LxxJCkOHYijsHXBBtvMquvuRVqcuwacsxc4kAaVypwVqdWmc3UFoVbk6vEhirPp96GdgbrUQKhdvQLfESgMTvSWlHVhu9CAKHh6PIeL3rIzlM6kWXp6Jq6epzw'

	,"number_row_data" : 100     # change this value to control the number of times the loop is ran
    }
cortex = Cortex1(url, user)
start(cortex)
