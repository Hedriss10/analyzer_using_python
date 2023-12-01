## Analisador sentimental com Python 

*Vamos considerar que, a cada vez que você precisa analisar as ações no mercado para tomar decisões, é necessário estar atento às declarações do CEO e às notícias que podem influenciar suas operações ao comprar ou vender ações. Esse processo demanda um tempo significativo para uma tomada de posição informada.*


**Seu problema:**

*Vamos refletir juntos. Já considerou analisar com cuidado aquilo em que pretende se envolver? Não estou falando apenas de ações, mas de qualquer assunto que demande sua atenção. Imagine ter diante de você um livro extenso para ler. Seria muito mais eficiente revisar um resumo antes de iniciar seus estudos e pesquisas, caso seja essa a sua intenção. Se você busca essa praticidade, está no lugar certo. Acompanhe este projeto e aproveite o poder da tecnologia.*


**Sugestão:**

*Recomendo enfaticamente que você adquira conhecimento em linguagens de programação, estrutura de modularização e conceitos relacionados, pois o que planejamos desenvolver juntos será implementado utilizando linguagem de programação, estrutura de aprendizado de máquina, processamento de linguagem natural, APIs e criação de gráficos com dashboards. Isso será essencial para a compreensão e execução bem-sucedida do projeto proposto.*


## Fluxo:

O fluxo

**Extract** -> **Summarize** -> **Analyze**

Primeiro, extrairemos os artigos de notícias com o pacote **Python** de notícias do **Google**, depois os resumiremos com o pacote **Python** para jornais e, no final, executaremos a análise de sentimento nos artigos de notícias extraídos e resumidos com o **VADER**.
 

## Como usar 

**Instalação das libs**

Para instalar as libs no seu projeto é bem simples executa via terminal, lembrando foi configurando com o ambiente virutal `pip` se você estiver usando outro packge do python para instalar pacotes recomendo fortemente que pesquise e estude esse instalador -> <a href="https://packaging.python.org/en/latest/tutorials/installing-packages/">pip package</a>

```
pip install -r requirements.txt 
```


### Importação das libs 

```
# importação das ferramentas 

from pandas import DataFrame 
from nltk import download
from datetime import date 
from matplotlib import pyplot as plt 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from GoogleNews import GoogleNews
from newspaper import article
from newspaper import Config
from wordcloud import WordCloud , STOPWORDS
```

### Extraindo as notícias 

```
now = date.today()
now = now.strftime("%m-%d-%Y")
yesterday = date.today() - timedelta(days=1)
yesterday = yesterday.strftime("%m-%d-%Y")
download('punkt')
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
config = Config()
config.browser_user_agent = user_agent
config.request_timeout = 10
```

Atribuimos as variáveis para fornezer o prazo de extração de notícias, que é essencialmente de 1 dia. o `nltk punkt` é um tokenizer (dados de sequência de caracteres) que divide o texto em uma lista de frases usando um algoritimo avançado.

Precisamos do `Config` porque às vezes o pacote do jornal pode não conseguir baixar um artigo devido à restrição do acesso a URL especificada. Para contornar essa restrição, definimos o `user_agent` variável para analisar esses artgios restritos e obter autorização.

Por fim, a conexão pode ocasionalmente antigir o tempo de limite, poís utilizar o módulo Python, `requests` então para evitar o mesmo, usamos `config.request_timeout`. 
