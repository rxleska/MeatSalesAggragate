from bs4 import BeautifulSoup as soup
import requests

HyveeBase = "https://www.hy-vee.com/aisles-online/search?search=" # add + to delimit words
search = "boneless skinless chicken breast"
Walmart = "https://www.walmart.com/search?q=" # ad %20 to delimit words 


# scrape the hyvee website
def scrapeHyvee(search):
    # format the search string
    search = search.replace(" ", "+")
    # create the url
    url = HyveeBase + search
    # open the connection and grab the page
    page = requests.get(url)
    # parse the html
    page_soup = soup(page.content, "html.parser")
    # grab the product containers
    containers = page_soup.findAll("div", {"class": "product-tile"})
    # print the number of containers
    print("There are " + str(len(containers)) + " containers on this page.")
    # create a list to hold the products
    products = []
    # loop through the containers
    for container in containers:
        # grab the product name
        product = container.find("div", {"class": "tile-name"}).text
        # grab the product price
        price = container.find("div", {"class": "tile-price"}).text
        # grab the product size
        size = container.find("div", {"class": "tile-size"}).text
        # grab the product unit
        unit = container.find("div", {"class": "tile-unit"}).text
        # grab the product image
        image = container.find("img", {"class": "tile-image"})["src"]
        # add the product to the list
        products.append([product, price, size, unit, image])
    # return the list
    return products

scrapeHyvee(search)
