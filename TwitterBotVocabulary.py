import tweepy
from tweepy import OAuthHandler

import matplotlib.pyplot as plt

def StringCleaning(s):
    string = ""
    for char in s:
        if (ord(char) > 122) or ((ord(char) < 97) and (char != "'")) or ("https://" in s):
            continue
        else:
            string = string + char
            
    return string

def main():
    
    appKey = "redacted"
    appSecret = "redacted"
    authToken = "redacted"
    authSecret = "redacted"
    
    auth = OAuthHandler(appKey, appSecret)
    auth.set_access_token(authToken, authSecret)

    api = tweepy.API(auth)

    handle = str(input("Enter the user's twitter handle: @"))

    rawTweets = []
    
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=handle).items(3000):
        if (tweet.text[0:2] != "RT"): # Make sure tweet isnt a retweet
            rawTweets.append(tweet.text)

    wordDict = {}
    for tweets in rawTweets:
        tweets = tweets.lower().split()
        for word in tweets:
            word = StringCleaning(word)
            if word in wordDict:
                wordDict[word] += 1
            else:
                wordDict[word] = 1

    wordList = []
    count = 0
    for key in wordDict:
        if (key == "") or (len(key) <= 4): # Arbitrary word length constraint
            continue
        else:
            appender = [key]
            wordList.append(appender)
            wordList[count].append(wordDict[key])# Puts dictionary values into 2d List
            count += 1

    wordList = sorted(wordList, key=lambda l:l[1], reverse = True) # sorts by values

    words = []
    values = []
    
    for i in range (len(wordList)): # Strips dictionary into two lists
            words.append(wordList[i][0])
            values.append(wordList[i][1])

    if len(words) > 15:
        words = words[0:15]
        values = values[0:15]

    x = range(len(words))

    plt.figure(figsize=(10,7))
    plt.style.use("seaborn-white")
    plt.xticks(x, words, rotation="vertical", size=7, fontname="Arial")
    plt.bar(x, values, color = "green", width = .25)
    plt.title("@%s's Tweet Vocabulary" %handle, fontweight="bold", fontname="Arial")
    plt.ylabel("Frequency",fontname="Arial")
    plt.xlabel("Words")
    plt.show()

    #NEXT: Handle @'s, Style the plot better
    #MAYBE: fill a list with common boring words?

main()
