#! /Users/liu/kouui/anaconda3/envs/recipe_py37/bin/python
# -*- coding: utf-8 -*-


import requests, lxml.html, re

def url_to_recipe(url):
    r"""
    """
    response = requests.get(url)
    root = lxml.html.fromstring(response.content)
    recipe_title = root.cssselect("title")[0].text_content()
    ingridient_name = root.cssselect("span.name")
    ingridient_amount = root.cssselect("div.ingredient_quantity")
    step = root.cssselect("p.step_text")

    src = root.cssselect("#main-photo > img")[0].get('src')
    src = re.findall(r'https://.+\.jpg', src)[0]

    recipe = {
        "url" : url,
        "title" : recipe_title,
        "ingridient" : {"name" : ingridient_name, "amount" : ingridient_amount} ,
        "step" : step,
        "image" : src,
    }

    return recipe

def format_recipe_string(recipe, sep="<br>"):
    r"""
    """
    recipe_string = {}

    recipe_string["url"] = recipe["url"]
    recipe_string["title"] = recipe["title"]
    recipe_string["image"] = recipe["image"]

    s = f"必要な材料{sep}"
    for i in range(len(recipe["ingridient"]["name"])):
        s += f'{recipe["ingridient"]["name"][i].text_content():<10s} ... {recipe["ingridient"]["amount"][i].text_content():<10s}{sep}'
    recipe_string["ingridient"] = s

    s = "作り方\n"
    for i in range(len(recipe["step"])):
        s += f"step {i:02d} ,\t {recipe['step'][i].text_content():s}{sep}"
    recipe_string["step"] = s

    return recipe_string

def scrap_by_search_word_list(search_word_list):
    r"""
    """
    #assert len(search_word_list)==2

    # 2つの検索ワードで検索する場合、このようなURLになる。
    url_cookpad = f"https://cookpad.com/search/{search_word_list[0]:s}"
    for word in search_word_list:
        url_cookpad += f"%E3%80%80{word:s}"

    # レシピ検索のhtmlを取得
    response = requests.get(url_cookpad)
    root = lxml.html.fromstring(response.content)
    root.make_links_absolute(response.url)
    url_list = []
    # 検索の上位にあるレシピのurlを獲得する
    for a in root.cssselect('a.recipe-title'):
        url = a.get('href')
        url_list.append(url)

    return url_cookpad, url_list



if __name__ == "__main__":

    search_words = ["えび","ホタテ"]

    url_cookpad, url_list = scrap_by_search_word_list(search_words)

    recipe = url_to_recipe(url_list[0])
    recipe_string = format_recipe_string(recipe,sep='\n')
    for k, v in recipe_string.items():
        print(v)
