from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import io
import jinja2
import csv

def by_id(driver, id_):
    return driver.find_element(by=By.ID, value=id_)

# font.link lable.font lable.text
assets = {"lables": [], "fonts": []}
with open('assets.csv') as csvfile:
    print("reading assets.csv:")
    reader = csv.reader(csvfile)
    next(reader, None)
    for lable in reader:
        new_lable = {"text": lable[0], "font": lable[1]}
        assets["lables"].append(new_lable)
print(assets["lables"])

with open('fonts.csv') as csvfile:
    print("reading fonts.csv:")
    reader = csv.reader(csvfile)
    next(reader, None)
    for font in reader:
        new_font = {"font": font[0], "link": font[1]}
        assets["fonts"].append(new_font)
print(assets["fonts"])

print("loading jinja2 environment")
jinja = jinja2.Environment(loader=jinja2.FileSystemLoader("./"))
print("loading template")
template = jinja.get_template("template.html")
context = {
    "fonts": assets["fonts"],
    "lables": assets["lables"],
}
print("context is ", context)

with open("rendered_template.html", mode="w") as rendered:
    print("rendering the template")
    rendered.write(template.render(context))

print("launching webdriver")
cService = webdriver.FirefoxService(executable_path='/usr/bin/geckodriver')
driver = webdriver.Firefox(service = cService)
driver.get("file:///home/k/Documents/Web/fonts/rendered_template.html")
screenshot = driver.get_screenshot_as_png()

print("cropping the screenshot")
element = by_id(driver, "content")
x, y = element.location['x'], element.location['y']
width, height = element.size['width'], element.size['height']
imageStream = io.BytesIO(screenshot)
image = Image.open(imageStream)
image = image.crop((int(x), int(y), int(width + x), int(height + y)))
image.save('./Screenshots/1.png')

print("quitting the webdriver")
driver.quit()
