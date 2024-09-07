import requests
from bs4 import BeautifulSoup
import re

import http
import json
import schedule
import time

def job():
    # Your script logic here
  

    # Fetch the webpage
    r = requests.get('https://tokenbaz.com/')
    print(r.status_code)

    # Parse the HTML content
    soup = BeautifulSoup(r.text, 'html.parser')

    # Find the table rows
    res = soup.find("div", {"id": "priceTableWrapper"})
    res = soup.find_all("tr", {"class": "price-table-row"})
    #print(len(res))

    sell = []
    buy = []

    # Calculate available_money in dollar
    available_money =150

    # Calculate allowedvar in toman
    allowedvar=300


    for i in res:
        eachsell = []
        eachbuy = []
        
        # Find the table cells
        a = i.find_all("td", {"class": "price-table-cell"})
        
        
        
        # Find the exchange link
        exchange_link = i.find("a", {"class": "exchange-link text-decoration-none"})
        eachsell.append((exchange_link.text).strip())
        eachbuy.append((exchange_link.text).strip())
        
        # Find the currency details
        costs = i.find_all("div", {"class": "currency-details-item"})
        
        
        
        # Process sell price
        sell_price_text = costs[0].text.strip()
        x = re.search(r"[0-9,]+(?:\.\d+)?", sell_price_text)
        if x:
            numeric_value = x.group().replace(",", "")
            numeric_value = float(numeric_value)
            eachsell.append(numeric_value)
        
        # Process buy price
        buy_price_text = costs[1].text.strip()
        x = re.search(r"[0-9,]+(?:\.\d+)?", buy_price_text)
        if x:
            numeric_value = x.group().replace(",", "")
            numeric_value = float(numeric_value)
            eachbuy.append(numeric_value)
        

        #######3
        sell_cell = a[1]
        buy_cell=a[3]
        # Convert text to float or infinity
        valuesell = (lambda text: float('inf') if text == "نامحدود" else float(text.replace(',', '')))((sell_cell.text).strip())
        
        valuebuy= (lambda text: float('inf') if text == "نامحدود" else float(text.replace(',', '')))((buy_cell.text).strip())


        if valuesell >= available_money:
            #eachsell.append(valuesell)
            sell.append(eachsell)
        
        if valuebuy >= available_money:
            #eachbuy.append(valuebuy)
            buy.append(eachbuy) 

    sell.sort(key = lambda x: x[1],reverse=True)
    buy.sort(key = lambda x: x[1])
    #print(len(sell),sell)
    #print("################")
    #print(len(buy),buy)
    final_list=[]
    for s in sell:
        for b in buy:
            if s[1]-b[1]>= allowedvar:
                final_list.append([b , s])
            else:
                break
    print("###########################3")
    print(final_list)

    if final_list :
        smstext="تتر"
        for i in final_list:
                text=str({i[0][0]:i[1][0]})
                smstext=smstext+"."+text
        print(smstext)
        
        
        conn = http.client.HTTPSConnection("api.sms.ir")
        payload = json.dumps({
        "lineNumber": 30007487128939,
        "messageText": smstext,
        "mobiles": [
          "09164057756"
          
        ],
        "sendDateTime": None
        })
        headers = {
        'X-API-KEY': "u8hWMtgzFUog4A4wJfwgJz6ojgg2fPA6jRW690qpl8lClcEnSFhoiLlXKRn2mM2W",
        'Content-Type': 'application/json'
      }
        conn.request("POST", "/v1/send/bulk", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

      

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)        

    #######  1.compare based on the value i said. and ideentify which ones are better. and the fees ishould pay in each exchange platform . do they have api for transaction?
    #   2. do it on doge and other curruency and getting fimiliar with low cost currunsys like doge  3.connect it to api gmail and automate it 4.and  can send and change some varibles