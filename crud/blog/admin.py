from django.contrib import admin
from .models import *
class PostInline(admin.TabularInline):
    model = ImagePost
class AdminPost(admin.ModelAdmin):
    prepopulated_fields = {"slug":('title',)}
    inlines = [PostInline]
class AdminCat(admin.ModelAdmin):
    prepopulated_fields = {"slug":('title',)}
class AdminTag(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}

admin.site.register(User)
admin.site.register(Dislike)
admin.site.register(Like)
admin.site.register(Post,AdminPost)
admin.site.register(Category,AdminCat)
admin.site.register(Tag,AdminTag)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Image)