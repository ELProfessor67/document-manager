from django.contrib import admin
from .models import Document,DocumentFile
from django.urls import reverse
from django.utils.html import format_html

# Define the admin class for the Document model
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document_name', 'about_description', 'is_default')  # Display these fields in the admin list view
    list_filter = ['is_default']  # Add filters for these fields in the admin list view
    search_fields = ['document_name']  # Add search functionality for these fields in the admin list view

# Register the Document model with the DocumentAdmin class
admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentFile)





