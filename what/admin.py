from django.contrib import admin

# Register your models here.
from what.models import *

admin.site.register(Period)
admin.site.register(Country)

admin.site.register(Composer)

admin.site.register(Work)
admin.site.register(WorkVersion)
admin.site.register(WorkVersionEnsemble)


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "key",
        "parent_id",
        "sequence",
        "is_ensemble",
    )