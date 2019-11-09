import requests
from bs4 import BeautifulSoup
import csv

def get_names():
    """ Scrapes the Herald Tribune website and returns a list of all names
        from today's obituaries
    """
    page = requests.get("http://www.legacy.com/obituaries/heraldtribune/browse?dateRange=today&type=paid")
    soup = BeautifulSoup(page.text, 'html.parser')

    names = soup.find_all('p', class_="ObitListItem__obitName___2nD2u")
    name_list = []
    
    for i in range(len(names)):
        name_list += [names[i].get_text()]

    return name_list

def get_dod():
    """ Scrapes the Herald Tribune website and returns a list of all dates
        of death from today's obituaries
    """
    page = requests.get("http://www.legacy.com/obituaries/heraldtribune/browse?dateRange=today&type=paid")
    soup = BeautifulSoup(page.text, 'html.parser')

    dates = soup.find_all('p', class_="ObitListItem__obitText___DAj-l")
    date_list = []

    for i in range(len(dates)):
        date_list += [dates[i].get_text().splitlines()[1]]

    return date_list

def get_obit():
    names = get_names()
    dods = get_dod()
    dictionary = dict(zip(names, dods))
    for k,v in dictionary.items():
        print(k,' | ',v)

    contact_list = []
    with open('ContactsExport.csv', 'rt') as f:
        reader = csv.reader(f)
        for row in reader:
            contact_list += [row[0]]

    for contact in contact_list:
        for name in names:
            nameWords = name.split()
            if all(word.lower() in contact.lower() for word in nameWords):
                print ('success ', name, ' ', contact)

    

   
    
