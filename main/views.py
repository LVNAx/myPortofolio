from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Person, Mahasiswa, Experience, Project, JourneyStage
from .forms import ProjectForm
import hmac
from django.conf import settings

PROFILE = {
    "name": "Nugraha",
    "npm": "2506541250",
    "study_program": "S1 Ilmu Komputer",
    "bio": (
        "A Computer Science student at Universitas Indonesia with a strong passion for data science, artificial intelligence, "
        "and software engineering, dedicated to building impactful and intelligent solutions."
    ),
}

# Untuk mengantisipasi yang ngedit
SECRET_HEADER = "X-Portfolio-Secret"


def is_owner(request, submitted_secret=""):
    """Cek kode rahasia dari header, atau dari field password kalau header tidak ada."""
    expected = settings.PORTFOLIO_SECRET
    if not expected:
        return False  # Kode belum diatur di .env, jadi tolak semua perubahan

    provided = request.headers.get(SECRET_HEADER) or submitted_secret
    return hmac.compare_digest(provided.encode(), expected.encode())


def show_main(request):
    context = {
        **PROFILE,
        "persons": Person.objects.all(),
        "mahasiswa_list": Mahasiswa.objects.all(),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        **PROFILE,
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_journey(request):
    context = {
        **PROFILE,
        "journeys": JourneyStage.objects.prefetch_related("activities").all(),
    }
    return render(request, "journey.html", context)


# Endpoint JSON, dipakai juga oleh project_list sebagai sumber data
def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")


def project_list(request):
    title_query = request.GET.get("title", "").strip()

    # Data diambil lewat endpoint JSON, lalu diubah kembali menjadi objek Project
    json_response = get_projects_json(request)
    projects = [
        item.object
        for item in serializers.deserialize("json", json_response.content.decode("utf-8"))
    ]

    context = {
        **PROFILE,
        "projects": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        if is_owner(request, form.cleaned_data.get("secret", "")):
            form.save()
            messages.success(request, "Proyek baru berhasil ditambahkan!")
            return redirect("main:project_list")

        form.add_error("secret", "Kode rahasia salah.")

    context = {
        **PROFILE,
        "form": form,
    }
    return render(request, "projects_form.html", context)


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if is_owner(request, request.POST.get("secret", "")):
            project.delete()
            messages.success(request, "Project berhasil dihapus!")
        else:
            messages.error(request, "Kode rahasia salah. Proyek tidak dihapus.")

    return redirect("main:project_list")