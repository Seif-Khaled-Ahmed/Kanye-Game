from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import cv2
import pytesseract
import random
from PIL import Image
import re
import requests
import json

def download_all_images(driver) -> None:
    links = []
    line_number = 0
    with open("../media/links.txt", "r") as file:
        for file in file.readlines():
            links.append((line_number, file.replace("\n", "")))
            line_number += 1
    
    for i in range(len(links)):
        #https://imgur.com/a/evWz7eW
        new_link = "https://api.imgur.com/post/v1/albums/" + links[i][1].split(".com")[1][3:]
        download_image(new_link, links[i][0])

def download_image(link: str, file_path: str) -> None:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36",
            "Referer": "https://imgur.com/",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "no-cors",
            "Sec-Fetch-Dest": "image",
        }

        params = {
            "client_id": "546c25a59c58ad7",
            "include": "media,adconfig,account,tags"
        }

        response = requests.get(link, params=params, headers=headers)

        response = json.loads(response.text)

        link = response["media"][0]["url"]

        params = {"maxwidth": 760, "fidelity": "grand"}

        response2 = requests.get(link, headers=headers, params=params)

        with open(f"../media/{file_path}.png", "wb") as file:
            file.write(response2.content)
    except:
        print(link)
def get_links(file_path: str) -> list[str]:
    """Uses Selenium to retrieve all the image links"""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f"https://www.reddit.com/r/hiphopheads/comments/1ijrgho/kanye_wests_rant_february_56_2025_kanye_expresses/")

    div = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, """//*[@id="t3_1ijrgho-post-rtjson-content"]"""))
    )
    
    p_list = div.find_elements(By.TAG_NAME, "p")
    
    links = []
    for i in range(len(p_list)):
        try:
            a_tag = p_list[i].find_element(By.XPATH, f"/html/body/shreddit-app/div[2]/div[1]/div/main/shreddit-post/div[2]/div/div/p[{i+1}]/a")
            href = a_tag.get_attribute("href")
            print(href)
            links.append(href)
        except:
            continue

    driver.quit()

    with open(file_path, "w", encoding="utf-8") as file:
        for link in links:
            file.writelines(link + "\n")

    return links

def hide_random_word(image_path, output_path="output.png"):
    num = 1

    # pytesseract.pytesseract.tesseract_cmd = r'../tesseract/tesseract.exe'
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    blacklist = {"ye", "kanyewest", "twitter", "views", "edited", "edite", "am", "pm", "oq", "qo", "about", "tweet", "privacy", "rules", "help", "emerald", "get t", "they", "than", "then", "with", "corn", "man", "the", "this", "last","what"}  

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    d = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

    words = d['text']

    ye = False
    valid_words = []
    for i in range(len(words)):
        word = words[i].strip().lower()
        
        if word == "@kanyewest":
            ye = True

        if len(word) <= 3 or word in blacklist or not re.match(r'^[a-zA-Z]+$', word) or ye == False:
            continue

        valid_words.append((i, words[i]))


    if len(valid_words) < 1:
        print("No words detected!")
        return("No words detected!")

        return
    
    percentage_to_hide = 0.25

    num = round(len(valid_words) * percentage_to_hide)

    num = max(1, min(len(valid_words), num))

    selected_words = []
    for i in range(num):
        index, selected_word = random.choice(valid_words)
        valid_words.remove((index, selected_word))
        selected_words.append((index, selected_word))

        words_to_remove = []
        for valid_word in valid_words:
            if valid_word[0] == index + 1 or valid_word[0] == index - 1:
                words_to_remove.append(valid_word)

        for word in words_to_remove:
            valid_words.remove(word)


        # Get bounding box of the selected word
        x, y, w, h = d['left'][index], d['top'][index], d['width'][index], d['height'][index]

        # Draw a white box over the word
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), -1)

    cv2.imwrite(output_path, image)

    selected_words.sort(key=lambda x: x[0])

    words = dict()


    for i in range(len(selected_words)):
        words[str(i)] = selected_words[i][1]

    return words
if __name__ == "__main__":
    # chrome_options = Options()
    # chrome_options.add_argument("--headless=new")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # driver = webdriver.Chrome(options=chrome_options)

    # download_all_images(driver)
    #get_links("../media/links.txt")


    # driver.quit()
    
    img_id = random.randint(0, 190)
    print(img_id)
    hide_random_word(f"../media/{img_id}.png", output_path=f"output_{img_id}.png")

