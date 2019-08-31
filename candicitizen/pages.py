from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Postular(Page):
    form_model = 'group'
    form_fields = ['postular']

    def is_displayed(self):
        return self.player.id_in_group == 2 and not self.group.use_strategy_method

    timeout_seconds = 600


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    MyPage,
    ResultsWaitPage,
    Results
]
