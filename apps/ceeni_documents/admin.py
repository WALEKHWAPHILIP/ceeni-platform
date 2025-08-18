from django.contrib import admin
from .models import (
    Document, 
    Section, 
    Embedding  
    ) # Import models exposed by models/__init__.py

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    # Columns to show in the admin list view for Document
    list_display = ("title", "doc_type", "published_at", "updated_at")
    # Fields searchable via the admin search box
    search_fields = ("title", "slug")
    # Filters available on the right sidebar in admin for quick filtering
    list_filter = ("doc_type",)
    
    # Automatically populate the slug field from the title field in admin forms
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("document", "index", "heading")
    search_fields = ("heading", "text")

@admin.register(Embedding)
class EmbeddingAdmin(admin.ModelAdmin):
    list_display = ("section", "model", "dim", "created_at")
