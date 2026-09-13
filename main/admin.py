from django.contrib import admin
from .models import (
    Person,
    Post,
    Mahasiswa,
    Experience,
    Project,
    JourneyStage,
    StageActivity,
)

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


class StageActivityInline(admin.TabularInline):
    """Biar StageActivity bisa langsung diisi dari halaman JourneyStage."""
    model = StageActivity
    extra = 1
    fields = ("title", "role", "category", "description", "order")


@admin.register(JourneyStage)
class JourneyStageAdmin(admin.ModelAdmin):
    list_display = ("name", "school", "period", "order")
    list_editable = ("order",)
    search_fields = ("name", "school", "tags")
    ordering = ("order", "start_year")
    inlines = [StageActivityInline]


@admin.register(StageActivity)
class StageActivityAdmin(admin.ModelAdmin):
    """Tetap didaftarkan terpisah kalau suatu saat perlu dikelola sendiri di luar inline."""
    list_display = ("title", "stage", "category", "order")
    list_filter = ("category", "stage")
    search_fields = ("title", "role")