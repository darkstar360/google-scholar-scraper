from bs4 import BeautifulSoup
import re


def find_type(article_element, *args, **kwargs):
    try:
        article_type = article_element.find('span', attrs={'class': 'gs_ct1'}).text
        # print(article_type)
    except:
        article_type = '[Article]'

    return article_type


def find_name_and_link(article_element, *args, **kwargs):
    try:
        article = article_element.find('a')
        article_name = article.text
        article_link = article['href']
    except Exception as e:
        article_name = 'Error'
        article_link = 'Error'
        print(e)

    return article_name, article_link


def find_article_author(article_element, *args, **kwargs):
    try:
        article_author = article_element.find('div', attrs={'class': 'gs_a'}).text
    except Exception as e:
        article_author = 'Error'
        print(e)
    return article_author


def find_publication_year(article_element, *args, **kwargs):
    try:
        article_year = article_element.find('div', attrs={'class': 'gs_a'}).text
        article_year = re.search(r'(\,|-) \d{4}', article_year).group(0).replace(',', '').replace('-', '')
    except Exception as e:
        article_year = 'Error'
        print(e)
    return article_year


def find_description(article_element, *args, **kwargs):
    try:
        article_description = article_element.find('div', attrs={'class': 'gs_rs'}).text
    except Exception as e:
        article_description = 'Error'
        print(e)
    return article_description


def find_citation(article_element, *args, **kwargs):
    cited_by = ''
    try:
        rows = article_element.find('div', attrs={'class': 'gs_fl'})
        citation_row = rows.find_all('a')
        for ele in citation_row:
            if ele.text.startswith('Cited by'):
                cited_by = re.search(r'by \d*', ele.text).group(0).replace('by ', '')
                break
    except Exception as e:
        cited_by = 'Error'
        print(e)
    return cited_by
