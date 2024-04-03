from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

#There are 3 sections: 
#1- Loading the given website and scraping store data 
#2- Clicking on link to navigate to store location address, and then scraping the address information
#3- Wrangling the data saved from the first 2 steps into a single, cleaned dataframe that can then be used to incorporate the review data and perform analytics



#STEP 1

#configuring webdriver
service = Service('/Users/austin/Downloads/chromedriver-mac-x64/chromedriver')
driver = webdriver.Chrome(service=service)

#go to lamadeleline webpage
driver.get(f'https://lamadeleine.com/locations')

#I use this time to manually zoom out on the map in browser (click the zoom out button on bottom right of page 8 times). This is needed to scrape ALL locations, not just the ones that show up as default
time.sleep(3)

#saving handle of original window, for use later
original_window = driver.current_window_handle

#navigating to elements I want to scrape
elements = driver.find_elements(By.CSS_SELECTOR, ".locationlist__wrapper")

#creating list to store scraped data 
elements_texts = []

#iterating through each element I want and printing
for element in elements:
    #print(element.text)
    elements_texts.append(element.text)

total_restaurants = 0

#iterating through text in my list and counting how many restaurants were scraped
for text in elements_texts:
    #count occurrences of unique marker for each restaurant
    num_restaurants = text.count('Get Directions\nCafé Details')
    total_restaurants += num_restaurants

print("Number of restaurants:", total_restaurants)




# STEP 2


#initiate counter and list (counter will just help with debugging)
i = 1
locations = []

#find the number of links I need to iterate over
num_of_directions = len(driver.find_elements(By.CSS_SELECTOR, ".location__directions"))

for index in range(num_of_directions):
    #refind the "directions" links each time
    directions_links = driver.find_elements(By.CSS_SELECTOR, ".location__directions")
    link = directions_links[index]

    #click link and switch to to new tab that opens
    link.click()
    driver.switch_to.window([window for window in driver.window_handles if window != original_window][0])

    #solution for getting destination element. I ran into issues where it would grab the starting point address instead of the destination address.
    aria_controls_selector = "input[aria-controls='sbsg51']"    

    #wait for element we are after to load, up to 20 sec
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tactile-searchbox-input')))

    #using destination address variable to ensure we get the html element
    address_element = driver.find_element(By.CSS_SELECTOR, aria_controls_selector)

    #retrieve attribute that we are after and print
    address_value = address_element.get_attribute('aria-label')

    #this print helps debug 
    print("Address " + str(i) + ": " + str(address_value))
    #(debugging)
    i = i + 1

    #add each new address to the address array
    locations.append(address_value)
   
    
    #closing tab and switching back to main tab
    driver.close()
    driver.switch_to.window(original_window)

#standardize delimiter in store_details list, this will help when turning it into a df
store_details = [text.replace('\n', ', ') for text in elements_texts]

#printing results from the 2 scrape drivers, helps debug
print("Store Details: ")
print (store_details)
print("Address Details: ")
print (locations)
driver.quit()





# STEP 3
#I will use pandas to manipulate the data

#create df for locations
locations_df = pd.DataFrame(locations, columns=['Address'])

#creating column names
columns_store = ['locationName', 'Status', 'Distance', 'phoneNumber', 'Extra 1', 'Extra 2']
#splitting data in store_details on commas, every 6 commas is a new entry
store_chunks = [store_details[0].split(', ')[i:i+6] for i in range(0, len(store_details[0].split(', ')), 6)]

#creating df for store_details
store_details_df = pd.DataFrame(store_chunks, columns=columns_store)
#dropping columns not needed
store_details_df = store_details_df.drop(columns=['Status','Distance','Extra 1', 'Extra 2'])

#combining address with store details
store_details_df['Address'] = locations_df['Address']



state_abbreviations = {
    "Texas": "TX",
    "California": "CA",
    "Maryland": "MD",
    #other states can be added as necessary
}

#function to replace state names with abbreviations
def abbreviate_state(address, state_map):
    for state, abbrev in state_map.items():
        if state in address:
            return address.replace(state, abbrev)
    return address

#call function
store_details_df['Address'] = store_details_df['Address'].apply(abbreviate_state, state_map=state_abbreviations)

#remove "destination" from the Address column data to prepare for splitting the column into smaller parts
store_details_df['Address'] = store_details_df['Address'].str.replace('Destination ', '')
print(store_details_df)


#splitting Address column into smaller parats
def split_address(row):
    #count the number of commas in the Address
    address = row['Address']
    num_commas = row['Address'].count(',')
    #debugging code
    # print(num_commas)
    # print("break")

    #this conditional helps clean the data. Some entries are missing street address, this accounts for that
    if num_commas == 1:
        #if only 1 comma, leave streetAddress column blank
        row['city'], row['state_postalCode'] = row['Address'].rsplit(', ', maxsplit=1)
        row['streetAddress'] = ""  # Set streetAddress to blank
    else:
        #if 2 commas, proceed with splitting (this is the expected # of commas)
        row['streetAddress_city'], row['state_postalCode'] = row['Address'].rsplit(', ', maxsplit=1)
        row['streetAddress'], row['city'] = row['streetAddress_city'].rsplit(', ', maxsplit=1)
    
    #split state_postalCode into state and postalCode by assuming state is always 2 characters
    row['state'] = row['state_postalCode'][:2]
    row['postalCode'] = row['state_postalCode'][2:]

    return row

#apply function to each row in df
store_details_df = store_details_df.apply(split_address, axis=1)


#drop unnecesssary columns
store_details_df.drop(columns=['Address', 'streetAddress_city', 'state_postalCode'], inplace=True)

#re order columns for ease of viewing
columns = list(store_details_df.columns)
new_columns_order = columns[1:-2] + [columns[0]] + columns[-2:]
store_details_df = store_details_df[new_columns_order]

print(store_details_df)

#exporting as a csv
file_path = '/Users/austin/Documents/BainCSV/store_details.csv'
store_details_df.to_csv(file_path, index=False)

file_path
