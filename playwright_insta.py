from playwright.sync_api import sync_playwright
from Password import my_username, my_pwd
import time
import csv
import os


def login(page):
    if page.wait_for_selector("//input[@name='username']") is not None:
        page.fill(selector="input[name=username]", value=my_username)  # Fill in the instagram username field
        page.fill(selector="input[name=password]", value=my_pwd)  # Fill in the instagram password field
        page.click(selector="button[type=submit]")  # Click the login button

        # Choose "Not Now" button
        '''
        You might get 2 pop-up alerts. Please adjust the codes below accordingly
        '''
        page.wait_for_selector('//button[contains(text(), "Not Now")]').click()
        page.wait_for_selector('//button[contains(text(), "Not Now")]').click()


def hashtag_search(page):
    # Target the search input field
    search_box = page.wait_for_selector("//input[@placeholder='Search']")

    # Search for the hashtag
    hashtag = "#topupshopeepay"
    search_box.fill(value=hashtag)

    # FIXING THE DOUBLE ENTER
    my_link = page.wait_for_selector("//a[contains(@href, '/" + hashtag[1:] + "/')]")
    my_link.click()
    time.sleep(4)


def scroll(page, posts):
    def store_post_links(anchors_list):
        # Loop through all the links and add them to the list variable "posts"
        for anchor in anchors_list:
            # Get the href attribute of the anchor
            href = anchor.get_attribute(name="href")
            href = f"https://www.instagram.com{href}"
            # Append the href to the list
            posts.append(href)

    # Scroll down the page
    page.evaluate(
        """
        var intervalID = setInterval(function () {
            var scrollingElement = (document.scrollingElement || document.body);
            scrollingElement.scrollTop = scrollingElement.scrollHeight;
        }, 2000);
        """
    )

    # page.keyboard.press("PageDown")
    # time.sleep(3)
    # # Wait for the page to load all the posts and then scrape the posts links
    # page.wait_for_selector("div.EZdmt ~ div > div > div.Nnq7C.weEfm a")
    # anchors = page.query_selector_all("div.EZdmt ~ div > div > div.Nnq7C.weEfm a")
    # store_post_links(anchors)

    # for x in range(130):
    #     print(f"Scrolling down {x} times")
    #     page.keyboard.press("PageDown")
    #     time.sleep(2)
    #     # Wait for the page to load all the posts and then scrape the posts links
    #     page.wait_for_selector("div.EZdmt ~ div > div > div.Nnq7C.weEfm a")
    #     anchors = page.query_selector_all("div.EZdmt ~ div > div > div.Nnq7C.weEfm a")
    #     store_post_links(anchors)
    #     time.sleep(1)

    prev_height = None
    while True:
        # Wait for the page to load all the posts and then scrape the posts links
        page.wait_for_selector("div.EZdmt ~ div > div > div.Nnq7C.weEfm a")
        anchors = page.query_selector_all("div.EZdmt ~ div > div > div.Nnq7C.weEfm a")
        store_post_links(anchors)

        curr_height = page.evaluate('(window.innerHeight + window.scrollY)')
        if not prev_height:
            prev_height = curr_height
            time.sleep(8)

        elif prev_height == curr_height:
            page.evaluate('clearInterval(intervalID)')
            break

        else:
            prev_height = curr_height
            time.sleep(8)


def scrap_posts_links(page, posts):
    scroll(page, posts)  # Scroll down the page and scrape each post link at the same time


def scrap_post_info(context, posts, count, row_list):
    new_page = context.new_page()  # Create a new tab
    new_page.goto(posts[count], timeout=0)  # Go to the post link
    new_page.wait_for_load_state()  # Wait for the page to load

    print(f"Scraping post {count + 1} of {len(posts)}: {new_page.url}")
    # Get the post url
    post_url = new_page.url

    # Get the username of the poster
    username = None
    if new_page.query_selector(selector="header.Ppjfr span > a") is not None:
        username = new_page.query_selector(selector="header.Ppjfr span > a").inner_text()

    # Get the post's total likes
    total_likes = None
    if new_page.query_selector(selector="section.EDfFK.ygqzn div._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll") is not None:
        if "Be the first to" in new_page.query_selector(
                selector="section.EDfFK.ygqzn div._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll").inner_text():
            total_likes = 0
        elif "Liked by" in new_page.query_selector(
                selector="section.EDfFK.ygqzn div._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll").inner_text():
            total_likes = 2
        elif "" in new_page.query_selector(
                selector="section.EDfFK.ygqzn div._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll").inner_text():
            total_likes = 0
        elif new_page.query_selector(
                selector="section.EDfFK.ygqzn div._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll div").inner_text() == "1 like":
            total_likes = 1
        else:
            if "likes" in new_page.query_selector(
                    selector="section.EDfFK.ygqzn div._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll div").inner_text():
                total_likes = new_page.query_selector(
                    selector="section.EDfFK.ygqzn div._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll div span").inner_text()
    else:
        total_likes = 0

    # Get the post's posted date
    post_upload_date = new_page.query_selector(selector="time._1o9PC").get_attribute(name="datetime")[:10]

    row_list.append([post_url, username, total_likes, post_upload_date])

    new_page.close()  # Close the tab


def remove_duplicates(posts):
    if len(posts) != len(set(posts)):
        # Remove duplicate links
        posts = list(dict.fromkeys(posts))
    return posts


def run(p):
    browser = p.chromium.launch(headless=False, slow_mo=50)
    postListContext = browser.new_context()
    page = postListContext.new_page()
    page.goto("https://www.instagram.com/")  # Open the instagram webpage

    login(page)  # Login to instagram
    hashtag_search(page)  # Search for the hashtag

    posts = []  # Create a list variable to store the post links

    scrap_posts_links(page, posts)  # Scrap the post links

    # Remove duplicates in list
    posts = remove_duplicates(posts)

    # Print the total posts that have been collected and the list of posts links
    print(f"Total posts: {len(posts)}\n")
    for index, post in enumerate(posts):
        print(f'{index + 1}: {post}')

    print("\n+--------------------------------------------------------------------+")
    print("|                      START SCRAPING EACH POST                      |")
    print("+--------------------------------------------------------------------+")
    row_list = [['Post URL', 'Username', 'Total Likes', 'Post Upload Date']]
    for count, post in enumerate(posts, start=0):
        time.sleep(1)
        scrap_post_info(postListContext, posts, count, row_list)

    # If the text file exists, clear the contents of the file
    if os.path.isfile("topupshopeepay.csv"):
        open('topupshopeepay.csv', 'w').close()

    # Store the results in the csv file
    with open('topupshopeepay.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_list)


with sync_playwright() as playwright:
    run(playwright)
