# from requests_html import HTMLSession
#
# if __name__ == '__main__':
#     # Create the session
#     session = HTMLSession()
#
#     # Define your hashtag
#     tag = 'topupshopeepay'
#
#     # Use the session to get the data
#     r = session.get(f'https://www.instagram.com/explore/tags/{tag}/')
#
#     # Render the page, up the number on scrolldown to page down multiple times on a page
#     r.html.render(sleep=1, keep_page=True, scrolldown=50)
#
#     # Get different categories of posts ("Top posts" and "Most recent")
#     posts = r.html.find('h2.yQ0j1 ~ div')
#
#     # If the list of posts categories is not empty,
#     if posts:
#
#         # Get the "Most reent" category of posts
#         most_recent_posts = posts[1]
#
#         for post in most_recent_posts.find('div.Nnq7C.weEfm > div.v1Nh3.kIKUG._bz0w'):
#
#             # Get the post's url
#             link = post.find('a', first=True).attrs['href']
#
#             # Get the post's image source
#             image_src = post.find('img[crossorigin=anonymous]', first=True).attrs['src']
#
#             # Use the session to post data
#             r_post = session.get(f'https://www.instagram.com{link}')
#
#             # Get username
#             username = r_post.html.find('a.sqdOP.yWX7d._8A5w5.ZIAjV', first=True).text
#
#             # Get number of likes
#             if r_post.html.find('div._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll', first=True) is not None:
#                 try:
#                     liked_by = r_post.html.find('div._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll', first=True).text
#                     if 'Liked by' in liked_by:
#                         num_likes = len(r_post.html.find('div._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll a', first=True))
#                 except:
#                     r_post.html.find('div._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll > a > div', first=True).text:
#
#             # if 'Liked by' in r_post.html.find('div._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll', first=True).text:
#             #
#             #     # E.g: Liked by ming_deng_09 and 1 other
#             #     num_likes = len(r_post.html.find('div._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll a', first=True))
#             #
#             # elif "likes" in r_post.html.find('div._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll > a > div', first=True).text:
#             #     pass
#             div._7UhW9.xLCgt.MMzan.KV - D4.uL8Hv.T0kll > a > div
#
