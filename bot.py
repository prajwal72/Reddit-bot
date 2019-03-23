import praw
import pyrebase

from config import config
firebase = pyrebase.initialize_app(config)
db = firebase.database()

reddit = praw.Reddit('bot1')
subreddits = ['memes', 'jokes', 'funny']

for subreddit in subreddits:
    sub = reddit.subreddit(subreddit)
    for post in sub.hot(limit = 100):
        id = post.id
        if db.child("post_ids").child(id).get().val() == 1:
            continue
        upvotes = post.ups
        if upvotes < 1000:
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
        db.child("posts").child(subreddit).push(data)
        db.child("post_ids").child(id).set(1)
