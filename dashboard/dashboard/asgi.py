# mysite/asgi.py
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","dashboard.settings")
import django
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import carts.routing

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            carts.routing.websocket_urlpatterns
        )
    ),
})

