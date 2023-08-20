from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, SlideTransition
import pandas as pd
import webbrowser

SHEET_ID = "1RPP1n2KIPHTGvyLrPNcr_Hx8-JGMCp6J8F71woej33I"
SHEET_NAME = "Munkalap1"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"


def get_datas():
    # kiolvassa az adatokat az excelből
    datas = pd.read_csv(URL)
    return datas


def user_sec_lvl(name):
    # visszaadja az adott user sec lvl-ét integerként
    data = get_datas()
    users = data["user"].to_list()
    user_lvl = data["user_sec_lvl"].to_list()
    users_dict = {key: int(value) for key, value in zip(users, user_lvl) if isinstance(key, str)}
    your_lvl = users_dict[name]
    return your_lvl


def links_kw(keywords):
    # listába válogatja a megadott kulcsszavaknak megfelelő linkeket
    links = []
    data = get_datas()
    video_keywords = data["keyword"].to_list()
    video_links = data['link'].to_list()
    for kw in keywords:
        for vid_kw, vid_link in zip(video_keywords, video_links):
            if kw in vid_kw.split(", "):
                links.append(vid_link)
    return list(set(links))


def splitter(keywords):
    # feldarabolja a stringet a vesszőknél és listaként adja vissza
    words = keywords.replace(' ', '').split(',')
    if "" in words:
        words.remove("")
    words = [word.lower() for word in words]
    return words


def links_to_print(user_links, kw_links):
    # listába válogatja a sec lvl-nek és kw-nek megfelelő linkeket
    links = [link for link in kw_links if link in user_links]
    return links


class DynamicLabelPopup(Popup):
    def __init__(self, dynamic_text, **kwargs):
        super(DynamicLabelPopup, self).__init__(**kwargs)
        content = BoxLayout(orientation='vertical')
        label = Label(text=dynamic_text)
        close_button = Button(
            text="Bezárás",
            on_release=self.dismiss,
            size_hint=(1, None),
            height=30)
        content.add_widget(label)
        content.add_widget(close_button)
        self.content = content


class Interface(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = SlideTransition()
        self.datas = get_datas()
        self.user = str()
        self.keywords = list()
        self.user_links = list()
        self.kw_links = list()
        self.links_to_print = list()

    def links_widget(self):
        # kattintható linkeket tesz az utolsó oldalra
        for link in self.links_to_print:
            self.btn = Button(
                text=link,
                size_hint=(.9, None),
                height=78,
                halign="center",
                background_color=(0, 0, 0, 0),
                on_press=self.btn_click)
            self.ids.links.add_widget(self.btn)
            self.btn.bind(width=self.adjust_text_width)

    def adjust_text_width(self, instance, value):
        instance.text_size = (value, None)

    def btn_click(self, click):
        # megnyitja a linket a szövegre kattintva
        webbrowser.open(click.text)

    def popup(self, text, title='Hiba!'):
        popup = DynamicLabelPopup(
            dynamic_text=text,
            title=title,
            title_align='center',
            size_hint=(.65, .5))
        popup.open()

    def is_user(self):
        #megvizsgálja, hogy a megadott User ID-nak van e hozzáférési jogosultsága
        users = self.datas["user"].to_list()
        user_list = [user for user in users if isinstance(user, str)]
        if self.ids.user_id.text in user_list:
            return True

    def is_empty(self, to_check):
        #megvizsgálja, hogy a mező ki lett e töltve
        if len(to_check) == 0:
            return True

    def links_sec_lvl(self):
        # listába válogatja a user sec lvl-nek megfelelő linkeket
        your_lvl = user_sec_lvl(name=self.user)
        video_sec_lvl = self.datas['security_level'].to_list()
        video_links = self.datas['link'].to_list()
        links = [vid_link for vid_sec_lvl, vid_link in zip(video_sec_lvl, video_links) if your_lvl >= vid_sec_lvl]
        return links

    def btn_continue(self):
        self.user = self.ids.user_id.text
        if not self.is_empty(self.user):
            if self.is_user():
                self.user_links = self.links_sec_lvl()
                self.current = 'keywords'
                self.transition.direction = 'left'
            else:
                self.popup(text='Nincs ilyen nevű felhasználó!', title='Nem létező user ID.')
        else:
            self.popup(text='Kérlek add meg a user ID-t!', title='A mező kitöltése kötelező.')

    def btn_search(self):
        self.keywords = self.ids.keywords.text
        if not self.is_empty(self.keywords):
            self.keywords = splitter(self.keywords)
            self.kw_links = links_kw(self.keywords)
            self.links_to_print = links_to_print(kw_links=self.kw_links, user_links=self.user_links)
            self.links_widget()
            self.current = 'results'
            self.transition.direction = 'left'
        else:
            self.popup(text='Kérlek add meg a keresendő kulcsszavakat!', title='A mező kitöltése kötelező.')

    def btn_back(self):
        if self.current == 'results':
            self.ids.links.clear_widgets()
            self.links_to_print = list()
            self.ids.keywords.text = str()
            self.keywords = list()
            self.kw_links = list()
            self.current = 'keywords'
        else:
            self.user_links = list()
            self.ids.user_id.text = str()
            self.user = str()
            self.current = 'user_id'
        self.transition.direction = 'right'


class AccessLocatorApp(App):
    ...


if __name__ == '__main__':
    AccessLocatorApp().run()
