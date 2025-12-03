from django.contrib import admin
from .models import SeekerModelOne,SeekerModelTwo,SeekerModelThree, User

admin.site.register(SeekerModelOne)
# admin.site.register(EmployerModelOne)
admin.site.register(SeekerModelTwo)
admin.site.register(SeekerModelThree)
# admin.site.register(EmployerModelTwo)
# admin.site.register(EmployerModelThree)
# admin.site.register(User)