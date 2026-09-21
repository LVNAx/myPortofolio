from django.urls import path
from main.views import (show_main, show_experience, project_list, show_journey, create_project, get_projects_json, 
                        delete_project, create_experience, delete_experience, get_experience_json)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("projects/", project_list, name="project_list"),
    path("journey/", show_journey, name="show_journey"),
    path("projects/add/", create_project, name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project"),

    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
]