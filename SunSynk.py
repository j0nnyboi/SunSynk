
import sys
import requests
import json
from requests.auth import HTTPBasicAuth

class SunSynk(object):
    def __init__(self, username,password):

        self.user_email=username
        self.user_password=password


    def login(self):

        headers = {
            'Content-type':'application/json', 
            'Accept':'application/json'
            }

        payload = {
            "username": self.user_email,
            "password": self.user_password,
            "grant_type":"password",
            "client_id":"csp-web"
            }
        raw_data = requests.post('https://api.sunsynk.net/oauth/token', json=payload, headers=headers).json()
        # Your access token extracted from response
        if(raw_data['success'] == False):#check to make sure respones is succcesful
            print(raw_data)
            return
        
        self.bearer_token = ('Bearer '+ raw_data["data"]["access_token"])
        print("Your Token = %s" % self.bearer_token)
        self.Plants()

    def Plants(self):
        self.headers_and_token = {
            'Content-type':'application/json', 
            'Accept':'application/json',
            'Authorization': self.bearer_token
            }
        payload={"page": 1,
                    "limit":1
                }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/plants", params=payload, headers=self.headers_and_token)).json()
        self.plant_id = data_response['data']['infos'][0]['id']
        print('Your plant id: %s' % self.plant_id)
        self.Plant_Details()

        

    def Plant_Details(self):
        payload={"lan": "en"
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/plant/%s"%self.plant_id, params=payload, headers=self.headers_and_token)).json()
        #print(data_response)
        self.userID = (data_response['data']['master']['id'])
        print("userID = %s" %self.userID)
        self.inverters()
        return data_response
        
    def Plant_realtime(self):
        data_response = (requests.get("https://api.sunsynk.net/api/v1/plant/%s/realtime"%self.plant_id, headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def Plant_flow(self):
        data_response = (requests.get("https://api.sunsynk.net/api/v1/plant/energy/%s/flow"%self.plant_id, headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def Plant_inverter(self):
        data_response = (requests.get("https://api.sunsynk.net/api/v1/plant/%s/inverters"%self.plant_id, headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def Plant_status(self):
        data_response = (requests.get("https://api.sunsynk.net/api/v1/user/%s/plantCount"%self.userID, headers=self.headers_and_token)).json()
        print(data_response)
        return data_response
    
    def Day_Chart(self,date):
        payload={"date":str(date),#date in yyyy-MM-dd formate
            "lan": "en"
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/plant/energy/%s/day"%self.plant_id,params=payload, headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def Month_Chart(self,date):
        payload={"date":str(date),#date in yyyy-MM formate
            "lan": "en"
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/plant/energy/%s/month"%self.plant_id,params=payload, headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def Year_Chart(self,date):
        payload={"date":str(date),#date in yyyy formate
            "lan": "en"
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/plant/energy/%s/year"%self.plant_id,params=payload, headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def Total_Chart(self):
        payload={"lan": "en"
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/plant/energy/%s/total"%self.plant_id,params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response
    def Status_count(self):
        payload={"type": -1
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverters/count",params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def inverters(self):
        payload={"page": 1,
                 "limit": 20,
                 "type": -1,
                 "status":1,
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverters",params=payload,headers=self.headers_and_token)).json()
        #print(data_response)
        self.inverterSerial = data_response['data']['infos'][0]['sn']
        print("My Serial number = %s"% self.inverterSerial)
        

    def interters_realtime(self):
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/%s/realtime/output"%self.inverterSerial,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def interters_Day(self,date,column):
        payload={"date": str(date),#yyyy-mm-dd formate
                 "lan": "en",
                 "column": column,#vac1,vac2,vac3/iac1,iac2,iac3/fac/pac/p_total
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/%s/output/day"%self.inverterSerial,params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def interters_Month(self,date):
        payload={"date": str(date),#yyyy-mm formate
                 "lan": "en",
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/%s/month"%self.inverterSerial,params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def interters_Year(self,date):
        payload={"date": str(date),#yyyyformate
                 "lan": "en",
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/%s/year"%self.inverterSerial,params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response
    
    def interters_Total(self):
        payload={"lan": "en"
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/%s/total"%self.inverterSerial,params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def grid_realtime(self):
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/grid/%s/realtime"%self.inverterSerial,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def grid_Day(self,date):
        payload={"date": str(date),#yyyy-mm-dd formate
                 "lan": "en",
                 "Column":"pac"
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/grid/%s/day"%self.inverterSerial,params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def grid_Month(self,date):
        payload={"date": str(date),#yyyy-mm formate
                 "lan": "en",
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/grid/%s/month"%self.inverterSerial,params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def grid_Year(self,date):
        payload={"date": str(date),#yyyy formate
                 "lan": "en"
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/grid/%s/year"%self.inverterSerial,params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def grid_Total(self):
        payload={
                 "lan": "en",
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/grid/%s/total"%self.inverterSerial,params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def battery_realtime(self):
        payload={"lan": "en",
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/battery/%s/realtime"%self.inverterSerial,params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def battery_Day(self,date):
        payload={"date": str(date),#yyyy-mm-dd formate
                 "lan": "en",
                 "Column":"pac"
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/battery/%s/day"%self.inverterSerial,params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def battery_Month(self,date):
        payload={"date": str(date),#yyyy-mm formate
                 "lan": "en",
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/battery/%s/month"%self.inverterSerial,params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def battery_Year(self,date):
        payload={"date": str(date),#yyyy formate
                 "lan": "en"
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/battery/%s/year"%self.inverterSerial,params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def battery_Total(self):
        payload={
                 "lan": "en",
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/battery/%s/total"%self.inverterSerial,params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def load_realtime(self):
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/load/%s/realtime"%self.inverterSerial,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def load_Day(self,date):
        payload={"date": str(date),#yyyy-mm-dd formate
                 "lan": "en",
                 "Column":"pac"
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/load/%s/day"%self.inverterSerial,params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

    def load_Month(self,date):
        payload={"date": str(date),#yyyy-mm formate
                 "lan": "en",
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/load/%s/month"%self.inverterSerial,params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response
    def load_Year(self,date):
        payload={"date": str(date),#yyyy formate
                 "lan": "en"
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/load/%s/year"%self.inverterSerial,params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response
    
    def load_Total(self):
        payload={
                 "lan": "en",
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/inverter/load/%s/total"%self.inverterSerial,params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

        
    def event(self,types):
        payload={"sdate": str(Sdate),#yyyy-mm-dd formate
                 "edate": str(Edate),#yyyy-mm-dd formate
                 "type": types, #1info,2warning,3fault
                 "page":1,
                 "limit":20,
                 "lan":"en"
            }
        data_response = (requests.get("https://api.sunsynk.net/api/v1/event",params=payload,headers=self.headers_and_token)).json()
        print(data_response)
        return data_response

