import praw
import pyrebase

from config import config
firebase = pyrebase.initialize_app(config)
db = firebase.database()

reddit = praw.Reddit('bot1')
subreddits = db.child("subreddits").get()

for subreddit in subreddits.each():
    sub = reddit.subreddit(subreddit.key())
    for post in sub.hot(limit = 100):
        id = post.id
        if db.child("post_ids").child(id).get().val() == 1:
            continue
        upvotes = post.ups
        if upvotes < subreddit.val():
            continue
        title = post.title
        text = post.selftext
        url = post.url
        if "comments" in url:
            url = "null"
        data = {
        "id" : id,
        "title" : title,
        "text" : text,
        "url" : url
        }
        db.child("posts").child(subreddit.key()).push(data)
        db.child("post_ids").child(id).set(1)
