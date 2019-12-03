from channels.generic.websocket import WebsocketConsumer
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
from .models import Choice


class PollsConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)("polls",
            self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("polls",
            self.channel_name)

    def receive(self, text_data):
        "Handle incoming websocket data"

        # I hate the dreadful hollow behind the little wood,
        # Its lips in the field above are dabbled with blood-red heath,
        # The red-ribb'd ledges drip with a silent horror of blood,
        # And Echo there, whatever is ask'd her, answers "Death."
        if text_data == "echo":
            self.send(text_data="death")

    def votes_changed(self, event):
        print("VOTES CHANGED", event)
        # Some vote totals have changed
        # Work out whether they are for the question for this channel
        # or for some other question
        url_route = self.scope.get("url_route")
        if not url_route: return
        url_args = url_route.get("kwargs")
        if not url_args: return
        our_question_id = url_args.get("question_id")
        if our_question_id is None: return

        # check our question ID against the one passed in by the event
        if str(our_question_id) != str(event["question_id"]): return

        # this is an event for our question! send a message
        self.send(text_data=json.dumps({
            "type": "votes",
            "vote_totals": event.get("vote_totals", [])
        }))

    @staticmethod
    @receiver(post_save, sender=Choice)
    def onChoiceChange(*args, **kwargs):
        print("A choice changed: send update notification", args, kwargs)
        channel_layer = get_channel_layer()
        question = kwargs["instance"].question
        vote_totals = [(c.id, c.votes) for c in question.choice_set.all()]
        async_to_sync(channel_layer.group_send)("polls", {
            "type": "votes.changed",
            "question_id": question.id,
            "vote_totals": vote_totals
        })
