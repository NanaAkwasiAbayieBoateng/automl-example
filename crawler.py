
import os
import csv
import argparse
import requests
import unicodedata
from concurrent.futures import ThreadPoolExecutor

import joblib
import pandas as pd
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

import autosklearn.classification as automl
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer


def get_urls(url):
    resp = requests.get(url)
    root = BeautifulSoup(resp.content, 'lxml')
    links = root.find_all('a', attrs={'class': 'item-link'})
        
    urls = [a.attrs.get('href') for a in links]
    return urls


def get_features(url):
    resp = requests.get(url)
    root = BeautifulSoup(resp.content, 'lxml')
    name = root.find('h1', attrs={'class': 'item-title__primary '}).text
    name = name.replace('\n', ' ')
    name = name.replace('\t', '')
    name = name.replace(';', ' ')
    desc_div = root.find('div', attrs={'class': 'item-description__text'})
    try:
        desc = desc_div.find('p').text
        desc = desc.replace('\n', ' ')
        desc = desc.replace('\t', '')
        desc = desc.replace(';', ' ')
    except:
        desc = ''
    return name, desc


def remove_nonlatin(string):
    new_chars = []
    for char in string:
        if char == '\n':
            new_chars.append(' ')
            continue
        try:
            if unicodedata.name(char).startswith(('LATIN', 'SPACE')):
                new_chars.append(char)
        except:
            continue
    return ''.join(new_chars)


def pre_processor(text):
    stops = set(stopwords.words("portuguese"))
    text = remove_nonlatin(text)
    words = text.lower().split()
    words = ' '.join([w for w in words if not w in stops])
    return words


def prepare_data(dataset):
    df = pd.read_csv(dataset, sep=';')
    df.descricao = df.descricao.str.replace('Produto Novo', '')
    df.dropna(inplace=True)
    df['nome_desc'] = df.nome + ' ' + df.descricao
    df.nome_desc = df.nome_desc.apply(pre_processor)
    df.drop(['nome','descricao'], axis=1, inplace=True)
    return df


def train(df, fit_file):
    print("Training...")
    train_size = 0.75
    vectorizer = CountVectorizer(
        analyzer="word",
        tokenizer=None,
        preprocessor=None,
        stop_words=None
    )
    clf = automl.AutoSklearnClassifier(
        include_preprocessors=["no_preprocessing",],
        exclude_preprocessors=None
    )
    encoder = LabelEncoder()

    y = df.categoria
    y = encoder.fit_transform(y)

    X = vectorizer.fit_transform(df.nome_desc)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=train_size
    )
    clf.fit(X_train, y_train)

    accuracy = clf.score(X_test, y_test)
    msg = "Accuracy with {:.0%} of testing data: {:.1%}".format(1 - train_size, accuracy)
    print(msg)
    joblib.dump(clf, fit_file)
    joblib.dump(encoder, 'encoder_%s' % fit_file)
    joblib.dump(vectorizer, 'vectorizer_%s' % fit_file)


def predict(text, fit_file='classifier.pkl'):
    clf = joblib.load(fit_file)
    vectorizer = joblib.load('vectorizer_%s' % fit_file)
    encoder = joblib.load('encoder_%s' % fit_file)
    
    text = pre_processor(text)
    text = vectorizer.transform([text])
    resp = clf.predict(text)[0]
    resp = encoder.classes_[resp]
    return resp


def save_dataset(data, dataset_file):
    with open(dataset_file, 'w') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(['nome', 'descricao', 'categoria'])
        for name, desc, categ in data:
            writer.writerow([name, desc, categ])


def scraper(categs):
    data = []
    for categ, url in categs:
        print(categ)
        jobs = [url % start for start in range(0, 50, 50)]
        urls_list = []
        
        with ThreadPoolExecutor(max_workers=15) as pool:
            futures = pool.map(get_urls, jobs)
            for urls in futures:
                f_utures = pool.map(get_features, urls)
                for features in f_utures:
                    features = features + (categ,)
                    data.append(features)
    return data


categs = [
    ('livro', 'https://livros.mercadolivre.com.br/literatura-estrangeira/_Desde_%s'),
    ('brinquedo', 'https://lista.mercadolivre.com.br/brinquedos-hobbies/bonecos-figuras-acao/_Desde_%s'),
    ('maquiagem', 'https://lista.mercadolivre.com.br/beleza-cuidado-pessoal/maquiagem/_Desde_%s'),
    ('game', 'https://games.mercadolivre.com.br/video-games/_Desde_%s'),

]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Scrap products and train a model to predict products categories.')

    parser.add_argument(
        '-s', '--scrap',
        help='Scrap products and save dataset (CSV)',
    )
    parser.add_argument(
        '--train',
        dest='train',
        action='store_true',
        help='Train and save to file (PKL)',
    )
    parser.add_argument(
        '--no-train',
        dest='train',
        action='store_false',
        help='No train',
    )
    parser.add_argument(
        '-p', '--predict',
        help='Predict',
    )

    args = parser.parse_args()
    dataset_file = args.scrap
    to_predict = args.predict
    should_train = args.train
    fit_file = 'classifier.pkl'

    if dataset_file and not os.path.isfile(dataset_file):
        data = scraper(categs)
        print(len(data))
        save_dataset(data, dataset_file)
    
    if dataset_file and should_train and not os.path.isfile(fit_file):
        df = prepare_data(dataset_file)
        train(df, fit_file)
    
    if to_predict:
        resp = predict(to_predict, fit_file)
        print("Category: %s" % resp)
  