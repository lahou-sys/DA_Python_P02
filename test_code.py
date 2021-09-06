import bs4 as bs
import requests
from urllib.parse import urljoin

web_url = 'http://books.toscrape.com'
sauce = requests.get(web_url)
soup = bs.BeautifulSoup(sauce.text, "html.parser")

section = soup.section

#print(section)

for url in section.find_all('a'):
    print(url['href'])
    print(urljoin(web_url,url.get('href')))
    print("")