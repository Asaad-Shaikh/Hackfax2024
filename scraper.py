from requests_html import HTMLSession

url = 'https://mason360.gmu.edu/events'

s = HTMLSession()
r = s.get(url)

r.html.render(sleep=3)  

h3_elements = r.html.find('div.media-body > h3.media-heading.header-cg--h4', first=False)
h2_elements = r.html.find('h2.header-cg--h4', first=False)

skip_string = "[eventName] [eventBadges] IF[:hybrid]='hybrid'--> Hybrid"

with open('events_combined.txt', 'w', encoding='utf-8') as file:
    h3_index = 2  

    for h2 in h2_elements[1:]:
        aria_label = h2.attrs.get('aria-label', 'No aria-label attribute')
        file.write(aria_label + '\n')
        
        while h3_index < len(h3_elements):
            h3 = h3_elements[h3_index]
            h3_text = h3.text.strip()
            
            h3_index += 1
            
            if h3_text == skip_string:
                break
            
            file.write(h3_text + '\n')

