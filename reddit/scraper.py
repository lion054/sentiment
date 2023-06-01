import praw

def scrape(location, topic, limit, time='week'):
    reddit = praw.Reddit(client_id='74Y8VMJuD6BArg',
                        client_secret="ku-1jR_kGEa2Pk92CMIRf4nzuYY", password='hackvengers',
                        user_agent='pls give me a job', username='csehack')

    text = []
    for submission in reddit.subreddit(location).search(topic, time_filter=time, sort='top', limit=limit):
        text.append(submission.title)
        if submission.is_self:
            text.append(submission.selftext)
    return text

scrape("australia", "Kevin Rudd", 20, 'all')