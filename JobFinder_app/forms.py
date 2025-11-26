from django import forms
from django.utils.safestring import mark_safe

class SeekerForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label=mark_safe('<br /><br />Your Email'))
    pythonex = forms.BooleanField(label=mark_safe('<br /><br /> Python'))
    java = forms.BooleanField(label='Java')
    javascript = forms.BooleanField(label='JavaScript')
    cplusplus = forms.BooleanField(label='C/C++')
    csharp = forms.BooleanField(label='C#')
    go = forms.BooleanField(label='Go')
    ruby = forms.BooleanField(label='Ruby')
    react = forms.BooleanField(label=mark_safe('<br /><br />React'))
    vue = forms.BooleanField(label='Vue.js')
    angular = forms.BooleanField(label='Angular',required=False,initial=False)
    angularyears = forms.IntegerField(label='Years experience', required=False)


    
    