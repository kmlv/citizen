from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range,
)
import random

author = 'Eli Pandolfo'

doc = """

"""


class Constants(BaseConstants):
    name_in_url = 'citizen'
    num_rounds = 10 # multiples of 5
    players_per_group = 5
    preferences = [15, 30, 50, 70, 95]

class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.group_randomly()
            for p in self.get_players():
                p.participant.vars['paying_round'] = random.randint(1,
                    Constants.num_rounds)
        else:
            self.group_like_round(1)
        for p in self.get_players():
            p.candidate_number = Constants.preferences[(self.round_number + \
                p.id_in_group - 2) % 5] # your candidate number
            # distance to each other for this given round
            p.participant.vars['distances'] = {d:
                abs(p.candidate_number - d) for d in Constants.preferences}
        if self.round_number > 5:
            self.session.vars['second_round_toggle'] = True
        else:
            self.session.vars['second_round_toggle'] = False

class Group(BaseGroup):
    ran = models.StringField()
    nominees = models.StringField()
    second_round = models.BooleanField()
    winner = models.StringField()

class Player(BasePlayer):
    candidate_number = models.IntegerField() # Your number
    ran = models.BooleanField(choices=[
        [True, 'Yes'],
        [False, 'No'],
    ]) # whether or not you entered the race
    preference = models.IntegerField() # The number your vote was cast for
    preference2 = models.IntegerField() # In case of a tie, the second number
    round_payoff = models.CurrencyField()

    # this only gets called on the randomly chosen paying round
    def set_payoffs(self, round_payoff):
        self.payoff = round_payoff

