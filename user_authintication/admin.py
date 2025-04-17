from django.contrib import admin


from .models import laptop
# Register your models here.
@admin.register(laptop)
class laptopAdmin(admin.ModelAdmin):
    list_display=('password','re_pass','laptop','re_laptop','email','textarea','checkbox','ram')