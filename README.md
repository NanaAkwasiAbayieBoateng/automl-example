# AutoML Example

AutoML ou Automated Machine Learning é um campo novo de pesquisa que tem o obejtivo de facilitar a escolha de algoritmos de machine learning, seus parâmetros, métodos de pré-processamento. Para saber mais, visite https://automl.info/automl/

Este projeto é um exemplo de aplicação de AutoML com a biblioteca [auto-sklearn](https://github.com/automl/auto-sklearn) que inclui um crawler para baixar dados de produtos e treinar o modelo e uma aplicação web que usa o modelo treinado para classificar dados de produtos.

# Instalação

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

# Baixando os dados e treinando o modelo

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

# Subindo a aplicação web

A aplicação web usa o framework Flask. Para iniciar o ambiente de desenvolvimento faça:

```
(env)$ python webapp.py
```

Acesse [http://localhost:5000](http://localhost:5000)


# Deploy em produção

O projeto já inclui os arquivos necessários para o deploy no Heroku. Estes arquivos são:

- Procfile
- run (bash)
- runapp.py
- production.ini

Este modelo de deploy **não é o ideal**, mas é uma forma simples de colocar o projeto em produção. Considere usar uma estratégia de deployment mais apropriada como o uso de nginx/gunicorn.

Para fazer o deploy (heroku):

- Se quiser manter um registro das consultas feitas no sistema, habilite o uso do Cloudinary:
  - Faça o cadastro no Cloudinary
  - Insira suas credenciais no arquivo .env do heroku ([saiba mais](https://devcenter.heroku.com/articles/heroku-local#copy-heroku-config-vars-to-your-local-env-file))
  - altere o parametro `use_cloudinary` no arquivo production.ini
- Faça o deploy com o comando ([saiba mais](https://devcenter.heroku.com/articles/git)):
```
(env)$ git push heroku master
```
 
O sistema automaticamente salvará as imagens e suas predições no Cloudinary se as credenciais estiverem presentes.

# Contribuições

Todas as contribuições são bem vindas! Não deixe de compartilhar dúvidas, sugestões, criticas e etc!