from urlextract import URLExtract
extractor = URLExtract()

from wordcloud import WordCloud
from collections import Counter

import pandas as pd
import emoji

def fetch_stats(selected_user,df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]
    
    #Number pf Messages
    num_messages = df.shape[0]

    #Number of words
    words = []
    for message in df["message"]:
         words.extend(message.split())

    #Number of media files
    num_media = df[df["message"] == "<Media omitted>\n"].shape[0]

    #Number of Links Shared
    links = []
    for message in df["message"]:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media, len(links)


def most_active_user(df):
    top5 = df["users"].value_counts().head()
    df = round((df["users"].value_counts()/df.shape[0])*100,2).reset_index().rename(columns = {"index":"Names", "users": "Percentage Chat"})
    return top5,df

def create_wordcloud(selected_user,df):
    f = open("stop_word.txt", "r")
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    temp = df[df["users"] != "Group_Notification"]
    temp = temp[temp["message"] != "<Media omitted>\n"]

    def remove_stop_words(message):
        new = []
        for word in message.lower().split():
            if word not in stop_words:
                new.append(word)

        return " ".join(new)

    wc = WordCloud(width = 500, height = 500, min_font_size = 10, background_color = "grey")
    temp["message"] = temp["message"].apply(remove_stop_words)
    df_wc = wc.generate(temp["message"].str.cat(sep = " "))
    return df_wc

def top_words(selected_user,df):

    f = open("stop_word.txt", "r")
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    temp = df[df["users"] != "Group_Notification"]
    temp = temp[temp["message"] != "<Media omitted>\n"]

    words = []

    for message in temp["message"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20))

def num_emojis(selected_user,df):
    emoji1 = []
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    for message in df["message"]:
        emoji1.extend([i for i in message if i in emoji.UNICODE_EMOJI["en"]])

    return pd.DataFrame(Counter(emoji1).most_common(len(Counter(emoji1)))).head(10)

def monthly_chat(selected_user,df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    timeline = df.groupby(["year","month_num","month"]).count()["message"].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["month"][i] + "-" + str(timeline["year"][i]))

    timeline["time"] = time
    return timeline

def active_day(selected_user,df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]
        
    return df["day_name"].value_counts()


def active_month(selected_user,df):
    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    return df["month"].value_counts() 

def activity_heatmap(selected_user,df):

    if selected_user != "Overall":
        df = df[df["users"] == selected_user]

    pivot = df.pivot_table(index = "day_name", columns = "period", values = "message", aggfunc = "count").fillna(0)

    return pivot