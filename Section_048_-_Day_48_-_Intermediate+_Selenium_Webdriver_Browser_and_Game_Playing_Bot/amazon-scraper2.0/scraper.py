from bs4 import BeautifulSoup
from browser_fetcher import fetch_html
from storage import save_results

def parse_products(html):
    soup = BeautifulSoup(html, 'lxml')
    return soup.find_all("div", {"data-component-type": "s-search-result"})

def extract_info(product):
    title = product.find("h2").get_text(strip=True) if product.find("h2") else "No title"
    price_elem = product.find(class_="a-offscreen")
    price = price_elem.get_text(strip=True) if price_elem else "N/A"
    rating_elem = product.find(class_="a-icon-alt")
    rating = rating_elem.get_text(strip=True).replace(" out of 5 stars", "") if rating_elem else "No rating"
    img = product.find("img", class_="s-image")
    image = img["src"] if img else ""
    link = product.find("a", href=True)
    url = f"https://amazon.in{link['href']}" if link else ""
    sponsored = bool(product.find(string=lambda x: x and "Sponsored" in x))
    
    return [title, price, f"{rating}/5" if rating != "No rating" else rating, 
            image, "Sponsored" if sponsored else "Organic", url]

def run_scraper(keyword):
    print(f"Scraping: {keyword}")
    url = f"https://www.amazon.in/s?k={keyword.replace(' ', '+')}"
    
    try:
        html = fetch_html(url)
        products = parse_products(html)
        
        if products:
            data = [extract_info(p) for p in products[:20]]
            save_results(data, keyword)
            print(f"✅ Found {len(data)} products")
            return True
        else:
            print("❌ No products found")
            save_results([["No products found", "", "", "", "", ""]], keyword)
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        save_results([[f"Error: {str(e)[:50]}", "", "", "", "", ""]], keyword)
        return False