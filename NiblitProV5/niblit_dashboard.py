# niblit_dashboard.py - KivyMD green/black ChatUI launcher
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

KV = '''
BoxLayout:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: 0,0.03,0,1
        Rectangle:
            pos: self.pos
            size: self.size
    MDToolbar:
        title: 'Niblit AI'
        md_bg_color: 0,0.1,0,1
        specific_text_color: 0,1,0,1
    ScrollView:
        id: scroll
        do_scroll_x: False
        MDBoxLayout:
            id: chat_box
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: dp(8)
            spacing: dp(6)
    BoxLayout:
        size_hint_y: None
        height: dp(56)
        spacing: dp(8)
        padding: dp(8)
        MDTextField:
            id: user_input
            hint_text: 'Type a message...'
            text_color: 0,1,0,1
            mode: 'rectangle'
        MDRaisedButton:
            text: 'Send'
            md_bg_color: 0,0.2,0,1
            on_release: app.on_send(user_input.text)
'''

class DashboardApp(MDApp):
    def __init__(self, core=None, **kwargs):
        self.core = core
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.theme_style = 'Dark'
        return Builder.load_string(KV)

    def on_start(self):
        Clock.schedule_once(lambda dt: self.add_message('system','Niblit online.'), 0.5)

    def add_message(self, who, text):
        box = self.root.ids.chat_box
        card = MDCard(size_hint=(1,None), padding=dp(8))
        if who == 'user':
            card.add_widget(MDLabel(text='You: ' + text, theme_text_color='Custom', text_color=(0,1,0,1)))
        else:
            card.add_widget(MDLabel(text='Niblit: ' + text, theme_text_color='Custom', text_color=(0,1,0,1)))
        card.height = dp(48)
        box.add_widget(card)
        Clock.schedule_once(lambda dt: self.root.ids.scroll.scroll_to(card), 0.1)

    def on_send(self, text):
        if not text: return
        self.add_message('user', text)
        if self.core:
            resp = self.core.respond(text)
        else:
            resp = 'local placeholder response'
        self.add_message('niblit', resp)
        self.root.ids.user_input.text = ''

def launch_dashboard(core=None):
    app = DashboardApp(core=core)
    app.run()