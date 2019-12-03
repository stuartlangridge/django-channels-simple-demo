# A simple demonstration of how to add Channels to the Django tutorial "polls" project.

The first commit is the ["polls" project from the Django tutorial](https://docs.djangoproject.com/en/2.2/intro/tutorial01/), up to [phase 4](https://docs.djangoproject.com/en/2.2/intro/tutorial04/).

The second commit then adds [Django Channels](https://channels.readthedocs.io/en/latest/) support to automatically push changes in the number of votes on a Question to the results page for that Question, via a Django Channel websocket, thus giving the results page live updates on changing votes.
