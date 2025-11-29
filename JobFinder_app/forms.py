from django import forms
from django.utils.safestring import mark_safe
from django.forms import ModelForm
from .models import SeekerModelOne, EmployerModelOne, SeekerModelTwo, SeekerModelThree, EmployerModelTwo, EmployerModelThree




class SeekerFormOne(ModelForm):
    class Meta:
        model = SeekerModelOne
        fields = ['first_name','last_name','total_years_of_experience',
                  'html_experience','css_experience']
class SeekerFormTwo(ModelForm):
    class Meta:
        model = SeekerModelTwo
        fields = ['python_experience','java_experience', 'javascript_experience',
                  'cplusplus_experience','csharp_experience','ruby_experience']
        

class SeekerFormThree(ModelForm):

    class Meta:
        model = SeekerModelThree
        fields = ['react_experience','vue_experience','angular_experience',
                  'django_experience','flask_experience','ruby_on_rails_experience',
                  'fastapi_experience','laravel_experience','express_experience',
                  'springboot_experience','springboot_experience','aspnet_experience',
                  'oracle_experience','mysql_experience','sqlite_experience',
                  'mongodb_experience','postgresql_experience'
                  ]







class EmployerFormTwo(ModelForm):

    class Meta:
        model = EmployerModelOne
        fields = ['total_years_of_experience',
                  'html_experience','css_experience'
                  ]
        
class EmployerFormTwo(ModelForm):
    class Meta:
        model = EmployerModelTwo
        fields = ['python_experience','java_experience', 'javascript_experience',
                  'cplusplus_experience','csharp_experience','ruby_experience']
        
class EmployerFormThree(ModelForm):
    class Meta:
        model = EmployerModelThree
        fields = ['react_experience','vue_experience','angular_experience',
                  'django_experience','flask_experience','ruby_on_rails_experience',
                  'fastapi_experience','laravel_experience','express_experience',
                  'springboot_experience','springboot_experience','aspnet_experience',
                  'oracle_experience','mysql_experience','sqlite_experience',
                  'mongodb_experience','postgresql_experience'
                  ]


    
    








##class SeekerForm(forms.Form):

    #Years_Experience = (
        #('0', '0'),
        #('1-3', '1-3'),
        #('3-5', '3-5'),
        #('5+', '5+'),
        #('10+', '10+'),
    ##)

    # name = forms.CharField(label='Your Name', max_length=100)
    # email = forms.EmailField(label=mark_safe('<br /><br />Your Email'))
    # python = forms.ChoiceField(choices=Years_Experience, label=mark_safe('Programming Languages<br /><br /> Python'))
    # java = forms.ChoiceField(choices=Years_Experience, label='Java')
    # javascript = forms.ChoiceField(choices=Years_Experience, label='JavaScript')
    # cplusplus = forms.ChoiceField(choices=Years_Experience, label='C/C++')
    # csharp = forms.ChoiceField(choices=Years_Experience, label='C#')
    # go = forms.ChoiceField(choices=Years_Experience, label='Golang')
    # ruby = forms.ChoiceField(choices=Years_Experience, label='Ruby')
    # react = forms.ChoiceField(choices=Years_Experience, label=mark_safe('<br /><br />Front End Frameworks<br /><br />React'))
    # vue = forms.ChoiceField(choices=Years_Experience, label='Vue.JS')
    # angular = forms.ChoiceField(choices=Years_Experience, label='Angular')
    # django = forms.ChoiceField(choices=Years_Experience, label=mark_safe('<br /><br />Back End Frameworks<br /><br />Django'))
    # flask = forms.ChoiceField(choices=Years_Experience, label='Flask')
    # rubyonrails = forms.ChoiceField(choices=Years_Experience, label='Ruby on Rails')
    # fastapi = forms.ChoiceField(choices=Years_Experience, label='FastAPI')
    # laravel = forms.ChoiceField(choices=Years_Experience, label='Laravel')
    # express = forms.ChoiceField(choices=Years_Experience, label='Express.JS')
    # spring = forms.ChoiceField(choices=Years_Experience, label='Spring Boot')
    # aspnet = forms.ChoiceField(choices=Years_Experience, label='ASP.NET')
    # mongodb = forms.ChoiceField(choices=Years_Experience, label=mark_safe('<br /><br />Databases<br /><br />MongoDB'))
    # mysql = forms.ChoiceField(choices=Years_Experience, label='MySQL')
    # sqlite = forms.ChoiceField(choices=Years_Experience, label='SQLite')
    # postgresql = forms.ChoiceField(choices=Years_Experience, label='PostgreSQL')
    # Oracle = forms.ChoiceField(choices=Years_Experience, label='Oracle')
    

# class NameForm(ModelForm):
#     class Meta:
#         model = NameModel
#         fields = ['first_name','last_name']