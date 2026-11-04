from django.urls import path

from main import api_views

app_name = "api"

urlpatterns = [
    path("projects/", api_views.project_list, name="project-list"),
    path("projects/<uuid:project_id>/", api_views.project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", api_views.project_star, name="project-star"),

    path("certifications/", api_views.certification_list, name="certification-list"),
    path("certifications/<uuid:certification_id>/", api_views.certification_detail, name="certification-detail"),
    path("certifications/<uuid:certification_id>/star/", api_views.certification_star, name="certification-star"),
]
