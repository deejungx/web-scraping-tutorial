# Make sure you have beautifulsoup, requests and lxml installed:
#    pip install beautifulsoup4
#    pip install requests
#    pip install lxml

import requests
from bs4 import BeautifulSoup

# To access any web page, we can use the "get" function from the requests module.
# We need to pass the url of the web site as argument for the function.
response = requests.get("https://www.google.com/")

# We can check the status of the response using the status_code property
# 200 indicates page was received successfully
print(response.status_code)

# For other potential status codes you may encounter,
# consult the following page:
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Status


# The main content of the web page is referred to as payload.
# It can be viewed in a variety of ways.

# The content property retrieves the content in raw bytes
# You will often need to convert that into strings
src_raw = response.content
# print(src_raw)

# To make things easier, the text property will
# do the conversion into strings for you.
# Optionally, you can specify the string encoding
# before accessing the text property
# response.encoding = 'utf-8'
src_string = response.text
# print(src_string)

# For information about the response itself,
# you can access the header property of the response
print(response.headers)

# You can access other HTTP methods too from the requests module
# requests.post('https://httpbin.org/post', data={'key': 'value'})
# requests.put('https://httpbin.org/put', data={'key': 'value'})
# requests.delete('https://httpbin.org/delete')
# requests.head('https://httpbin.org/get')
# requests.patch('https://httpbin.org/patch', data={'key': 'value'})
# requests.options('https://httpbin.org/get')

# Now that we have the source of the page, we can use the
# BeautifulSoup module to extract and process information from the content.
# To do that, we create a BeautifulSoup instance based on the
# raw source variable we have created above:
soup = BeautifulSoup(src_raw, 'lxml')

# To check if Beautifulsoup has successfully managed to parse the data,
# we can run the prettify function to make Beautifulsoup display the html content
# in a well-organized nested structure.
print(soup.prettify())
# print("\n")

# Now that we have the parsed data from the web site stored in beautifulsoup instance,
# we can navigate through the information in a variety of ways:

# <title> element of the page
print(soup.title)
# First instance of an <a> element tag
print(soup.a)
# To list all instances of a given tag element,
# use can use the find_all() function
print(soup.find_all('a'))

# A quite common task performed in web scraping is
# obtaining all the URLs from the <a> tags in the page
for link in soup.find_all('a'):
    print(link.get('href'))

# To extract all the text visible in the web page,
# you can use the get_text() function
# print("\n")
print(soup.get_text())
