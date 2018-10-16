import math
import os
import random
import urllib.request
from datetime import datetime
from io import BytesIO

import qrcode
from PIL import Image, ImageFont, ImageDraw


class Test():
    def test(self):
        # border = Image.open(r'C:\Users\Administrator\Desktop\开发笔记\mask.png')
        # flower = Image.open(r'C:\Users\Administrator\Desktop\开发笔记\my_avator1.png')
        # # source = border.convert('RGB')
        # # flower.paste(source, mask=border)
        # # flower.save('new.png')
        #
        # source = flower.convert('RGB')
        # border.paste(source, mask=flower)
        # border.save('new.png')

        # 打开图片
        background_img = Image.open(r'C:\Users\Administrator\Desktop\开发笔记\background.jpg')
        total_width = 580
        height = 1032
        background_img = background_img.resize((total_width, height), Image.ANTIALIAS)
        draw = ImageDraw.Draw(background_img)

        # 时间
        year_and_month = str(datetime.now().year) + '.' + str(datetime.now().month)
        day = str(datetime.now().day)
        day_font = ImageFont.truetype('Hiragino SansGBW3.otf', 39)
        month_and_year_font = ImageFont.truetype('Hiragino SansGBW3.otf', 20)
        day_width, day_height = day_font.getsize(day)

        month_width, month_height = month_and_year_font.getsize(year_and_month)
        draw.line([(250, 41), (330, 41)], fill='#fff', width=2)
        draw.text(((total_width - day_width) / 2, 50), day, font=day_font, fill='#fff')
        draw.text(((total_width - month_width) / 2, 95), year_and_month, font=month_and_year_font, fill='#fff')
        draw.line([(250, 124), (330, 124)], fill='#fff', width=2)

        # 主题
        content = self.get_poster_motto_by_chance()
        content_list = content.split(' ')
        for index, content in enumerate(content_list):
            content_font = ImageFont.truetype('Hiragino SansGBW3.otf', 30)
            author_font = ImageFont.truetype('Hiragino SansGBW3.otf', 22)
            content_w, _ = content_font.getsize(content)
            author_w, _ = author_font.getsize(content)
            if '—' in content:
                draw.text(((total_width - author_w) / 2, 300 + index * 54), content, font=author_font, fill='#fff')
            else:
                draw.text(((total_width - content_w) / 2, 300 + index * 50), content, font=content_font, fill='#fff')
        # 中部内容框
        nickname = '微信昵称'
        sign = '刚刚在【{project_name}】上完成打卡'.format(project_name='练就好声音')
        sign_font = ImageFont.truetype('Hiragino SansGBW3.otf', 16)
        # 微信头像
        raw_avator_img = Image.open(r'C:\Users\Administrator\Desktop\开发笔记\my_avator.png')
        raw_avator_img = raw_avator_img.resize((64, 64), Image.ANTIALIAS)
        # 将头像处理成圆角矩形
        crop_avator_img_path = self.crop_circle(raw_avator_img)
        raw_avator_img.close()
        crop_avator_img = Image.open(crop_avator_img_path)
        background_img.paste(crop_avator_img, (22, 838))

        nickname_font = ImageFont.truetype('Hiragino SansGBW3.otf', 24)
        draw.text((105, 842), nickname, font=nickname_font, fill='#202020')
        draw.text((105, 884), sign, font=sign_font, fill='#999')
        # 统计标题
        draw.text((22, 935), '累计打卡', font=sign_font, fill='#666')
        draw.text((158, 935), '声音能量', font=sign_font, fill='#666')
        draw.text((314, 935), '今日练习', font=sign_font, fill='#666')
        # 统计值
        punch_record_num = str(78)
        total_coin = str(300)
        practice_duration = str(1)
        statistical_font = ImageFont.truetype('Hiragino SansGBW3.otf', 30)
        first_font = '篇'
        second_font = '分贝'
        third_font = '分钟'
        punch_record_width, r_h = statistical_font.getsize(punch_record_num)
        total_coin_width, c_h = statistical_font.getsize(total_coin)
        practice_duration_width, d_h = statistical_font.getsize(practice_duration)

        draw.text((20, 960), punch_record_num, font=statistical_font, fill='#3030')
        draw.text((20 + punch_record_width + 4, 970), first_font, font=sign_font, fill='#666')
        draw.text((152, 960), total_coin, font=statistical_font, fill='#3030')
        draw.text((152 + total_coin_width + 4, 970), second_font, font=sign_font, fill='#666')
        draw.text((314, 960), practice_duration, font=statistical_font, fill='#3030')
        draw.text((314 + practice_duration_width + 4, 970), third_font, font=sign_font, fill='#666')

        # 二维码
        qr_code_file_path = self.get_daily_attendance_qr_code()
        qr_img = Image.open(qr_code_file_path)
        qr_img = qr_img.resize((92, 92), Image.ANTIALIAS)
        background_img.paste(qr_img, (456, 857))
        qr_img.close()
        # os.remove(qr_code_file_path)

        # 二维码底部描述
        draw.line([(436, 870), (436, 985)], fill='#ddd', width=2)
        bottom_content_font = ImageFont.truetype('Hiragino SansGBW3.otf', 15)
        draw.text((456, 955), '在这里，让声', font=bottom_content_font, fill='#24bcfc')
        draw.text((456, 978), '音变得更好听', font=bottom_content_font, fill='#24bcfc')

        # 转成IO流
        bytes_in = BytesIO()
        background_img.save(bytes_in, format='PNG')
        img_IO = bytes_in.getvalue()

        with open(r'C:\Users\Administrator\Desktop\开发笔记\nice.jpg', 'wb') as f:
            f.write(img_IO)
        background_img.show()
        background_img.close()

    def crop_circle(self, img):
        # 圆角半径
        img = img.convert('RGBA')
        rad = 15
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
        crop_avator_img_path = os.getcwd() + '/crop_avator.png'
        print(crop_avator_img_path)
        return crop_avator_img_path

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
        qr_img.save('qr_code_of_daily_attendance.jpg')
        qr_code_file_path = os.getcwd() + '/qr_code_of_daily_attendance.jpg'
        return qr_code_file_path

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
