from bs4 import BeautifulSoup as soup
import requests

# add + to delimit words
HyveeBase = "https://www.hy-vee.com/aisles-online/search?search="
search = "boneless skinless chicken breast"
Walmart = "https://www.walmart.com/search?q="  # ad %20 to delimit words


Test = "https://www.hy-vee.com/deals/ads?search=boneless%20skinless%20chicken%20breast"
# get html
html = requests.get(Test).text
# Save html to file
with open("test.html", "w") as file:
    file.write(html)
