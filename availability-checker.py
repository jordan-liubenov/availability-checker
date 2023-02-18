import requests
from bs4 import BeautifulSoup
import json

targetSpan = "fx-availability fx-availability--on-date js-fx-tooltip-trigger"
targetHeader = "fx-product-headline product-title__title"

url = "https://www.thomann.de/gb/fender_sq_cv_bass_vi_lrl_bk.htm"

def scrapePage():
    res = requests.get(url)
    scrapedPage = res.text
    return scrapedPage

def getAvailability(scrapedPage):
    Manja = BeautifulSoup(scrapedPage, "html.parser")
    allSpans = Manja('span')
    for tag in allSpans:
        currentClass = tag.get("class")
        if currentClass == targetSpan.split(" "):
            availability = tag.text.strip()
            return availability

def getProductName(scrapedPage):
    Manja = BeautifulSoup(scrapedPage, "html.parser")
    allHeaders = Manja('h1')
    for tag in allHeaders:
        currentClass = tag.get("class")
        if currentClass == targetHeader.split(" "):
            productName = tag.text.strip()
            return productName

def formatOutput(availability, productName):
    if availability == "In stock":
        return f"===={productName} is {availability}===="
    else:
        return f"===={productName} will be {availability}!===="
    

def sendTelegram(messageStr):
    headers = {'Content-Type': 'application/json'}
    
    data_dict = {'chat_id': 0,
    'text': messageStr,
    'parse_mode': 'HTML',
    'disable_notification': False}
    data = json.dumps(data_dict)

    url = f'https://api.telegram.org/bot{bentan_key}/sendMessage'

    res = requests.post(url, data=data, headers=headers, verify=False)

    print(res.json())

def lambda_handler(event, context):
    page = scrapePage()
    availability = getAvailability(page)
    productName = getProductName(page)
    output = formatOutput(availability, productName)
    sendTelegram(output)
