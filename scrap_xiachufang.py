#! /Users/liu/kouui/anaconda3/envs/recipe_py37/bin/python
# -*- coding: utf-8 -*-


import requests, lxml.html, re
from bs4 import BeautifulSoup

def url_to_recipe(url):
    r"""
    """
    response = requests.get(url)
    root = BeautifulSoup(response.content,'html.parser')
    recipe_title = root.find('h1',class_='page-title').getText().strip()
    src = root.find('div', class_='cover image expandable block-negative-margin')
    src = src.find('img')['src'].split('@')[0]
    ingredient = root.find('div',class_='ings')
    #print( ingredient.find_all('td', class_='name') )
    ingredient_name = [x.getText().strip() for x in ingredient.find_all('td', class_='name')]
    ingredient_amount = [x.getText().strip() for x in ingredient.find_all('td', class_='unit')]

    recipe = {
        "url" : url,
        "title" : recipe_title,
        "ingridient" : {"name" : ingredient_name, "amount" : ingredient_amount} ,
        "image" : src,
    }

    return recipe

def format_recipe_string(recipe, sep="<br>", is_step=False):
    r"""
    """
    recipe_string = {}

    recipe_string["url"] = recipe["url"]
    recipe_string["title"] = recipe["title"]
    recipe_string["image"] = recipe["image"]

    s = f"必要な材料{sep}"
    for i in range(len(recipe["ingridient"]["name"])):
        s += f'{recipe["ingridient"]["name"][i]:<10s} ... {recipe["ingridient"]["amount"][i]:<10s}{sep}'
    recipe_string["ingridient"] = s

    return recipe_string

def scrap_by_search_word_list(search_word_list):
    r"""
    """
    #assert len(search_word_list)==2

    # 2つの検索ワードで検索する場合、このようなURLになる。
    search_keyword = "+".join(search_word_list)
    url_main = f"http://www.xiachufang.com/search/?keyword={search_keyword}&cat=1001"

    # レシピ検索のhtmlを取得
    response = requests.get(url_main)
    root = BeautifulSoup(response.content,'html.parser')
    recipe_list = root.find_all('div',class_='info pure-u')
    #print(f"totally {len(recipe_list)} recipe in one page")
    url_list = []
    for recipe in recipe_list:
        for a in recipe.find_all('a', href=True):
            if 'recipe' in a['href']:
                url_list.append(f"http://www.xiachufang.com{a['href']}")
                break

    return url_main, url_list



if __name__ == "__main__":

    search_words = ["虾仁","白菜"]

    url_cookpad, url_list = scrap_by_search_word_list(search_words)

    recipe = url_to_recipe(url_list[0])
    recipe_string = format_recipe_string(recipe,sep='\n')
    for k, v in recipe_string.items():
        print(v)
