"""
Graduation Report Application for PC and Mobile
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER

imageViewStylePack = Pack(
    width=300, height=300, alignment=CENTER, 
    padding_top=15, padding_bottom=15, font_weight='bold'
)
before_btn_after_Pack = Pack(
    width=150, height=60, text_align='center', color='#11AAFF', background_color='#0000FF', font_size=20
)
before_btn_after_clicked = Pack(
    width=150, height=60, text_align='center', color='#11AAFF', background_color='#0000AA', font_size=20
)
class SR(toga.App):

    def file_open(self, event_source):
        try:
            open_file_path = self.main_window.open_file_dialog("Choose Photo")
            print(open_file_path)
            self.before = toga.images.Image(open_file_path)
            self.image_view.image = self.before
        except ValueError:
            pass
    
    def save(self, *args, **kwargs):
        print(*args)
        # 결과 이미지인 self.res_img.image를 저장한다.
        self.main_window.save_file_dialog("저장 위치 선택", "filename", "JPEG")

    def click_before(self, *args, **kwargs):
        self.result_box.remove(self.res_img)
        self.result_box.insert(0, self.image_view)
        self.after_btn.style.background_color = '#0000FF'
        self.before_btn.style.background_color = '#0000AA'

    def click_after(self, *args, **kwargs):
        self.result_box.remove(self.image_view)
        self.result_box.insert(0, self.res_img)
        self.after_btn.style.background_color = '#0000AA'
        self.before_btn.style.background_color = '#0000FF'
    
    def srStart(self, evenv_source):
        # if self.image_view.image == self.no_img:
        #     self.main_window.error_dialog("Error", "사진을 선택하세요")
        #     return

        self.main_box.style.visibility='hidden'
        self.result_box = toga.Box(style=Pack(
            direction=COLUMN, alignment=CENTER, width=350,
            background_color='#5F157E'
        ))

        # 결과 이미지
        self.res_img = toga.ImageView(style=imageViewStylePack, \
            image=toga.images.Image('C:\\Users\\LeeJongGeol\\Desktop\\new_model\\cropped_imgs\\test\\2018.jpg'))
        self.result_box.add(self.res_img)

        # 버튼과 ImageView 배치
        self.container = toga.Box(
            style=Pack(alignment='center', padding_top=3, height=400, width=350,
            background_color='#5F157E', color='#FFFFFF', direction=COLUMN))
        
        # 가로로 BEFORE, AFTER 버튼 배치할 레이아웃
        btns_box = toga.Box(style=Pack(alignment='center', direction=ROW))
        self.before_btn = toga.Button("BEFORE", on_press=self.click_before, style=before_btn_after_Pack)
        self.after_btn = toga.Button("AFTER", on_press=self.click_after, style=before_btn_after_clicked)
        btns_box.add(self.before_btn)
        btns_box.add(self.after_btn)
        self.container.add(btns_box)
        self.container.add(self.result_box)

        save_btn = toga.Button("저장하기", on_press=self.save, style=Pack(
            padding_top=10, width=300, height=40, padding_bottom=45, font_size=17, font_weight='bold'
        ))

        resultpage_title = toga.Label("복원 전후 비교", style=Pack(
            text_align="center", font_size=20, font_weight="bold", height=60
        ))

        container_box = toga.Box(style=Pack(
            direction=COLUMN, alignment='center',
            background_color='#5F157E'
        ), children=[resultpage_title, self.container, save_btn])
        self.main_window.content = container_box


    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.size = (360, 600)

        self.main_box = toga.Box(style=Pack(
            direction=COLUMN, alignment=CENTER, padding_top=15,
            background_color='#5F157E'
        ))
        self.main_box.add(toga.Label("저해상도 이미지 복원", style=Pack(
            text_align="center", font_size=20, font_weight="bold", height=60
        )))

        self.no_img = toga.images.Image("resources\\no_img.PNG")
        self.image_view = toga.ImageView(image=self.no_img, style=imageViewStylePack)
        self.main_box.add(self.image_view)

        btn = toga.Button("사진 선택하기", on_press=self.file_open, style=Pack(
            padding_top=20, width=200, height=60, font_size=17, font_weight='bold'
        ))
        self.main_box.add(btn)

        srbtn = toga.Button("복원 시작하기", on_press=self.srStart, style=Pack(
            padding_top=10, width=200, height=60, padding_bottom=45, font_size=17, font_weight='bold'
        ))
        self.main_box.add(srbtn)

        self.main_window.content = self.main_box
        self.main_window.show()

    


def main():
    return SR()
