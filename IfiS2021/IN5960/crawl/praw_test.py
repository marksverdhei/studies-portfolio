import praw
import psaw
import os
import IPython
import pandas as pd
import numpy as np
import pickle
from cred import id, secret, username, password, user_agent

if os.path.isfile("posts.pickle"):
    with open("posts.pickle", "rb") as f:
        post_dict = pickle.load(f)
else:
    post_dict = {}

reddit = praw.Reddit(
    client_id=id,
    client_secret=secret,
    username=username,
    password=password,
    user_agent=user_agent
)

sr_name = "savedyouaclick"

api = psaw.PushshiftAPI(reddit)

data = list(api.search_submissions(subreddit=sr_name, limit=7000))
print(data)
# sr = reddit.subreddit(sr_name)
# postit = subreddit.new(limit=None)
post_dict = {p.id: p for p in data}
print(len(post_dict))
# def extend_post_dict(iterator):
#     size = len(post_dict)
#     post_dict.update((p.id, p) for p in iterator)
#     delta = len(post_dict) - size
#     print("Extended dict by", delta, "elements")
#
# IPython.embed()
#
with open("posts5k.pickle", "wb+") as f:
    pickle.dump(post_dict, f)
# posts = list(postit)
# print("saved posts.pickle")
#
# df = pd.DataFrame({"title": [p.title for p in posts], "url": [p.url for p in posts]})
#
# df.to_csv("reddit_data.tsv", sep="\t", index=False)
