from django.db import models

from multiselectfield import MultiSelectField


class Presence(models.TextChoices):
    YES = "yes", "Я приду/мы придем"
    NO = "no", "Прийти не получится :("
    LATER = "later", "Скажу ответ чуть позже"


class DrinkPreferences(models.TextChoices):
    SHAMP = "shamp", "Шампанское"
    WHITE_WINE = "white_wine", "Белое вино"
    RED_WINE = "red_wine", "Красное вино"
    SAMOGON = "samogon", "Папин самогон"
    VODKA = "vodka", "Водка"
    KON = "kon", "Коньяк"
    NO = "no", "А я и не пью"


class Guest(models.Model):

    name = models.CharField('Имя и Фамилия', max_length=500)
    presence = models.CharField('Присутствие', max_length=5, choices=Presence.choices, default=Presence.LATER)
    drink_preferences = MultiSelectField('Предпочтения по напиткам', max_length=200, choices=DrinkPreferences.choices, blank=True, null=True)
    food_wishes = models.TextField('Предпочтения по еде', blank=True, null=True)

    def __str__(self):
        return self.name

