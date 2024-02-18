import requests
from bs4 import BeautifulSoup

# Step 1: Define the URL to scrape
url = "https://catalog.gmu.edu/programs/#filter=.filter_22"
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

# Modified Step 4: Find all elements with class "title" under <div class="item-container">
containers = soup.find_all('div', class_='item-container')

# Define the criteria for each category
major_keywords = ["BA", "BS", "BFA", "BM", "MFA", "MA", "MS", "PhD", "MEd", "MPA", "MPH", "MD", "DO", "MSN", "DNP", "DDS", "DPT", "DVM"]
minor_keywords = ["Minor"]
certificate_keywords = ["Certificate", "Licensure", "Endorsement"]

# Initialize dictionaries to store programs for each category
majors = []
minors = []
certificates = []
others = []

# Categorize the programs
for container in containers:
    titles = container.find_all('span', class_='title')
    for title in titles:
        categorized = False
        for keyword in major_keywords:
            if keyword in title.text:
                majors.append(title.text + "\n")
                categorized = True
                break
        if not categorized:
            for keyword in minor_keywords:
                if keyword in title.text:
                    minors.append(title.text + "\n")
                    categorized = True
                    break
        if not categorized:
            for keyword in certificate_keywords:
                if keyword in title.text:
                    certificates.append(title.text + "\n")
                    categorized = True
                    break
        if not categorized:
            others.append(title.text + "\n")

# Write the categorized programs to the output file
with open("output_sorted.txt", "w") as file:
    file.write("Majors:\n")
    file.writelines(majors)
    file.write("\nMinors:\n")
    file.writelines(minors)
    file.write("\nCertificates:\n")
    file.writelines(certificates)
    file.write("\nOthers:\n")
    file.writelines(others)

print("Programs sorted and saved to output_sorted.txt")
