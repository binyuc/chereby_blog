from flask import Blueprint, render_template

from module.index import Index

index = Blueprint('index', __name__)


@index.route('/')
def get_index():
    article = Index()
    result = article.find_limit_with_article(0, 8)
    type_count = article.find_count_by_type()
    subtype_count = article.find_count_by_subtype()
    for article in result:
        article.createtime = article.createtime.strftime('%Y-%m-%d')
    return render_template('index.html', result=result, type_count=type_count, subtype_count=subtype_count)


@index.route('/popular')
def get_index_popular():
    article = Index()
    result = article.find_limit_with_article_popular(0, 8)
    type_count = article.find_count_by_type()
    subtype_count = article.find_count_by_subtype()
    for article in result:
        article.createtime = article.createtime.strftime('%Y-%m-%d')
    return render_template('index.html', result=result, type_count=type_count, subtype_count=subtype_count)


@index.route('/cover')
def cover():
    return render_template('cover.html')

@index.route('/poker')
def poker():
    return render_template('poker.html')