from django.contrib import admin
from .models import Role, UserProfile  # ✅ import your models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



# Register your models here.

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']

admin.site.unregister(User)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    def get_role(self, obj):
        return obj.userprofile.role.name if hasattr(obj, 'userprofile') and obj.userprofile.role else '—'
    get_role.short_description = 'Role'

    inlines = (UserProfileInline,)  # ✅ show role inside user form
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'get_role')

# Register custom user admin
admin.site.register(User, UserAdmin)



