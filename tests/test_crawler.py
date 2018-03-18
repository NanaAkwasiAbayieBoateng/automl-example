import pytest
import pandas as pd

from crawler import get_urls
from crawler import get_features
from crawler import remove_nonlatin
from crawler import pre_processor
from crawler import prepare_data


def test_get_urls_return_all_links_with_class_item_link(mocker):
    class Response():
        content = """
            <html>
                <div>
                    <a class="bla" href="www.submarino.com.br">teste</a>
                    <a class="item-link" href="www.americanas.com.br">teste</a>
                    <a class="item-link" href="www.shopfacil.com.br">teste</a>
                </div>
            </html>
        """
    mocker.patch('crawler.requests.get', return_value=Response())
    urls = get_urls('www.google.com')
    assert len(urls) == 2
    assert 'www.americanas.com.br' in urls
    assert 'www.shopfacil.com.br' in urls


def test_get_features_return_name_desc_from_product_page(mocker):
    class Response():
        content = """
            <html>
                <div>
                    <h1 class="item-title__primary ">Nome Teste</h1>
                    <a class="item-link" href="www.americanas.com.br">teste</a>
                    <div class="item-description__text">
                        <p>teste descrição
bla bla</p>
                    </div>
                </div>
            </html>
        """
    mocker.patch('crawler.requests.get', return_value=Response())
    nome, desc = get_features('www.google.com')
    assert nome == "Nome Teste"
    assert desc == "teste descrição bla bla"


def test_remove_nonlatin_remove_special_chars():
    clean = remove_nonlatin("!@#Teste&%")
    assert clean == "Teste"


def test_pre_processor_remove_stop_words():
    clean = pre_processor("Eu vou de lá para cá e novamente")
    assert clean == "vou lá cá novamente"


def test_prepare_data_apply_some_transformations(mocker):
    df = pd.DataFrame({
        'nome': ["Teste1", "Teste2", "Teste 3"], 
        'descricao': ["Produto Novo bla bla", "Teste 123", None]
    })
    mocker.patch('crawler.pd.read_csv', return_value=df)
    df = prepare_data(df)
    assert list(df.nome_desc.values) == ['teste bla bla', 'teste teste']
    assert df.columns == ['nome_desc']
