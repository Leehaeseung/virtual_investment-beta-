import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import time
from threading import Thread

# 공유 변수
current_price = None

def get_stock_price(symbol):
    try:
        stock_data = yf.download(symbol, start=datetime.now(), end=datetime.now())
        if stock_data.empty:
            raise Exception(f'No price data found for {symbol}. The symbol may be delisted.')
        return stock_data['Close'].iloc[-1]
    except Exception as e:
        st.error(f"Error retrieving stock price: {e}")
        return None

def update_prices():
    global current_price
    while True:
        stock_price = get_stock_price('005930.KS')  # 삼성전자의 종목 코드
        if stock_price is not None:
            current_price = stock_price
            st.write(f'Updated Stock Price: {current_price}')
        time.sleep(10)  # 10초 간격으로 주가 업데이트

# 백그라운드 스레드에서 update_prices() 함수 실행
update_thread = Thread(target=update_prices)
update_thread.start()

st.title('Stock Price Tracker')

# 주가를 표시하는 부분
st.header('Stock Symbol: 005930.KS')  # 삼성전자의 종목 코드
st.write(f'Current Stock Price: {current_price}')
