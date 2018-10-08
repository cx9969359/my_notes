from numpy import *
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw
import sys, os


class Test():
    def test(self):
        image = Image.open(r'C:\Users\Administrator\Desktop\background.png')

        # 打开图片
        draw = ImageDraw.Draw(image)
        width, height = image.size()



if __name__ == '__main__':
    Test().test()
