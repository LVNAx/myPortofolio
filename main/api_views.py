from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Certification, Experience, Project
from main.permissions import (
    IsPortfolioOwnerOrEditorOrReadOnly, IsPortfolioOwnerOrReadOnly,
)
from main.serializers import (
    CertificationSerializer, ExperienceSerializer, ProjectSerializer,
)
from main.views import EXPERIENCE_SORT, get_experience_filter


def toggle_star(request, obj, serializer_class):
    # Akun pemberi star selalu request.user, klien tidak bisa memilih user lain
    if obj.starred_by.filter(pk=request.user.pk).exists():
        obj.starred_by.remove(request.user)
    else:
        obj.starred_by.add(request.user)
    serializer = serializer_class(obj, context={"request": request})
    return Response(serializer.data)


# Projects

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_list(request):
    if request.method in ("GET", "HEAD"):
        projects = Project.objects.prefetch_related("starred_by").order_by("order", "-started_at", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            projects = projects.filter(title__icontains=title)
        serializer = ProjectSerializer(
            projects, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = ProjectSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related("starred_by"), pk=project_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = ProjectSerializer(project, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ProjectSerializer(
        project, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return toggle_star(request, project, ProjectSerializer)


# Certifications (bagian pilihan tugas, Editor boleh PUT/PATCH)

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def certification_list(request):
    if request.method in ("GET", "HEAD"):
        certifications = Certification.objects.prefetch_related("starred_by").order_by("-issued_at", "id")
        query = request.query_params.get("q", "").strip()
        if query:
            certifications = certifications.filter(
                Q(title__icontains=query) | Q(issuer__icontains=query)
            )
        serializer = CertificationSerializer(
            certifications, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = CertificationSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def certification_detail(request, certification_id):
    certification = get_object_or_404(
        Certification.objects.prefetch_related("starred_by"), pk=certification_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = CertificationSerializer(certification, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        certification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = CertificationSerializer(
        certification, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def certification_star(request, certification_id):
    certification = get_object_or_404(Certification, pk=certification_id)
    return toggle_star(request, certification, CertificationSerializer)


# Experience (Editor boleh PUT/PATCH, hanya pemilik yang boleh create/delete)

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_list(request):
    if request.method in ("GET", "HEAD"):
        # Filter ?category dan ?sort dari halaman lama, plus pencarian ?q
        category, sort = get_experience_filter(request)
        experiences = Experience.objects.prefetch_related("starred_by")
        if category:
            experiences = experiences.filter(category=category)
        query = request.query_params.get("q", "").strip()
        if query:
            experiences = experiences.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        experiences = experiences.order_by(EXPERIENCE_SORT[sort], "title", "id")
        serializer = ExperienceSerializer(
            experiences, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = ExperienceSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def experience_detail(request, experience_id):
    experience = get_object_or_404(
        Experience.objects.prefetch_related("starred_by"), pk=experience_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = ExperienceSerializer(experience, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        experience.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ExperienceSerializer(
        experience, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    return toggle_star(request, experience, ExperienceSerializer)
