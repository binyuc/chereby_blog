import random, string
from datetime import datetime

from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

class ImageCode:
    def gen_text(self):
        list = random.sample(string.ascii_lowercase + string.digits, 5)
        return ''.join(list)

    def rand_color(self):
        red = random.randint(32, 200)
        green = random.randint(22, 255)
        blue = random.randint(32, 200)
        return red, green, blue

    def draw_lines(self, draw , num, width, height):
        for num in range(num):
            x1 = random.randint(0, width /2 )
            y1 = random.randint(0,height /2)
            x2 = random.randint(0,width)
            y2 = random.randint(height /2,height)
            draw.line(((x1,y1),(x2,y2)),fill='black', width=2)

    def draw_verify_code(self):
        code = self.gen_text()
        width, height = 120, 50
        im = Image.new('RGB', (width, height), 'white')
        font = ImageFont.truetype(font='common/SimHei.ttf', size=40)
        draw = ImageDraw.Draw(im)
        for i in range(5):
            draw.text((5 + random.randint(-3, 3) + 23 * i, 5 + random.randint(-3, 3)),
                      text=code[i], fill=self.rand_color(), font=font)
            
        self.draw_lines(draw, 4, width, height)
        # im.show()
        return im, code


    def get_code(self):
        image, code = self.draw_verify_code()
        buf = BytesIO()
        image.save(buf, 'jpeg')
        bstring = buf.getvalue()
        return code, bstring


# 单个模型类转换为标准的Python List数据
def model_list(result):
    list = []
    for row in result:
        dict = {}
        for k, v in row.__dict__.items():
            if not k.startswith('_sa_instance_state'):
                # 如果某个字段的值是datetime类型，则将其格式为字符串
                if isinstance(v, datetime):
                    v = v.strftime('%Y-%m-%d %H:%M:%S')
                dict[k] = v
        list.append(dict)

    return list

# SQLAlchemy连接查询两张表的结果集转换为[{},{}]
# Comment，Users， [(Comment, Users),(Comment, Users),(Comment, Users)]
def model_join_list(result):
    list = []  # 定义列表用于存放所有行
    for obj1, obj2 in result:
        dict = {}
        for k1, v1 in obj1.__dict__.items():
            if not k1.startswith('_sa_instance_state'):
                if not k1 in dict:  # 如果字典中已经存在相同的Key则跳过
                    dict[k1] = v1
        for k2, v2 in obj2.__dict__.items():
            if not k2.startswith('_sa_instance_state'):
                if not k2 in dict:  # 如果字典中已经存在相同的Key则跳过
                    dict[k2] = v2
        list.append(dict)
    return list

if __name__ == '__main__':
    ImageCode().get_code()
