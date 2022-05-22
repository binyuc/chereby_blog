from flask import Blueprint, render_template, jsonify, abort
from module.article import Article
from module.comment import Comment
import math

article = Blueprint('article', __name__)


@article.route('/article_list/page=<int:page>')
def get_article_page(page):
    start = (page - 1) * 5
    article = Article()
    result = article.find_limit_with_article(start, 5)
    total = math.ceil(article.get_total_count() / 5)
    for article in result:
        article.createtime = article.createtime.strftime('%Y-%m-%d')
    type_count = article.find_count_by_type()
    subtype_count = article.find_count_by_subtype()
    return render_template('article_list.html', result=result, total=total, page=page,type_count=type_count,subtype_count=subtype_count)


@article.route('/article_list/type=<int:type>&page=<int:page>')
def classify(type, page):
    start = (page - 1) * 5
    article = Article()
    result = article.find_by_type(type, start, 5)
    total = math.ceil(article.get_count_by_type(type) / 10)
    type_count = article.find_count_by_type()
    subtype_count = article.find_count_by_subtype()
    return render_template('article_list.html', result=result, page=page, total=total, type=type,type_count=type_count,subtype_count=subtype_count)

@article.route('/article_list/type=<int:type>&page=<int:page>&subtype=<subtype>')
def subtype(type, page,subtype):
    start = (page - 1) * 5
    article = Article()
    result = article.find_by_subtype(type, subtype,start, 5)
    total = math.ceil(article.get_count_by_subtype(type,subtype) / 10)
    type_count = article.find_count_by_type()
    subtype_count = article.find_count_by_subtype()
    return render_template('article_list.html', result=result, page=page, total=total, type=type,subtype=subtype,type_count=type_count,subtype_count=subtype_count)

@article.route('/search_list/page=<int:page>&keyword=<keyword>')
def search(page, keyword):
    keyword = keyword.strip()
    if keyword is None or keyword == '' or '%' in keyword or len(keyword) > 10:
        abort(404)
    article = Article()
    start = (page - 1) * 5
    result = article.find_by_aricle_headline(keyword, start, 5)
    total = math.ceil(article.get_count_by_headline(keyword))
    type_count = article.find_count_by_type()
    subtype_count = article.find_count_by_subtype()
    return render_template('search_list.html', result=result, total=total, page=page, keyword=keyword,type_count=type_count,subtype_count=subtype_count)


@article.route('/article/articleid=<int:articleid>')
def get_article_by_articleid(articleid):
    article = Article()

    result = article.find_by_id(articleid)
    article.update_read_count(articleid=articleid)
    comment_user = Comment().get_comment_user_list(articleid, 0, 50)
    type_count = article.find_count_by_type()
    subtype_count = article.find_count_by_subtype()
    # app.logger.info(comment_user)
    return render_template('article_single.html', result=result, comment_user=comment_user,type_count=type_count,subtype_count=subtype_count)
