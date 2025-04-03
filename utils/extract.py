import requests
import pandas as pd
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

# melakukan pencarian berdasarkan elemen pada HTML
def extract_fashion_data(product_details):
    title = product_details.find('h3').text.strip() 
    price = product_details.find('span', class_='price')
    rating = product_details.find('p', string=lambda text: text and "Rating" in text)
    colors = product_details.find('p', string=lambda text: text and "Colors"in text)
    size = product_details.find('p', string=lambda text: text and "Size"in text)
    gender = product_details.find('p', string=lambda text: text and "Gender"in text)

    # mengembalikan nilai berdasarkan elemen 
    return {
        "title" : title,
        "price" : price,
        "rating" : rating,
        "colors" : colors,
        "size" : size,
        "gender" : gender
    }

# melakuakn request pada website dan mengambil isi dari konten HTML
def fetch_page_content(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    
    except requests.exceptions.RequestException as e:
        print(f"error saat mengambil {url}: {e}")
        return None

# melakukan scraping data pada url
def scrape_fashion_data(url):
    # melakukan scraping
    content = fetch_page_content(url)
    if not content:
        return []
    
    soup = BeautifulSoup(content, 'html.parser')
    data = []
    # berdasarkan kontainer
    product_container = soup.find('div',class_='collection-grid', id='collectionList')

    if product_container:
        # berdasarkan class product-details
        products = product_container.find_all('div', class_='product-details')
        for product_details in products:
            # melakukah ekstrasi data pada setiap variabel yang telah ditentukan pada def extract
            fashion_data  = extract_fashion_data(product_details)
            data.append(fashion_data)
    return data

def main():
    url = 'https://fashion-studio.dicoding.dev/'
    fashion_data = scrape_fashion_data(url)

    # menampilkan hasil scrape pada bentuk pandas
    if fashion_data:
        df = pd.DataFrame(fashion_data)
        print(df)
    else:
        print("tidak ditemukan")

if __name__ == "__main__":
    main()  