from django.contrib import admin
from posts.models import Post, Tag, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "rate", "author", "created_at", "updated_at", "category", "get_tags")
    search_fields = ("title", "content")
    list_editable = ("rate", "author")

    def get_tags(self, obj):
        return ", ".join([t.name for t in obj.tags.all()])
    get_tags.short_description = "Теги"

admin.site.register(Tag)
admin.site.register(Category)
