from django.forms import DateInput, ModelForm, Textarea, TextInput, URLInput
from main.models import Project, Experience
from django import forms


class ProjectForm(ModelForm):
    secret = forms.CharField(
        label="Kode Rahasia",
        required=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    class Meta:
        model = Project
        fields = [
            "title",
            "role",
            "category",
            "description",
            "highlights",
            "tech_stack",
            "live_url",
            "github_url",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Nama Proyek",
            "role": "Peran",
            "category": "Kategori",
            "description": "Deskripsi Proyek",
            "highlights": "Poin Penting",
            "tech_stack": "Teknologi yang Digunakan",
            "live_url": "URL Situs",
            "github_url": "URL GitHub",
            "started_at": "Tanggal Mulai",
            "ended_at": "Tanggal Selesai",
        }

        widgets = {
            "title": TextInput(attrs={"placeholder": "Portfolio Website"}),
            "role": TextInput(attrs={"placeholder": "Fullstack Developer"}),
            "description": Textarea(attrs={"placeholder": "Ceritakan proyekmu", "rows": 3}),
            "highlights": Textarea(attrs={"placeholder": "Satu poin per baris", "rows": 3}),
            "tech_stack": TextInput(attrs={"placeholder": "Django, Python, HTML, CSS"}),
            "live_url": URLInput(attrs={"placeholder": "https://lvnasandbox.vercel.app"}),
            "github_url": URLInput(attrs={"placeholder": "https://github.com/LVNAx/myPortofolio"}),
            "started_at": DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "ended_at": DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }

class ExperienceForm(ModelForm):
    secret = forms.CharField(
        label="Kode Rahasia",
        required=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current_password"}),
    )

    class Meta:
        model = Experience
        fields = ["title", "category", "description", "started_at", "ended_at"]

        labels = {
            "title": "Judul Pengalaman",
            "category": "Kategori",
            "description": "Deskripsi",
            "started_at": "Tanggal Mulai",
            "ended_at": "Tanggal Selesai",
        }

        widgets = {
            "title": TextInput(attrs={"placeholder": "Teaching Assistant"}),
            "description": Textarea(attrs={"placeholder": "Ceritakan apa yang sudah kamu lakukan", "rows": 3}),
            "started_at": DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "ended_at": DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }

        