from django.contrib import messages
from django.contrib.auth import login, logout 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Person, Mahasiswa, Experience, Project, JourneyStage
from .forms import ProjectForm, ExperienceForm
import datetime
from django.views.decorators.http import require_POST
from django.templatetags.static import static

PROFILE = {
    "name": "Nugraha",
    "npm": "2506541250",
    "study_program": "S1 Ilmu Komputer",
    "bio": (
        "A Computer Science student at Universitas Indonesia with a strong passion for data science, artificial intelligence, "
        "and software engineering, dedicated to building impactful and intelligent solutions."
    ),
}

def is_editor(user):
    # True kalau user udah login dan tergabung dalam grup editor.
    return user.is_authenticated and user.groups.filter(name="Editor").exists()

def can_edit(user):
    # Pemilik (si superuser) dan editor boleh mengubah data.
    return user.is_superuser or is_editor(user)

def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        **PROFILE,
        "persons": Person.objects.all(),
        "mahasiswa_list": Mahasiswa.objects.all(),
        "last_login": last_login,
    }
    return render(request, "index.html", context)

def show_experience(request):
    category, sort = get_experience_filter(request)

    # Data akan diambil dari JSON, lalu bakal diubah jadi objek experience
    json_response = get_experience_json(request)
    experiences = [
        item.object
        for item in serializers.deserialize("json", json_response.content.decode("utf-8"))
    ]

    context = {
        **PROFILE,
        "experience_list": experiences,
        "category_choices": Experience.EXPERIENCE_CHOICES,
        "selected_category": category,
        "selected_sort": sort,
        "can_edit": can_edit(request.user),
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
    projects = Project.objects.prefetch_related("starred_by").all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # JSON disusun manual supaya bisa menyisipkan logika star per pengguna
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user.is_authenticated and request.user in starred_users

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "role": project.role,
                "category": project.get_category_display(),
                "description": project.description,
                "highlights": project.highlight_list,
                "tech_stack": project.tech_stack,
                "thumbnail_url": static(project.thumbnail) if project.thumbnail else "",
                "live_url": project.live_url,
                "github_url": project.github_url,
                "is_ongoing": project.is_ongoing,
                "star_count": len(starred_users),
                "is_starred": is_starred,
                "starred_by_names": ", ".join(u.username for u in starred_users),
            },
        })

    return JsonResponse(data, safe=False)


def project_list(request):
    # Daftar proyek tidak lagi dirender di sini. Halaman hanya membawa kerangka,
    # lalu JavaScript mengambil datanya dari get_projects_json.
    title_query = request.GET.get("title", "").strip()

    context = {
        **PROFILE,
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "projects.html", context)

@login_required(login_url="/login/") # Memeriksa request.user dlu
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:project_list")

    # Karena sekarang udah ada role editor, maka yang secret kita hapus

    context = {
        **PROFILE,
        "form": form,
    }
    return render(request, "projects_form.html", context)

@login_required(login_url="/login/") 
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        # is_owner tadi udah kita delete
        project.delete()
        messages.success(request, "Proyek berhasil dihapus")

    return redirect("main:project_list")

EXPERIENCE_SORT = {
    "newest": "-started_at",
    "oldest": "started_at",
}

def get_experience_filter(request):
    # Ini utk membaca ?category dan ?sort dari url akan cuman nerima nilai yang valid

    category = request.GET.get("category", "").strip()
    if category not in dict(Experience.EXPERIENCE_CHOICES):
        category = ""

    sort = request.GET.get("sort", "newest")
    if sort not in EXPERIENCE_SORT:
        sort = "newest"

    return category, sort

# Endpoint JSON, dipakai juga oleh show_experience sebagai sumber data
def get_experience_json(request):
    category, sort = get_experience_filter(request)
    experiences = Experience.objects.all()

    if category:
        experiences = experiences.filter(category=category)

    experiences = experiences.order_by(EXPERIENCE_SORT[sort], "title")
    experience_json = serializers.serialize("json", experiences, use_natural_foreign_keys=True) # Ini kita tambahkan dengan tujuan mencegah bocornya id pengguna
    return HttpResponse(experience_json, content_type="application/json")

@login_required(login_url="/login/") 
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        **PROFILE,
        "form": form,
    }
    return render(request, "experience_form.html", context)

@login_required(login_url="/login/") 
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
            raise PermissionDenied
    
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")

    return redirect("main:show_experience")

@login_required(login_url="/login/") 
def edit_experience(request, experience_id):
    if not can_edit(request.user):
        raise PermissionDenied
    
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)  # instance = data lama yang diedit

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")


    context = {
        **PROFILE,
        "form": form,
        "is_edit": True,
    }
    return render(request, "experience_form.html", context)

# Tutorial-4 AuthSessionCookie
def register(request):
    """
    UserCreationForm ini secara otomatis akan menyediakan Username, Password1, dan Password2.is_valid() 
    yang mana ini itu akan mengecek username dan kecocokan antara password. Ohh malah sampai konfigurasi 
    password yang tepatnya.
    """
    form = UserCreationForm(request.POST or None)   

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun anda berhasil dibuat. Silakan login.")
        return redirect("main:login_user")

    context = {
        "name":"Nugraha",
        "form":form
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        
        login(request, user) # Ini utk menciptakan sebuah sesi (session), form.get_user() tu ia ngambil informasi sang user
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Nugraha",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:project_list")

# Star Experience: semua akun yang udah login boleh
@login_required(login_url="/login/")
def toggle_experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")

@require_POST # Hanya menerima method POST, yang lain 405
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status = 403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk":str(project.id)},
            status = 201,
        )

    return JsonResponse({"errors":form.errors.get_json_data()}, status=400)