from django.forms import DateInput, ModelForm, Textarea, TextInput, URLInput
from main.models import Project, Experience, Certification
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

class CertificationForm(ModelForm):
    class Meta:
        model = Certification
        fields = [
            "title",
            "issuer",
            "category",
            "issued_at",
            "credential_url",
        ]

        labels = {
            "title": "Nama Sertifikasi",
            "issuer": "Nama penerbit",
            "category": "Kategori",
            "issued_at": "Tanggal Terbit",
            "credential_url": "Bukti Sertifikasi",
        }

        widgets = {
            "title": TextInput(attrs={"placeholder": "Meta Backend Developer"}),
            "issuer": TextInput(attrs={"placeholder": "Coursera"}),
            "issued_at": DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "credential_url": URLInput(attrs={"placeholder": "https://coursera.org/verify/.."}),
        }

    
    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama sertifikat tidak boleh hanya berisi tag HTML.")
        return title

    def clean_issuer(self):
        issuer = strip_tags(self.cleaned_data["issuer"]).strip()
        if not issuer:
            raise ValidationError("Nama penerbit tidak boleh hanya berisi tag HTML.")
        return issuer

class ProjectForm(ModelForm):
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
    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML,")
        return title

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data["tech_stack"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()
    

class ExperienceForm(ModelForm):

    class Meta:
        model = Experience
        fields = ["title", "category", "description", "thumbnail", "started_at", "ended_at"]

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
            "thumbnail": URLInput(attrs={"placeholder": "https://drive.google.com"}),
        }        