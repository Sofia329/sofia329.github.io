import os
import  sys
import threading
from django.apps import AppConfig



# the below app.config for websocket thread is with help of generative AI

class TradingConfig(AppConfig):

    name = "trading"

    def ready(self):

        global _start

        if "runserver" not in sys.argv:
            return

        if os.environ.get("RUN_MAIN") != "true":
            return

        from . import live_stream
        threading.Thread(
            target=live_stream.run,
            daemon=True,
            name="yf-ws-stream",
        ).start()
