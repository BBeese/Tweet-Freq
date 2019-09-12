from tweepy import OAuthHandler
import tweepy
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


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
    Authenticates credentials to use Twitter's services.
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

    title = f"@{handle}s's Tweet Vocabulary"
    fig = go.Figure(data=go.Bar(x=words, y=values))
    fig.update_layout(title_text=title)
    fig.show()

    # plt.style.use("seaborn-white")
    # plt.yticks(word_count, words, size=10, fontname="Arial")
    # plt.barh(word_count, values, color="green")
    # plt.title("@%s's Tweet Vocabulary" % handle, fontweight="bold", fontname="Arial")
    # plt.xlabel("Frequency", fontname="Arial")
    # plt.ylabel("Words")
    # plt.show()

    return


def pull_tweets(api, handle, items):
    """
    Gets a specified number of tweets from the Twitter user's account.
    :param api: Twitter verification object
    :param handle: String; A Twitter account's address
    :param items: Int; Number of tweets to pull
    :return: List; The past <items> Tweets from this user
    """
    tweets = []
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=handle).items(items):
        # Make sure tweet isn't a retweet
        if tweet.text[0:2] != "RT":
            tweets.append(tweet.text)

    return tweets


def count_words(tweets):
    """
    Populates a dictionary with words from the tweets, counts the number of instances of each word
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

def count_words_TRIAL(tweets):
    """
    Populates a dictionary with words from the tweets, counts the number of instances of each word
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
    
    # pd.Series(word_dict).to_frame()
    df_word_dict = pd.DataFrame.from_dict(word_dict, orient = 'index', columns=['Count'])
    return df_word_dict


def dict_to_2d(d, length):
    """
    :param d: dictionary
    :param length: min length of words to include
    :return: 2d list version of dictionary parameter
    """
    word_list = []
    count = 0
    for key in d:
        # '4' is an arbitrary word length constraint
        if (key == "") or (len(key) <= length):
            continue
        else:
            # Puts dictionary values into 2d List
            appender = [key]
            word_list.append(appender)
            word_list[count].append(d[key])
            count += 1

    # Sorts by values
    word_list = sorted(word_list, key=lambda l: l[1], reverse=True)

    return word_list


def dict_strip(d):
    """
    :param d: dictionary to turn into 2d list
    :return: 2 separate lists with corresponding word-value pairs
    """
    words = []
    values = []
    # Strips dictionary into two lists
    for i in range(len(d)):
        words.append(d[i][0])
        values.append(d[i][1])

    if len(words) > 15:
        words = words[0:15]
        values = values[0:15]

    return words, values


def pandas_method(word_dictionary):
    display_words = word_dictionary.nlargest(10, "Count")
    display_words['Word'] = display_words.index
    fig = px.bar(display_words, x="Word", y='Count')
    fig.show()

    #Can either:
    #Use existing method (dict_to_2d), modify it to remove key from dictionary if length too short
    #OR do dataframe manipulation. 
    # **** W I P ****

def main():

    api = authenticate()
    handle = str(input("Enter the user's twitter handle: @"))
    raw_tweets = pull_tweets(api, handle, 100)
    #word_dict = count_words_TRIAL(raw_tweets)
    word_dict = count_words(raw_tweets)
    word_2d_list = dict_to_2d(word_dict, 4)
    words_payload, values_payload = dict_strip(word_2d_list)
    graph(range(len(words_payload)), words_payload, values_payload, handle)

    # TODO: Handle @'s, Style the plot better
    # TODO: Unit Tests
    # TODO: MAYBE: fill a list with common boring words?
    # TODO: MAYBE: Error handling (@ name doesn't exist, not enough tweets/words, etc)
    # TODO: Python library 'Dash' for embedding graph into webpage
    # TODO: Move data into a pandas dataframe, might be able to sort without all my functions,
            # Will also have more access to customizability with my graph. 


main()
