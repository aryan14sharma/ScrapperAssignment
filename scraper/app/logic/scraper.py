import time
import requests
from parse_handler.parser import parser_chain_of_responsibility
from storage.storage import Storage
from bs4 import BeautifulSoup

class ProductScraper:
    def __init__(self, pages_limit: int, storage: Storage, cache_storage: Storage,proxy: str = None):
        self.pages_limit = pages_limit
        self.storage = storage
        self.cache_storage = cache_storage
        self.proxy = {"http": proxy, "https": proxy} if proxy else None

    def scrape(self):
        products = []
        for page in range(1, self.pages_limit + 1):
            url = f"https://dentalstall.com/shop/page/{page}/"
            try:
                response = requests.get(url, proxies=self.proxy, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "html.parser")
                products += self.parse_page(soup)
            except requests.RequestException:
                time.sleep(5)
        self.store_products(products)
        self.store_products_in_cache(products)
        return {"total_products": len(products)}

    def parse_page(self, soup):
        products = []
        for product in soup.select(".product"):
            title_element = product.select_one(".woo-loop-product__title")
            price_element = product.select_one(".price")
            image_element = product.select_one("img")

            if title_element:
                product_title = title_element.text.strip()
                product_price = self.parse_price(price_element.text.strip()) if price_element else 0.0
                path_to_image = image_element["src"] if image_element else "No image available"

                products.append({
                    "product_title": product_title,
                    "product_price": product_price,
                    "path_to_image": path_to_image
                })
        return products

    def parse_price(self, price_text):
        price_text = parser_chain_of_responsibility.apply(price_text)
        try:
            return float(price_text)    
        except ValueError:
            return 0

    def store_products(self, products):
        for product in products:
            if "product_title" in product:
                self.storage.save(product["product_title"], product)
         
    def store_products_in_cache(self, products):
        for product in products:
            if "product_title" in product:
                self.cache_storage.save(product["product_title"], product)