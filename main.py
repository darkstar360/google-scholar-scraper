from dearpygui import core, simple
from dearpygui.core import *
from dearpygui.simple import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.options import Options

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import re
from decimal import Decimal
from datetime import datetime
import time
import csv
import random
import subprocess
import json

from modules.article_finder import *


def start_scrape(sender, data):
    print('sender#', sender)
    print('data#', data)
    with window('main_window'):
        keywords = get_value('input_keyword')
        page_num = int(get_value('pages'))
        from_year = get_value('from_year')
        to_year = get_value('to_year')
    print('keywords: ', keywords)
    subprocess.Popen(
        '"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="D:\\scraper"')
    option = Options()
    # option.headless = True
    option.add_argument('--incognito')
    option.add_argument("--disable-blink-features")
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    option.add_argument("--disable-extensions")
    driver = webdriver.Chrome(executable_path='chromedriver_win32/chromedriver.exe', options=option)
    driver.get('https://scholar.google.com')
    search_box = driver.find_element_by_id('gs_hdr_tsi')
    search_box.send_keys(keywords)
    search_box.send_keys(Keys.ENTER)
    time.sleep(random.randint(2, 5))
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'gs_res_sb_yyc')))
    url = driver.current_url
    url += '&as_ylo=' + from_year + '&as_yhi=' + to_year
    # driver.get(url)
    # wait = WebDriverWait(driver, 10)
    # element.click()
    # wait = WebDriverWait(driver, 20)
    # element = wait.until(EC.element_to_be_clickable((By.ID, 'gs_as_ylo')))
    # element.send_keys(from_year)
    # wait = WebDriverWait(driver, 20)
    # element = wait.until(EC.visibility_of_element_located((By.NAME, 'as_yhi')))
    # element.send_keys(to_year)
    # wait = WebDriverWait(driver, 20)
    # element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'gs_btn_lsb')))
    # element.click()
    # # page_source = BeautifulSoup(driver.page_source, 'lxml')
    i = 0
    scraped = []
    driver.get(url)
    while True:
        i += 1
        page_source = BeautifulSoup(driver.page_source, 'lxml')
        next_page = page_source.find('span', attrs={'class': 'gs_ico gs_ico_nav_next'})
        main_content = page_source.find('div', attrs={'id': 'gs_res_ccl_mid'})
        articles = main_content.find_all('div', attrs={'class': 'gs_ri'})
        # scraped = []
        for article in articles:
            article_type = find_type(article)
            # print(article_type)
            article_name, article_link = find_name_and_link(article)
            # print(article_name, article_link)
            article_author = find_article_author(article)
            # print(article_author)
            article_year = find_publication_year(article)
            # print(article_year)
            article_description = find_description(article)
            # print(article_description)
            cited_by = find_citation(article)
            # print(cited_by)
            data = {
                'article': article_type,
                'article_name': article_name,
                'article_link': article_link,
                'article_author': article_author,
                'published_year': article_year,
                'article_description': article_description,
                'article_cited_by': cited_by
            }
            scraped.append(data)
        if next_page is None or i >= page_num:
            break
        else:
            next_page_ref = next_page.find_parent('a')['href']
            time.sleep(random.randint(1, 3))
            driver.find_element_by_link_text('Next').click()
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.ID, 'gs_res_ccl_mid')))
            time.sleep(5)
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')

    with open('scraped_data.json', 'w') as output:
        json.dump(scraped, output)
        print(len(scraped), scraped)
        output.close()
    driver.close()


set_main_window_size(540, 720)
set_global_font_scale(1.25)
set_theme('Gold')
set_style_window_padding(30, 30)

with window(name='main_window', width=525, height=680):
    set_window_pos('main_window', 0, 0)
    # core.add_text('Testing')
    add_drawing('logo', width=520, height=290, )
    add_separator()
    add_spacing(count=12)
    add_text('Please Enter keywords with space', color=[232, 163, 33])
    add_input_text(name='input_keyword', label='Enter Keywords', width=350, hint='Keywords')
    add_spacing(count=12)
    add_input_text(name='pages', label='Pages To Scrape', width=300, hint='Number of pages')
    add_spacing(count=12)
    add_input_text(name='from_year', label='From Year (4 digits)', width=300, hint='Year (like 2001)')
    add_spacing(count=12)
    add_input_text(name='to_year', label='To Year(4 digits)', width=300, hint='Year (like 2019)')
    add_spacing(count=12)
    add_button("scrape", callback=start_scrape)
    # add_text('jijinisa', wrap=0)

    draw_image("logo", "scholar_logo_64dp.png", [0, 0], [520, 192])

    start_dearpygui()
