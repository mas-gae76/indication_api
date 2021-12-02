from django.contrib import admin
from .models import Counter, History
from .forms import CounterAdminForm


class CounterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'value', )
    search_fields = ('name', 'user__username', )
    list_display_links = ('name', )
    form = CounterAdminForm


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'type', 'value', 'consumption', 'counter')
    search_fields = ('date', 'counter__name', 'type', )
    list_display_links = ('date', 'counter', )
    exclude = ('type', )

    def save_model(self, request, obj, form, change):
        # флаг создания / изменения записи оператором
        if request.user.is_staff:
            obj.type = True
        return super(HistoryAdmin, self).save_model(request, obj, form, change)


admin.site.register(Counter, CounterAdmin)
admin.site.site_header = 'Админка'
