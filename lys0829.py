import pyupbit 
import pandas 
import datetime 
import time

access = ""
secret = ""

# RSI get start
def rsi(ohlc: pandas.DataFrame, period: int = 14): 
    delta = ohlc["close"].diff() 
    ups, downs = delta.copy(), delta.copy() 
    ups[ups < 0] = 0 
    downs[downs > 0] = 0

    AU = ups.ewm(com = period-1, min_periods = period).mean() 
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean() 
    RS = AU/AD

    return pandas.Series(100 - (100/(1 + RS)), name = "RSI")

# coin list
coinlist = ["KRW-BCHA", "KRW-ADA", "KRW-FLOW", "KRW-BTC", "KRW-XRP", "KRW-SAND", "KRW-BCG", "KRW-BSV"]  
lower27 = [] 
higher72 = [] 


# auto trade start
upbit = pyupbit.Upbit(access, secret)
print("Auto angel start")

#get
def buy(coin): 
    money = upbit.get_balance("KRW") 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    total = amount * cur_price 
    h = 2000000 # get unit
    w = 0.97
    if total < h * w : 
        res = upbit.buy_market_order(coin, h) 
    else : 
        pass 
    return

#sell
def sell(coin): 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    total = amount * cur_price 
    ys = 1.011 #target gain
    h = 2000000 # get unit
    if h * ys < total < h * 1.5 : 
        res = upbit.sell_market_order(coin, amount) 
    elif h * 2 * ys < total < h * 3 : 
        res = upbit.sell_market_order(coin, amount * 0.5) 
    else : 
        pass
    return

    # initiate 
for i in range(len(coinlist)): 
    lower27.append(False) 
    higher72.append(False)

while(True): 
    for i in range(len(coinlist)): 
        data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute3") 
        now_rsi = rsi(data, 14).iloc[-1] 
        print("coin name: ", coinlist[i]) 
        print("time: ", datetime.datetime.now()) 
        print("RSI :", now_rsi) 
        print() 
        if now_rsi <= 26 : 
            lower27[i] = True 
        elif now_rsi >= 29 and lower27[i] == True: 
            buy(coinlist[i]) 
            lower27[i] = False

        elif now_rsi >= 72 :
            higher72[i] = True
        elif now_rsi < 68 and higher72[i] == True: 
            sell(coinlist[i]) 
            higher72[i] = False

    time.sleep(5)