import os
import time
from Password import my_username, my_pwd
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def login():
    # Target username and password
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    # Enter username and password
    username.clear()
    username.send_keys(my_username)
    password.clear()
    password.send_keys(my_pwd)

    # Target the login button and click it
    WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    # Choose "Not Now" button
    ''' You might get 2 pop-up alerts. Please adjust the codes below accordingly '''
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()  # alert1
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()  # alert2


def hashtag_search():
    # Target the search input field
    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
    search_box.clear()

    # Search for the hashtag cat
    keyword = "#topupshopeepay"
    search_box.send_keys(keyword)

    # FIXING THE DOUBLE ENTER
    my_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/" + keyword[1:] + "/')]")))
    my_link.click()
    time.sleep(6)  # Wait 6 seconds for the page to load


def store_post_links(anchors_list):
    # Loop through all the links and add them to the list variable "posts"
    for anchor in anchors_list:
        # Get the href attribute of the anchor
        href = anchor.get_attribute("href")
        # Append the href to the list
        posts.append(href)


def scroll_scrap_posts():
    SCROLL_PAUSE_TIME = 5
    last_height = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")  # Scroll down to the bottom of the page
    time.sleep(SCROLL_PAUSE_TIME)  # Wait to load page
    # Target all the link elements on the page
    anchors = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.EZdmt ~ div > div > div.Nnq7C.weEfm a")))
    store_post_links(anchors)
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        # Target all the link elements on the page
        anchors = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.EZdmt ~ div > div > div.Nnq7C.weEfm a")))
        store_post_links(anchors)

        # Update the last height
        last_height = new_height

    # for count in range(300):
    #     # Scroll down to bottom
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #
    #     # Wait to load page
    #     time.sleep(SCROLL_PAUSE_TIME)
    #
    #     # Target all the link elements on the page
    #     anchors = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.EZdmt ~ div > div > div.Nnq7C.weEfm a")))
    #     store_post_links(anchors)


def store_posts_url(posts_urls):
    # If the text file exists, clear the contents of the file
    if os.path.isfile("post_url.txt"):
        open('post_url.txt', 'w').close()

    # Store the post links into a text file
    with open('post_url.txt', 'a') as f:
        for post_url in posts_urls:
            if type(post_url) is str:
                f.write(post_url)
                f.write('\n')


options = webdriver.ChromeOptions()  # Create a new Chrome session
driver_path = os.path.join(os.path.dirname(__file__), 'chromedriver.exe')  # Path to the chromedriver.exe
driver = webdriver.Chrome(options=options, executable_path=driver_path)  # Launch Chrome driver with the options

driver.get('https://www.instagram.com/')  # Open the instagram webpage
driver.maximize_window()  # Maximize browser window
login()  # Login to instagram
hashtag_search()  # Search for the hashtag
posts = []  # Create a list to store the post links
scroll_scrap_posts()  # Scroll down and scrape the post links

if len(posts) != len(set(posts)):
    posts = list(dict.fromkeys(posts))  # Remove duplicate links

# Print the total posts that have been collected and the list of posts links
print(f"Total posts: {len(posts)}\n")
for index, post in enumerate(posts):
    print(f'{index + 1}: {post}')

store_posts_url(posts)  # Store the post links into a text file
