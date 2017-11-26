from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import urllib.parse
import threading

visited = []
count = 0

def content(html):
    string = ""
    for h in html.findAll("h"): string += h.text + " "
    for h in html.findAll('h1'): string += h.text + " "
    for h in html.findAll("h2"): string += h.text + " "
    for h in html.findAll("h3"): string += h.text + " "
    for h in html.findAll("h4"): string += h.text + " "
    for h in html.findAll("h5"): string += h.text + " "
    for h in html.findAll("h6"): string += h.text + " "
    string += "\n"
    for p in html.findAll("p"): string += p.text + " "

    return string

def loop(link):
    global visited
    global count

    uClient = uReq(link)
    pageHtml = uClient.read()
    uClient.close()

    count += 1
    page_soup = soup(pageHtml, "html.parser")

    f = open("content.txt", "a")
    f.write(link + "\n" + content(page_soup) + "\n\n")
    f.close()

    links = page_soup.findAll("a")
    for l in links:
        url = l['href']
        if url not in visited:
            visited += [url]
            try:
                uClient = uReq(url).read()
                print(url.hostname, link)
                print("entering (", count, ")", url)
                loop(url)
            except:
                try:
                    path =  urllib.parse.urljoin(link, url)
                    uClient = uReq(path).read()
                    print("visiting (", count, ")", path)
                    loop(path)
                except:
                    print("failed:", url)


t1 = threading.Thread(target = loop, args = ("http://www.straitstimes.com/",))
t2 = threading.Thread(target = loop, args = ("http://www.tnp.sg/",))
t3 = threading.Thread(target = loop, args = ("http://www.todayonline.com/",))
t4 = threading.Thread(target = loop, args = ("http://www.businesstimes.com.sg/",))

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()
