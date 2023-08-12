import re
from collections import Counter
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
extract=URLExtract()
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Fetch the number of messages
    num_messages = df.shape[0]

    # Fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Fetch the number of media messages (sticker omitted or media omitted)
    num_media_messages = df[df['message'].str.contains(r'(sticker|media|image|document) omitted', case=False, regex=True)].shape[0]

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

    return num_messages, len(words), num_media_messages,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'count': 'Percent', 'user': 'Name'})
    return x,df

def create_wordcloud(selected_user,df):

    f = open('chat1.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    excluded_words = ['sticker omitted', 'media omitted', 'image omitted', 'document omitted', 'omitted']

    words = []

    for message in df['message']:
        for word in message.lower().split():
            if word not in stop_words and word not in excluded_words:
                words.append(word)

    word_counts = Counter(words)
    most_common_df = pd.DataFrame(word_counts.most_common(20), columns=['Word', 'Count'])
    return most_common_df