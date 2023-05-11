from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import MyUser
from django.contrib.auth.models import Group

class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(is_superuser=False)
        else:
            return qs.none()

admin.site.register(MyUser, CustomUserAdmin)
admin.site.unregister(Group)
