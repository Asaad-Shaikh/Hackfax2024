from requests_html import HTMLSession
from bs4 import BeautifulSoup


url = 'https://catalog.gmu.edu/programs/#filter=.filter_22&.filter_23'
base_url = 'https://mason360.gmu.edu'

s = HTMLSession()
r = s.get(url)

r.html.render(sleep=1)  

major_elements = r.html.find('div.tab_content', first=False)
print(major_elements.text)