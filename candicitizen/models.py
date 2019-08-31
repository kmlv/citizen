from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range,
)
import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'candicitizen'
    num_rounds = 5 # multiples of 5
    players_per_group = 5
    preferences = [15, 30, 50, 70, 95]
    # The following will be moved to a separate config file
    B = 10 # prize for being elected
    C = 10 # cost for running in the first round
    D = 10 # cost for running in the second round
    endowment = c(100) # initial endowment for each player
    second_round = True # whether there will be a second round of voting or not

class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.group_randomly()
        else:
            self.group_like_round(1)
        for p in self.get_players():
            p.candidate_number = Constants.preferences[(self.round_number + \
                p.id_in_group - 2) % 5] # your candidate number
            # distance to each other for this given round
            p.participant.vars['distances'] = {d:
                abs(p.candidate_number - d) for d in Constants.preferences}


class Group(BaseGroup):
    won_first = models.StringField()
    second_round = models.BooleanField()
    won_second = models.StringField()
    ran = models.StringField()

class Player(BasePlayer):
    candidate_number = models.IntegerField() # Your number
    ran = models.BooleanField(choices=[
        [True, 'Yes'],
        [False, 'No'],
    ]) # whether or not you entered the race
    preference = models.IntegerField() # The number your vote was cast for
    preference2 = models.IntegerField() # In case of a tie, the second number
    # set payoffs

