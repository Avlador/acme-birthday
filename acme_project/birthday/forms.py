from django import forms
from birthday.models import Birthday, Congratulation
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
BEATLES = {'L;jy Ktyyjy', 'Пол полкович', ' Ринго Гринго'}


class BirthdayForm(forms.ModelForm):
    class Meta:
        model = Birthday
        # exclude = ('author')
        fields = ('first_name', 'last_name', 'birthday')
        widgets = {'birthday': forms.DateInput(attrs={'type': 'date'})}

    def clean(self):
        super().clean()
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if f'{first_name} {last_name}' in BEATLES:
            send_mail(
                subject='Another Beatles member',
                message=f'{first_name} {last_name} пытался опубликовать запись!',
                from_email='birstday_form@acme_not',
                recipient_list=['admin@acme.not'],
                fail_silently=True
            )
            raise ValidationError(
                'Мы тоже любим Битлз, йоооооооу введи норм имя плиз'
            )

class CongratulationForm(forms.ModelForm):
    class Meta:
        model = Congratulation
        fields = ('text',)