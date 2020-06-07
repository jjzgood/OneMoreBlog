from django.contrib import admin
from .models import Post,Tag
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author','created_time', 'modified_time']
    fields = ['title', 'excerpt','body','tags']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Post,PostAdmin)
admin.site.register(Tag)