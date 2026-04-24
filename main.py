from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton

from services.weather_service import WeatherService
from managers.favorites_manager import FavoritesManager
from managers.settings_manager import SettingsManager

from screens.home_screen import HomeScreen
from screens.search_screen import SearchScreen
from screens.favorites_screen import FavoritesScreen
from screens.forecast_screen import ForecastScreen
from screens.settings_screen import SettingsScreen

API_KEY = "48a6c8f768aa8431c407a95bf8b878f1"

KV = '''
<Footer@MDBoxLayout>:
    size_hint_y: None
    height: "90dp"
    padding: 0, 10, 0, 15
    md_bg_color: 0.75, 0.9, 0.95, 1

    MDBoxLayout:
        orientation: "vertical"

        MDIconButton:
            icon: "home"
            pos_hint: {"center_x": 0.5}
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color if app.active_screen == "home" else (0,0,0,1)
            on_release:
                app.root.current = "home"
                app.active_screen = "home"

        MDLabel:
            text: "[b]Ana Sayfa[/b]"
            markup: True
            halign: "center"

    MDBoxLayout:
        orientation: "vertical"

        MDIconButton:
            icon: "magnify"
            pos_hint: {"center_x": 0.5}
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color if app.active_screen == "search" else (0,0,0,1)
            on_release:
                app.root.current = "search"
                app.active_screen = "search"

        MDLabel:
            text: "[b]Ara[/b]"
            markup: True
            halign: "center"

    MDBoxLayout:
        orientation: "vertical"

        MDIconButton:
            icon: "heart"
            pos_hint: {"center_x": 0.5}
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color if app.active_screen == "favorites" else (0,0,0,1)
            on_release:
                app.open_favorites()

        MDLabel:
            text: "[b]Favoriler[/b]"
            markup: True
            halign: "center"

    MDBoxLayout:
        orientation: "vertical"

        MDIconButton:
            icon: "chart-line"
            pos_hint: {"center_x": 0.5}
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color if app.active_screen == "forecast" else (0,0,0,1)
            on_release:
                app.open_forecast()

        MDLabel:
            text: "[b]Tahmin[/b]"
            markup: True
            halign: "center"

    MDBoxLayout:
        orientation: "vertical"

        MDIconButton:
            icon: "cog"
            pos_hint: {"center_x": 0.5}
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color if app.active_screen == "settings" else (0,0,0,1)
            on_release:
                app.root.current = "settings"
                app.active_screen = "settings"

        MDLabel:
            text: "[b]Ayarlar[/b]"
            markup: True
            halign: "center"


ScreenManager:
    HomeScreen:
    SearchScreen:
    FavoritesScreen:
    ForecastScreen:
    SettingsScreen:


<HomeScreen>:
    name: "home"

    MDBoxLayout:
        orientation: "vertical"

        MDBoxLayout:
            orientation: "vertical"
            padding: 20
            spacing: 12

            MDLabel:
                id: city
                text: "Yükleniyor..."
                halign: "center"
                font_style: "H3"

            MDLabel:
                id: temp
                text: ""
                halign: "center"
                font_style: "H1"

            MDLabel:
                id: desc
                text: ""
                halign: "center"
                font_style: "H5"

            MDBoxLayout:
                orientation: "horizontal"
                spacing: 20

                MDLabel:
                    id: humidity
                    text: ""
                    halign: "center"

                MDLabel:
                    id: wind
                    text: ""
                    halign: "center"

            MDRaisedButton:
                id: fav_btn
                text: "♡ Favorilere Ekle"
                pos_hint: {"center_x": 0.5}
                on_release: app.toggle_favorite()

        Footer:


<SearchScreen>:
    name: "search"

    MDBoxLayout:
        orientation: "vertical"

        MDBoxLayout:
            orientation: "vertical"
            padding: 20
            spacing: 20

            MDLabel:
                text: "Şehir Arama"
                halign: "center"
                font_style: "H4"

            MDTextField:
                id: city_input
                hint_text: "Şehir gir"

            MDRaisedButton:
                text: "Ara"
                pos_hint: {"center_x": 0.5}
                on_release: app.search_city(city_input.text)

        Footer:


<FavoritesScreen>:
    name: "favorites"

    MDBoxLayout:
        orientation: "vertical"

        MDBoxLayout:
            orientation: "vertical"
            padding: 20
            spacing: 15

            MDLabel:
                text: "Favori Şehirler"
                halign: "center"
                font_style: "H4"

            MDBoxLayout:
                id: favorites_list
                orientation: "vertical"
                spacing: 10

        Footer:


<ForecastScreen>:
    name: "forecast"

    MDBoxLayout:
        orientation: "vertical"

        MDBoxLayout:
            orientation: "vertical"
            padding: 20
            spacing: 15

            MDLabel:
                id: forecast_title
                text: "5 Günlük Tahmin"
                halign: "center"
                font_style: "H4"

            MDBoxLayout:
                id: forecast_list
                orientation: "vertical"
                spacing: 10

        Footer:


<SettingsScreen>:
    name: "settings"

    MDBoxLayout:
        orientation: "vertical"

        MDBoxLayout:
            orientation: "vertical"
            padding: 20
            spacing: 15

            MDLabel:
                text: "Ayarlar"
                halign: "center"
                font_style: "H4"

            MDRaisedButton:
                text: "Tema Değiştir"
                pos_hint: {"center_x": 0.5}
                on_release: app.change_theme()

            MDRaisedButton:
                text: "Celsius / Fahrenheit"
                pos_hint: {"center_x": 0.5}
                on_release: app.change_unit()

        Footer:
'''


class SkyMateApp(MDApp):
    active_screen = StringProperty("home")

    def build(self):
        self.service = WeatherService(API_KEY)
        self.favorites_manager = FavoritesManager()
        self.settings_manager = SettingsManager()

        self.root = Builder.load_string(KV)
        self.load_weather("Yalova")

        return self.root

    def load_weather(self, city):
        weather = self.service.get_weather(city)
        home = self.root.get_screen("home")

        if weather:
            home.ids.city.text = weather.get_city()
            home.ids.temp.text = weather.get_temp()
            home.ids.desc.text = weather.get_desc()
            home.ids.humidity.text = weather.get_humidity()
            home.ids.wind.text = weather.get_wind()
            self.update_favorite_button()

    def is_favorite(self, city):
        return city in self.favorites_manager.get_favorites()

    def update_favorite_button(self):
        home = self.root.get_screen("home")
        city = home.ids.city.text

        if self.is_favorite(city):
            home.ids.fav_btn.text = "♥ Favorilerden Kaldır"
        else:
            home.ids.fav_btn.text = "♡ Favorilere Ekle"

    def toggle_favorite(self):
        home = self.root.get_screen("home")
        city = home.ids.city.text

        if city == "" or city == "Yükleniyor...":
            return

        if self.is_favorite(city):
            self.favorites_manager.remove_favorite(city)
            print(f"{city} favorilerden kaldırıldı")
        else:
            self.favorites_manager.add_favorite(city)
            print(f"{city} favorilere eklendi")

        self.update_favorite_button()

    def search_city(self, city):
        if city.strip() == "":
            return

        self.load_weather(city)
        self.root.current = "home"
        self.active_screen = "home"

    def open_favorites(self):
        screen = self.root.get_screen("favorites")
        box = screen.ids.favorites_list
        box.clear_widgets()

        favorites = self.favorites_manager.get_favorites()

        if not favorites:
            box.add_widget(
                MDRaisedButton(
                    text="Favori yok",
                    disabled=True,
                    pos_hint={"center_x": 0.5}
                )
            )
        else:
            for city in favorites:
                btn = MDRaisedButton(
                    text=city,
                    pos_hint={"center_x": 0.5}
                )
                btn.bind(on_release=lambda x, c=city: self.open_city(c))
                box.add_widget(btn)

        self.root.current = "favorites"
        self.active_screen = "favorites"

    def open_city(self, city):
        self.load_weather(city)
        self.root.current = "home"
        self.active_screen = "home"

    def open_forecast(self):
        self.root.current = "forecast"
        self.active_screen = "forecast"

    def change_theme(self):
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"

    def change_unit(self):
        pass


SkyMateApp().run()