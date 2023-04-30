from dotenv.main import load_dotenv
import os
import telebot
from opt_chain import *
import threading
import time
import schedule
import json


load_dotenv()
API_KEY = os.environ['API_KEY']

bot = telebot.TeleBot(API_KEY)

def currentTime():
    current_time = time.strftime("%I:%M:%S %p", time.localtime())
    return current_time


def currentPCR(iname):
    if iname == "nf":
        strikeprice = strike_price("nf")
        url = url_nf
        step = 50
    if iname == "bnf":
        strikeprice = strike_price("bnf")
        url = url_bnf
        step = 100
    if iname == "fnf":
        strikeprice = strike_price("fnf")
        url = url_fnf
        step = 50
    _, CE_oi_Total , _ = CE(url, strikeprice, step)
    _, PE_oi_Total , _ = PE(url, strikeprice, step)
    PCR = round((PE_oi_Total/CE_oi_Total), 2)
    return PCR



def logPCR():
    cT = currentTime()
    def nfPCR():
        pcr = str(currentPCR("nf"))
        x = {
            cT : pcr
        }
        with open ("nf.json", "r") as f:
            jsondata = json.load(f)
            jsondata.update(x)
        with open ("nf.json", "w") as f:
            json.dump(jsondata, f, indent=4)


    def bnfPCR():
        pcr = str(currentPCR("bnf"))
        x = {
            cT : pcr
        }
        with open ("bnf.json", "r") as f:
            jsondata = json.load(f)
            jsondata.update(x)
        with open ("bnf.json", "w") as f:
            json.dump(jsondata, f, indent=4)
    def fnfPCR():
        pcr = str(currentPCR("fnf"))
        x = {
            cT : pcr
        }
        with open ("fnf.json", "r") as f:
            jsondata = json.load(f)
            jsondata.update(x)
        with open ("fnf.json", "w") as f:
            json.dump(jsondata, f, indent=4)
    tf1 = threading.Thread(target=nfPCR, daemon=True)
    tf2 = threading.Thread(target=bnfPCR, daemon=True)
    tf3 = threading.Thread(target=fnfPCR, daemon=True)
    tf1.start()
    tf2.start()
    tf3.start()

# schedule.every(5).seconds.do(logPCR)
schedule.every(15).minutes.do(logPCR)
def log15():
    while True:
        schedule.run_pending()
        time.sleep(1)
t1 = threading.Thread(target=log15, daemon=True)
t1.start()


        
def sendPCR(iname):
    curr_time = []
    pcr = []
    if iname == "nf":
        with open ("nf.json", "r") as f:
            jsondata = json.load(f)
            invertedjsondata = dict(reversed(list(jsondata.items())))
            for i in range(24):
                pairs = list(invertedjsondata.items())[i]
                curr_time.append(pairs[0])
                pcr.append(pairs[1])

    if iname == "bnf":
        with open ("bnf.json", "r") as f:
            jsondata = json.load(f)
            invertedjsondata = dict(reversed(list(jsondata.items())))
            for i in range(24):
                pairs = list(invertedjsondata.items())[i]
                curr_time.append(pairs[0])
                pcr.append(pairs[1])

    if iname == "fnf":
        with open ("fnf.json", "r") as f:
            jsondata = json.load(f)
            invertedjsondata = dict(reversed(list(jsondata.items())))
            for i in range(24):
                pairs = list(invertedjsondata.items())[i]
                curr_time.append(pairs[0])
                pcr.append(pairs[1])

    return curr_time, pcr



@bot.message_handler(commands = ["start"])
def greet(message):
    reply = """
This Bot allows you to get vital information from NSE Option Chain.
Reply with /help to get a list of all the commands."""
    bot.reply_to(message, reply)


@bot.message_handler(commands = ["help"])
def greet(message):
    reply = """
/Nifty50 for Support and Resistance Values of Nifty 50.
/BankNifty for Support and Resistance Values of Bank Nifty.
/FinNifty for for Support and Resistance Values of Fin Nifty.
/PCR for current PCR value.
/Nifty50PCRTrend for change in NIFTY 50 PCR over time.
/BankNiftyPCRTrend for change in BANK NIFTY PCR over time.
/FinNiftyPCRTrend for change in FIN NIFTY PCR over time."""
    bot.reply_to(message, reply)


@bot.message_handler(commands = ["Nifty50"])
def greet(message):
    nf_strike_price = strike_price("nf")
    expiry, _, support = CE(url_nf, nf_strike_price, 50)
    _, _, resistance = PE(url_nf, nf_strike_price, 50)
    reply = f"""
Contract Expiry Date : {expiry}
NIFTY 50 Nearest Strike Price : {nf_strike_price}
Major Support : {support}
Major Resistance : {resistance}"""
    bot.reply_to(message, reply)


@bot.message_handler(commands = ["BankNifty"])
def greet(message):
    bnf_strike_price = strike_price("bnf")
    expiry, _, support = CE(url_bnf, bnf_strike_price, 100)
    _, _, resistance = PE(url_bnf, bnf_strike_price, 100)
    reply = f"""
Contract Expiry Date : {expiry}
BANK NIFTY Nearest Strike Price : {bnf_strike_price}
Major Support : {support}
Major Resistance : {resistance}"""
    bot.reply_to(message, reply)


@bot.message_handler(commands = ["FinNifty"])
def greet(message):
    fnf_strike_price = strike_price("fnf")
    expiry, _, support = CE(url_fnf, fnf_strike_price, 50)
    _, _, resistance = PE(url_fnf, fnf_strike_price, 50)
    reply = f"""
Contract Expiry Date : {expiry}
FIN NIFTY Nearest Strike Price : {fnf_strike_price}
Major Support : {support}
Major Resistance : {resistance}"""
    bot.reply_to(message, reply)


@bot.message_handler(commands = ["PCR"])
def greet(message):
    nf = currentPCR("nf")
    bnf = currentPCR("bnf")
    fnf = currentPCR("fnf")
    reply = f"""
Current PCR is as Follows:
NIFTY 50 : {nf}
BANK NIFTY : {bnf}
FIN NIFTY : {fnf}"""
    bot.reply_to(message, reply)


@bot.message_handler(commands = ["Nifty50PCRTrend"])
def greet(message):
    currTime, pcr = sendPCR("nf")
    reply = f"""
The PCR change is given in 15 minutes time frame with lastest on TOP
{currTime[0]}     :     {pcr[0]}
{currTime[1]}     :     {pcr[1]}
{currTime[2]}     :     {pcr[2]}
{currTime[3]}     :     {pcr[3]}
{currTime[4]}     :     {pcr[4]}
{currTime[5]}     :     {pcr[5]}
{currTime[6]}     :     {pcr[6]}
{currTime[7]}     :     {pcr[7]}
{currTime[8]}     :     {pcr[8]}
{currTime[9]}     :     {pcr[9]}
{currTime[10]}     :     {pcr[10]}
{currTime[11]}     :     {pcr[11]}
{currTime[12]}     :     {pcr[12]}
{currTime[13]}     :     {pcr[13]}
{currTime[14]}     :     {pcr[14]}
{currTime[15]}     :     {pcr[15]}
{currTime[16]}     :     {pcr[16]}
{currTime[17]}     :     {pcr[17]}
{currTime[18]}     :     {pcr[18]}
{currTime[19]}     :     {pcr[19]}
{currTime[20]}     :     {pcr[20]}
{currTime[21]}     :     {pcr[21]}
{currTime[22]}     :     {pcr[22]}
{currTime[23]}     :     {pcr[23]}
"""
    bot.reply_to(message, reply)

@bot.message_handler(commands = ["BankNiftyPCRTrend"])
def greet(message):
    currTime, pcr = sendPCR("bnf")
    reply = f"""
The PCR change is given in 15 minutes time frame with lastest on TOP
{currTime[0]}     :     {pcr[0]}
{currTime[1]}     :     {pcr[1]}
{currTime[2]}     :     {pcr[2]}
{currTime[3]}     :     {pcr[3]}
{currTime[4]}     :     {pcr[4]}
{currTime[5]}     :     {pcr[5]}
{currTime[6]}     :     {pcr[6]}
{currTime[7]}     :     {pcr[7]}
{currTime[8]}     :     {pcr[8]}
{currTime[9]}     :     {pcr[9]}
{currTime[10]}     :     {pcr[10]}
{currTime[11]}     :     {pcr[11]}
{currTime[12]}     :     {pcr[12]}
{currTime[13]}     :     {pcr[13]}
{currTime[14]}     :     {pcr[14]}
{currTime[15]}     :     {pcr[15]}
{currTime[16]}     :     {pcr[16]}
{currTime[17]}     :     {pcr[17]}
{currTime[18]}     :     {pcr[18]}
{currTime[19]}     :     {pcr[19]}
{currTime[20]}     :     {pcr[20]}
{currTime[21]}     :     {pcr[21]}
{currTime[22]}     :     {pcr[22]}
{currTime[23]}     :     {pcr[23]}
"""
    bot.reply_to(message, reply)

@bot.message_handler(commands = ["FinNiftyPCRTrend"])
def greet(message):
    currTime, pcr = sendPCR("fnf")
    reply = f"""
The PCR change is given in 15 minutes time frame with lastest on TOP
{currTime[0]}     :     {pcr[0]}
{currTime[1]}     :     {pcr[1]}
{currTime[2]}     :     {pcr[2]}
{currTime[3]}     :     {pcr[3]}
{currTime[4]}     :     {pcr[4]}
{currTime[5]}     :     {pcr[5]}
{currTime[6]}     :     {pcr[6]}
{currTime[7]}     :     {pcr[7]}
{currTime[8]}     :     {pcr[8]}
{currTime[9]}     :     {pcr[9]}
{currTime[10]}     :     {pcr[10]}
{currTime[11]}     :     {pcr[11]}
{currTime[12]}     :     {pcr[12]}
{currTime[13]}     :     {pcr[13]}
{currTime[14]}     :     {pcr[14]}
{currTime[15]}     :     {pcr[15]}
{currTime[16]}     :     {pcr[16]}
{currTime[17]}     :     {pcr[17]}
{currTime[18]}     :     {pcr[18]}
{currTime[19]}     :     {pcr[19]}
{currTime[20]}     :     {pcr[20]}
{currTime[21]}     :     {pcr[21]}
{currTime[22]}     :     {pcr[22]}
{currTime[23]}     :     {pcr[23]}
"""
    bot.reply_to(message, reply)

bot.polling()


# Ends here