from django.contrib import admin
from infi.clickhouse_orm.query import Q

from .apps import AppcraftLoggingConfig as LogsConfig
from .clickhouse.changelist import ClickHouseChangeList
from .clickhouse.models import LogModel
from .models import LogProxyModel


@admin.register(LogProxyModel)
class LogAdmin(admin.ModelAdmin):
    search_fields = ['method', 'url']

    def get_queryset(self, request):
        return LogModel.objects_in(LogsConfig.db).order_by('-start_at')

    def get_changelist(self, request, **kwargs):
        return ClickHouseChangeList

    def get_object(self, request, object_id, from_field=None):
        clickhouse_instance = LogModel.objects_in(LogsConfig.db).filter(uuid=object_id)[0]
        return LogProxyModel.from_clickhouse_model(clickhouse_instance)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_search_results(self, request, queryset, search_term):
        if not search_term:
            return queryset

        chained_lookups = Q()
        for field in self.search_fields:
            condition = {f'{field}__istartswith': search_term}
            chained_lookups |= Q(**condition)
        return queryset.filter(chained_lookups)
