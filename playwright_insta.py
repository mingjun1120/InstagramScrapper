from playwright.sync_api import sync_playwright
from Password import my_username, my_pwd
import time


def login(page):
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

            # Wait for the page to load all the posts and then scrape the posts links
            page.wait_for_selector("div.EZdmt ~ div > div > div.Nnq7C.weEfm a")
            anchors = page.query_selector_all("div.EZdmt ~ div > div > div.Nnq7C.weEfm a")
            store_post_links(anchors)

        elif prev_height == curr_height:
            page.evaluate('clearInterval(intervalID)')
            break

        else:
            prev_height = curr_height
            time.sleep(8)


def scrap_posts_links(page, posts):
    scroll(page, posts)


def run(p):
    browser = p.chromium.launch(headless=False, slow_mo=50)
    page = browser.new_page()
    page.goto("https://www.instagram.com/")  # Open the instagram webpage

    login(page)  # Login to instagram
    hashtag_search(page)  # Search for the hashtag

    # Create a list variable to store the post links
    posts = []

    scrap_posts_links(page, posts)  # Scrap the post links

    if len(posts) != len(set(posts)):
        # Remove duplicate links
        posts = list(dict.fromkeys(posts))

    # Print the total posts that have been collected and the list of posts links
    print(f"Total posts: {len(posts)}\n")
    for index, post in enumerate(posts):
        print(f'{index + 1}: {post}')


with sync_playwright() as playwright:
    run(playwright)
