from tweepy import OAuthHandler
import tweepy
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import date
from nltk.corpus import stopwords
# nltk.download('stopwords')

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
    Populates a dictionary with only interseting words from the tweets, counts the number of instances of each word
    :param tweets: List; list of each tweet from pull_tweets
    :return: dictionary with int values for each string key
    """

    word_dict = {}
    stop = stopwords.words('english')
    for tweet in tweets:
        clean_tweet = tweet.lower().split()
        for word in clean_tweet:
            w = string_cleaning(word)
            if w in stop or w == "":
                continue
            elif w in word_dict:
                word_dict[w] += 1
            else:
                word_dict[w] = 1
    
    df_word_dict = pd.DataFrame.from_dict(word_dict, orient = 'index', columns=['Count'])
    return df_word_dict


def graph(word_dictionary, handle, num_tweets):
    """
    :param word_dictionary: Dataframe; dataframe of words and their respective counts
    :param handle: String: User's twitter handle
    :param num_tweets: Int: Number of tweets to pull from user
    :return: null
    """

    # Month abbreviation, day and year	
    today = date.today()
    d8 = today.strftime("%b-%d-%Y")

    title_string = f"@{handle}s's Tweet Vocabulary -- Last {num_tweets} Tweets -- {d8}"
    display_words = word_dictionary.nlargest(10, "Count")
    display_words['Word'] = display_words.index

    fig = px.bar(display_words, x="Word", y='Count')
    fig.update_layout(title_text=title_string)
    fig.show()


def main():

    api = authenticate()
    num_tweets = 500
    handle = str(input("Enter the user's twitter handle: @"))
    raw_tweets = pull_tweets(api, handle, num_tweets)
    word_dict = count_words(raw_tweets)
    graph(word_dict, handle, num_tweets)

    # TODO: MAYBE: Error handling (@ name doesn't exist, not enough tweets/words, etc)


if __name__ == "__main__":
    main()
