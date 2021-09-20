"""
Graduation Report Application for PC and Mobile
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER

import numpy as np
import PIL as pil
import datetime
import tensorflow as tf

input_image_view_style = Pack(
    width=300, height=300, alignment=CENTER,
    font_weight='bold', background_color='#4A868C',
    padding_top=3
)
btns_before_after_unclicked = Pack(
    width=150, height=60, text_align='center', color='#BAF1EE', background_color='#306065', font_size=20
)
btns_before_after_clicked = Pack(
    width=150, height=60, text_align='center', color='#BAF1EE', background_color='#234549', font_size=20
)
main_window_content_style = Pack(
    direction=COLUMN, alignment=CENTER, background_color='#0E1F26'
)
title_label_pack = Pack(
    text_align="center", font_size=20, font_weight="bold", height=60,
    color='#FFFFFF'
)

def new_file_path():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

class SR(toga.App):

    def file_open(self, event_source):
        try:
            open_file_path = self.main_window.open_file_dialog("Choose Photo")
            self.input_image = pil.Image.open(open_file_path).convert("RGB")
            self.input_image = np.array(self.input_image) / 255.0
            self.image_view.image = toga.images.Image(open_file_path)
        except ValueError:
            pass

    def new_filename(self):
        now = datetime.datetime.now()
        now = now.strftime('%Y%m%d_%H%M%S')
        return "sr_" + now + ".jpg"

    def save(self, *args, **kwargs):
        # 결과 이미지인 self.res_img.image를 저장한다.
        try:
            file_save_path = self.main_window.save_file_dialog("저장 위치 선택", self.new_filename())
            with pil.Image.open("src\\SR\\tmp_imgs\\" + self.fn + ".jpg") as im:
                im.save(file_save_path)
                im.close()
        except ValueError:
            pass

    def click_before(self, *args, **kwargs):
        self.result_box.remove(self.res_img)
        self.result_box.insert(0, self.image_view)
        self.after_btn.style.background_color = '#306065'
        self.before_btn.style.background_color = '#234549'

    def click_after(self, *args, **kwargs):
        self.result_box.remove(self.image_view)
        self.result_box.insert(0, self.res_img)
        self.after_btn.style.background_color = '#234549'
        self.before_btn.style.background_color = '#306065'

    def predict(self):
        result = None
        model = tf.keras.models.load_model('model_200.h5')
        result = model.predict(self.input_image.reshape((1, 300, 300, 3)))
        result = (result * 255).astype(np.uint8)
        self.fn = new_file_path()
        with pil.Image.fromarray(result.reshape((300, 300, 3))) as result:
            result.save("src\\SR\\tmp_imgs\\" + self.fn + ".jpg")
            result.close()

    def back(self, *args, **kwargs):
        no_img = toga.images.Image("resources\\no_img.PNG")
        self.image_view.image = no_img
        self.container_box.style.visibility = 'hidden'
        self.main_box.style.visibility = 'visible'

    def srStart(self, evenv_source):
        if self.image_view.image == self.no_img:
            self.main_window.error_dialog("Error", "사진을 선택하세요")
            return
        
        # model 불러와서 예측하기~~~
        self.predict()

        self.result_box = toga.Box(style=Pack(
            direction=COLUMN, alignment=CENTER,
            background_color='#4A868C'
        ))

        # 결과 이미지
        self.res_img = toga.ImageView(style=input_image_view_style,
                                      image=toga.images.Image("tmp_imgs\\" + self.fn + ".jpg"))
        self.result_box.add(self.res_img)

        # 버튼과 ImageView 배치
        self.container = toga.Box(
            style=Pack(alignment='center', padding_top=3, height=400, width=350,
                       background_color='#4A868C', color='#FFFFFF', direction=COLUMN))

        # 가로로 BEFORE, AFTER 버튼 배치할 레이아웃
        btns_box = toga.Box(style=Pack(alignment='center', direction=ROW))
        self.before_btn = toga.Button(
            "BEFORE", on_press=self.click_before, style=btns_before_after_unclicked)
        self.after_btn = toga.Button(
            "AFTER", on_press=self.click_after, style=btns_before_after_clicked)
        btns_box.add(self.before_btn)
        btns_box.add(self.after_btn)
        self.container.add(btns_box)
        self.container.add(self.result_box)

        save_btn = toga.Button("저장하기", on_press=self.save, style=Pack(
            padding_top=10, width=300, height=40, font_size=17, font_weight='bold',
            background_color="#121213", color='#86B8BE'
        ))

        back_btn = toga.Button("처음으로", on_press=self.back, style=Pack(
            padding_top=10, width=300, height=40, padding_bottom=45, font_size=17, font_weight='bold',
            background_color="#121213", color='#86B8BE'
        ))

        resultpage_title = toga.Label("복원 전후 비교", style=title_label_pack)

        self.container_box = toga.Box(style=main_window_content_style,
                                 children=[resultpage_title, self.container, save_btn, back_btn])
        self.main_box.style.visibility = 'hidden'
        self.main_window.content = self.container_box

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.size = (360, 600)

        self.main_box = toga.Box(style=main_window_content_style)
        self.main_box.add(toga.Label("저해상도 이미지 복원", style=title_label_pack))

        self.no_img = toga.images.Image("resources\\no_img.PNG")
        self.image_view = toga.ImageView(
            image=self.no_img, style=input_image_view_style)
        self.main_box.add(self.image_view)

        btn = toga.Button("사진 선택하기", on_press=self.file_open, style=Pack(
            padding_top=20, width=200, height=60, font_size=17, font_weight='bold',
            background_color='#306065', color='#BAF1EE'
        ))
        self.main_box.add(btn)

        srbtn = toga.Button("복원 시작하기", on_press=self.srStart, style=Pack(
            padding_top=10, width=200, height=60, padding_bottom=45, font_size=17, font_weight='bold',
            background_color='#306065', color='#BAF1EE'
        ))
        self.main_box.add(srbtn)

        self.main_window.content = self.main_box
        self.main_window.show()


def main():
    return SR()
