from django import forms

class GuestForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    attending = forms.ChoiceField(choices=[('Да', 'Да, я буду/ мы будем'), ('Нет', 'Нет, прийти не получится')], required=True)
    transfer = forms.ChoiceField(choices=[('Да', 'Да'), ('Нет', 'Нет')], required=False)
    # home = forms.ChoiceField(choices=[('Да', 'Да'), ('Нет', 'Нет')], required=False)
    drinks = forms.MultipleChoiceField(choices=[('Водка', 'Водка'), 
                                                ('Виски', 'Виски'), 
                                                ('Белое вино', 'Белое вино'), 
                                                ('Красное вино', 'Красное вино'), 
                                                ('Шампанское', 'Шампанское'),
                                                ('Я не пью', 'Я не пью')], 
                                       required=False)
    message = forms.CharField(widget=forms.Textarea, required=False)