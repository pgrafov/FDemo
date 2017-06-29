from django.forms import ModelForm

from main.models import Url


class UrlForm(ModelForm):

    class Meta:
        model = Url
        fields = ['link']
