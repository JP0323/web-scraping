import requests
from bs4 import BeautifulSoup
import csv
from phones_list import phones
import re

# URL of the PHP page you want to scrape

def generate_csv(response):
    

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        
        specs = []
        features = []
        
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Save the page HTML to a file
        '''
        with open('product_page.html', 'w', encoding='utf-8') as html_file:
            html_file.write(soup.prettify())
        '''
        flipkart = 'Online at Best Price On Flipkart.com'

        title = soup.title.string
        
        # Define a regular expression pattern to match text inside brackets
        pattern_brackets = r'\([^)]*\)'

        # Remove the text inside brackets
        title = re.sub(pattern_brackets, '', title)
        
        # Remove the 'flipkart' text from the 'title'
        title = title.replace(flipkart, '')
        
        # Create a CSV file to store the extracted data
        csv_file = open(title.strip()+'.csv', 'w', newline='', encoding='utf-8')
        csv_writer = csv.writer(csv_file)
        
        # To extract the price
        price_tag = soup.find(string='₹')
        price = price_tag.parent.text.strip()
        specs.append('Price')
        features.append(price)
        
        #To all all available colors
        if soup.find(string='Color'):
            color_tag = soup.find(string='Color').parent.parent
            ind_colors = color_tag.find_all('div',class_='_3Oikkn _3_ezix _2KarXJ')
            all_colors = []
            for color in ind_colors:
                all_colors.append(color.text.strip())
            
            specs.append('Available colors')
            features.append(all_colors)
        
        # to add all available rams
        if soup.find(string='RAM'):
            ram_tag = soup.find(text='RAM').parent.parent
            ind_rams = ram_tag.find_all('div',class_='_3Oikkn _3_ezix _2KarXJ')
            all_rams = []
            
            for ram in ind_rams:
                all_rams.append(ram.text.strip())
                
            specs.append('Available RAMS')
            features.append(all_rams)
            
        # To all all available Storage options
        if soup.find(string='Storage'):
            storage_tag = soup.find(string='Storage').parent.parent
            ind_storages = storage_tag.find_all('div',class_='_3Oikkn _3_ezix _2KarXJ')
            all_storages = []
            
            for storage in ind_storages:
                all_storages.append(storage.text.strip())
                
            specs.append('Available Storages')
            features.append(all_storages)
        
        # Find all the feature sections
        feature_sections = soup.find_all('div', class_='flxcaE')
        
        for feature_section in feature_sections:
            feature_heading = feature_section.text.strip()
            #csv_writer.writerow([feature_heading])
            
            #print(feature_section.parent)
            # Find the table within the feature section
            table = feature_section.parent.find('table', class_='_14cfVK')
            # Find all rows within the table
            rows = table.find_all('tr', class_='_1s_Smc row')
            
            for row in rows:
                # Find the specification (first <td> element)
                spec = row.find('td', class_='_1hKmbr col col-3-12').text.strip()
                specs.append(spec)
                # Find the feature (text inside the <li> element)
                feature = row.find('li', class_='_21lJbe').text.strip()
                features.append(feature)
                # Write the data to the CSV file
        csv_writer.writerow(specs)
        csv_writer.writerow(features)
        
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        
    # Close the CSV file
    csv_file.close()

    print("Data has been extracted and saved to product_specs.csv")
    
for phone in phones:
    # Send an HTTP GET request to the PHP page
    response = requests.get(phone)
    generate_csv(response)