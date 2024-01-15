import requests
from bs4 import BeautifulSoup
import time
import streamlit as st
def get_samsung_stock_price_naver():
    try:
        url = "https://finance.naver.com/item/main.nhn?code=005930"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 웹페이지에서 주식 가격을 가져오기
        price_element = soup.select_one("div.today span.blind")  # 네이버 금융 페이지 구조에 따라 조절해야 할 수 있음

        if price_element:
            return price_element.text
        else:
            print("Error: Could not retrieve stock price.")
            return None

    except Exception as e:
        print("Error:", e)
        return None
samsung=get_samsung_stock_price_naver()
def get_lg_stock_price_naver():
    try:
        url = "https://finance.naver.com/item/main.nhn?code=066570"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 웹페이지에서 주식 가격을 가져오기
        price_element = soup.select_one("div.today span.blind")

        if price_element:
            return price_element.text
        else:
            print("Error: Could not retrieve LG stock price.")
            return None

    except Exception as e:
        print("Error:", e)
        return None
lg=get_lg_stock_price_naver()
def get_hmm_stock_price_naver():
    try:
        url = "https://finance.naver.com/item/main.nhn?code=005380"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 웹페이지에서 주식 가격을 가져오기
        price_element = soup.select_one("div.today span.blind")

        if price_element:
            return price_element.text
        else:
            print("Error: Could not retrieve HMM stock price.")
            return None

    except Exception as e:
        print("Error:", e)
        return None
hmm=get_hmm_stock_price_naver()
def get_bitcoin_price_naver():
    try:
        # 네이버에서 비트코인 시세를 검색하는 URL
        url = "https://search.naver.com/search.naver?query=비트코인+시세"

        # HTTP GET 요청을 보내고 응답을 받음
        response = requests.get(url)

        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 시세 정보가 들어 있는 요소를 찾음
        price_element = soup.select_one('strong.price em')

        if price_element:
            # 가격 정보를 텍스트로 추출
            price_text = price_element.get_text(strip=True)
            return price_text

        else:
            print("Error: Could not retrieve Bitcoin price.")
            return None

    except Exception as e:
        print("Error:", e)
        return None
bitcoin= get_bitcoin_price_naver()
def get_sp500_index_from_naver():
    # 네이버 금융 페이지의 S&P 500 지수 URL
    url = "https://finance.naver.com/world/sise.nhn?symbol=SPI@SPX"

    # HTTP GET 요청을 통해 페이지 콘텐츠 가져오기
    response = requests.get(url)
    if response.status_code != 200:
        return "Error: 페이지를 불러올 수 없습니다."

    # BeautifulSoup을 사용하여 HTML 내용 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # S&P 500 지수가 포함된 태그 찾기
    index_tag = soup.find('em', {'class': 'no_up'})

    # 지수 정보 추출
    if index_tag:
        index_value = index_tag.get_text().strip()
        return index_value
    else:
        return "Error: S&P 500 지수를 찾을 수 없습니다."



sp500 = get_sp500_index_from_naver()
def get_dollar_price_naver():
        # 네이버에서 비트코인 시세를 검색하는 URL
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%8B%AC%EB%9F%AC+%ED%99%98%EC%9C%A8&oquery=sp500&tqi=ii11Dsqo1awssjxd%2B8dssssstwh-395199"

    # HTTP GET 요청을 보내고 응답을 받음
    response = requests.get(url)

    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 시세 정보가 들어 있는 요소를 찾음
    price_element = soup.find("strong",attrs={"class":"price"})
    return price_element.get_text()
dollar= get_dollar_price_naver()

print(get_sp500_index_from_naver())
