import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv

current_page = 1;

#data = [];
item = {};
proceed = True;

csv_file = open('scrape.csv', 'w');
csv_writer = csv.writer(csv_file);
csv_writer.writerow(['id', 'name', 'link', 'phone', 'address', 'type', 'description', 'years', 'dollar', 'rating', 'menu_URL', 'order_online']);

def textify(item):
    if item is not None:
        return item.text;
    else:
        return None;

def boolify(item):
    if item == '':
        return False;
    else:
        return True;

def remove_non_numeric_chars(input_str: str) -> str:
    numeric_chars = [char for char in input_str[0:4] if char.isdigit()]
    result_string = ''.join(numeric_chars)
    return result_string

def chop(input_str: str) -> str:
    return input_str[0:150] + '[...]'

while(proceed):
    print("Currently scraping page: " + str(current_page));
    url = "https://www.yellowpages.com/search?geo_location_terms=New%20York%20City%2C%20NY&search_terms=restaurants&page="+str(current_page);
    source = requests.get(url);
    soup = BeautifulSoup(source.text,"lxml");

    #if soup.title.text == "404 Not Found":
    if current_page == 3:
        proceed = False;
    else:
        restaurant_all = soup.find_all('div', class_='v-card');
        for info in restaurant_all:
            item['business_name'] = info.span.text;
            item['Link'] = "https://www.yellowpages.com" + info.find("a").attrs["href"];
            item['years'] = textify(info.find("div", class_="count"));
            item['type'] = textify(info.find("div", class_="categories"));
            item['order_online'] = boolify(textify(info.find("div", class_="listing-ctas")));

            primary_info_all = info.find_all("div", class_="info-section info-primary");
            for primary_info in primary_info_all:
                item['id'] = remove_non_numeric_chars(textify(primary_info.find("h2", class_="n")));
                item['menu'] = "https://www.yellowpages.com" + primary_info.find("a").attrs["href"];
                try:
                    item['ratings'] = primary_info.find("div", class_="ratings").attrs["data-tripadvisor"];
                except:
                    item['ratings'] = ''
            secondary_info_all = info.find_all("div", class_="info-secondary");
            for secondary_info in secondary_info_all:
                item['addr'] = textify(secondary_info.find("div", class_="street-address"));
                item['phone'] = textify(secondary_info.find("div", class_="phones phone primary"));
                item['dollar'] = textify(secondary_info.find("div", class_="price-range"));
                
            snippet = info.find_all("div", class_="snippet");
            for snip in snippet:
                try:
                    item['description'] = chop(textify(snip.find("p", class_="body")));
                except:
                    item['description'] = ''
            #data.append(item);
            csv_writer.writerow([item['id'], item['business_name'], item['Link'], item['phone'], item['addr'], item['type'], item['description'], item['years'], item['dollar'], item['ratings'], item['menu'], item['order_online']]);
    current_page += 1;
csv_file.close;

#print(data)
#df = pd.DataFrame(data);
#df.to_csv("info.csv");

