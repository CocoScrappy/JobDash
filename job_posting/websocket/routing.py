from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/search/userId/(?P<user_id>\d+)/$",consumers.ScraperConsumer.as_asgi())
]