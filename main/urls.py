from django.urls import path
from main.views import show_main, show_experience, project_list, show_journey

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("projects/", project_list, name="project_list"),
    path("journey/", show_journey, name="show_journey"),
]