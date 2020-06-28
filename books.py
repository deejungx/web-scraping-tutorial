# Introduction to Web Scraping
# Access the online bookstore here:
# http://books.toscrape.com/
# To do:
#    To Collect the information of all books from the online
#    bookstore and store them in a csv file.
#    CSV format:
#        Title, Genre, Cost, Image URL, Availability, Rating, Description, UPC
# Scraping Pipeline:
#    1. Carefully Observe and Inspect the Web page
#    2. Scrape the HTML content using requests
#    3. Parse and extract data using Beautiful Soup
#    4. Store the data in a file for easier access in the future

import requests
from bs4 import BeautifulSoup

# Imports urllib.parse to join urls and form absolute url
import urllib.parse

# Import the csv library for using the csv writer
import csv


def get_book_urls():
    # Declares an empty list to store all the urls
    product_urls = []

    # Navigates the pagination of book listing
    for i in range(1, 51):
        response = requests.get("http://books.toscrape.com/catalogue/"
                                "category/books_1/page-{num}.html"
                                .format(num=i))

        # Checks status code for ensuring that successful response occurred
        print(response.status_code)
        
        # Creates a Soup instance
        src = response.content
        soup = BeautifulSoup(src, "lxml")

        # Finds all the cards displaying individual books
        product_cards = soup.find_all("article", class_="product_pod")

        # Displays the relative urls of each individual book detail page
        for product in product_cards:
            print(product.find("a")["href"])

            # Displays absolute url formed by joining relative url with current url
            relative_url = product.find("a")["href"]
            print(urllib.parse.urljoin("http://books.toscrape.com/"
                                    "catalogue/category/books_1/",
                                    relative_url)
                )

            # Appends the absolute url to product_urls list
            absolute_url = urllib.parse.urljoin("http://books.toscrape.com/"
                                                "catalogue/category/books_1/",
                                                relative_url)
            product_urls.append(absolute_url)

            # save product urls to a file for easier access
            with open('url_list.txt', 'w') as f_handle:
                for url in product_urls:
                    f_handle.write('{}\n'.format(url))

# Call the function to get all books urls and store them in a file
# Uncomment this to run the function:
# get_book_urls()

product_urls = []


with open('url_list.txt', 'r') as file_handle:
    for line in file_handle:
        current_url = line[:-1]
        product_urls.append(current_url)

# Declare an empty list to store all details of books
product_record_list = []

# Iterate over all the the product urls to visit them individually
for product_url in product_urls:
    # Scrape and parse the detail page
    product_page = requests.get(product_url)
    page_src = product_page.content
    product_soup = BeautifulSoup(page_src, "lxml")

    # find product_main block by matching class of element
    product_main = product_soup.find("div", class_="product_main")

    # get title of the book
    product_name = product_main.h1.string

    # get price of the book
    product_price = product_main.find("p", class_="price_color").string

    # get availability of the book
    product_stock = " ".join(product_main.find("p", class_="instock").
                                contents[2].
                                split()
                                )

    # get rating of the book
    product_rating = product_main.find("p", class_="star-rating")["class"][1]

    # get genre of the book
    product_genre = list(product_soup.find("ul", class_="breadcrumb").children)[5].a.string

    # find the absolute URL of the book's cover image
    relative_image_url = product_soup.find("div", id="product_gallery").img["src"]
    product_image_url = urllib.parse.urljoin(product_url, relative_image_url)

    # catch books without a product description and assign a default value
    try:
        # get product description of the book
        product_description = product_soup.find("div", id="product_description"). \
            next_siblings[1].string
    except AttributeError:
        # assigns default value
        product_description = ""

    # get UPC of the book
    product_upc = product_soup.find_all("td")[0].string

    # add the list of book details to the final list
    product_record_list.append([product_name,
                                product_genre,
                                product_price,
                                product_image_url,
                                product_stock,
                                product_rating,
                                product_description,
                                product_upc])

    # tracking the progress of execution
    print("%d of 1000" % len(product_record_list))

# save the records of books on a csv file named book_db using UTF-8 encoding
with open("book_db.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(product_record_list)
