import requests

class AltexScraper:
    def __init__(self):
        self.base_url = 'https://altex.ro/cauta/?q='
        self.xhr_base_url = 'https://fenrir.altex.ro/v2/catalog/search/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'If-None-Match': 'W/"8ba5e-MJNcnuIukr6rMB4kxUZot6xI6ZE"',
            'TE': 'trailers'
        }

    def search_product(self, product_name):
        search_url = f"{self.base_url}{product_name.replace(' ', '%20')}"
        print("Constructed URL:", search_url)

        s = requests.Session()

        res = s.get(search_url, headers=self.headers)
        res.raise_for_status()

        # construiesc  XHR URL
        xhr_url = f"{self.xhr_base_url}{product_name.replace(' ', '%20')}?size=48"
        xhr_headers = self.headers.copy()
        xhr_headers.update({
            'Host': 'fenrir.altex.ro',
            'Referer': search_url
        })

        
        res = s.get(xhr_url, headers=xhr_headers)
        res.raise_for_status()
        data = res.json()

        
        print(data)

        return data

    def get_price_and_name(self, product_name):
        data = self.search_product(product_name)
       
        if 'products' in data and data['products']:
            first_product = data['products'][0]
            first_price = first_product.get('price')
            product_name = first_product.get('name')
            url_key = first_product.get('url_key')
            sku = first_product.get('sku')
            if url_key and sku:
                product_link = f"https://altex.ro/{url_key}/cpd/{sku}"
            else:
                product_link = "Link not available"
            return {"price": first_price, "name": product_name, "link": product_link}
        else:
            print("No products found or 'products' key is missing")
            return None

if __name__ == '__main__':
    scraper = AltexScraper()
    product_name = "iphone 15 pro max"
    
  
    result = scraper.get_price_and_name(product_name)
    if result:
        print(f"First product name: {result['name']}")
        print(f"First product price: {result['price']} Lei")
        print(f"First product link: {result['link']}")
