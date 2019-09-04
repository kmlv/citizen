from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):

    def play_round(self):
        ran = True if random.random() < 0.5 else False
        if self.subsession.round_number == 1:
            yield (pages.Introduction)
        yield (pages.Voting, {
            'ran': ran,
        })
        yield (pages.Results)
        if self.subsession.round_number == Constants.num_rounds:
            yield (pages.FinalResults)

