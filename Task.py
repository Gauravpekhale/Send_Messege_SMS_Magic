import pandas as pd
import winsound
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
import urllib.request
from datetime import date,datetime
import pytz
import re


def connected():
        try:
            urllib.request.urlopen('http://google.com') 
            return True
        except:
            return False
            
def send_mail(User_Email,message):
    if(not connected()):
        return "Connection Error : No internet Available !"
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if(not re.fullmatch(regex, User_Email)):
        return "Invalid Email ID"
    try:

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls(context=ssl.create_default_context())
        server.login("gaurav.arun.pekhale@gmail.com","ewxibdzywvohgwxf")

        msg = MIMEMultipart()

        msg['Subject'] ="SMS Magic Assingment"
        msg['From'] = 'gaurav.arun.pekhale@gmail.com'
        msg['To'] = User_Email
        
        msg.attach(MIMEText(message, "plain"))
        
        server.send_message(msg)
        winsound.Beep(900,700)
        return "Success"
        
    except Exception as E:
        return str(E)

def get_schedule(date_str):
    if str(date_str)=="" or len(str(date_str))==0:
        return True
    return (datetime.strptime(str(date_str),'%d/%m/%y').date()==(date.today()))

def SMS_Check( phone , msg , Country):
    if len(str(phone)) != 10 :
        return "Invalid Number"
    if len(msg) < 1 and len(msg) >= 160 :
        return "Invalid message"

    if Country=='INDIA':
        timezone=pytz.timezone('Asia/Kolkata')
    
    elif Country=='USA':
        timezone=pytz.timezone('US/Central')
        
    else :
        return "Invalid Country"

    Current_time=datetime.now(timezone).time()
    now=datetime.now(timezone).time()
    limit_time1=now.replace(hour=10,minute=0,second=0,microsecond=0)
    limit_time2=now.replace(hour=17,minute=0,second=0,microsecond=0)

    if Current_time > limit_time1 and Current_time < limit_time2 :
        return True
    else :
        return False  

def send_sms(phone, msg):
    import requests

    url = "https://api.txtbox.in/v1/sms/send"

    payload = "mobile_number="+str(phone)+"+&sms_text="+msg+"helloWorld&sender_id=SMS_Magic"
    headers = {
    'apikey': "9f81fddf27be1aa3e73a0619392cbc0c",
    'content-type': "application/json",
    'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.text
    
    

def main():
    df=pd.read_csv("sample.csv")
    df.drop_duplicates(inplace=True, keep="first")
    with open('log.txt',"w") as fp :
        for date_str,msg,email,phone, country in zip(df["Schedule On"],df["Message"],df['Email'],df["Phone"],df["Country"]):
            if(get_schedule(date_str)):
                response_email=send_mail(User_Email=email,message=msg)
                response_sms=SMS_Check(phone,msg,country)
                if response_sms==True :
                    response_sms = send_sms(phone,msg)
                elif response_sms==False :
                    continue
                
                fp.write("\n***********   Email  ****************\n")
                fp.write(response_email)
                fp.write("\n***********   SMS    ****************\n")
                fp.write(str(response_sms))
    fp.close()



    


if __name__=="__main__":
    main()