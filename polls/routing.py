from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/polls/(?P<question_id>[0-9]+)$',
        consumers.PollsConsumer),
]
