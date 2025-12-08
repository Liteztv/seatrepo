from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.forms import ModelForm
from .models import ( SeekerModelOne, SeekerModelTwo, SeekerModelThree, Profile, Job, JobRequirementOne, JobRequirementTwo, JobRequirementThree, SeekerResume
                     
                      )



class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ["username", "email", "password"]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class SeekerFormOne(ModelForm):
    class Meta:
        model = SeekerModelOne
        exclude = ('user',)
        fields = '__all__'
        # fields = ['first_name','last_name','total_years_of_experience',
        #           'html_experience','css_experience']
class SeekerFormTwo(ModelForm):
    class Meta:
        model = SeekerModelTwo
        exclude = ('user',)
        fields = '__all__'
        # fields = ['python_experience','java_experience', 'javascript_experience',
        #           'cplusplus_experience','csharp_experience','ruby_experience']
        

class SeekerFormThree(ModelForm):

    class Meta:
        model = SeekerModelThree
        exclude = ('user',)
        fields = '__all__'
        # fields = ['react_experience','vue_experience','angular_experience',
        #           'django_experience','flask_experience','ruby_on_rails_experience',
        #           'fastapi_experience','laravel_experience','express_experience',
        #           'springboot_experience','springboot_experience','aspnet_experience',
        #           'oracle_experience','mysql_experience','sqlite_experience',
        #           'mongodb_experience','postgresql_experience'
        #           ]

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "location", "description", "interview_questions"]
        widgets = {
            "interview_questions": forms.Textarea(attrs={"rows": 5}),
        }




class JobRequirementOneForm(forms.ModelForm):
    class Meta:
        model = JobRequirementOne
        exclude = ("job",)


class JobRequirementTwoForm(forms.ModelForm):
    class Meta:
        model = JobRequirementTwo
        exclude = ("job",)


class JobRequirementThreeForm(forms.ModelForm):
    class Meta:
        model = JobRequirementThree
        exclude = ("job",)

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = SeekerResume
        fields = ["resume"]

    def clean_resume(self):
        resume = self.cleaned_data.get("resume")

        if not resume:
            return resume

        if not resume.name.lower().endswith(".pdf"):
            raise ValidationError("Only PDF files are allowed for resumes.")

        if resume.content_type != "application/pdf":
            raise ValidationError("Uploaded file must be a valid PDF.")

        return resume


# class ResumeUploadForm(forms.ModelForm):
#     class Meta:
#         model = SeekerResume
#         fields = ["resume"]
#         resume = forms.FileField(
#         label="Upload Resume (PDF recommended)",
#         help_text="PDF files open directly in the browser."
#     )










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