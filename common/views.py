from django.shortcuts import render
from django.views import View
from django.conf import settings
from common.forms import GuestForm

import requests

import logging


logger = logging.getLogger(__name__)


def send_to_telegram(message):

    url = f'https://api.telegram.org/bot{settings.TOKEN}/sendMessage'

    try:
        response = requests.post(url, json={'chat_id': settings.CHAT_ID, 'text': message})
        logger.info(response.text)
    except Exception as e:
        msg_error = f"{e}\n{message}"
        logger.error(msg_error)


class Invitation(View):
    form_class = GuestForm
    template_name = "main.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        logger.debug(f"Данные формы: {form.data}")
        if form.is_valid():
            guest = form.save()
            msg = f"Заполнил анкету {guest.name}\n" \
                  f"Присутствие: {guest.get_presence_display()}\n" \
                  f"Напитки: {guest.get_drink_preferences_display()}\n" \
                  f"Комментарии: {guest.food_wishes}"
            logger.debug(msg)
            send_to_telegram(msg)
            return render(request, self.template_name)

        msg_error = f"{form.errors}\n{form.data}"
        logger.error(msg_error)

        return render(request, self.template_name)
