from flask import Blueprint, render_template, request, jsonify, make_response
from module.poker import *
import time
from multiprocessing import Pool


poker = Blueprint('poker', __name__)


@poker.route('/poker-run', methods=['POST'])
def poker_run_post():
    try:
        my_card1 = request.form.get('my_card1')
        my_card2 = request.form.get('my_card2')
        flop1 = request.form.get('flop1')
        flop2 = request.form.get('flop2')
        flop3 = request.form.get('flop3')
        flop4 = request.form.get('flop4')
        flop5 = request.form.get('flop5')
    except Exception as e:
        print(e)
        return 'request form get error'
    my_hand_list = [my_card1, my_card2]
    for i in my_hand_list:
        if 'none' in i:
            return 'hand card empty'
    for i in [flop1, flop2, flop3]:
        if 'none' in i:
            return 'flop card empty'
    card_list = []
    for i in [my_card1, my_card2, flop1, flop2, flop3, flop4, flop5]:
        if 'none' in i:
            pass
        else:
            card_list.append(i)
    if len(set(card_list)) < len(card_list):
        return 'duplicated card find'

    open_board_deck = []
    for i in [flop1, flop2, flop3, flop4, flop5]:
        if 'none' in i:
            pass
        else:
            open_board_deck.append(i)
    if len(set(card_list)) < len(card_list):
        return 'duplicated card find'
    try:
        print('调用成功')
        print(my_card1, my_card2, flop1, flop2, flop3, flop4, flop5)
        res = Poker().poker_run(my_hold_cards=[my_card1, my_card2], open_board_deck=open_board_deck,
                        enemy_hold_cards=[None, None])
        print(res)
        return res
    except Exception as e:
        print(e)
        return 'model excute failed'




# @poker.route('/progress_bar')
# def progress():
#     """查看进度"""
#     response = make_response(jsonify(dict(n=pbar.n, total=pbar.total)))
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', '*')
#     response.headers.add('Access-Control-Allow-Methods', '*')
#     return response
