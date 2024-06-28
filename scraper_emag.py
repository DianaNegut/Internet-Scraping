import requests
from bs4 import BeautifulSoup

def get_search_url(product_name):
    base_url = "https://www.emag.ro/search/"
    formatted_product_name = product_name.replace(' ', '%20')
    return f"{base_url}{formatted_product_name}"

def extract_price_and_name_emag(soup):
    product_element = soup.find('div', {'class': 'card-v2'})
    if product_element:
        name_element = product_element.find('a', {'class': 'card-v2-title'})
        price_element = product_element.find('p', {'class': 'product-new-price'})
        
        if name_element and price_element:
            name_text = name_element.text.strip()
            price_text = price_element.text.strip().split()[0].replace('.', '').replace(',', '.')
            product_link = name_element.get('href')
            return {"name": name_text, "price": float(price_text), "link": product_link}
    return None

def get_price_emag(product_url, headers):
    try:
        response = requests.get(product_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return extract_price_and_name_emag(soup)
        else:
            print(f"Failed to fetch product. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching product: {e}")
    return None

if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    search_url = get_search_url("iphone 13")
    result = get_price_emag(search_url, headers)
    if result:
        print(f"First product name: {result['name']}")
        print(f"First product price: {result['price']} Lei")
        print(f"First product link: {result['link']}")
    else:
        print("No product found or an error occurred.")
