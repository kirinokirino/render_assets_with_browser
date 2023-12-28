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
font_names = set()
lable_font_names = set()
with open('assets.csv') as csvfile:
    print("reading assets.csv:")
    reader = csv.reader(csvfile)
    next(reader, None)
    for lable in reader:
        new_lable = {"text": lable[0].strip(), "font": lable[1].strip()}
        lable_font_names.add(lable[1].strip())
        assets["lables"].append(new_lable)
print(assets["lables"])

with open('fonts.csv') as csvfile:
    print("reading fonts.csv:")
    reader = csv.reader(csvfile)
    next(reader, None)
    for font in reader:
        new_font = {"font": font[0].strip(), "link": font[1].strip()}
        font_names.add(font[0].strip())
        assets["fonts"].append(new_font)
print(assets["fonts"])

if len(lable_font_names - font_names) > 0:
    print("WARNING: Fonts used in lables, that are not found in fonts table: " + str(lable_font_names - font_names))

if len(font_names - lable_font_names) > 0:
    print("WARNING: Unused fonts: " + str(font_names - lable_font_names))

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

# Unhide selected element, make a screenshot, crop it, save it, hide it again
element = by_id(driver, "content")
button = by_id(driver, "next_button")
for i in range(len(assets["lables"])):
    screenshot = driver.get_screenshot_as_png()

    print("cropping the screenshot")
    x, y = element.location['x'], element.location['y']
    width, height = element.size['width'], element.size['height']
    imageStream = io.BytesIO(screenshot)
    image = Image.open(imageStream)
    image = image.crop((int(x), int(y), int(width + x), int(height + y)))
    image.save('./Screenshots/' + str(i) + '.png')
    button.click()

print("quitting the webdriver")
driver.quit()
