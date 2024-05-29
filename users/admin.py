from django.contrib import admin
from users.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'last_name', 'email', 'created')
    search_fields = ('user__username', 'name', 'last_name', 'email')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('user')
        return queryset