import praw
from praw.models import MoreComments
import pandas as pd
import numpy as np
import random
import re
from pmaw import PushshiftAPI
import datetime as dt
from datetime import datetime
from datetime import date
import config

reddits = pd.read_csv('/Users/elishillman/Documents/Bantr/reddit_shows.csv')
reddits.columns = ['Show', 'Sub']

reddits['Normal_Sub'] = reddits['Sub'].str.replace("r/",'').str.lower()

reddit = praw.Reddit(
    client_id=config.client_id,
    client_secret=config.client_secret,
    password=config.password,
    user_agent=config.user_agent,
    username=config.username,
)

def getActive(row):
    try:
        subreddit = reddit.subreddit(row['Normal_Sub'])
        return subreddit.active_user_count
    except:
        return 0
    
reddits['Active Users'] = reddits.apply(lambda row: getActive(row), axis = 1)
currentDateAndTime = datetime.now()
currentTime = currentDateAndTime.strftime("%m-%d-%Y, %H:%M:%S")
active_df = pd.DataFrame()
active_df['Show'] = reddits['Show']
active_df[f'{currentTime}'] = reddits['Active Users']

updated = pd.read_csv('/Users/elishillman/Documents/Bantr/Active_users/Actives.csv')
updated[f'{currentTime}'] = active_df[f'{currentTime}']
updated.to_csv('/Users/elishillman/Documents/Bantr/Active_users/Actives.csv', index=False)
