import requests
from bs4 import BeautifulSoup

url = "https://catalog.gmu.edu/programs/#filter=.filter_22&.filter_23"

# Send an HTTP request to the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all elements that contain the major names
major_elements = soup.find_all("div", class_="courseblock")

# Extract and print the major names
for major_element in major_elements:
    major_name = major_element.find("p", class_="courseblocktitle").text.strip()
    print(major_name)
