#!/usr/bin/env python3

from urllib.request import urlopen
from bs4 import BeautifulSoup

def fetch(url):
    """
    Fetch the content of the url and return a beautifulsoup object.
    """
    try:
        html = urlopen(url)
    except:
        return None

    return BeautifulSoup(html, 'lxml')

def scrape_opac(url):
    """
    Count the number of search results in the OPAC catalog.
    The count is based on number of hits close to the page buttons.
    """
    bsObj = fetch(url)
    if bsObj == None:
        return "Unable to connect to the website."
    else:
        pages = bsObj.find('strong', {'class': 'pages'}).get_text()
        count = pages.split()[-1]
        return count

def count_books():
    "Return the number of print books in the OPAC catalog."
    return scrape_opac(
        'https://vzlbs2.gbv.de/DB=69/SET=3/TTL=1/CMD?ACT=SRCHA&IKT=1016&SRT=YOP&TRM=bar+4*'
    )

def count_ebooks():
    "Return the number of eBooks in the OPAC catalog."
    return scrape_opac(
        'https://vzlbs2.gbv.de/DB=69.1/SET=21/TTL=20991/CMD?ACT=SRCH&IKT=31&SRT=YOP&TRM=20*+19*'
    )

def count_journals():
    """
    Fetch the A-Z Journal Finder page with a doped query that displays all available publications. The media
    count is fetched from the row "Total number of journals: X" above the search results.
    """
    az_url = "http://sfx.gbv.de/sfx_kueh/az/default?param_type_save=browseLetterGroup"
    az_url += "&param_letter_group_value=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9,"
    az_url += "A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2CA%2CB%"
    az_url += "2CC%2CD%2CE%2CF%2CG%2CH%2CI%2CJ%2CK%2CL%2CM%2CN%2CO%2CP%2CQ%2CR%2CS%2CT%2CU%2CV%2CW%2CX%2CY"
    az_url += "&param_letter_group_script_value=Latin"

    bsObj = fetch(az_url)
    if bsObj == None:
        return "Unable to connect to the website."
    else:
        total_number = bsObj.find('strong').get_text()
        count = total_number.split()[-1]
        return count

def count_databases():
    """
    Count the number of databases listed on the library website.
    The count is based on the heading elements that compose
    the accordion.
    """
    bsObj = fetch(
        'https://www.the-klu.org/faculty-research/library/library-collection/research-databases/')
    if bsObj == None:
        return "Unable to connect to the website."
    else:
        return len(bsObj.findAll("div", {"class": "heading"}))


if __name__ == '__main__':
    title = "===========================================================================\n"
    title += "  _  ___   _   _   _    _ _                        __  __        _ _\n"
    title += " | |/ / | | | | | | |  (_) |__ _ _ __ _ _ _ _  _  |  \/  |___ __| (_)__ _ \n"
    title += " | ' <| |_| |_| | | |__| | '_ \ '_/ _` | '_| || | | |\/| / -_) _` | / _` |\n"
    title += " |_|\_\____\___/  |____|_|_.__/_| \__,_|_|  \_, | |_|  |_\___\__,_|_\__,_|\n"
    title += "                                            |__/                          \n"
    title += "===========================================================================\n"
    title += "Display the count of all media available in the KLU Library collection.\n"

    print("\n\n")
    print(title)
    print("[+] Print Books (Titles):", count_books())
    print("[+] eBooks:", count_ebooks())
    print("[+] eJournals:", count_journals())
    print("[+] Databases:", count_databases())
