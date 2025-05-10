from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests
import logging
from common.forms import GuestForm  # Убедись, что форма импортирована


from django.views.generic import TemplateView, RedirectView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

class UnlockView(TemplateView):
    template_name = "unlock.html"

@method_decorator(never_cache, name='dispatch')
class MobileRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        user_agent = self.request.META.get('HTTP_USER_AGENT', '').lower()
        if "mobile" in user_agent or "android" in user_agent or "iphone" in user_agent:
            return "/unlock/"
        return "/main/"

logger = logging.getLogger(__name__)

# Замените на свои данные
TELEGRAM_BOT_TOKEN = "7738261243:AAGftaKXWSglJ1hkfKYx5GPYLjGZhf7ngfQ"
TELEGRAM_CHAT_ID = "-4782301339"

def send_to_telegram(name, attending, transfer, drinks, message):
    """Формирует и отправляет сообщение в Telegram."""
    text = f"📝 Новая анкета:\n\n👤 Имя: {name}\n✅ Присутствие: {attending} \n"
    if attending == "Да":
        text += f"🚗 Нужен трансфер: {transfer}\n 🥂 Напитки: {', '.join(drinks) if drinks else '—'}\n"
    text += f"💬 Сообщение: {message}"

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    response = requests.post(telegram_url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})

    return response.status_code == 200

@method_decorator(csrf_exempt, name="dispatch")  # Отключаем CSRF для формы
class Invitation(View):
    form_class = GuestForm
    template_name = "main.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'request': request})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get("name")
            attending = form.cleaned_data.get("attending")
            # home = form.cleaned_data.get("home")
            transfer = form.cleaned_data.get("transfer") if attending == "Да" else None
            drinks = form.cleaned_data.get("drinks") if attending == "Да" else []
            message = form.cleaned_data.get("message", "—")

            logger.debug(f"Отправка анкеты: {name}, присутствие: {attending}, трансфер: {transfer}, напитки: {drinks}, сообщение: {message}")

            # Отправляем в Telegram
            if send_to_telegram(name, attending, transfer, drinks, message):
                return JsonResponse({"status": "success", "message": "Анкета успешно отправлена!"})
            else:
                return JsonResponse({"status": "error", "message": "Ошибка заполнения анкеты."})

        logger.error(f"Ошибка валидации формы: {form.errors}")
        return JsonResponse({"status": "error", "message": "Некорректные данные."})
