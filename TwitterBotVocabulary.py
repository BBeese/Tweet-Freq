import tweepy
from tweepy import OAuthHandler

import matplotlib.pyplot as plt


def string_cleaning(s):
    string = ""
    for char in s.lower():
        if (ord(char) > 122) or ((ord(char) < 97) and (char != "'")) or ("https://" in s):
            continue
        else:
            string = string + char

    return string


def authenticate():
    app_key = "ikZS64uOU2yVSsvteK3PQqxLc"
    app_secret = "TYEeT3cZDlvvs1nqUnlb6rTOLlESMLCJacDGbCZVCr7fjIR858"
    auth_token = "452468893-MN2lZaifrqXPe6kl9YLScKhncnexJZ6wazccfgma"
    auth_secret = "MU80whUp1wUQ3D4hsrDnU57VjxmndyxFtj4twR3UEBQDp"

    auth = OAuthHandler(app_key, app_secret)
    auth.set_access_token(auth_token, auth_secret)

    api = tweepy.API(auth)

    return api


def graph(word_count, words, values, handle):
    plt.figure(figsize=(7, 7))
    plt.style.use("seaborn-white")
    plt.xticks(word_count, words, rotation="vertical", size=10, fontname="Arial")
    plt.bar(word_count, values, color="green", width=.25)
    plt.title("@%s's Tweet Vocabulary" % handle, fontweight="bold", fontname="Arial")
    plt.ylabel("Frequency", fontname="Arial")
    plt.xlabel("Words")
    plt.show()

    return


def main():
    api = authenticate()
    handle = str(input("Enter the user's twitter handle: @"))
    raw_tweets = []

    for tweet in tweepy.Cursor(api.user_timeline, screen_name=handle).items(3000):
        # Make sure tweet isn't a retweet
        if tweet.text[0:2] != "RT":
            raw_tweets.append(tweet.text)

    word_dict = {}
    for tweets in raw_tweets:
        tweets = tweets.lower().split()
        for word in tweets:
            word = string_cleaning(word)
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1

    word_list = []
    count = 0
    for key in word_dict:
        # '4' is an arbitrary word length constraint
        if (key == "") or (len(key) <= 4):
            continue
        else:
            # Puts dictionary values into 2d List
            appender = [key]
            word_list.append(appender)
            word_list[count].append(word_dict[key])
            count += 1

    # Sorts by values
    word_list = sorted(word_list, key=lambda l: l[1], reverse=True)

    words = []
    values = []

    # Strips dictionary into two lists
    for i in range(len(word_list)):
        words.append(word_list[i][0])
        values.append(word_list[i][1])

    if len(words) > 15:
        words = words[0:15]
        values = values[0:15]

    graph(range(len(words)), words, values, handle)

    # TODO: Handle @'s, Style the plot better
    # TODO: Unit Tests
    # TODO: MAYBE: fill a list with common boring words?
    # TODO: MAYBE: Error handling (@ name doesn't exist, not enough tweets/words, etc)


main()
