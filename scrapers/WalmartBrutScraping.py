import asyncio
import json
import httpx
from typing import List, Dict
from loguru import logger as log
from parsel import Selector

BASE_HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "en-US;en;q=0.9",
    "accept-encoding": "gzip, deflate",
}

def parse_product(html_text: str) -> Dict:
    """Parse Walmart product and extract all reviews"""
    sel = Selector(text=html_text)
    
    # Extraire les données du produit principal
    data = sel.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
    data = json.loads(data)
    
    # Extraire les données du produit
    _product_raw = data["props"]["pageProps"]["initialData"]["data"]["product"]
    wanted_product_keys = [
        "availabilityStatus",
        "averageRating",
        "brand",
        "id",
        "imageInfo",
        "manufacturerName",
        "name",
        "orderLimit",
        "orderMinLimit",
        "priceInfo",
        "shortDescription",
        "type",
    ]
    product = {k: v for k, v in _product_raw.items() if k in wanted_product_keys}
    
    # Extraire tous les avis (reviews_raw)
    reviews_raw = data["props"]["pageProps"]["initialData"]["data"]["reviews"]
    
    return {"product": product, "reviews_raw": reviews_raw}

async def scrape_products(urls: List[str], session: httpx.AsyncClient):
    """Scrape Walmart product pages and get reviews for each category"""
    log.info(f"Scraping {len(urls)} products from Walmart")
    responses = await asyncio.gather(*[session.get(url) for url in urls])
    results = []
    for resp in responses:
        assert resp.status_code == 200, "Request is blocked"
        product_data = parse_product(resp.text)
        results.append(product_data)
    log.success(f"Scraped {len(results)} products data")
    return results

async def run():
    # Limit connection speed to prevent scraping too fast
    limits = httpx.Limits(max_keepalive_connections=5, max_connections=5)
    client_session = httpx.AsyncClient(headers=BASE_HEADERS, limits=limits)
    
    # Run the scrape_products function
    data = await scrape_products(
        urls=[
            "https://www.walmart.com/ip/Apple-MacBook-Air-13-3-inch-Laptop-Space-Gray-M1-Chip-8GB-RAM-256GB-storage/609040889?classType=VARIANT&athbdg=L1102&from=/search",
            "https://www.walmart.com/ip/BTFL-3QT-AIRFRY-ROSE/7843623654?classType=VARIANT",
            "https://www.walmart.com/ip/CeraVe-Intensive-Moisturizing-Body-Lotion-with-Hydro-Urea-for-Dry-Skin-Itch-Relief-16-oz/5404617849?adsRedirect=true",
            "https://www.walmart.com/ip/Renwick-Faux-Leather-Barrel-Accent-Chair-Set-of-2-Black/721105679?athAsset=eyJhdGhjcGlkIjoiNzIxMTA1Njc5IiwiYXRoc3RpZCI6IkNTMDIwIiwiYXRoYW5jaWQiOiJJdGVtQ2Fyb3VzZWwiLCJhdGhyayI6MC4wfQ==&athena=true",
            "https://www.walmart.com/ip/CANADA-WEATHER-GEAR-Men-s-Flannel-Shirt-Casual-Button-Down-Long-Sleeve-Sweatshirts-for-Men-M-XXL/8439708559?classType=VARIANT",
            "https://www.walmart.com/ip/Sofia-Jeans-Women-s-Plus-Size-Eva-Skinny-Ankle-Jeans-Sizes-14W-28W/12874873369?classType=VARIANT",
        ],
        session=client_session
    )
    
    # Enregistrer les résultats dans un fichier JSON (sur le bureau)
    with open("walmart_products_with_reviews.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    log.info(f"Saved product data with reviews to 'Desktop/walmart_products_with_reviews.json'")

if __name__ == "__main__":
    asyncio.run(run())
