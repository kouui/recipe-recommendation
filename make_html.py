#! /Users/liu/kouui/anaconda3/envs/recipe_py37/bin/python
# -*- coding: utf-8 -*-

from scrap_xiachufang import url_to_recipe, format_recipe_string, scrap_by_search_word_list
from itertools import product, combinations
import random

def replace_string_in_table(str_list, recipe_string_list, sup_title, sup_url, n):
    r"""
    """
    key_list = ["{colspan}","{href-suptitle}","{href-title}","{suptitle}", "{title}","{image-src}","{ingridient}"]
    key_content_dict = {
        "{colspan}" : f"{n}",
        "{href-suptitle}" : sup_url,
        "{suptitle}" : sup_title,
        "{href-title}" : "url",
        "{title}" : "title",
        "{image-src}" : "image",
        "{ingridient}" : "ingridient",
    }

    #-- search for index
    key_index_dict = {}
    for key in key_list:
        for i, line in enumerate(str_list):
            if key in line:
                key_index_dict[key] = i
                break

    for key in ("{colspan}", "{href-suptitle}", "{suptitle}"):
        str_list[key_index_dict[key]] = str_list[key_index_dict[key]].replace(key, key_content_dict[key])

    index_key_dict = {}
    for key in ("{href-title}", "{title}", "{image-src}","{ingridient}"):
        idx = key_index_dict[key]
        if idx not in index_key_dict.keys():
            index_key_dict[idx] = []
        index_key_dict[idx].append(key)

    for idx in index_key_dict.keys():
        s_total = ""
        for k in range(n):
            s = str_list[idx]
            for key in index_key_dict[idx]:
                s = s.replace(key, recipe_string_list[k][key_content_dict[key]])
            s_total += s

        str_list[idx] = s_total

    return None

def get_single_table_string(search_word_list, fname_dict, n_recipe=3):
    r"""
    """
    #-- scrap recipe

    url_main, url_list = scrap_by_search_word_list(search_word_list)

    recipe_string_list = []
    for i in range(n_recipe):
        recipe = url_to_recipe(url_list[i])
        recipe_string = format_recipe_string(recipe,sep="<br>")
        recipe_string_list.append(recipe_string)

    #-- make index.html

    with open(fname_dict["template"]["table"], 'r') as f:
        lines = f.readlines()

    sup_title = "+".join(search_word_list)
    sup_url   = url_main
    _ = replace_string_in_table(lines, recipe_string_list, sup_title=sup_title, sup_url=sup_url, n=n_recipe)
    single_table_string = "".join(lines)

    return single_table_string

def get_multi_table_string(word_dict, fname_dict, n_recipe=3):
    r"""
    """
    table_string_list = []

    if len(word_dict["肉"]) == 0:
    # 没有肉的时候
        if len(word_dict["蔬菜"]) > 2:
        # 有很多菜就把菜组合起来吃
            for pair in combinations(word_dict["蔬菜"],2):
                single_table_string = get_single_table_string(pair, fname_dict, n_recipe=n_recipe)
                table_string_list.append(single_table_string)
        else:
        # 没有多少菜了，就单个搜菜
            for item in word_dict["蔬菜"]:
                pair = [item,]
                single_table_string = get_single_table_string(pair, fname_dict, n_recipe=n_recipe)
                table_string_list.append(single_table_string)

    else:
    # 有肉的时候
        if len(word_dict["蔬菜"]) > 0:
        # 有肉有菜，肉菜组合搜索，最后随机搜下肉
            for pair in product( word_dict["肉"], word_dict["蔬菜"] ):
                single_table_string = get_single_table_string(pair, fname_dict, n_recipe=n_recipe)
                table_string_list.append(single_table_string)

            item = random.choice( word_dict["肉"] )
            pair = [item,]
            single_table_string = get_single_table_string(pair, fname_dict, n_recipe=n_recipe)
            table_string_list.append(single_table_string)

        else:
        #只有肉的话单独搜全部肉
            for item in word_dict["肉"]:
                pair = [item,]
                single_table_string = get_single_table_string(pair, fname_dict, n_recipe=n_recipe)
                table_string_list.append(single_table_string)


    return "\n".join(table_string_list)



if __name__ == "__main__":

    fname = {
    "template" : {"table" : "./contents/table.template",
                  "index" : "./contents/index.template",
                  "style" : "./contents/style.template"},
    "output" : "./templates/index0.html",
    }

    #words = ["えび","ホタテ","小松菜"]
    words = {
        "蔬菜" : ["土豆", "青椒"],
        "肉" : ["鸡胸肉",],
    }

    multi_table_string = get_multi_table_string(words, fname_dict=fname, n_recipe=3)

    with open(fname["template"]["index"], 'r') as f:
        index_string = f.read()
    with open(fname["template"]["style"], 'r') as f:
        style_string = f.read()

    index_string = index_string.replace("{style}", style_string)
    index_string = index_string.replace("{table}", multi_table_string)

    with open(fname["output"], 'w') as f:
        f.write(index_string)
