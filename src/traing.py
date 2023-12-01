from pandas import DataFrame, to_datetime
from nltk import download
from datetime import date, timedelta
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from GoogleNews import GoogleNews
from newspaper import Article, Config
from wordcloud import WordCloud, STOPWORDS

# Download de recursos necessários
download('punkt')
def get_google_news_data(company_name, start_date, end_date):
    google_news = GoogleNews(start=start_date, end=end_date)
    google_news.search(company_name)
    return google_news.result()

def extract_articles(news_df):
    articles_list = []

    for i in news_df.index:
        article_dict = {}
        article = Article(news_df['link'][i], config=config)  # fornecendo o link

        try:
            article.download()  # fazendo o download do artigo
            article.parse()  # analisando o artigo
            article.nlp()  # processamento de linguagem natural (nlp)
        except Exception as e:
            if "404" in str(e):
                print(f"Erro 404: Artigo não encontrado ({news_df['link'][i]})")
            else:
                print(f"Erro ao processar o artigo {i}: {str(e)}")
            continue

        article_dict['Date'] = news_df['date'][i]
        article_dict['Media'] = news_df['media'][i]
        article_dict['Title'] = article.title
        article_dict['Article'] = article.text
        article_dict['Summary'] = article.summary
        article_dict['Key_words'] = article.keywords

        articles_list.append(article_dict)

    return DataFrame(articles_list)

def perform_sentiment_analysis(news_df):
    if 'Summary' not in news_df.columns or len(news_df['Summary']) == 0:
        print("Nenhum dado disponível para realizar a análise de sentimento.")
        return 0, 0, 0

    positive = 0
    negative = 0
    neutral = 0
    positive_list = []
    negative_list = []
    neutral_list = []

    for news in news_df['Summary']:
        analyzer = SentimentIntensityAnalyzer().polarity_scores(news)
        neg = analyzer['neg']
        neu = analyzer['neu']
        pos = analyzer['pos']

        if neg > pos:
            negative_list.append(news)
            negative += 1
        elif pos > neg:
            positive_list.append(news)
            positive += 1
        elif pos == neg:
            neutral_list.append(news)
            neutral += 1

    positive_percentage = (positive / len(news_df)) * 100
    negative_percentage = (negative / len(news_df)) * 100
    neutral_percentage = (neutral / len(news_df)) * 100

    return positive_percentage, neutral_percentage, negative_percentage

def plot_sentiment_pie_chart(positive_percentage, neutral_percentage, negative_percentage, company_name):
    labels = [f'Positive [{round(positive_percentage)}%]', f'Neutral [{round(neutral_percentage)}%]',
              f'Negative [{round(negative_percentage)}%]']
    sizes = [positive_percentage, neutral_percentage, negative_percentage]
    colors = ['yellowgreen', 'blue', 'red']

    plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(labels)
    plt.title(f"Resultados da Análise de Sentimento para {company_name}")
    plt.axis('equal')
    plt.show()

def generate_wordcloud(text, company_name):
    stopwords = set(STOPWORDS)
    all_words = ' '.join([news for news in text])
    wordcloud = WordCloud(background_color='black', width=1600, height=800, stopwords=stopwords,
                          min_font_size=20, max_font_size=150, colormap='prism').generate(all_words)

    fig, ax = plt.subplots(figsize=(20, 10), facecolor='k')
    plt.imshow(wordcloud)
    ax.axis("off")
    fig.tight_layout(pad=0)
    plt.title(f'Wordcloud para {company_name}')
    plt.show()

if __name__ == "__main__":
    # Entrada do usuário
    company_name = input("Forneça o nome da empresa ou um ticket: ")

    if company_name:
        start_date = (date.today() - timedelta(days=1)).strftime("%m-%d-%Y")
        end_date = date.today().strftime("%m-%d-%Y")

        print(f"Procurando e analisando {company_name}. Por favor, seja paciente; pode demorar um pouco...")

        # Configurando cabeçalho
        config = Config()
        config.browser_user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"
        )
        config.request_timeout = 10

        # Coletando dados do Google News
        news_data = get_google_news_data(company_name, start_date, end_date)

        if not news_data:
            print(f"Nenhuma notícia encontrada para {company_name}.")
        else:
            # Convertendo dados em DataFrame
            news_df = DataFrame(news_data)

            # Extraindo informações dos artigos
            articles_df = extract_articles(news_df)

            # Análise de Sentimento
            positive_percentage, neutral_percentage, negative_percentage = perform_sentiment_analysis(articles_df)

            # Apresentando resultados
            print(f"Sentimento Positivo: {positive_percentage:.2f}%")
            print(f"Sentimento Neutro: {neutral_percentage:.2f}%")
            print(f"Sentimento Negativo: {negative_percentage:.2f}%")

            # Plotando gráfico de pizza
            plot_sentiment_pie_chart(positive_percentage, neutral_percentage, negative_percentage, company_name)

            # Wordcloud
            generate_wordcloud(articles_df['Summary'].values, company_name)
