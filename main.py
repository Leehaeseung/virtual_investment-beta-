
import yfinance as yf
import plotly.graph_objs as go
import streamlit as st
from torch import layout
from streamlit_option_menu import option_menu
import time
import requests
from bs4 import BeautifulSoup
import requests
import recent_price as rp
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
from threading import Thread
st.set_page_config(layout="wide")
#변수선언
INIT_KRW=100000000
stock_keys = {
    "삼성전자": "samsung",
    "비트코인": "bitcoin",
    "S&P500": "SP500",
    "LG전자": "lg",
    "HMM": "hmm"
    # 나머지 주식에 대한 매핑도 추가
}
#현재가#
# 세션 상태에 'usd' 키가 없으면 초기화
if 'usd' not in st.session_state:
    st.session_state.usd = INIT_KRW
if 'samsung' not in st.session_state:
    st.session_state.samsung=0
if 'bitcoin' not in st.session_state:    
    st.session_state.bitcoin=0
if 'SP500' not in st.session_state:
    st.session_state.SP500=0
if 'lg' not in st.session_state:
    st.session_state.lg=0
if 'hmm' not in st.session_state:
    st.session_state.hmm=0
    
if 'new_price' not in st.session_state:
    st.session_state['new_price'] = {}

def update_prices():
    samsung = rp.get_samsung_stock_price_naver()
    lg = rp.get_lg_stock_price_naver()
    hmm = rp.get_hmm_stock_price_naver()
    bitcoin = rp.get_bitcoin_price_naver()
    sp500_dollar = rp.get_sp500_index_from_naver()
    dollar=rp.get_dollar_price_naver()
        # 쉼표 제거 및 float 변환
    sp500_dollar_float = float(sp500_dollar.replace(',', ''))
    dollar_float = float(dollar.replace(',', ''))
    # 곱셈 연산 수행
    sp500 = sp500_dollar_float * dollar_float
    # 결과를 포맷팅하여 문자열로 변환
    sp500_formatted = f"{sp500:,.2f}"
    st.session_state['new_price'] = {'삼성전자': samsung, '비트코인': bitcoin, 'S&P500': sp500_formatted, 'LG전자': lg, 'HMM': hmm}
# 총 자산 계산 함수


col1, col2 = st.columns([5,2])
def get_data(period):  #불변#
    dictionary={'1일':'1d','5일':'5d','1달':'1mo','3달':'3mo','1년':'1y','2년':'2y','5년':'5y','최대':'max'}
    interval={'1일':'1m','5일':'1m','1달':'1h','3달':'1h','1년':'1d','2년':'1d','5년':'1d','최대':'1d'}
    return yf.download(tickers=NAME,period=dictionary[period], interval=interval[period])

def num(NAME,select,samsung,bitcoin,lg,hmm,sp500): #종목이름#
    price_dict = {'삼성전자':samsung,'비트코인':bitcoin,'S&P500':sp500,'LG전자':lg,'HMM':hmm} #종목추가#
    result=yf.Ticker(NAME)
    result_info=result.info
    name=result_info["shortName"]
    currency=result_info["currency"]
    currentPrice=str(price_dict[select])+"KRW"
    
    return name,currency,currentPrice,price_dict
with st.sidebar:
    select=st.selectbox("종목",("삼성전자","LG전자","HMM","비트코인","S&P500"))        #종목이름#
    period=st.selectbox("뭐임마",("1일","5일","1달","3달","1년","2년","5년","최대"),)
    def calculate_total_assets():
        total_stock_value = sum(float(st.session_state['new_price'][stock].replace(',', '')) * float(st.session_state[stock_keys[stock]]) for stock in stock_keys)
        total_assets = st.session_state.usd + total_stock_value
        return total_assets

    # 가격 업데이트 버튼
    if st.button('가격 업데이트'):
        update_prices()
        total_assets = calculate_total_assets()  # 총 자산 계산
        st.write("총 자산: " + f'{total_assets:,.2f}' + "원")  # 총 자산 출력

    update_prices()


#홈페이지 생성부분, 종목추가: #

price_title = col1.empty()  # Placeholder for updating price
price = st.session_state['new_price'][select]
if st.session_state['new_price']:
    price = st.session_state['new_price'][select]
    price_title.write(f"현재가: {price}"+"원")
    
dic={'삼성전자':'005930.KS','비트코인':'BTC-USD','S&P500':'^GSPC','LG전자':'066570.KS','HMM':'011200.KS'}#종목코드#
NAME=dic[select]    
data=get_data(period)

with col1:
    name,currency,currentPrice,price_dict=num(NAME,select,rp.samsung,rp.bitcoin,rp.lg,rp.hmm,rp.sp500)#종목 가격#
    fig = go.Figure([go.Scatter(x=data.index, y=data['Close'])])
    fig.update_layout(title_text=select,height=360)
    st.plotly_chart(fig,use_container_width=True)

with col2:
    st.header('TRADING')
    st.write("종목: "+select)
    wallet=col2.empty()
    your_stocks=col2.empty()   
    input_price=col2.empty() 
    wallet.write("당신의 지갑:"+f'{st.session_state.usd:,.2f}'+"원")
    your_stocks.write(
    "니꺼:<br>삼성:" + str(st.session_state.samsung) +
    "<br>비트코인:" + str(st.session_state.bitcoin) +
    "<br>SP500:" + str(st.session_state.SP500) +
    "<br>LG전자" + str(st.session_state.lg),
    unsafe_allow_html=True
)


    stocks=float(st.number_input(label="수량 (최소단위:0.1)",min_value=0.0,step=0.1))
    st.markdown("""
    <style>
    .small-font {
        font-size:10px;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="small-font">많이 누르면 페이지가 멈춥니다.</p>', unsafe_allow_html=True)
    col21,col22=st.columns([1,1])
    with col21:
        buy_price=float(price.replace(',',''))*float(stocks)
        
        input_price.write("금액:"+f"{buy_price:,.2f}"+"원")
        if st.session_state.usd >= buy_price:
            if st.button("buy"):
                stock_key = stock_keys[select]  # 'select'를 st.session_state 키로 변환
                st.session_state[stock_key] += stocks  # st.session_state 업데이트
                st.session_state.usd -= buy_price
                wallet.write("당신의 지갑:" + f'{st.session_state.usd:,.2f}' + "원")
                # 업데이트된 your_stocks 출력
                your_stocks.write(
                    "니꺼:<br>삼성:" + str(st.session_state.samsung) +
                    "<br>비트코인:" + str(st.session_state.bitcoin) +
                    "<br>SP500:" + str(st.session_state.SP500) +
                    "<br>LG전자" + str(st.session_state.lg),
                    unsafe_allow_html=True
        )

        else:
            st.button("욕심부리지마라")
    with col22:
        sell_price=float(price.replace(',',''))*float(stocks)
        if st.session_state[stock_keys[select]] >= stocks:
            if st.button("sell"):
                stock_key = stock_keys[select]  # 'select'를 st.session_state 키로 변환
                st.session_state[stock_key] -= stocks  # st.session_state 업데이트
                st.session_state.usd += sell_price
                wallet.write("당신의 지갑:" + f'{st.session_state.usd:,.2f}' + "원")
                # 업데이트된 your_stocks 출력
                your_stocks.write(
                    "니꺼:<br>삼성:" + str(st.session_state.samsung) +
                    "<br>비트코인:" + str(st.session_state.bitcoin) +
                    "<br>SP500:" + str(st.session_state.SP500) +
                    "<br>LG전자" + str(st.session_state.lg),
                    unsafe_allow_html=True
        )
        else:
            st.button("수량부족")


