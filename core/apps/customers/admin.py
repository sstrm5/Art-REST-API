from django.contrib import admin

from core.apps.customers.customer_session_model import CustomerSession
from core.apps.customers.models import Customer
from django.contrib.auth.models import Group, User
# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name',
                    'last_name', 'in_process', 'role')


@admin.register(CustomerSession)
class CustomerSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'access_token',
                    'device_info', 'updated_at', 'created_at')


admin.site.unregister(User)
admin.site.unregister(Group)
