from django.contrib import admin
from .models import Person, Post, Mahasiswa, Experience

admin.site.register(Person)
admin.site.register(Post)

@admin.register(Mahasiswa)
class MahasiswaAdmin(admin.ModelAdmin):
    list_display = ("display_name", "npm")

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "started_at", "ended_at")
    list_filter = ("category",)