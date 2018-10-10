import urllib.request
from datetime import datetime
from io import BytesIO

import qrcode
from PIL import Image, ImageFont, ImageDraw


class Test():
    def test(self):
        # 打开图片
        background_img = Image.open(r'C:\Users\Administrator\Desktop\开发笔记\my_notes\background.png')
        draw = ImageDraw.Draw(background_img)

        # 商标
        brand = '声德·练就好声音'
        brand_font = ImageFont.truetype('simsun.ttc', 40)
        draw.text((30, 40), brand, font=brand_font, fill='#000000')

        # 时间
        day = str(datetime.now().day)
        month = datetime.now().strftime('%b')
        year = str(datetime.now().year)
        day_font = ImageFont.truetype('simsun.ttc', 55)
        month_and_year_font = ImageFont.truetype('simsun.ttc', 35)
        draw.text((50, 150), day, font=day_font, fill='#000')
        draw.text((50, 210), month, font=month_and_year_font, fill='#000')
        draw.text((110, 210), year, font=month_and_year_font, fill='#000')

        # 标题
        title = '你的声音里藏着你走过的路，看过的文字。'
        title_font = ImageFont.truetype('simsun.ttc', 28)
        draw.text((120, 350), title, font=title_font, fill='#000')

        # 中部内容框
        draw.polygon([(40, 550), (710, 550), (710, 900), (40, 900)], fill='#fff')
        nickname = '微信昵称'
        sign = '刚刚在【{project_name}】上完成打卡'.format(project_name='练就好声音')
        sign_font = ImageFont.truetype('simsun.ttc', 24)
        # 微信头像
        # avator_url = Image.open(urllib.request.urlopen(student.avator))
        avator_img = Image.open(r'C:\Users\Administrator\Desktop\开发笔记\my_notes\my_avator.jpg')
        background_img.paste(avator_img, (130, 580))
        draw.text((280, 580), nickname, font=title_font, fill='#000')
        draw.text((280, 630), sign, font=sign_font, fill='#000')
        # 线
        draw.line([(120, 720), (630, 720)], fill='#000', width=1)
        # 统计标题
        draw.text((100, 750), '累计打卡', font=sign_font, fill='#000')
        draw.text((320, 750), '声音能量', font=sign_font, fill='#000')
        draw.text((540, 750), '今日练习', font=sign_font, fill='#000')
        # 统计值
        punch_record_num = 48
        total_coin = 398
        practice_duration = 38
        draw.text((100, 810), str(punch_record_num), font=day_font, fill='#000')
        draw.text((180, 826), '篇', font=sign_font, fill='#000')
        draw.text((320, 810), str(total_coin), font=day_font, fill='#000')
        draw.text((400, 826), '分贝', font=sign_font, fill='#000')
        draw.text((540, 810), str(practice_duration), font=day_font, fill='#000')
        draw.text((620, 826), '分钟', font=sign_font, fill='#000')

        # 底部内容框
        draw.polygon([(40, 950), (710, 950), (710, 1200), (40, 1200)], fill='#fff')
        bottom_title_font = ImageFont.truetype('simsun.ttc', 32)
        bottom_content_font = ImageFont.truetype('simsun.ttc', 26)
        draw.text((80, 1000), '练就好声音', font=bottom_title_font, fill='#000')
        draw.text((80, 1050), '在这里，让声音变得更好听', font=bottom_content_font, fill='#000')
        # 二维码提示语
        draw.polygon([(100, 1100), (400, 1100), (400, 1150), (100, 1150)], fill='#bfbfbf')
        draw.text((156, 1112), '长按识别二维码', font=bottom_content_font, fill='#000')
        # 二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=7,
            border=4,
        )
        qr.add_data('http://baidu.com')
        qr.make(fit=True)
        qr_img = qr.make_image()
        qr_img.save('daily_attendance.jpg')
        qr_img = Image.open(r'C:\Users\Administrator\Desktop\开发笔记\my_notes\daily_attendance.jpg')
        background_img.paste(qr_img, (490, 980))
        # background_img.thumbnail((350,1000),Image.ANTIALIAS)

        # 转成IO流
        bytes_in = BytesIO()
        background_img.save(bytes_in, format='PNG')
        img_IO = bytes_in.getvalue()

        with open(r'C:\Users\Administrator\Desktop\开发笔记\nice.png', 'wb') as f:
            f.write(img_IO)
        background_img.show()

    def create_downloadable_poster(self, poster):
        """
        将本地生成的二进制poster文件上传至OSS并获得key
        :param poster:
        :return:
        """
        upload_folder, file_name = self.init_upload()
        poster_file_name = file_name + '.jpg'
        poster_file_path = os.path.join(upload_folder, poster_file_name)
        # 上传文件
        with open(poster_file_path, "wb") as pdf:
            for chunk in poster.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)
        # 获取key
        key = self.upload_file(poster_file_name, 'daily_attendance')
        return key


if __name__ == '__main__':
    Test().test()
