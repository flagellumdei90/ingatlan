############################################
# 1. lépés: Iroda linkek legyűjtése honlapról
############################################
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from time import sleep
import datetime

############# print running info
time_kezd = datetime.datetime.now()
print (time_kezd, "- A kód futtatása elindult.")

# Set up Chrome options
options = Options()
options.headless = True  # Set to True if you don't want to see the browser

# Initialize the WebDriver
driver = webdriver.Chrome(options=options)

# Navigate to the page
url = 'https://www.eston.hu/property-search'
driver.get(url)

# Wait for the page to load fully
wait = WebDriverWait(driver, 5) #20

#Scroll down to the bottom of the page
for x in range(1): #350
    driver.execute_script("window.scrollBy(0, 2);") # 250
    time.sleep(5)  # Give time for new items to load #10

# Wait for the elements to be present
element_name = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.property-title')))
element_address = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.property-addres')))
#property_link = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
element_link = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="/property/"]')))
element_price = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.property-attribute-item div+ div .mg-left')))
element_min_availability = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.property-attribute-item:nth-child(1) .area')))
element_max_availability = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.property-attribute-item+ .property-attribute-item .area')))
element_submarket = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.submarket div+ div .property-att-text')))
element_district = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.district div+ div .property-att-text')))
element_city = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.nonvisible div+ div .property-att-text')))

# Create arrays to store data
name_array = []
address_array = []
link_array = []
price_array = []
min_availability_array = []
max_availability_array = []
city_array = []
submarket_array = []
district_array = []

# Loop through the elements and save them to the array
for name in element_name:
    name_array.append(name.text)

for address in element_address:
    address_array.append(address.text)

# Loop through the links and save the href to the link_array
for link in element_link:
    href = link.get_attribute("href")
    if href:  # Only add if href is not empty
        link_array.append(href)
        
for price in element_price:
    price_array.append(price.text)

for min_availability in element_min_availability:
    min_availability_array.append(min_availability.text)

for max_availability in element_max_availability:
    max_availability_array.append(max_availability.text)

for city in element_city:
    city_array.append(city.text)

for submarket in element_submarket:
    submarket_array.append(submarket.text)

for district in element_district:
    district_array.append(district.text)

# Close the driver
driver.quit()

#remove duplicates
link_array2 = list(dict.fromkeys(link_array))
url_list = link_array2 # ez tartalmazza a linkeket, amiken később végig kell mennie a kódnak

############# print running info
time_step1 = datetime.datetime.now()
print (time_step1, "- Az első rész sikeresen lefutott. Az összes talált iroda száma: ", len(link_array2))

############################################
# 2. lépés: Iroda linkeket tároló tömb teljességének ellenőrzése és tömb átalakítása dataframe-re (df1 tábla)
############################################
# Check compliteness
print ("összes link: ", len(link_array2))
print ("összes név: ", len(name_array))
print ("összes cím: ", len(address_array))
print ("összes ár: ", len(price_array))
print ("összes min elérhetőség: ", len(min_availability_array))
print ("összes max elérhetőség: ", len(max_availability_array))
print ("összes város: ", len(city_array))
print ("összes alszegmens: ", len(submarket_array))
print ("összes kerület: ", len(district_array))

import pandas as pd

# tömb mentése DataFrame-be
df1 = pd.DataFrame({
    'Name': name_array,
    'Address': address_array,
    'Link': link_array2,
    'Office rent (EUR/m2/month)': price_array,
    'Min availability (m2)': min_availability_array,
    'Max availability (m2)': max_availability_array,
    'City': city_array,
    'District': district_array,
    'Submarket': submarket_array
    
})

############# print running info
time_step2 = datetime.datetime.now()
print (time_step2, "- A második rész sikeresen lefutott. A tömbök letárolásra kerültek a df1 táblába.")

############################################
# 3. lépés: Iroda linkeken végigmenni és legyűjteni az infókat ciklussal (df2 táblába)
############################################

n_loop=len(url_list) # hány ingatlant nézzen

# Részletes adatok legyűjtése
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Set up Chrome options
options = Options()
options.headless = True  # Set to True if you don't want to see the browser

# Initialize the lists to store the data (outside the loop)
link_array3 = []
garage_array = []
service_charge_array = []
category_array = []
description_array = []
image_array = []

# Initialize the WebDriver
driver = webdriver.Chrome(options=options)

# Navigate to the page
for i in range(n_loop):
    url = url_list[i]
    driver.get(url)
    # print(f"Successfully loaded: {url}")
   
    # Wait for the page to load fully
    wait = WebDriverWait(driver, 10)

    # Add the URL to the link array
    link_array3.append(url)
    
    # Garázsadatok
    try:
        element_garage = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.under-garage .div-block-111 div')))
        garage_text = element_garage[0].text if element_garage else "NA"
        garage_array.append(garage_text)
    except Exception as e:
        print(f"Error loading garage elements for URL {url}: {e}")
        garage_array.append("NA")
         
    # Szolgáltatási díj
    try:
        element_service_charge = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.property-page-list-item:nth-child(7) .div-block-111 > div:nth-child(1)')))
        service_charge_text = element_service_charge[0].text if element_service_charge else "NA"
        service_charge_array.append(service_charge_text)
    except Exception as e:
        print(f"Error loading service charge elements for URL {url}: {e}")
        service_charge_array.append("NA")
        
    # Kategória
    try:
        element_category = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.last .div-block-111 div')))
        category_text = element_category[0].text if element_category else "NA"
        category_array.append(category_text)
    except Exception as e:
        print(f"Error loading category elements for URL {url}: {e}")
        category_array.append("NA")
    
    # Leírás
    try:
        element_description = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p')))
        description_text = element_description[0].text if element_description else "NA"
        description_array.append(description_text)
    except Exception as e:
        print(f"Error loading description elements for URL {url}: {e}")
        description_array.append("NA")

    # Kép
    try:
        element_images = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.image-28')))  # Modify selector if needed
        image_links = [img.get_attribute("src") for img in element_images if img.get_attribute("src")]
        image_array.append(image_links if image_links else ["NA"])
    except Exception as e:
        print(f"Error loading images for URL {url}: {e}")
        image_array.append(["NA"])

# Close the driver
driver.quit()

############# print running info
time_step3 = datetime.datetime.now()
print (time_step3, "- A harmadik rész sikeresen lefutott. A df2 táblába mentésre kerültek az irodák részletes adatai.")
       
############################################
# 4. lépés:timestamp hozzáfézése a táblához (df2)
############################################

# for timestamp
now = datetime.datetime.now()
formatted_time = now.strftime("%Y-%m-%d %H:%M")
formatted_date = now.strftime("%Y-%m-%d")

# Combine into a pandas DataFrame
df2 = pd.DataFrame({
    'TimeStamp': formatted_time,
    'Link': link_array3,
    'Underground garage (EUR/place/month)': garage_array,
    'Service charge (EUR/m2/month)': service_charge_array,
    'Real Estate Category': category_array,
    'Description': description_array,
    'Image': image_array 
})

############# print running info
time_step4 = datetime.datetime.now()
print (time_step4, "- A negyedik rész sikeresen lefutott. Timestamp hozzáfűzve a df2 táblához.")

############################################
# 5. lépés: a két tábla összefűzése (df1: linkeket tartalmazza, alap infókkat, df2: részletesebb infók az ingatlanokról)
############################################
#df1 és df2 összevonása
df_all = pd.merge(df1, df2, on='Link')

# Specify the new column order
column_order = [
    'TimeStamp','Link', 'Name', 'Address', 'Office rent (EUR/m2/month)', 'Min availability (m2)', 
    'Max availability (m2)', 'City', 'District', 'Submarket',
    'Underground garage (EUR/place/month)', 'Service charge (EUR/m2/month)', 
    'Real Estate Category', 'Description', 'Image'
]

# Reorder the columns of df_all
df_all = df_all[column_order]

# df_all tábla kiíratása
df_all

############# print running info
time_step5 = datetime.datetime.now()
print (time_step5, "- Az ötödik rész sikeresen lefutott. Összefűzve a df1 és df2 tábla.")

