from requests_html import HTMLSession
from bs4 import BeautifulSoup


url = 'https://mason360.gmu.edu/events'
base_url = 'https://mason360.gmu.edu'

s = HTMLSession()
r = s.get(url)

r.html.render(sleep=3)  

h2_elements = r.html.find('h2.header-cg--h4', first=False)

skip_string = "[eventName] [eventBadges] IF[:hybrid]='hybrid'--> Hybrid"
h3_elements = r.html.find('div.media-body > h3.media-heading.header-cg--h4', first=False)

hrefs = []

for h3 in h3_elements:
    # Find <a> tags within the h3 element
    a_tags = h3.find('a', first=False)
    # Extract the href attribute from each <a> tag
    for a in a_tags:
        href = a.attrs.get('href')
        if href and "rsvp" in href:
            hrefs.append(base_url + href)

with open('events_combined.txt', 'w', encoding='utf-8') as file:
    for newUrl in hrefs:
        new_response = s.get(newUrl)
        new_response.html.render(sleep=1)
        soup = BeautifulSoup(new_response.content, 'html.parser')
        target_divs = soup.find_all('div', class_='col-md-4_5')

        title = new_response.html.find('title', first=True).text if new_response.html.find('title') else 'No Title Found'
        parts = title.split(' - ')

        if len(parts) == 3:
            modified_title = 'Event: ' + parts[0] + ' - ' + parts[1] 
            organizer = 'Organizer: ' + parts[2]
        else:
            modified_title = 'Event: ' + parts[0]
            organizer = 'Organizer: ' + parts[1]
            
        file.write(f"Link: {newUrl}\n{modified_title}\n{organizer}\n")

        # Iterate through each div and find <p> tags
        for div in target_divs:
            p_tags = div.find_all('p')

        counter = 1  
        for p in p_tags:
            dwrite = p.get_text(strip=True)            
            if counter == 1:
                file.write("Date: " + dwrite + "\n")
            elif counter == 2:
                file.write("Time: " + dwrite + "\n")
            else:
                file.write(dwrite + "\n")
            counter += 1  




