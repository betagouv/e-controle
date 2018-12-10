from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


User = get_user_model()


class EmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        user_email = self.cleaned_data['email']
        if not User.objects.filter(email=user_email).exists():
            raise forms.ValidationError(_(f"Aucun utilisateur trouvé"))
        return user_email

    def send_email(self):
        print('envoie ok')
        pass
