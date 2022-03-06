from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import snscrape.modules.twitter as sntwitter
import nltk
from collections import Counter
import json

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')

from nltk.corpus import stopwords

lemmatize = WordNetLemmatizer()

tickers = ["AAPL"] #, "MSFT", "FB"]
ranges = {
    "2012": ('2012-01-01', '2012-07-31'),
    # "2013": ('2013-01-01', '2013-12-31')
}
english_stopwords = stopwords.words('english') + ["#", "@", "$", "?", "%", "'s", "http", ":", "-", ".", "'", ",", "[", "]", "(", ")"] + [t.lower() for t in tickers]
result = {}
for ticker in tickers:
    result[ticker] = {}
    for year, time_range in ranges.items():
        result[ticker][year] = Counter({})
        stream = sntwitter.TwitterSearchScraper(f'#{ticker} since:{time_range[0]} until:{time_range[1]}').get_items()
        print(f"Fetching tweet for ticker {ticker} and year {year}")
        for tweet in stream:
            tokens = word_tokenize(tweet.content.lower())
            lemmatized_words = []
            for w in tokens:
                if w not in english_stopwords:
                    rootWord = lemmatize.lemmatize(w)
                    lemmatized_words.append(rootWord)
            counts_lemmatized_words = Counter(lemmatized_words)
            result[ticker][year] += counts_lemmatized_words
        result[ticker][year] = {k:v for k, v in result[ticker][year].items() if v >= 10}


with open("twitter_data.json", "w") as f:
    f.write(json.dumps(result))