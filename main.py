# -*- coding: utf-8 -*-
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

def range_char(start, stop):
    return (chr(n) for n in range(ord(start), ord(stop) + 1)

def get_max_page_count(driver, url):
    driver.get(url)
    page_info = driver.find_elements(By.TAG_NAME, 'p')
    max_len = len(page_info[-1].find_elements(By.TAG_NAME, 'a')) + 2
    return max_len

def extract_words_from_page(driver, letter, page_number):
    url = f'https://bslsignbank.ucl.ac.uk/dictionary/search/?query={letter}&page={page_number}'
    driver.get(url)
    table_body = driver.find_element(By.ID, 'searchresults').find_element(By.TAG_NAME, 'tbody')
    word_lists = table_body.find_elements(By.TAG_NAME, 'td')
    
    English_word = []
    URL = []
    
    for words_list in word_lists:
        words = words_list.find_elements(By.TAG_NAME, 'p')
        
        for word in words:
            word_text = word.text
            word_url = word.find_element(By.TAG_NAME, 'a').get_attribute('href')
            English_word.append(word_text)
            URL.append(word_url)
    
    return English_word, URL

def get_keywords_from_url(driver, word_url):
    driver.get(word_url)
    keywords = driver.find_element(By.ID, 'keywords').text.replace('Keywords:', '')
    return keywords

def main():
    base_url = 'https://bslsignbank.ucl.ac.uk/dictionary/search/?query='
    option = webdriver.EdgeOptions()
    option.add_argument('headless')
    driver = webdriver.Edge(options=option)
    
    English_word = []
    URL = []
    
    for letter in range_char('A', 'Z'):
        max_page_count = get_max_page_count(driver, base_url + letter)
        
        for page_number in range(1, max_page_count):
            english_words, urls = extract_words_from_page(driver, letter, page_number)
            English_word.extend(english_words)
            URL.extend(urls)
    
    Meaning_Sign = [get_keywords_from_url(driver, word_url) for word_url in URL]
    
    df = pd.DataFrame({'English Word': English_word, 'URL': URL, 'Meaning Sign': Meaning_Sign})
    df.to_csv('bsl_words.csv', index=False)
    
    driver.quit()

if __name__ == '__main__':
    main()
