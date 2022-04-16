from email import message
import sys
import pyupbit

# 현재가 조회
def get_current_price(up, coin_name):
    message=''
    result='none'
    try: result=pyupbit.get_current_price(coin_name)
    except: message="{}".format(sys.exc_info())

    # error message check
    try: message=result['error']['message']
    except: 
        message='good' if message=='' else message
    return message, result

# 코인별 잔고 조회
def get_balances(up, coin_name):
    message=''
    result='none'
    trade_coin='none'
    buy_amt=0
    buy_price=0
    try:
        trade_coin=coin_name.split('-')[1]
        result=up.get_balances()
    except:
        message="{}".format(sys.exc_info())
    
    try: #error mess
        # age check
        message = result[0]['error']['message']
    except: #no error message -> normal state
        if message == '':
            message = 'good'

    if message=='good':
        for temp in result:
            if temp['currency'] == trade_coin:
                buy_amt=temp['balance']
                buy_price=temp['avg_buy_price']
    return message, buy_amt, buy_price

#주문상태 조회
def get_order_status(up, coin_name, uuid):
    message=''
    state='none' # wait : 미체결, done : 체결
    side='none'
    price='none'
    amt='none'
    result={'state':'none','side':'none','price':'0','volume':'0'}

    try: result=up.get_order(uuid)
    except: message="{}".format(sys.exc_info())

    # error msg check
    try: message=result['error']['message']
    except:# 에러메시지가 없으면 잘되었다는 상황이므로
        if message=='':
            message="good"
            state=result['state']
            side=result['side']
            price=result['price']
            volume=result['volume']
    return message,state,price,amt

#지정가 매수
def buy_limit_order(up, coin_name, price, amt):
    message=''
    uuid='none'
    result={'uuid':''}

    try: result=up.buy_limit_order(coin_name, price, amt)
    except: message="{}".format(sys.exc_info())

    # error msg check
    try: message=result['error']['message']
    except:# 에러메시지가 없으면 잘되었다는 상황이므로
        if message=='':
            message='good'
            uuid=result['uuid']
    return message, uuid

#지정가 매도
def sell_limit_order(up, coin_name, price, amt):
    message=''
    uuid='none'
    result={'uuid':''}

    try: result=up.sell_limit_order(coin_name, price, amt)
    except: message="{}".format(sys.exc_info())

    # error msg check
    try: message=result['error']['message']
    except:# 에러메시지가 없으면 잘되었다는 상황이므로
        if message=='':
            message='good'
            uuid=result['uuid']
    return message, uuid

#시장가 매수
def buy_market_order(up, coin_name, price, amt):
    message=''
    uuid='none'
    result={'uuid':''}

    try: result=up.buy_market_order(coin_name, price, amt)
    except: message="{}".format(sys.exc_info())

    # error msg check
    try: message=result['error']['message']
    except:# 에러메시지가 없으면 잘되었다는 상황이므로
        if message=='':
            message='good'
            uuid=result['uuid']
    return message, uuid

#시장가 매도
def sell_market_order(up, coin_name, price, amt):
    message=''
    uuid='none'
    result={'uuid':''}

    try: result=up.sell_market_order(coin_name, price, amt)
    except: message="{}".format(sys.exc_info())

    # error msg check
    try: message=result['error']['message']
    except:# 에러메시지가 없으면 잘되었다는 상황이므로
        if message=='':
            message='good'
            uuid=result['uuid']
    return message, uuid

# 주문취소
def buy_market_order(up, uuid):
    message=''
    result={'uuid':''}

    try: result=up.cancel_order(uuid)
    except: message="{}".format(sys.exc_info())

    # error msg check
    try: message=result['error']['message']
    except:# 에러메시지가 없으면 잘되었다는 상황이므로
        if message=='':
            message='good'
            uuid=result['uuid']
    return message, uuid

# 전체 미체결 주문 취소
def cancel_all_order(up,coin_name):
    message=''
    uuid='none'
    result={'uuid':''}
    result_list=list()

    try: result=up.get_order(coin_name,state='wate')
    except: message="{}".format(sys.exc_info())

    # error msg check
    try: message=result['error']['message']
    except:# 에러메시지가 없으면 잘되었다는 상황이므로
        message='good'

    if message=='good':
        for result in result_list:
            try : result = up.cancel_order(result['uuid'])
            except: 
                message="{}".format(sys.exc_info())
                break

# 이익실현주문 (limit)
def take_profit(up, coin_name, buy_amt, buy_price, now_price, take_profit_rate):
    buy_price_tot = float(buy_amt)*float(buy_price) # 구매금액
    now_price_tot = float(buy_amt)*float(now_price) # 현재금액
    revenue_price = buy_price_tot * take_profit_rate # 이익 실현 금액
    message='not yet'
    uuid='none'

    if (now_price_tot - buy_price_tot) > revenue_price: #이익실현가 도달시 매도
        try:
            trade_price = "{:0.0{}f}".format(float(now_price),0) # 정수
            trade_amt="{:0.0{}f}".format(float(buy_amt),4) # 소수점 4자리
            message, uuid = sell_limit_order(up, coin_name, trade_price, trade_amt)
        except:
            message="{}".format(sys.exc_info())
    return message,uuid

#손실 최소화 주문 (limit)
def stop_loss(up, coin_name, buy_amt, buy_price, now_price, stop_loss_rate):
    buy_price_tot = float(buy_amt)*float(buy_price) # 구매금액
    now_price_tot = float(buy_amt)*float(now_price) # 현재금액
    stop_price = buy_price_tot * stop_loss_rate # 손실최소화 금액
    message='not yet'
    uuid='none'

    if (buy_price_tot - now_price_tot) > stop_price: #손실최소화 금액 도달시 매도
        try:
            trade_price = "{:0.0{}f}".format(float(now_price),0) # 정수
            trade_amt="{:0.0{}f}".format(float(buy_amt),4) # 소수점 4자리
            message, uuid = sell_limit_order(up, coin_name, trade_price, trade_amt)
        except:
            message="{}".format(sys.exc_info())
    return message,uuid