import httpx;
import asyncio;
import logging as log;
import json as jsn;

import BigBasketMeta as meta;
from http.cookiejar import CookieJar ;
class BigBasket:

    def __init__(self,phonenumber=00000000):
        self.phonenumber = phonenumber;
        self.OTP = 000000000;
        self.headerlogin = meta.headerlogin
        #self.headerBanner = meta.headerBanner
        self.headerlogin = meta.headerlogin;
        self.clientAsync = httpx.AsyncClient(http2=True);
        self.cookie= CookieJar({});
        self.OTPSend =False;
        self.token="";
        self.city="";
        
        return None;
    
    async def __CallForOTP(self):
        async with self.clientAsync as client:
            r = await client.get(meta.InitURL,headers=meta.headeroriginal)
            
            cookies = client.cookies;
            headerloginCopy= meta.headerlogin
            headerloginCopy["x-csrftoken"] = dict(cookies).get("csrftoken");
            self.token = dict(cookies).get("csrftoken");  

            await asyncio.sleep(7);            
            payload=jsn.dumps({"identifier":str(self.phonenumber)} );
            try:
                r = await client.post(meta.OTPURL,data=payload,headers = headerloginCopy)
                if(r.status_code == 200  and ("OTP sent successfully" in r.content.decode())):#{"message": "OTP sent successfully", "show_message": true}
                    print("OTP successfully requested");
                    self.OTPSend= True;
                    self.cookie = client.cookies;
                else:
                    print("Error while requesting OTP");
            except Exception as e:
                print("Error occured while requesting OTP");  

    async def __LoginAndFetch(self):
        async with self.clientAsync as client:
            try:
                self.clientAsync = httpx.AsyncClient(http2=True,cookies=self.cookie);
                headerloginCopy= meta.headerlogin;
                headerloginCopy["x-csrftoken"]=self.token;
                
                ##### Login using OTP #######
                payloadLogin=jsn.dumps({"mobile_no":str(self.phonenumber),"mobile_no_otp":str(self.OTP)})
                r = await client.post(meta.LoginURL,data=payloadLogin,headers = headerloginCopy)
                ##### Login using OTP #######

                ####################################################################
                ##### Change accept document type from application/json to all
                ##### Calling this token URL to generate the CSRF token used post
                ##### login
                ####################################################################
                headerloginCopy["accept"]="*/*";
                r = await client.get(meta.tokenURL,headers = headerloginCopy);

                cookies = client.cookies;   
                headerloginCopy["x-csrftoken"] = dict(cookies).get("csrftoken");

                ######################################################################
                ######  The Bakset URL is called to intialize the checkout Basket on the
                ######  Bigbasket server
                ######################################################################

                headerloginCopy["accept"]="application/json, text/plain, */*";
                r = await client.get(meta.BasketURL,headers = headerloginCopy);

                
                
                ######################################################################
                ######### Get all addresses  for the account logged in ###############
                ######################################################################
                
                r = await client.get(meta.AddressURL,headers = headerloginCopy);                
                addressdict = r.json()
                print("Choose the address you want to check");
                
                addresses = addressdict.get("response").get("addresses");
                
                #######################################################################
                ######### Print all addresses for user to choose from #################
                #######################################################################

                for address in addresses:
                    print("Press %s for the address %s %s at the address %s" %(address['id'],address['first_name'],address['last_name'],address['address_2']))
                

                #######################################################################
                ######### Ask for user input for the address that needs ###############
                #########           to be checked                       ###############
                #######################################################################
                chosenaddress = input("Enter your choice")

                
                for address in addresses:
                    if address.get("id") == chosenaddress:
                        self.city=address.get("city_id")

                payloadLogin=jsn.dumps({"city_id":str(self.city),"addr_id":chosenaddress})
                
                r = await client.post(meta.setCityURL,data=payloadLogin,headers = headerloginCopy)

                payloadLogin=jsn.dumps({"addr_id":chosenaddress})
                
                r = await client.post(meta.LocationURL,data=payloadLogin,headers = headerloginCopy)
                
                if  "\"status\": \"failure\"" in r.content.decode():    
                    print("The slot is not available")
                else:
                    print("Slots available")


            except Exception  as e:
                print(e);
                
            
            
            



    async def __LoginAndFetchController(self):
        await self.__LoginAndFetch();

    async def __OTPGenController(self):
            await self.__CallForOTP(); 


#####################################################################
            
        


    
    def  generate_OTP(self):
        print('Requesting OTP');
        asyncio.run(self.__OTPGenController());

    def  LoginToAccount(self,OTP):
        self.OTP = OTP;
        asyncio.run(self.__LoginAndFetchController());

    
    




    
    

    
        
        