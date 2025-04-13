import pandas as pd
import requests
from bs4 import BeautifulSoup
import time 
import random
from datetime import date, datetime

zillow = "https://www.zillow.com/beaverton-or/fsbo/?searchQueryState=%7B%22usersSearchTerm%22%3A%22Redding%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.64684715332031%2C%22east%22%3A-121.97530784667968%2C%22south%22%3A40.42663065068017%2C%22north%22%3A40.861148566020944%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A47322%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Afalse%2C%22category%22%3A%22cat2%22%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A11%7D"


headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'cache-control': 'no-cache',
        "cookie":'zguid=24|$7f42baba-788a-454e-acd8-c7e70f6bcd0a; zgsession=1|07ad1397-f7a6-4531-a105-d4bca175efea; _ga=GA1.2.223205435.1670447769; zjs_user_id=null; zg_anonymous_id="f81804b7-21eb-436f-bad0-f01b703651c1"; zjs_anonymous_id="7f42baba-788a-454e-acd8-c7e70f6bcd0a"; pxcts=5e493448-7674-11ed-b2dc-644241697947; _pxvid=5e4921bb-7674-11ed-b2dc-644241697947; _gcl_au=1.1.526233822.1670447769; DoubleClickSession=true; _cs_c=0; utag_main=v_id:0184ee72268b006125c4b5717eb005075001706d00bd0$_sn:1$_se:1$_ss:1$_st:1670449569228$ses_id:1670447769228;exp-session$_pn:1;exp-session$dcsyncran:1;exp-session$tdsyncran:1;exp-session$dc_visit:1$dc_event:1;exp-session$dc_region:us-west-2;exp-session; __pdst=09ff59cdf472426eacb1952bcb738760; _fbp=fb.1.1670447770893.1427663025; _pin_unauth=dWlkPU4yUmlPR05tTW1NdFpqTmtPQzAwTVRCbExXRmxNVFl0WWpsallUTXhObU5qTURSbQ; __gads=ID=d928549d0d10c8e9:T=1670447789:S=ALNI_MZ2vCJ2ydoGKLwyiyQYWMmyMCEYJQ; _clck=1qbb1tk|1|f7c|0; _gid=GA1.2.1791235879.1670882459; KruxPixel=true; _hp2_ses_props.1215457233={"ts":1670882460214,"d":"www.zillow.com","h":"/"}; JSESSIONID=B88E7D43186DA90EE0DE5F8DA7AACC79; __gpi=UID=0000090d94d3217f:T=1670447789:RT=1670882470:S=ALNI_MaAipz_xEdVRpITS8FF3nykzhwmoQ; KruxAddition=true; _cs_id=a94aef50-32ce-a2eb-9bc6-a30e415f9d22.1670447769.2.1670882869.1670882460.1.1704611769485; _cs_s=2.5.0.1670884669842; _hp2_id.1215457233={"userId":"8071024779595274","pageviewId":"163331852153630","sessionId":"6773580954950247","identity":null,"trackerVersion":"4.0"}; _px3=d7187c16d3b4aa8e6a17c41fd3c7a5b01734926532028f17f4d634859aeba7fa:dUo86PtbNlNKA8CZqLHYaoXgh8ycBIjgE9SPY4Cik8ptyERaZb2wmlvQx86ZWq4RXRqf9W2XnMPML2zorVfU8Q==:1000:fVEHHukaM2fXQlbQ7Vgi7fmbR8b7+Az/0OH6IafLOJBgN7Nm4QWTZFGBJvTbUMo9tlP5Th/oUV2NTPep5G6H8DYBq5FXNEuwJlD2I7Ua+RLl01AwAY12KgHGMfqnAo/5AKhS4oSCizJNnEIW04hByD7kcbhyjwJVhSOaIY4+e90W2FqwkfD7qRkI1271cG+KFSxJItlwJHMOP5OW9ZNeBw==; _uetsid=77596cd07a6811eda4312d337bb09dfe; _uetvid=5f656990767411edbbd27b674a5aa2f4; _gat=1; AWSALB=Xn+HEaMwzpjce9C0eM27aLDTttvXqk1xmaOaQzeLWyndx8vXSE9sl1B65prYLU+Hd7B8hMMVXixgBvD1rQPOu/OZppgEgTJdGIDR05QI+u6gmeguex1fD5iSpw5x; AWSALBCORS=Xn+HEaMwzpjce9C0eM27aLDTttvXqk1xmaOaQzeLWyndx8vXSE9sl1B65prYLU+Hd7B8hMMVXixgBvD1rQPOu/OZppgEgTJdGIDR05QI+u6gmeguex1fD5iSpw5x; search=6|1673475124255|rect=39.04111161492053%2C-121.19050515136719%2C38.174031858212814%2C-121.74119484863282&rid=20288&disp=map&mdm=auto&p=1&z=1&lt=fsbo&fs=1&fr=0&mmm=0&rs=0&ah=0&singlestory=0&housing-connector=0&abo=0&garage=0&pool=0&ac=0&waterfront=0&finished=0&unfinished=0&cityview=0&mountainview=0&parkview=0&waterview=0&hoadata=1&zillow-owned=0&3dhome=0&featuredMultiFamilyBuilding=0&commuteMode=driving&commuteTimeOfDay=now		20288						; _clsk=1ufr8i|1670883124606|37|0|e.clarity.ms/collect',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

# query parameters, where you put in city, bounds, etc.
params ={"searchQueryState":'{"usersSearchTerm":"Beaverton, OR","mapBounds":{"west":-122.86684715332031,"east":-122.73530784667968,"south":45.49163065068017,"north":45.56448566020944},"regionSelection":[{"regionId":47322,"regionType":6}],"isMapVisible":false,"category":"cat2","filterState":{"sort":{"value":"globalrelevanceex"},"ah":{"value":true},"fore":{"value":false},"fsba":{"value":false},"nc":{"value":false},"cmsn":{"value":false},"auc":{"value":false}},"isListVisible":true,"mapZoom":11}'} 

response = requests.get(zillow, headers=headers, params = params)

response.status_code

encod = response.encoding
contents = response.content.decode(encod)

soup = BeautifulSoup(contents, 'html.parser')
soup

#Print out the title of the pages 
titles = soup.title.text
print(titles)

#2022
time.sleep(random.uniform(15, 119)) # wait untill page loads completely 
today = date.today().strftime("%m/%d/%y")
table1 = pd.DataFrame(columns = ["Address", "Price", "Link", "Posted_Time", "Detail"])

houses = soup.find_all("article", {"class": "StyledPropertyCard-c11n-8-73-8__sc-jvwq6q-0 gHGLmX srp__sc-15y3msw-0 epgJFL property-card list-card_not-saved"})

for house in houses:
    try:
        address = house.find("address", {"data-test":"property-card-addr"}).text
        price = house.find("span", {"data-test":"property-card-price" }).text
        link = house.find("div", {"class":"StyledPropertyCardDataWrapper-c11n-8-73-8__sc-1omp4c3-0 gXNuqr property-card-data" }).a["href"]     
        posted = house.find("div", class_ = "StyledPropertyCardBadgeArea-c11n-8-73-8__sc-wncxdw-0 hlsElW").text + " From " + str(today)
        detail = house.find("span", {"class":"StyledPropertyCardHomeDetails-c11n-8-73-8__sc-1mlc4v9-0 jlVIIO" }).text
    except Exception as e:
        address = None
        price = None
        link = None
        posted = None
        detail = None

            
    table1 = table1.append({"Address": address, "Price": price, "Link": link,
                            "Posted_Time": posted, "Detail": detail }, ignore_index=True)
        
table1   