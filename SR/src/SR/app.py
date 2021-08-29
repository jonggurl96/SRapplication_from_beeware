"""
Graduation Report Application for PC and Mobile
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER


class SR(toga.App):

    def file_open(self, event_source):
        try:
            open_file_path = self.main_window.open_file_dialog("Choose Photo")
            print(open_file_path)
            self.before = toga.images.Image(open_file_path)
            self.image_view.image = self.before
        except ValueError:
            pass

    def srStart(self, evenv_source):
        self.main_box.style.visibility='hidden'
        result_box = toga.Box(style=Pack(
            direction=COLUMN, padding=15, alignment='center',
            background_color='#1188FF'
        ))
        result_box.add(toga.Label("new page"))
        self.main_window.content = result_box


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
            background_color='#FF00FF'
        ))
        self.main_box.add(toga.Label("저해상도 이미지 복원", style=Pack(
            text_align="center", font_size=20, font_weight="bold"
        )))

        self.no_img = toga.images.Image("resources\\no_img.PNG")
        self.image_view = toga.ImageView(image=self.no_img, style=Pack(
            width=300, height=300, alignment=CENTER, padding_top=10
        ))
        self.main_box.add(self.image_view)

        btn = toga.Button("Choose Photo", on_press=self.file_open, style=Pack(
            padding_top=30, width=200, height=60
        ))
        self.main_box.add(btn)

        srbtn = toga.Button("Start Resolution", on_press=self.srStart, style=Pack(
            padding_top=10, width=200, height=60, padding_bottom=20
        ))
        self.main_box.add(srbtn)

        self.main_window.content = self.main_box
        self.main_window.show()

    


def main():
    return SR()
