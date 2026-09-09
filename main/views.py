from django.shortcuts import render
from .models import Person, Post, Mahasiswa, Experience

PROFILE = {
    "name": "Nugraha",
    "npm": "2506541250",
    "study_program": "S1 Ilmu Komputer",
    "bio": (
        "A Computer Science student at Universitas Indonesia with a strong passion for data science, artificial intelligence,"
        "and software engineering, dedicated to building impactful and intelligent solutions."
    ),
}

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