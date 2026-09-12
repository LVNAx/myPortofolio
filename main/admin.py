from django.contrib import admin
from .models import Person, Post, Mahasiswa, Experience, Project

admin.site.register(Person)
admin.site.register(Post)

@admin.register(Mahasiswa)
class MahasiswaAdmin(admin.ModelAdmin):
    list_display = ("display_name", "npm")

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "started_at", "ended_at")
    list_filter = ("category",)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "role", "category", "started_at", "is_ongoing", "order")
    list_filter = ("category",)
    search_fields = ("title", "tech_stack")
    list_editable = ("order",)