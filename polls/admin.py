from django.contrib import admin

from . import models


class ChoiceAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class PollAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(models.Poll, PollAdmin)
admin.site.register(models.Choice, ChoiceAdmin)
admin.site.register(models.Vote)

