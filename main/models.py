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