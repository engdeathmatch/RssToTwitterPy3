# RssToTwitterPy3
Watches multiple RSS feeds and publishes updates to Twitter. Written in Python3.  Includes the first image found on the post in the tweet when posting to Twitter.

Installation
------------
1. Ensure you have the following packages installed:
 - feedparser
 - twython
 - bs4
 - configparser
2. Create a Twitter API app
3. Edit Twitter settings in auth.txt
4. Edit RSS feeds to monitor in feeds.txt
5. Update tweet variable (line 31) with any specific text you'd like to tweet out with the post.

Output
------
When run manually, if no entries are found for a feed, it will output:

> No entries found.

If a new post is found, it will display the link of that post before tweeting out the message.

To Do
-----
While everything generally works, I haven't done much with the error handling on this yet.  If something happens that is unexpected, the application does not currently gracefully handle it.
