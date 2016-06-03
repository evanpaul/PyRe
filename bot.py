#!/usr/bin/env python
# A simple call-and-response bot
# TO DO:
# - Detailed Logs
# - Save phrase and reply to new section of config file
import praw
import api_auth
import time

SLEEP_TIME = 10 # Time to sleep between searches in seconds
results = open("results.txt", "a")
matches = 0
# Parse saved API refresh token
r = api_auth.get_info()
f = open('token.txt', 'r')
refresh_token = f.readline().strip()
r.refresh_access_information(refresh_token) # Refresh API access

user = r.get_me()
print "Logged in as", user.name

# Popular subreddits to avoid because of bot policies
disallowed = [
    "AdviceAnimals",
    "anime",
    "askhistorians",
    "askscience",
    "askreddit",
    "aww",
    "cosplay",
    "depression",
    "forwardsfromgrandma",
    "geckos",
    "giraffes",
    "gifs",
    "grindsmygears",
    "me_irl",
    "misc",
    "movies",
    "news",
    "pics",
    "politicaldiscussion",
    "politics",
    "science",
    "suicidewatch",
    "talesfromtechsupport",
    "torrent",
    "torrents",
    "trackers"
]

checked = [] # Comments that have already been checked (shouldn't really be an issue with /r/all, but just to be sure)
# Change these to fit your usecase
target = "sneak peak"
reply_string = "Sneak peek*\n\nhttp://theoatmeal.com/comics/sneak_peek\n\n---\n*I am a bot, report any misfires or complaints via private message to /u/StealthSummit*"
total = 0
# Main loop
while True:
    print "Fetching..."
    count = 0
    comments = praw.helpers.flatten_tree(r.get_comments("all", sort = "new", limit = 1000)) # Grabs up to 1000 latest comments
    for comment in comments:
        count+=1
        if target in comment.body.lower() and comment.submission.subreddit not in disallowed and comment.id not in checked:
            print "Match found!"
            matches += 1
            print comment.permalink
            results.write(comment.permalink)
            comment.reply(reply_string)
        checked.append(comment.id)
        print comment.id,"..."
    total += count
    print "Checked",count,"comments"
    print matches, "matches so far"
    print total, "comments checked this session"
    # Flush buffer every so often
    if len(checked) > 2400:
        checked = []
    print "Sleeping for:",SLEEP_TIME,"seconds"
    time.sleep(SLEEP_TIME)

results.close()
