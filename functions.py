import requests
from bs4 import BeautifulSoup
import time


def get_search_url(product_name):
    base_url = "https://www.emag.ro/search/"
    formatted_product_name = product_name.replace(' ', '%20')
    return f"{base_url}{formatted_product_name}"


def extract_price_emag(soup):
    price_element = soup.find('p', {'class': 'product-new-price'})
    if price_element:
        price_text = price_element.text.strip().split()[0].replace('.', '').replace(',', '.')
        return float(price_text)
    return None


def get_price_emag(product_url, headers):
    try:
        response = requests.get(product_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return extract_price_emag(soup)
        else:
            print(f"Failed to fetch product. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product: {e}")
    return None


def check_price(product_name, target_price, headers):
    search_url = get_search_url(product_name)
    product_url = search_url  
    current_price = get_price_emag(product_url, headers)
    if current_price is not None:
        print(f"Current Price on eMAG for {product_name}: {current_price}")
        if current_price < target_price:
            print(f"Alert: Price dropped below {target_price}!")
    else:
        print(f"Failed to fetch current price for {product_name}.")


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
target_price = 1000  


while True:
    product_name = input("Introdu numele produsului pentru căutare pe eMAG: ")
    check_price(product_name, target_price, headers)
    time.sleep(3600)  
