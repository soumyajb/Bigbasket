
import os;  
import re;
import sys;
import requests;
sys.path.append(os.getcwd());




from Bigbasket import BigBasket;




if len(sys.argv)<2:
    print ("Usage : python3 Mainpython <phonenumber>");
else:
    newsession = BigBasket(sys.argv[1]);
    ''' Initialize a BigBasket Object with phonenumber'''

    newsession.generate_OTP()
    '''Send the OTP to the users mobile'''

    OTP=input("Please enter the OTP requested from BigBasket");
    newsession.LoginToAccount(OTP);

