from bs4 import BeautifulSoup
import requests

def get_sp500_price_investing():
    # Investing.com S&P 500 페이지 URL
    url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=S%26P500&oquery=S%26P500+%ED%95%9C%ED%99%94&tqi=ii2bFwqo1LwsschoaxGssssssxd-082226'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    price_element=soup.find("span",attrs={"class":"spt_con dw"})
    
    return price_element.strong.get_text()
sp500 = get_sp500_price_investing()
print(sp500)