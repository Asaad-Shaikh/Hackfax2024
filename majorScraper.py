import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Step 1: Define the URL to scrape
url = "https://catalog.gmu.edu/programs/programsa-z/"
baseUrl = "https://catalog.gmu.edu/"

# Step 2: Fetch HTML content
response = requests.get(url)
if response.status_code == 200:
    html_content = response.text
else:
    print("Error fetching the page:", response.status_code)
    exit()

# Step 3: Parse HTML with Beautiful Soup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the container with the id 'az_sitemap_simple'
container = soup.find('div', id='az_sitemap_simple')

# Check if the container was found
if container:
    # Find all 'li' elements within the container
    list_items = container.find_all('li')
    with open('output.txt', 'w', encoding='utf-8') as file:
    # Loop over each 'li' element
        for li in list_items:
            a_tag = li.find('a')  # Find the first <a> tag within the list item
            if a_tag and a_tag.has_attr('href'):
                program_string = f"Program: {a_tag.text}\n"
                length_of_string = len(program_string)
                if(length_of_string>14 and program_string.startswith("Program:")):
                    file.write(f"Program: {a_tag.text}\n")
                    print(f"Program: {a_tag.text}")
                    full_url = urljoin(baseUrl, a_tag['href'])  # Combine the base URL with the relative URL
                    # Make a GET request to the full URL
                    program_response = requests.get(full_url)
                    if program_response.status_code == 200:
                        # Parse the response content with BeautifulSoup
                        program_soup = BeautifulSoup(program_response.content, 'html.parser')
                        # Find the first <p> tag within a div with class 'tab_content'
                        p_tag = program_soup.find('div', class_='tab_content').find('p')
                        if p_tag:
                            p_text = p_tag.get_text(strip=True)
                            description_string = f"Description: {p_text}"
                            if description_string.startswith("Description:"):
                                print(f"Description: {p_text}\nLink for more info: {full_url}")
                                file.write(f"Description: {p_text}\nLink for more info: {full_url}\n")

