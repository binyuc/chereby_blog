import json

import pandas as pd
import xgboost as xgb

# TODO 部署前需要改
# root_path = 'D:/Jupyter/爬虫/blog/resource/model/'
root_path = '/root/blogin/blog/resource/model/'

class Fun():

    def anjuke_model(self, area, floor, bedroom, living_room, bathroom, direction, district, neighborhood, built_year):
        tar = xgb.Booster(model_file=root_path + 'xgb.model')
        df = pd.DataFrame(
            data=[[area, floor, bedroom, living_room, bathroom, direction, district, neighborhood, built_year]],
            columns=['area', 'floor', 'bedroom', 'living_room', 'bathroom', 'direction', 'district', 'neighborhood',
                     'built_year'])
        with open(root_path + 'neighborhood_list.json') as fp:
            neighborhood_list = json.load(fp)
        with open(root_path + 'direction_list.json') as fp:
            direction_list = json.load(fp)
        with open(root_path + 'district_list.json') as fp:
            district_list = json.load(fp)
        with open(root_path + 'floor_list.json') as fp:
            floor_list = json.load(fp)
        df['direction'] = df['direction'].apply(lambda x: [i['num'] for i in direction_list if x == i['label']][0])
        df['floor'] = df['floor'].apply(lambda x: [i['num'] for i in floor_list if x == i['label']][0])
        df['district'] = df['district'].apply(lambda x: [i['num'] for i in district_list if x == i['label']][0])
        df['neighborhood'] = df['neighborhood'].apply(
            lambda x: [i['num'] for i in neighborhood_list if x == i['label']][0])
        for col in ['direction', 'floor', 'district', 'neighborhood']:
            df[col].astype('category')
        df = df[['bedroom', 'living_room', 'bathroom', 'area', 'direction', 'floor', 'built_year', 'district',
                 'neighborhood']]
        x_test = xgb.DMatrix(df)
        res = tar.predict(x_test)[0]
        return res

    def anjuke_get_location(self):
        with open(root_path + 'shanghai_list.json') as fp:
            shanghai_list = json.load(fp)
        return shanghai_list


if __name__ == '__main__':
    Fun().anjuke_get_location()
