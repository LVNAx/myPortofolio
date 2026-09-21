import uuid
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Person(models.Model):
    display_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=17)

    def __str__(self):
        return self.display_name

class Post(models.Model):
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
    content = models.CharField(max_length=125)
    published_date = models.DateTimeField(default=timezone.now)

class Mahasiswa(models.Model):
    display_name = models.CharField(max_length=30)
    npm = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=17)

    def __str__(self):
        return f"{self.npm} {self.display_name}"

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

import uuid
from django.db import models


class Project(models.Model):
    CATEGORY_CHOICES = [
        ("web", "Web Development"),
        ("data", "Data Science"),
        ("competition", "Competition"),
        ("course", "Course Project"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # Samakan aja pakai ID kayak Experience
    title = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="web")
    description = models.TextField()
    highlights = models.TextField(blank=True, help_text="Satu project dalam satu baris")
    tech_stack = models.CharField(max_length=200, help_text="Pisahkan dengan koma")
    thumbnail = models.CharField(max_length=200, blank=True)
    live_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    started_at = models.DateField()
    ended_at = models.DateField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-started_at"]

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None

    @property
    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]

    @property
    def highlight_list(self):
        return [line.strip() for line in self.highlights.splitlines() if line.strip()]

def validate_word_count(value):
    total = len(value.split())
    if total < 50:
        raise ValidationError(f"Deskripsi minimal 50 kata, saat ini baru {total} kata.")
    if total > 150:
        raise ValidationError(f"Deskripsi maksimal 150 kata, saat ini sudah {total} kata.")


class JourneyStage(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    school = models.CharField(max_length=150)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(null=True, blank=True)
    photo = models.CharField(max_length=200, blank=True)
    logo = models.CharField(max_length=200, blank=True)
    tags = models.CharField(max_length=120, blank=True)
    description = models.TextField(validators=[validate_word_count])
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "start_year"]

    def __str__(self):
        return f"{self.name} ({self.school})"

    @property
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]

    @property
    def period(self):
        if self.end_year:
            return f"{self.start_year} sampai {self.end_year}"
        return f"{self.start_year} until now"


class StageActivity(models.Model):

    class Category(models.TextChoices):
        OLIMPIADE = "olimpiade", "Olimpiade"
        ORGANISASI = "organisasi", "Organisasi"
        LAINNYA = "lainnya", "Lainnya"

    # Ini adalah yang akan menjadi konektor antara Activity dan juga Education kita
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stage = models.ForeignKey(
        JourneyStage,
        on_delete=models.CASCADE,
        related_name="activities",
    )

    title = models.CharField(max_length=150)
    role = models.CharField(max_length=120, blank=True)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.LAINNYA,
    )
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    @property
    def point_list(self):
        return [line.strip() for line in self.description.splitlines() if line.strip()]

    class Meta:
        ordering = ["order", "title"]
        verbose_name_plural = "Stage activities"

    def __str__(self):
        return f"{self.title} ({self.stage.name})"