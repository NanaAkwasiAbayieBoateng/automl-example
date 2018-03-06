# AutoML Example

AutoML ou Automated Machine Learning é um campo novo de pesquisa que tem o obejtivo de facilitar a escolha de algoritmos de machine learning, seus parâmetros, métodos de pré-processamento. Para saber mais, visite https://automl.info/automl/

Este projeto é um exemplo de aplicação de AutoML com a biblioteca [auto-sklearn](https://github.com/automl/auto-sklearn) que inclui um crawler para baixar dados de produtos e treinar o modelo e uma aplicação web que usa o modelo treinado para classificar dados de produtos.

## Instalação

Consideramos que a instalação será feita em um "virtualenv"

1. Clone o repositório;

```
(env)$ git clone git@github.com:rafaelnovello/automl-example.git
```

2. Faça a instalação das dependências:

A biblioteca auto-sklearn depende das bibliotecas de sistema. No Ubuntu:

```
(env)$ sudo apt-get install build-essential swig
```
Agora é só instalar as dependências do projeto

```
(env)$ pip install -r requirements.txt
```

## Baixando os dados e treinando o modelo

- Apenas baixando os dados

```
(env)$ python crawler.py -s dataset.csv --no-train
```

- Baixando os dados e treinando o modelo. Se o arquivo CSV já existir ele será reaproveitado. **Leva vários minutos**.

```
(env)$ python crawler.py -s dataset.csv --train
```

- Fazendo classificações na linha de comando

```
(env)$ python crawler.py -p "Grand Theft Auto V™ (GTA V)"
```

Caso não queira esperar pelo processo de raspagem dos dados e treinamento do modelo, é possível baixar o modelo pré-treinado:

- [Arquivo CSV](https://s3.amazonaws.com/automl-example/produtos.csv)
- [Modelo Classificador](https://s3.amazonaws.com/automl-example/classifier.pkl)
- [Modelo de Encoding](https://s3.amazonaws.com/automl-example/encoder_classifier.pkl)
- [Modelo de Vetorização](https://s3.amazonaws.com/automl-example/vectorizer_classifier.pkl)

Todos os modelos são necessários para a classificação.

## Subindo a aplicação web

A aplicação web usa o framework Flask. Para iniciar o ambiente de desenvolvimento faça:

```
(env)$ python webapp.py
```

Acesse [http://localhost:5000](http://localhost:5000)

## Rodando os testes

Para executar os testes da aplicação basta instalar as dependências e rodar os testes como abaixo:

```
(env)$ pip install -r test-requirements.txt

(env)$ pytest tests
```

## Solução de problemas

1. A instalação das dependências pode apresentar problemas em ambientes novos. Caso o comando `pip install` falhe:

- Instale as bibliotecas numpy e Cython separadamente e após a instalação das mesmas rode o comando novamente

```
(env)$ pip install numpy Cython

(env)$ pip install -r requirements.txt
```


## Contribuições

Todas as contribuições são bem vindas! Não deixe de compartilhar dúvidas, sugestões, criticas e etc!