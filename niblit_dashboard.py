# niblit_dashboard.py
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

KV = '''
BoxLayout:
    orientation: 'vertical'
    MDToolbar:
        title: 'Niblit'
        elevation: 4
        md_bg_color: app.theme_cls.primary_color
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
        height: dp(48)
        spacing: dp(6)
        padding: dp(6)
        MDTextField:
            id: user_input
            hint_text: 'Type a message...'
            size_hint_x: 0.85
        MDRaisedButton:
            text: 'Send'
            size_hint_x: 0.15
            on_release: app.on_send(user_input.text)
'''

class DashboardApp(MDApp):
    def __init__(self, core=None, **kwargs):
        self.core = core
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(KV)

    def on_start(self):
        Clock.schedule_once(lambda dt: self.add_message('system','Niblit online.'), 0.4)
        Clock.schedule_interval(lambda dt: self._update_status(), 5)

    def add_message(self, who, text):
        box = self.root.ids.chat_box
        card = MDCard(padding=dp(8), size_hint=(1,None))
        if who == 'user':
            card.add_widget(MDLabel(text='You: ' + text))
        else:
            card.add_widget(MDLabel(text='Niblit: ' + text))
        card.height = dp(48)
        box.add_widget(card)
        Clock.schedule_once(lambda dt: self.root.ids.scroll.scroll_to(card), 0.05)

    def on_send(self, text):
        if not text:
            return
        self.add_message('user', text)
        if self.core:
            resp = self.core.respond(text)
        else:
            resp = 'local placeholder response'
        self.add_message('niblit', resp)
        self.root.ids.user_input.text = ''

    def _update_status(self):
        try:
            if self.core and hasattr(self.core, 'sensors'):
                s = getattr(self.core, 'sensors', None)
                if s and hasattr(s, 'SENSOR_STATUS'):
                    st = s.SENSOR_STATUS if hasattr(s, 'SENSOR_STATUS') else None
                else:
                    st = None
            else:
                st = None
            if st:
                self.add_message('system', f"GPS: {st.get('gps')}, last: {st.get('last_update')}")
        except Exception:
            pass

def launch_dashboard(core=None):
    app = DashboardApp(core=core)
    app.run()