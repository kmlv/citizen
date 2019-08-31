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
    num_rounds = 1
    endowment = c(100)

    players_per_group = 5

    # instructions_template = 'public_goods/instructions.html'

    # """Amount allocated to each player"""
    B = 10
    C = 10
    D = 10


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.private_value = random.randint(0, Constants.endowment)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    postular = models.BooleanField(
        doc="""Postular""",
    )
