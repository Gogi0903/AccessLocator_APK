from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

class DynamicLabelPopup(Popup):
    def __init__(self, dynamic_text, **kwargs):
        super(DynamicLabelPopup, self).__init__(**kwargs)
        content = BoxLayout(orientation='vertical')
        label = Label(text=dynamic_text)
        close_button = Button(text="Bezárás", on_release=self.dismiss)
        content.add_widget(label)
        content.add_widget(close_button)
        self.content = content

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        open_button = Button(text='Nyitás', on_release=self.open_popup)
        layout.add_widget(open_button)
        return layout

    def open_popup(self, instance):
        dynamic_text = "Ez egy dinamikus Label a Popup ablakban!"
        popup = DynamicLabelPopup(dynamic_text=dynamic_text, title="Dinamikus Label Popup")
        popup.open()

if __name__ == '__main__':
    MyApp().run()
