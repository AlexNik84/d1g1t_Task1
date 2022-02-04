from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import json



chrome = webdriver.Chrome(executable_path="C:/Users/xandr/Desktop/chromedriver.exe")

chrome.maximize_window()
chrome.get("https://condos.ca?nocache=1")

"""chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
wait = WebDriverWait(chrome, 20)
element = chrome.find_element("#search-input")
wait.until(EC.element_to_be_clickable((By.ID, "#search-input")))
element.click()"""

inputPath = '#autoComplete > div.styles___Flex-sc-1lfxfux-0.clKrwZ.styles___InputContainer-sc-1rclri9-3.gjrMjh > div > div.styles___AlgoAutoSuggest-sc-1km20ud-0.iEWSjz.appAutoSuggest > div > input'
WebDriverWait(chrome, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, inputPath))).send_keys("Toronto")
WebDriverWait(chrome, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, inputPath))).send_keys(Keys.ENTER)


def get_condos(city, mode):
    url = f'https://condos.ca/{city}/condos-for-{mode}'
    chrome.get(url)
    page_content = chrome.page_source
    soup = BeautifulSoup(page_content, 'html.parser')
    return soup


condos = get_condos('toronto', 'sale')
print(condos)
raw_prices = []
links_list = []
condos_info = []

for price in condos.find_all('div', class_='dHPUdq'):
    raw_price = price.get_text()
    # formatted_price = int(raw_price.split('$')[1].replace(',', ''))
    # prices.append(formatted_price)
    raw_prices.append(raw_price)

for a in condos.find_all('a', class_='cncVOT'):
    link = a.get('href')
    links_list.append(link)

for link, price in zip(links_list, raw_prices):
    condos_info.append({"Web link": link, "Price": price})

sorted_condos_info = sorted(condos_info, key=lambda d: d['Price'])
#print(sorted_condos_info)  # testing purposes


def find_condo(d):
    url1 = f'https://condos.ca{sorted_condos_info[d - 1]["Web link"]}'
    chrome.get(url1)
    specific_prop_content = chrome.page_source
    soup1 = BeautifulSoup(specific_prop_content, 'html.parser')
    return soup1


fifth_condo = find_condo(5)
address = fifth_condo.find('h1', class_="ccBSix").text

table_headers = []

for i in fifth_condo.find_all("th"):
    header = i.text
    table_headers.append(header)

table_content = []

rows = fifth_condo.tbody.find_all("tr")
for row in rows:
    cols = row.find_all('td')
    for ele in cols:
        content = ele.text.strip()
        table_content.append(content)

fift_condo_details = []

h=0
i=1
j=2
incr = 3

while h < (len(table_content)) and i < (len(table_content)) and j < (len(table_content)):
    fift_condo_details.append({table_headers[0]: table_content[h], table_headers[1]: table_content[i], table_headers[2]: table_content[j]})
    i+=incr
    j+=incr
    h+=incr

def write_to_json(d):
    with open(f'C:/Users/xandr/Desktop/{address}.json', 'w') as file:  # Used C:/ since my current system is Windows
        json.dump(d, file, indent=4)
        file.truncate()
        file.close()

write_to_json(fift_condo_details)