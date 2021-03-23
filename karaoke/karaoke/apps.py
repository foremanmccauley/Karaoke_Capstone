from django.apps import AppConfig

class KaraokeConfig(AppConfig):
    name = 'karaoke'

    def ready(self):
        import karaoke.signals