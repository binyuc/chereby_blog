from flask import Blueprint, render_template, request, jsonify

from module.fun import Fun

fun = Blueprint('fun', __name__)


@fun.route('/anjuke-predict', methods=['POST'])
def model_predict():
    try:
        estate = request.form.get('estate')
        area = int(request.form.get('area'))
        floor = request.form.get('floor')
        bedroom = int(request.form.get('bedroom'))
        living_room = int(request.form.get('living_room'))
        bathroom = int(request.form.get('bathroom'))
        direction = request.form.get('direction')
        district = request.form.get('district')
        neighborhood = request.form.get('neighborhood')
        built_year = int(request.form.get('built_year'))
    except Exception as e:
        print(e)
        return 'parse parma failed unknown'
    fun = Fun()
    try:
        res = fun.anjuke_model(area, floor, bedroom, living_room, bathroom, direction, district, neighborhood,
                               built_year)
        return str(round(res, 3))
    except Exception as e:
        print(e)
        return 'model excute failed'


@fun.route('/anjuke')
def get_location_list():
    fun = Fun()
    shanghai_list = fun.anjuke_get_location()
    return render_template('/tableau/anjuke.html', shanghai_list=shanghai_list)


@fun.route('/anjuke', methods=['POST'])
def filter_location_list():
    district = request.form.get('district')
    filtered_list = []
    fun = Fun()
    shanghai_list = fun.anjuke_get_location()
    for loc in shanghai_list:
        for k, v in loc.items():
            if district == k:
                filtered_list = list(loc.values())[0]
    return jsonify(filtered_list)
