# Importando as ferramentas 
from pandas import DataFrame 
from nltk import download
from datetime import date 
from datetime import timedelta
from matplotlib import pyplot as plt 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from GoogleNews import GoogleNews
from newspaper import article
from newspaper import Config
from wordcloud import WordCloud , STOPWORDS


# Extraindo notícias 
now = date.today()
now = now.strftime("%m-%d-%Y")
yesterday = date.today() - timedelta(days=1)
yesterday = yesterday.strftime("%m-%d-%Y")
download('punkt')
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
config = Config()
config.browser_user_agent = user_agent
config.request_timeout = 10