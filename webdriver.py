from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import io

def by_id(driver, id_):
    return driver.find_element(by=By.ID, value=id_)

cService = webdriver.FirefoxService(executable_path='/usr/bin/geckodriver')
driver = webdriver.Firefox(service = cService)

driver.get("file:///home/k/Documents/Web/fonts/index.html")

screenshot = driver.get_screenshot_as_png()

element = by_id(driver, "content")

# Cropping
x, y = element.location['x'], element.location['y']
width, height = element.size['width'], element.size['height']
imageStream = io.BytesIO(screenshot)
image = Image.open(imageStream)
image = image.crop((int(x), int(y), int(width + x), int(height + y)))
image.save('./Screenshots/1.png')

driver.quit()
