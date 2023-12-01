# Importando as ferramentas 
from pandas import DataFrame 
from nltk import download
from datetime import date 
from datetime import timedelta
from matplotlib import pyplot as plt 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from GoogleNews import GoogleNews
from newspaper import article, Article
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


# salvando o ticket da empresa
company_name = input("Forneça o nome da empresa ou um ticket: ")

if company_name != '':
    
    print(f"Procurando e analisando {company_name}, Por favor, seja paciente, pode demorar um pouco..")
    google_news = GoogleNews(start=yesterday, end=now)
    google_news.search(company_name)
    result = google_news.result()
    
    # resultado 
    df = DataFrame(result)
    print(df.head())
    
    
try:
    list =[] #creating an empty list 
    for i in df.index:
        dict = {} #creating an empty dictionary to append an article in every single iteration
        article = Article(df['link'][i],config=config) #providing the link
        try:
          article.download() #downloading the article 
          article.parse() #parsing the article
          article.nlp() #performing natural language processing (nlp)
        except:
           pass 
        #storing results in our empty dictionary
        dict['Date']=df['date'][i] 
        dict['Media']=df['media'][i]
        dict['Title']=article.title
        dict['Article']=article.text
        dict['Summary']=article.summary
        dict['Key_words']=article.keywords
        list.append(dict)
    check_empty = not any(list)
    # print(check_empty)
    if check_empty == False:
      news_df=DataFrame(list) #creating dataframe
      print(news_df)

except Exception as e:
    print("Erro ocorrido:" + str(e))
    print('Parece que houve algum erro na recuperação dos dados. Tente novamente ou tente com um ticker diferente.' )
