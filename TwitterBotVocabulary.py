import tweepy
from tweepy import OAuthHandler

import matplotlib.pyplot as plt


def string_cleaning(s):
    """
    :param s: String
    :return: a 'clean' version of s, containing only lowercase letters.
    """

    string = ""
    for char in s.lower():
        if (ord(char) > 122) or ((ord(char) < 97) and (char != "'")) or ("https://" in s):
            continue
        else:
            string = string + char

    return string


def authenticate():
    """
    :return: Verified object
    Authenticates credentials against Twitter's services.
    """

    app_key = "ikZS64uOU2yVSsvteK3PQqxLc"
    app_secret = "TYEeT3cZDlvvs1nqUnlb6rTOLlESMLCJacDGbCZVCr7fjIR858"
    auth_token = "452468893-MN2lZaifrqXPe6kl9YLScKhncnexJZ6wazccfgma"
    auth_secret = "MU80whUp1wUQ3D4hsrDnU57VjxmndyxFtj4twR3UEBQDp"

    auth = OAuthHandler(app_key, app_secret)
    auth.set_access_token(auth_token, auth_secret)

    api = tweepy.API(auth)

    return api


def graph(word_count, words, values, handle):
    """
    :param word_count: Int; how many words are graphed on the x-axis
    :param words: List of Strings; words being plotted on x-axis
    :param values: List of Ints; counts of each corresponding words in 'words' ^
    :param handle: String; Title of the graph, the user's twitter handle
    :return:
    """

    plt.figure(figsize=(7, 7))
    plt.style.use("seaborn-white")
    plt.xticks(word_count, words, rotation="vertical", size=10, fontname="Arial")
    plt.bar(word_count, values, color="green", width=.25)
    plt.title("@%s's Tweet Vocabulary" % handle, fontweight="bold", fontname="Arial")
    plt.ylabel("Frequency", fontname="Arial")
    plt.xlabel("Words")
    plt.show()

    return


def pull_tweets(api, handle):
    """
    Gets a specified number of tweets from the Twitter user's account.
    :param api: Twitter verification object
    :param handle: String; A Twitter account's address
    :return: List; The past 3000 Tweets from this userr
    """
    tweets = []
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=handle).items(3000):
        # Make sure tweet isn't a retweet
        if tweet.text[0:2] != "RT":
            tweets.append(tweet.text)

    return tweets


def count_words(tweets):
    """
    Populates a dictionary with words from the tweets, counts the nuuber of instances of each word
    :param tweets: List; list of each tweet from pull_tweets
    :return: dictionary with int values for each string key
    """
    word_dict = {}
    for tweets in tweets:
        clean_tweets = tweets.lower().split()
        for word in clean_tweets:
            w = string_cleaning(word)
            if w in word_dict:
                word_dict[w] += 1
            else:
                word_dict[w] = 1

    return word_dict


def main():
    api = authenticate()
    handle = str(input("Enter the user's twitter handle: @"))
    raw_tweets = pull_tweets(api, handle)
    word_dict = count_words(raw_tweets)

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
