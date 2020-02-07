#! /Users/liu/kouui/anaconda3/envs/recipe_py37/bin/python
# -*- coding: utf-8 -*-


from flask import Flask, render_template, request
from make_html import get_multi_table_string
app = Flask(__name__)


@app.route('/generate')
def generate_index_html():
    r"""
    """
    word_string = request.args.get("list")
    word_list = word_string.split('-')

    fname = {
    "template" : {"table" : "./contents/table.template",
                  "index" : "./contents/index.template",
                  "style" : "./contents/style.template"},
    "output" : "./templates/index.html",
    }

    #word_list = ["えび","ホタテ","小松菜"]

    multi_table_string = get_multi_table_string(word_list, fname_dict=fname, n_recipe=3, n_combination=2)

    with open(fname["template"]["index"], 'r') as f:
        index_string = f.read()
    with open(fname["template"]["style"], 'r') as f:
        style_string = f.read()

    index_string = index_string.replace("{style}", style_string)
    index_string = index_string.replace("{table}", multi_table_string)

    with open(fname["output"], 'w') as f:
        f.write(index_string)

    return "link : <a href='http://127.0.0.1:7777/'>http://127.0.0.1:7777/</a>"

@app.route('/')
def index_html():
    r"""
    """

    return render_template('index.html')


if __name__ == "__main__":

    app.run(debug=True, port=7777, threaded=True)
