from django import forms
from common.models import Guest


class GuestForm(forms.ModelForm):
    # drink_preferences = forms.MultipleChoiceField(choices=DrinkPreferences.choices, required=False)
    # name = forms.CharField()
    # presence = forms.ChoiceField(choices=Presence.choices)
    # #food_wishes = forms.CharField()
    #
    # def get_required_fields

    class Meta:
        model = Guest
        fields = "__all__"

    def get_required_fields(self) -> list:
        return [field for field, data in self.fields.items() if data.required is True]
