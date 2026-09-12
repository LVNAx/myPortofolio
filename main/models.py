import uuid
from django.db import models
from django.utils import timezone

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
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
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