import math
import os
import urllib.request
from datetime import datetime
from io import BytesIO

import qrcode
from PIL import Image, ImageFont, ImageDraw
import random


class Test():
    def test(self):
        # 打开图片
        background_img = Image.open(r'C:\Users\Administrator\Desktop\开发笔记\background.jpg')
        width = 580
        height = 1032
        background_img = background_img.resize((width, height), Image.ANTIALIAS)
        draw = ImageDraw.Draw(background_img)

        # 时间
        year = str(datetime.now().year)
        month = str(datetime.now().month)
        day = str(datetime.now().day)
        day_font = ImageFont.truetype('simsun.ttc', 39)
        month_and_year_font = ImageFont.truetype('simsun.ttc', 20)

        draw.line([(250, 41), (330, 41)], fill='#fff', width=2)
        draw.text((268, 50), day, font=day_font, fill='#fff')
        draw.text((254, 95), year + '.' + month, font=month_and_year_font, fill='#fff')
        draw.line([(250, 124), (330, 124)], fill='#fff', width=2)

        # 主题
        content = self.get_poster_motto_by_chance()
        content_list = content.split(' ')
        for index, content in enumerate(content_list):
            content_font = ImageFont.truetype('simsun.ttc', 30)
            w, h = content_font.getsize(content)
            draw.text(((width - w) / 2, 306 + index * 50), content, font=content_font, fill='#fff')

        # 中部内容框
        nickname = '微信昵称'
        sign = '刚刚在【{project_name}】上完成打卡'.format(project_name='练就好声音')
        sign_font = ImageFont.truetype('simsun.ttc', 19)
        # 微信头像
        # avator_url = Image.open(urllib.request.urlopen(student.avator))
        raw_avator_img = Image.open(r'C:\Users\Administrator\Desktop\开发笔记\my_avator.jpg')
        raw_avator_img = raw_avator_img.resize((64, 64), Image.ANTIALIAS)

        # 将头像处理成圆角矩形
        self.crop_circle(raw_avator_img)
        raw_avator_img.close()
        crop_avator_img = Image.open(r'C:\Users\Administrator\Desktop\开发笔记\crop_avator.png')
        background_img.paste(crop_avator_img, (22, 838))

        nickname_font = ImageFont.truetype('simsun.ttc', 26)
        draw.text((105, 842), nickname, font=nickname_font, fill='#202020')
        draw.text((105, 884), sign, font=sign_font, fill='#999')
        # 统计标题
        draw.text((22, 935), '累计打卡', font=sign_font, fill='#666')
        draw.text((158, 935), '声音能量', font=sign_font, fill='#666')
        draw.text((314, 935), '今日练习', font=sign_font, fill='#666')
        # 统计值
        punch_record_num = 48
        total_coin = 398
        practice_duration = 38
        statistical_font = ImageFont.truetype('simsun.ttc', 32)
        draw.text((22, 960), str(punch_record_num), font=statistical_font, fill='#3030')
        draw.text((70, 970), '篇', font=sign_font, fill='#666')
        draw.text((152, 960), str(total_coin), font=statistical_font, fill='#3030')
        draw.text((204, 970), '分贝', font=sign_font, fill='#666')
        draw.text((314, 960), str(practice_duration), font=statistical_font, fill='#3030')
        draw.text((350, 970), '分钟', font=sign_font, fill='#666')

        # 二维码
        self.get_daily_attendance_qr_code()
        qr_img = Image.open(r'C:\Users\Administrator\Desktop\开发笔记\qr_code_of_daily_attendance.png')
        background_img.paste(qr_img, (456, 857))

        # 二维码底部描述
        draw.line([(436, 870), (436, 985)], fill='#ddd', width=2)
        bottom_content_font = ImageFont.truetype('simsun.ttc', 15)
        draw.text((456, 960), '在这里，让声', font=bottom_content_font, fill='#24bcfc')
        draw.text((456, 980), '音变得更好听', font=bottom_content_font, fill='#24bcfc')

        # 转成IO流
        bytes_in = BytesIO()
        background_img.save(bytes_in, format='PNG')
        img_IO = bytes_in.getvalue()

        with open(r'C:\Users\Administrator\Desktop\开发笔记\nice.png', 'wb') as f:
            f.write(img_IO)
        background_img.show()
        background_img.close()

    def crop_circle(self, img):
        # 圆角半径
        rad = 10
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        alpha = Image.new('L', img.size, 255)
        w, h = img.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        img.putalpha(alpha)
        img.save('crop_avator.png')

    def circle(self, img, size_x, size_y, antialias=4):
        size_enlarge = (size_x * antialias, size_y * antialias)
        img = img.resize((size_x, size_y))
        mask = Image.new('L', size_enlarge, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size_enlarge, fill=255)
        mask = mask.resize(img.size, Image.ANTIALIAS)
        img.putalpha(mask)
        return img

    def get_daily_attendance_qr_code(self):
        """
        生成日签带参二维码
        :return:
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=1,
        )
        qr.add_data('http://baidu.com')
        qr.make(fit=True)
        qr_img = qr.make_image()
        qr_img.save('qr_code_of_daily_attendance.png')

    def get_poster_motto_by_chance(self):
        """
        从句子库中随机获得一句
        :return:
        """
        file = open(r'C:\Users\Administrator\Desktop\开发笔记\motto.txt')
        line_list = []
        while True:
            line = file.readline()
            if not line:
                break
            line_list.append(line.strip())
        file.close()
        target_sentence = random.choice(line_list)
        return target_sentence


if __name__ == '__main__':
    Test().test()
