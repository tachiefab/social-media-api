from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
	list_display = ["user", "content_type", "content_object", "parent", "content", "timestamp"]
	search_fields = ["user", "content"]
	list_filter = ["user", "content"]

	class Meta:
		model = Comment

admin.site.register(Comment, CommentAdmin)
