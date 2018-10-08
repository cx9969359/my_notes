from numpy import *
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw
import sys, os


class Test():
    def test(self):
        title = '声德练就好声音'
        title_font = ImageFont.truetype(font_medium_type, 40)
        # 打开图片
        image = Image.open(r'C:\Users\Administrator\Desktop\background.png')
        # 画图
        draw = ImageDraw.Draw(image)
        # 标题
        draw.text((20, 10), title, font=title_font)
        # 内容框
        draw.polygon([(20, 240), (350, 240), (350, 400), (20, 400)], fill='#ffffff')
        draw.polygon([(20, 440), (350, 440), (350, 600), (20, 600)], fill='#ffffff')
        image.show()


if __name__ == '__main__':
    Test().test()
