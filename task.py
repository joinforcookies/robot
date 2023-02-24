import time
import urllib.request
import os

from robot.api import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import io

# create a new instance of the Edge browser
browser = webdriver.Edge(executable_path="msedgedriver.exe")

# open a Google image search page and search for "puppy"
search_keyword = "puppy"
browser.get(f"https://www.google.com/search?q={search_keyword}&tbm=isch")

# wait for the search results to appear
time.sleep(5)

# create a folder to store the images
folder_name = "puppy_images"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# find the image elements and save the images to disk
image_elements = browser.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
for i, image_element in enumerate(image_elements):
    # click on the image to display the full-size version
    browser.execute_script("arguments[0].click();", image_element)
    time.sleep(1)
    
    # find the source URL of the image and save it to disk
    source_url = browser.find_element(By.CSS_SELECTOR, ".n3VNCb").get_attribute("src")
    if source_url.startswith("data:image"):
        continue  # ignore images that are in base64 format
    file_extension = os.path.splitext(source_url)[1]
    file_name = f"puppy_image_{i}"
    file_path = os.path.join(folder_name, file_name)
    
    # open the image using Pillow to convert it to the correct format
    with urllib.request.urlopen(source_url) as url:
        image_data = url.read()
    image = Image.open(io.BytesIO(image_data))
    if file_extension.lower() == ".png":
        file_path += ".png"
        image.save(file_path)
    else:
        file_path += ".jpg"
        image.convert("RGB").save(file_path)
    logger.info(f"Saved image {i} to {file_path}")
    
# close the browser
browser.quit()