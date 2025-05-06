
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
import webbrowser
import re
import feedparser

store = JsonStore('user_data.json')
job_store = JsonStore('rss_jobs.json')


class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        box = BoxLayout(orientation='vertical', size_hint=(0.7, 0.3), spacing=10)

        label = Label(text="Karibu kwenye Ajira Plus+", font_size='20sp')
        button = Button(text="Ingia", size_hint=(1, 0.5))
        button.bind(on_press=self.go_next)

        box.add_widget(label)
        box.add_widget(button)
        anchor.add_widget(box)
        self.add_widget(anchor)

    def go_next(self, instance):
        if store.exists('user'):
            App.get_running_app().user_name = store.get('user')['name']
            self.manager.current = 'home'
        else:
            self.manager.current = 'register'


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10), size_hint=(0.9, None))
        layout.bind(minimum_height=layout.setter('height'))

        layout.add_widget(Label(text="Jisajili", font_size='20sp', size_hint=(1, None), height=dp(30)))
        self.username_input = TextInput(hint_text="Jina Kamili", size_hint=(1, None), height=dp(40))
        self.password_input = TextInput(hint_text="Nenosiri", password=True, size_hint=(1, None), height=dp(40))
        self.confirm_input = TextInput(hint_text="Dhibitisha Nenosiri", password=True, size_hint=(1, None), height=dp(40))
        register_button = Button(text="Jisajili", size_hint=(1, None), height=dp(40))
        register_button.bind(on_press=self.register_user)

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(self.confirm_input)
        layout.add_widget(register_button)

        wrapper = AnchorLayout(anchor_x='center', anchor_y='center')
        wrapper.add_widget(layout)
        self.add_widget(wrapper)

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.3))
        popup.open()

    def validate_password(self, password):
        return (
            len(password) >= 6 and
            re.search(r"[A-Za-z]", password) and
            re.search(r"\d", password) and
            re.search(r"[!@#$%^&*(),.?":{}|<>]", password)
        )

    def register_user(self, instance):
        user = self.username_input.text.strip()
        password = self.password_input.text.strip()
        confirm = self.confirm_input.text.strip()

        if not self.validate_password(password):
            self.show_popup("Nenosiri Dhaifu", "Tumia nenosiri lenye herufi, namba, alama maalum na urefu wa kuanzia 6.")
            return

        if password != confirm:
            self.show_popup("Tofauti ya Nenosiri", "Nenosiri na uthibitisho havifanani.")
            return

        App.get_running_app().user_name = user
        store.put('user', name=user)
        self.manager.current = 'home'


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        root_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        scroll_view = ScrollView(size_hint=(1, 1))
        content_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, padding=dp(20))
        content_layout.bind(minimum_height=content_layout.setter('height'))

        banner = Image(source='banner.png', size_hint=(1, None), height=dp(150))
        content_layout.add_widget(banner)

        self.welcome_label = Label(text="Karibu!", font_size='20sp', size_hint=(1, None), height=dp(40))
        content_layout.add_widget(self.welcome_label)

        features = [
            ("💼 Ajira Chap", "rss"),
            ("🎓 Mafunzo", None),
            ("📝 CV na Barua za Kazi", None),
            ("📢 Matangazo ya Biashara", None),
            ("📰 Magazeti ya Leo", None),
            ("💬 Jukwaa la Vijana", None),
            ("▶️ Video za Mafunzo", "https://youtube.com/playlist?list=..."),
            ("📄 PDF za Mwongozo", "https://example.com/mwongozo.pdf")
        ]

        for text, target in features:
            btn = Button(text=text, size_hint=(1, None), height=dp(40))
            if target:
                btn.bind(on_press=lambda instance, val=target: self.feature_clicked(instance, val))
            content_layout.add_widget(btn)

        logout_btn = Button(text="🚪 Toka (Logout)", size_hint=(1, None), height=dp(40))
        logout_btn.bind(on_press=self.logout)
        content_layout.add_widget(logout_btn)

        scroll_view.add_widget(content_layout)
        root_layout.add_widget(scroll_view)
        self.add_widget(root_layout)

    def on_pre_enter(self):
        username = App.get_running_app().user_name
        self.welcome_label.text = f"Karibu {username} kwenye Ajira Plus+"

    def feature_clicked(self, instance, target):
        if target.startswith("http"):
            webbrowser.open(target)
        else:
            self.manager.current = target

    def logout(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="Je uko tayari kuondoka Ajira Plus+?"))

        buttons = BoxLayout(spacing=10, size_hint=(1, None), height=dp(40))
        btn_yes = Button(text="Ndiyo")
        btn_no = Button(text="Hapana")
        buttons.add_widget(btn_yes)
        buttons.add_widget(btn_no)
        content.add_widget(buttons)

        popup = Popup(title="Thibitisha Kuondoka", content=content, size_hint=(0.85, 0.4))
        btn_yes.bind(on_press=lambda x: self.exit_app(popup))
        btn_no.bind(on_press=popup.dismiss)
        popup.open()

    def exit_app(self, popup):
        popup.dismiss()
        App.get_running_app().stop()


class RSSScreen(Screen):
    def __init__(self, **kwargs):
        super(RSSScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        self.search_input = TextInput(hint_text='Tafuta ajira...', size_hint=(1, None), height=dp(40))
        self.search_input.bind(text=self.filter_jobs)
        self.layout.add_widget(self.search_input)

        self.scroll = ScrollView()
        self.feed_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        self.feed_box.bind(minimum_height=self.feed_box.setter('height'))
        self.scroll.add_widget(self.feed_box)

        self.layout.add_widget(Label(text='Ajira Mpya Kutoka Mtandaoni', font_size='18sp', size_hint=(1, None), height=dp(40)))
        self.layout.add_widget(self.scroll)

        btn_back = Button(text="<< Rudi Nyumbani", size_hint=(1, None), height=dp(40))
        btn_back.bind(on_press=self.go_back)
        self.layout.add_widget(btn_back)

        self.add_widget(self.layout)

    def on_pre_enter(self):
        self.load_jobs()

    def load_jobs(self):
        self.feed_box.clear_widgets()
        url = 'https://www.brightermonday.co.tz/jobs.rss'
        feed = feedparser.parse(url)

        if feed.entries:
            job_store.clear()
            for i, entry in enumerate(feed.entries[:20]):
                job_store.put(str(i), title=entry.title, link=entry.link)

        self.display_jobs()

    def display_jobs(self, keyword=''):
        self.feed_box.clear_widgets()
        for key in job_store:
            data = job_store.get(key)
            if keyword.lower() in data['title'].lower():
                btn = Button(text=data['title'], size_hint=(1, None), height=dp(50))
                btn.bind(on_press=lambda instance, url=data['link']: webbrowser.open(url))
                self.feed_box.add_widget(btn)

        if not self.feed_box.children:
            self.feed_box.add_widget(Label(text="Hakuna ajira zinazolingana na ulichotafuta.", size_hint=(1, None), height=dp(40)))

    def filter_jobs(self, instance, value):
        self.display_jobs(keyword=value)

    def go_back(self, instance):
        self.manager.current = 'home'


class AjiraPlusApp(App):
    user_name = ''

    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(RSSScreen(name='rss'))
        sm.current = 'welcome'
        return sm


if __name__ == '__main__':
    AjiraPlusApp().run()
