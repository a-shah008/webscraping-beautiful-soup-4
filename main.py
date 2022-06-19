from bs4 import BeautifulSoup
import requests
import re

# Finds the top 10 cheapest graphics card on the Newegg.com website
# DISCLAIMER: If too many automated requests (basically running this script) have been made, 
# Newegg will automatically block your computer for the next 24 hours from using their website. 
# This will make this script not work; it will alternatively continue giving errors.
# Specific line that gives an error if your computer it blocked: 17 to 18
no_errors = True
while no_errors:
    try:
        search_term = input("What graphics card do you want to search for (ex. 2080, 3080, 3090, etc.): ")

        url = f"https://www.newegg.com/p/pl?d={search_term}&N=4131"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")
        print("Requested Desired Page...")

        page_text = doc.find(class_="list-tool-pagination-text").strong
        pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])
        print("Found pages and corresponding text...")

        items_found = {}

        print("Looping through pages...")
        for page in range(1, pages + 1):
            url = f"https://www.newegg.com/p/pl?d={search_term}&N=4131&page={page}"
            page = requests.get(url).text
            doc = BeautifulSoup(page, "html.parser")
            print("Requested specific page...")
            
            div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
            items = div.find_all(text=re.compile(search_term))
            print("Received all items within specific div section...")

            for item in items:
                print("Looping through those items...")
                parent = item.parent
                if parent.name != "a":
                    continue

                link = parent["href"]
                next_parent = item.find_parent(class_="item-container")
                try:
                    price = next_parent.find(class_="price-current").find("strong").string
                    items_found[item] = {"price": int(price.replace(",", "")), "link":link}
                    print("Finding items and their respective prices and adding them to the items dictionary...")
                except:
                    pass

        sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])

        print("Printing all items found...")
        for item in sorted_items[:10]:
            print("")
            print(item[0])
            print(f"${item[1]['price']}")
            print(item[1]['link'])
            print("---------------------------------------------------------------------")
        break

    except Exception:
        print("Error occurred...")
        no_errors = False
        print("A problem in the code was detected. Automatically aborting script.")
        break