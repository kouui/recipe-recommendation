#! /Users/liu/kouui/anaconda3/envs/recipe_py37/bin/python
# -*- coding: utf-8 -*-


from flask import Flask, render_template, request
from make_html import get_multi_table_string
app = Flask(__name__)

global_var = {
    "table_string" : "",
}

def filter_empty_string(s):
    r"""
    """
    return list(filter(None,s))


@app.route('/generate')
def generate_index_html():
    r"""
    """
    word_string = request.args.get("list")
    word_ = word_string.split('_')
    #print(word_)

    word_dict = {}
    word_dict["肉"] = filter_empty_string( word_[0].split('-') )
    word_dict["蔬菜"] = filter_empty_string( word_[1].split('-') )
    word_dict["主食"] = filter_empty_string( word_[2].split('-') )

    #print(f"肉 ： {word_dict['肉']}")
    #print(f"蔬菜： {word_dict['蔬菜']}")

    fname = {
    "template" : {"table" : "./contents/table.template",
    #              "index" : "./contents/index.template",
    #              "style" : "./contents/style.template"
                 },
    #"output" : "./templates/index.html",
    }

    #word_list = ["えび","ホタテ","小松菜"]

    multi_table_string = get_multi_table_string(word_dict, fname_dict=fname, n_recipe=3)

    #-- GAE's file system is read only
    #with open(fname["template"]["index"], 'r') as f:
    #    index_string = f.read()
    #with open(fname["template"]["style"], 'r') as f:
    #    style_string = f.read()

    #index_string = index_string.replace("{style}", style_string)
    #index_string = index_string.replace("{table}", multi_table_string)

    #with open(fname["output"], 'w') as f:
    #    f.write(index_string)
    global_var["table_string"] = multi_table_string

    return "link : <a href='https://recipe-recommendation-267614.appspot.com/'>https://recipe-recommendation-267614.appspot.com/</a>"

@app.route('/')
def index_html():
    r"""
    """

    #print( global_var["table_string"] )

    return render_template('index.html', table_string=global_var["table_string"])


if __name__ == "__main__":

    app.run(host='127.0.0.1', debug=True, port=8080, threaded=True)
