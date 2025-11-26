from django import forms
from django.utils.safestring import mark_safe
#from . models import ExperienceModel

class SeekerForm(forms.Form):

    Years_Experience = (
        ('0', '0'),
        ('1-3', '1-3'),
        ('3-5', '3-5'),
        ('5+', '5+'),
        ('10+', '10+'),
    )

    #name = forms.CharField(label='Your Name', max_length=100)
    #email = forms.EmailField(label=mark_safe('<br /><br />Your Email'))
    python = forms.ChoiceField(choices=Years_Experience, label=mark_safe('Programming Languages<br /><br /> Python'))
    java = forms.ChoiceField(choices=Years_Experience, label='Java')
    javascript = forms.ChoiceField(choices=Years_Experience, label='JavaScript')
    cplusplus = forms.ChoiceField(choices=Years_Experience, label='C/C++')
    csharp = forms.ChoiceField(choices=Years_Experience, label='C#')
    go = forms.ChoiceField(choices=Years_Experience, label='Golang')
    ruby = forms.ChoiceField(choices=Years_Experience, label='Ruby')
    react = forms.ChoiceField(choices=Years_Experience, label=mark_safe('<br /><br />Front End Frameworks<br /><br />React'))
    vue = forms.ChoiceField(choices=Years_Experience, label='Vue.JS')
    angular = forms.ChoiceField(choices=Years_Experience, label='Angular')
    django = forms.ChoiceField(choices=Years_Experience, label=mark_safe('<br /><br />Back End Frameworks<br /><br />Django'))
    flask = forms.ChoiceField(choices=Years_Experience, label='Flask')
    rubyonrails = forms.ChoiceField(choices=Years_Experience, label='Ruby on Rails')
    fastapi = forms.ChoiceField(choices=Years_Experience, label='FastAPI')
    laravel = forms.ChoiceField(choices=Years_Experience, label='Laravel')
    express = forms.ChoiceField(choices=Years_Experience, label='Express.JS')
    spring = forms.ChoiceField(choices=Years_Experience, label='Spring Boot')
    aspnet = forms.ChoiceField(choices=Years_Experience, label='ASP.NET')
    mongodb = forms.ChoiceField(choices=Years_Experience, label=mark_safe('<br /><br />Databases<br /><br />MongoDB'))
    mysql = forms.ChoiceField(choices=Years_Experience, label='MySQL')
    sqlite = forms.ChoiceField(choices=Years_Experience, label='SQLite')
    postgresql = forms.ChoiceField(choices=Years_Experience, label='PostgreSQL')
    Oracle = forms.ChoiceField(choices=Years_Experience, label='Oracle')
    

#class ExperienceForm(form.ModelForm):
    #class Meta:
        #model = ExperienceModel


    
    