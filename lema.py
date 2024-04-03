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
locations = ['Destination 2100 Ross Ave, Dallas, TX 75201', 'Destination 2100 McKinney Ave, Dallas, TX 75201', 'Destination 2211 Empire Central Dr, Dallas, TX 75235', 'Destination 3012 Mockingbird Ln, Dallas, TX 75205', 'Destination 8400 Westchester Dr, Dallas, TX 75225', 'Destination 4343 W Northwest Hwy, Dallas, TX 75220', 'Destination 8687 N Central Expy #3000, Dallas, TX 75225', 'Destination 11930 Preston Rd, Dallas, TX 75230', 'Destination 15125 Montfort Dr, Dallas, TX 75254', 'Destination 6430 N MacArthur Blvd, Irving, TX 75039', 'Destination 1320 W Campbell Rd, Richardson, TX 75080', 'Destination 2375 International Pkwy, Dallas, TX 75261', 'Destination 520 W 15th St, Plano, TX 75075', 'Destination 5000 W Park Blvd, Plano, TX 75093', 'Destination 2101 N Collins St, Arlington, TX 76011', 'Destination 900 TX-114, Grapevine, TX 76051', 'Destination 4201 S Cooper St, Arlington, TX 76015', 'Destination 987 I-30 Frontage Rd, Rockwall, TX 75032', 'Destination State Hwy 121, Frisco, TX 75034', 'Destination 810 W McDermott Dr, Allen, TX 75013', 'Destination 2500 Cross Timbers Rd, Flower Mound, TX 75028', 'Destination 1140 S Preston Rd, Prosper, TX 75078', 'Destination 3625 W University Dr, McKinney, TX 75071', 'Destination 8825 N Fwy, Fort Worth, TX 76177', 'Destination 4626 SW Loop 820, Fort Worth, TX 76109', 'Destination 6140 Camp Bowie Blvd, Fort Worth, TX 76116', 'Destination 2816 Marketplace Dr, Waco, TX 76711', 'Destination 419 W SW Loop 323, Tyler, TX 75701', 'Destination 14028 Research Blvd, Austin, TX 78717', 'Destination 9828 Great Hills Trl Suite 650 Ste 650, Austin, TX 78759', 'Destination 1954 24th Ave NW, Norman, OK 73069', 'Destination Barbara Jordan Blvd, Austin, TX 78723', 'Destination 5493 Brodie Ln, Austin, TX 78745', 'Destination 247 S Loop 336 W, Conroe, TX 77304', 'Destination 9595 Six Pines Dr, The Woodlands, TX 77380', 'Destination 6635 Spring Stuebner Rd, Spring, TX 77389', 'Destination 5505-A FM 1960, Houston, TX 77069', 'Destination 19710 Northwest Fwy, Houston, TX 77065', 'Destination 4570 Kingwood Dr, Kingwood Area, TX 77345', 'Destination 23322 Mercantile Pkwy, Katy, TX 77449', 'Destination 12850 Memorial Dr, Houston, TX 77024', 'Destination Amy Nguyen, Parkway Villages Shopping Center, 1560 Eldridge Pkwy #136, Houston, TX 77077', 'Destination 10001 Westheimer Rd Suite 2123 Ste 2123, Houston, TX 77042', 'Destination 1901 Taylor St, Houston, TX 77007', 'Destination la Madeleine, 5885 San Felipe St #100, Houston, TX 77057', 'Destination 5015 Westheimer Rd, Houston, TX 77056', 'Destination 1964 W Gray St, Houston, TX 77019', 'Destination 420 Meyerland Plz, Houston, TX 77096', 'Destination Sugar Land, Texas 77479', 'Destination 8115 S Olympia Ave, Tulsa, OK 74132', 'Destination 11200 Broadway St, Pearland, TX 77584', 'Destination 8134 Agora Pkwy, Selma, TX 78154', 'Destination 18030 US-281, San Antonio, TX 78232', 'Destination 931 W Bay Area Blvd, Webster, TX 77598', 'Destination la Madeleine, 11745 I-10 Suite 101, San Antonio, TX 78230', 'Destination 722 Northwest Loop 410, San Antonio, TX 78216', 'Destination 3805 Broadway, San Antonio, TX 78209', 'Destination Lake Jackson, Texas 77566', 'Destination 12208 W Markham St, Little Rock, AR 72211', 'Destination City Bank, 8201 Quaker Ave #100, Lubbock, TX 79424', 'Destination 2207 Kaliste Saloom Rd, Lafayette, LA 70508', 'Destination 7615 Jefferson Hwy, Baton Rouge, LA 70809', 'Destination 7707 Bluebonnet Blvd Suite 190, Baton Rouge, LA 70810', 'Destination Heinen, 3448 N Hwy 190, Covington, LA 70433', 'Destination 1200 S Clearview Pkwy Suite 1312, Harahan, LA 70123', 'Destination 3300 Severn Ave, Metairie, LA 70002', 'Destination 601 S Carrollton Ave, New Orleans, LA 70118', 'Destination El Dorado West, El Paso, TX 79938', 'Destination LOFT, 8889 Gateway Blvd W, El Paso, TX 79925', 'Destination N Mesa St, El Paso, TX 79912', 'Destination 2110 Louisiana Blvd NE, Albuquerque, NM 87110', 'Destination Food Network Kitchen, 6000 N Terminal Pkwy, Atlanta, GA 30320', 'Destination 8700 spine Rd, Atlanta, GA 30337', 'Destination Lauren Bone Cain Salon, 4101 Roswell Rd #301, Marietta, GA 30062', 'Destination 1165 Perimeter Center W Suite 350, Atlanta, GA 30338', 'Destination 2255 Pleasant Hill Rd Suite 480 Ste 480, Duluth, GA 30096', 'Destination 1795 Mall of Georgia Blvd, Buford, GA 30519', 'Destination 2156 E Williams Field Rd, Gilbert, AZ 85296', 'Destination W Chandler Blvd, Chandler, AZ 85226', 'Destination Sweet Republic, 3400 Sky Hbr Blvd, Phoenix, AZ 85034', 'Destination Luhrs Tower, Phoenix, AZ 85003', 'Destination 4175 Millenia Blvd, Orlando, FL 32839', 'Destination 1833 Fountain Dr, Reston, VA 20190', 'Destination 7906 L Tysons Corner Center E3l, McLean, VA 22102', 'Destination Dr. Richard Morris, 5876 Kingstowne Towne Ctr Suite 170, Alexandria, VA 22315', "Destination 5841 Crossroads Center Way, Bailey's Crossroads, VA 22041", 'Destination Gaithersburg, Maryland 20878', 'Destination 524 King St, Alexandria, VA 22314', 'Destination 7607 Old Georgetown Rd, Bethesda, MD 20814', 'Destination Connecticut Connection, Washington, DC 20036', 'Destination 6211 Columbia Crossing Cir, Columbia, MD 21045']
store_details = ["San Jacinto, Closed, 0.7 mi, 214-220-3911, Get Directions, Café Details, Park District - Petite Market & Bakery, Closed, 1.1 mi, 972-913-2280, Get Directions, Café Details, Dallas Love Field, Closed, 4.8 mi, 214-358-7614, Get Directions, Café Details, Mockingbird, Open until 9:00 PM, 4.3 mi, 214-696-0800, Get Directions, Café Details, Berkshire, Open until 7:00 PM, 6.1 mi, 945-279-0912, Get Directions, Café Details, Midway, Open until 9:00 PM, 6.5 mi, 214-357-5621, Get Directions, Café Details, Northpark, Open until 8:00 PM, 6.5 mi, 214-696-2398, Get Directions, Café Details, Preston Forest, Open until 9:00 PM, 9.3 mi, 972-233-6446, Get Directions, Café Details, Montfort, Open until 9:00 PM, 12.4 mi, 469-885-8080, Get Directions, Café Details, MacArthur, Open until 9:00 PM, 12.5 mi, 469-385-1700, Get Directions, Café Details, Coit & Campbell, Open until 9:00 PM, 14.1 mi, 972-671-4887, Get Directions, Café Details, DFW, Closed, 16.5 mi, 972-426-5210, Get Directions, Café Details, Collin Creek, Open until 9:00 PM, 17.4 mi, 972-398-3003, Get Directions, Café Details, Plano, Open until 9:00 PM, 17.3 mi, 972-407-1878, Get Directions, Café Details, North Arlington, Open until 9:00 PM, 17.4 mi, 817-461-3634, Get Directions, Café Details, Grapevine, Open until 9:00 PM, 19.7 mi, 817-251-0255, Get Directions, Café Details, South Arlington, Open until 9:00 PM, 20.7 mi, 817-417-5100, Get Directions, Café Details, Rockwall, Open until 9:00 PM, 21.8 mi, 972-722-6650, Get Directions, Café Details, Frisco, Open until 9:00 PM, 22.0 mi, 972-704-2000, Get Directions, Café Details, Allen, Open until 9:00 PM, 23.5 mi, 972-338-4927, Get Directions, Café Details, Flower Mound, Open until 9:00 PM, 23.8 mi, 469-240-5888, Get Directions, Café Details, Gates of Prosper, Open until 9:00 PM, 30.9 mi, 945-207-1286, Get Directions, Café Details, McKinney, Open until 9:00 PM, 31.4 mi, 469-581-1300, Get Directions, Café Details, Presidio Junction, Open until 9:00 PM, 31.5 mi, 682-593-5605, Get Directions, Café Details, Overton Park, Open until 9:00 PM, 35.2 mi, 817-717-5200, Get Directions, Café Details, Camp Bowie, Open until 9:00 PM, 36.1 mi, 817-654-0471, Get Directions, Café Details, Waco, Open until 9:30 PM, 90.8 mi, 254-262-3171, Get Directions, Café Details, Tyler, Open until 9:00 PM, 92.8 mi, 903-258-9050, Get Directions, Café Details, Lakeline, Open until 9:30 PM, 169.6 mi, 512-410-7535, Get Directions, Café Details, Arboretum, Open until 9:30 PM, 173.8 mi, 512-502-2474, Get Directions, Café Details, Norman, Open until 9:30 PM, 174.8 mi, 405-416-1942, Get Directions, Café Details, Mueller, Open until 9:30 PM, 178.9 mi, 512-366-3825, Get Directions, Café Details, Sunset Valley, Open until 9:30 PM, 186.0 mi, 512-287-4081, Get Directions, Café Details, Conroe, Open until 9:00 PM, 189.7 mi, 936-444-4601, Get Directions, Café Details, Woodlands, Open until 9:00 PM, 196.9 mi, 281-419-5826, Get Directions, Café Details, Spring, Open until 9:00 PM, 200.4 mi, 346-298-6390, Get Directions, Café Details, Champions, Open until 9:00 PM, 207.6 mi, 281-893-0723, Get Directions, Café Details, Crossroads, Open until 9:00 PM, 209.6 mi, 281-720-1000, Get Directions, Café Details, Kingwood, Open until 9:00 PM, 211.1 mi, 281-360-1681, Get Directions, Café Details, West Grand, Open until 9:00 PM, 215.0 mi, 281-395-2888, Get Directions, Café Details, Town & Country, Open until 9:00 PM, 219.8 mi, 713-465-7370, Get Directions, Café Details, Parkway Village, Open until 9:00 PM, 219.8 mi, 281-940-8516, Get Directions, Café Details, Carillon, Open until 9:00 PM, 222.6 mi, 713-266-7686, Get Directions, Café Details, Sawyer Heights, Open until 8:00 PM, 223.5 mi, 832-916-4001, Get Directions, Café Details, Tanglewood, Open until 9:00 PM, 223.1 mi, 832-726-1315, Get Directions, Café Details, Houston Galleria, Open until 8:00 PM, 224.2 mi, 713-993-0287, Get Directions, Café Details, River Oaks, Open until 9:00 PM, 224.4 mi, 713-526-9666, Get Directions, Café Details, Meyerland, Open until 10:00 PM, 227.5 mi, 713-218-8075, Get Directions, Café Details, First Colony, Open until 9:00 PM, 230.9 mi, 281-494-4400, Get Directions, Café Details, Tulsa Hills, Open until 9:00 PM, 230.3 mi, 918-289-0348, Get Directions, Café Details, Pearland, Open until 9:00 PM, 237.7 mi, 832-916-3598, Get Directions, Café Details, The Forum, Open until 9:30 PM, 239.7 mi, 210-306-2922, Get Directions, Café Details, Northwoods, Open until 9:30 PM, 240.4 mi, 210-499-0208, Get Directions, Café Details, Clearlake, Open until 9:00 PM, 244.1 mi, 281-316-6135, Get Directions, Café Details, Huebner Oaks, Open until 9:30 PM, 246.8 mi, 210-691-1227, Get Directions, Café Details, Park North, Open until 9:30 PM, 246.6 mi, 210-979-9161, Get Directions, Café Details, Alamo Heights, Open until 9:30 PM, 249.4 mi, 210-829-7291, Get Directions, Café Details, Lake Jackson, Open until 9:00 PM, 270.2 mi, 979-480-1223, Get Directions, Café Details, West Little Rock, Closed, 286.6 mi, 501-221-7777, Get Directions, Café Details, Kingsgate, Open until 9:00 PM, 299.8 mi, 806-698-6313, Get Directions, Café Details, Shops at Martial, Open until 9:00 PM, 333.4 mi, 337-504-7369, Get Directions, Café Details, Jefferson, Open until 9:00 PM, 371.8 mi, 225-927-6072, Get Directions, Café Details, Perkins Rowe, Open until 9:00 PM, 374.1 mi, 225-766-1875, Get Directions, Café Details, Mandeville, Open until 9:00 PM, 425.6 mi, 985-626-7004, Get Directions, Café Details, Elmwood, Open until 9:00 PM, 435.6 mi, 504-818-2450, Get Directions, Café Details, Severn, Open until 9:00 PM, 435.5 mi, 504-456-1624, Get Directions, Café Details, Carrollton, Open until 9:00 PM, 439.1 mi, 504-861-8662, Get Directions, Café Details, Tierra Del Este, Open until 9:00 PM, 557.2 mi, 915-229-2700, Get Directions, Café Details, Fountains at Farrah, Open until 9:00 PM, 563.4 mi, 915-225-3660, Get Directions, Café Details, La Villita, Open until 9:00 PM, 572.8 mi, 915-845-9808, Get Directions, Café Details, Uptown, Open until 8:00 PM, 582.4 mi, 505-274-7555, Get Directions, Café Details, Atlanta Airport Kiosk Terminal C Gate 40, Closed, 716.2 mi, 404-761-7222, Get Directions, Café Details, Atlanta Airport Kiosk - Terminal C Gate 7, Closed, 716.8 mi, 404-761-7222, Get Directions, Café Details, East Cobb, Open until 9:00 PM, 717.8 mi, 770-579-3040, Get Directions, Café Details, Perimeter, Open until 9:00 PM, 722.4 mi, 770-392-0516, Get Directions, Café Details, Gwinnett, Open until 9:00 PM, 734.5 mi, 770-814-0355, Get Directions, Café Details, Buford, Open until 9:00 PM, 743.3 mi, 470-589-1528, Get Directions, Café Details, San Tan Village, Open until 9:00 PM, 865.7 mi, 480-485-8490, Get Directions, Café Details, The Met, Open until 9:00 PM, 875.0 mi, 480-999-2095, Get Directions, Café Details, Phoenix Sky Harbor International Airport, Open until 10:00 PM, 880.2 mi, 602-275-6582, Get Directions, Café Details, Luhrs City Center, Closed, 884.6 mi, 480-436-8152, Get Directions, Café Details, Millenia Mall, Closed, 959.2 mi, 321-332-7001, Get Directions, Café Details, Reston, Open until 9:00 PM, 1166.4 mi, 703-707-0704, Get Directions, Café Details, Tysons Corner, Closed, 1172.6 mi, 703-962-1264, Get Directions, Café Details, Kingstowne, Open until 9:00 PM, 1174.4 mi, 571-385-2455, Get Directions, Café Details, Bailey's Crossroads, Open until 9:00 PM, 1176.2 mi, 703-379-5551, Get Directions, Café Details, Downtown Crown, Open until 9:00 PM, 1177.1 mi, 240-449-4879, Get Directions, Café Details, Alexandria, Open until 9:00 PM, 1179.8 mi, 703-739-2854, Get Directions, Café Details, Bethesda, Closed, 1180.4 mi, 301-215-9142, Get Directions, Café Details, Connecticut Ave., Closed, 1181.7 mi, 202-780-9988, Get Directions, Café Details, Columbia, Open until 9:00 PM, 1198.7 mi, 410-872-4900, Get Directions, Café Details"]

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