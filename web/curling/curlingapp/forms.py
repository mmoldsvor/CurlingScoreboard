from django.forms import ModelForm
from curlingapp.models import Round, Scoreboard, Match

class MatchForm(ModelForm):
    class Meta:
        fiels = ['matchName','camId','redTeam','yellowTeam']


class ContactForm(forms.Form):
    yourname = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(required=False, label='Your Email Address')
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)