from django.contrib import admin
from .models import *


@admin.register(User)
class PersonalUser(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'type')}),
        ('Names', {'fields': ('ChineseName', 'EnglishName')}),
        ('Teacher', {'fields': ('subject',)}),
        ('Student', {'fields': ('Class',)})
    )


admin.site.register(Class)
admin.site.register(Assignment)
admin.site.register(PersonalAssignment)


@admin.register(Attachment)
class AttachmentFile(admin.ModelAdmin):
    fields = ('name', 'content', 'md5')
    readonly_fields = ('size', )
