import feedparser
import urllib.request, urllib.parse, urllib.error
from twython import Twython
from bs4 import BeautifulSoup
import os
from configparser import SafeConfigParser
images = 'none'

parser = SafeConfigParser()
parser.read('feeds.cfg')
parser.read('auth.cfg')
#Import connection keys for Twitter from configuration file
cfg = {}
for item in parser.options('auth_info'):
    item_config = parser.get('auth_info', item)
    cfg[item] = item_config

#Download the image file from the blog if it was determined there is one
#Writes the file to a temporary local file to upload to Twitter later.
def download(url):
    f = urllib.request.urlopen(images)
    data = f.read()
    with open(local_file, 'wb') as code:
        code.write(data)

#Function to actually send the tweet.  If there is an image file associated,
#it is uploaded to the twitter image service and tweeted out on the else branch
def go_tweet():
    twitter = Twython(cfg['consumer_key'], cfg['consumer_secret'],
                        cfg['access_token'], cfg['access_token_secret'])
    tweet= '#STARTTAG: ' + title + ' ' + d.entries[0].link + ' via ' + name

#Tweet context if no images are in the post
    if images == 'none':
        try:
            twitter.update_status(status = tweet)
        except TwythonError as e:
            print (e)

#Tweet using this if images are in the post
    else:
        tweet_file = open(local_file, 'rb')
        response = twitter.upload_media(media=tweet_file)
        twitter.update_status(status = tweet, media_ids=[response['media_id']])


#Define feeds to check for new posts, key is the Twitter handle of the author
edm_feeds = {}

#imports variables from configuration file
for user in parser.options('feeds'):
    feedurl = parser.get('feeds', user)
    edm_feeds[user] = feedurl

#cycles through each feed defined in edm_feeds and checks for new content
for name in edm_feeds.keys():
    d=feedparser.parse(edm_feeds[name])

#Open tracking file and create variable to determine if the page has been
#promoted yet.
    filename = 'feedstats.txt'
    with open(filename) as file_object:
        lines = file_object.readlines()
        url_string = ''
    for line in lines:
        url_string += line.rstrip()

#Setting post to the link for the first entry.  Later check and verify whether
#this link has been promoted already.
    post = d.entries[0].link

    if post in url_string:
        print('No new entries.')
    else:
        print (d.entries[0].link)
        #Sets the total tweet_lenght (before title is added) to the length
        #of the author's user name plus the 40 characters in the tweet text.
        #Sets the max length of the title to 130 - that.
        tweet_length = len(name) + 40
        max_title = 130-tweet_length
        title = d.entries[0].title

        #Grabs the name of the first image file in the post
        statusupdate = d.entries[0].content
        images = BeautifulSoup(statusupdate[0]['value'],"html.parser")
        try:
            images = images.find("img")["src"]
        except:
            images = "none"
        #If there is an image associated with the post, decrease the max_title
        #size to accomodate the image URL, set the local file name based on the
        #suffix of the image file, call the function to download the image.
        if images != 'none':
            max_title = max_title - 23
            file_type = (images[-3:])
            local_file = 'tempfile.' + file_type
            download(images)

        #If the title is too long, truncate it.
        if len(title) > max_title:
            title = title [0:max_title]
            title = title + '... '

        #Call the function to submit the Twitter update
        go_tweet()

        #Write the URL of the tweeted post to the tracking file
        with open(filename, 'a') as file_object:
            file_object.write(d.entries[0].link + '\n')
        #delete the temporary local image file
        if images != 'none':
            os.remove(local_file)
