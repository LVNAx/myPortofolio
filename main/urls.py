from django.urls import path
from main.views import (show_main, show_experience, project_list, show_journey, create_project, get_projects_json, 
                        delete_project, create_experience, delete_experience, get_experience_json, edit_experience,
                        register, login_user, logout_user, toggle_star, toggle_experience_star, create_project_ajax)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("projects/", project_list, name="project_list"),
    path("journey/", show_journey, name="show_journey"),

    # Project Path
    path("projects/add/", create_project, name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project"),
    path("projects/add-ajax/", create_project_ajax, name = "create_project_ajax"),

    # Experience Path
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    path("experience/<uuid:experience_id>/edit/", edit_experience, name="edit_experience"),
    path("experience/<uuid:experience_id>/star/", toggle_experience_star, name="toggle_experience_star"),

    #  Register Path
    path("register/", register, name="register"),
    path("login/", login_user, name="login_user"),
    path("logout/", logout_user, name="logout_user"),
    # Tambahkan path ini ke dalam urlpatterns
    path(
        "projects/<uuid:project_id>/star/",
        toggle_star,
        name="toggle_star",
    ),
]