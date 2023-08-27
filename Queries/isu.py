from bs4 import BeautifulSoup as bs
import requests
import re

# class to store meats


class Meat:
    def __init__(self, name, pricePerPound, avaliable):
        self.name = name
        # split on spaces - / and , to get a list of words
        self.nameList = re.split(r"[\s\/,]+", name)
        # remove empty strings
        self.nameList = list(filter(None, self.nameList))
        # remove words with out any letters
        self.nameList = list(
            filter(lambda x: re.search(r"[a-zA-Z]", x), self.nameList))
        # convert all words to lowercase
        self.nameList = list(map(lambda x: x.lower(), self.nameList))
        self.pricePerPound = pricePerPound
        self.avaliable = avaliable

    def __str__(self):
        return f"{self.name} costs {self.pricePerPound} and is {'available' if self.avaliable else 'not available'}"


def getMeats():
    # Required Information
    website = "https://www.meatscience.ag.iastate.edu/meat-sales"
    # Get html
    html = requests.get(website).text
    # convert to soup
    soup = bs(html, "html.parser")
    # get tbody table
    tbody = soup.find("tbody")
    # get all table rows from tbody
    rows = tbody.find_all("tr")
    # convert rows to list
    rows = list(rows)
    # get meats from rows
    meats = []
    for row in rows:
        # get name by getting the first td
        name = row.find("td").text
        # get price per pound by getting the second td
        pricePerPound = row.find_all("td")[1].text
        # get avaliable by getting the fourth td
        avaliable = row.find_all("td")[3]
        # then getting the value of the input element with the id contains "edit-submit"
        avaliable = avaliable.find(
            "input", id=lambda x: x and "edit-submit" in x)
        # get value of avaliable
        avaliable = avaliable["value"]
        avaliable = True if avaliable == "Add to Cart" else False
        # create meat object
        meat = Meat(str(name).strip(), str(
            pricePerPound).strip(), str(avaliable).strip())
        # add meat to list
        meats.append(meat)
    return meats


# # get meats
# meats = getMeats()
# # print all word lists
# for meat in meats:
#     print(meat.nameList)


def searchMeats(search):
    # get meats
    meats = getMeats()
    # convert search to list of words
    search = re.split(r"[\s\/,]+", search)
    # remove empty strings
    search = list(filter(None, search))
    # remove words with out any letters
    search = list(filter(lambda x: re.search(r"[a-zA-Z]", x), search))
    # convert all words to lowercase
    search = list(map(lambda x: x.lower(), search))

    # create map of number of matches to meat array
    matches = {}
    # loop through meats
    for meat in meats:
        # get number of matches
        numMatches = 0
        # loop through search
        for word in search:
            # if word is in meat name list
            if word in meat.nameList:
                # increment numMatches
                numMatches += 1
        # add meat to matches list
        if numMatches in matches:
            matches[numMatches].append(meat)
        else:
            matches[numMatches] = [meat]

    # return list of meats with the most matches
    return matches[max(matches.keys())]


# search meats
for meat in searchMeats("ribs"):
    print(meat)
