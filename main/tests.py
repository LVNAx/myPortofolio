from datetime import date

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Project

class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")
class ProjectTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Sandbox",
            role="Fullstack Developer",
            category="web",
            description="Situs monitoring akademik dan harian.",
            highlights="Resend email otomatis\nRubrik IP otomatis",
            tech_stack="Next.js, Resend, Tailwind CSS",
            live_url="https://lvnasandbox.vercel.app",
            started_at=date(2026, 6, 1),
            order=1,
        )

    def test_project_url_is_accessible(self):
        response = self.client.get(reverse("main:project_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_project_page_displays_data(self):
        response = self.client.get(reverse("main:project_list"))

        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.role)
        self.assertContains(response, self.project.description)
        self.assertContains(response, "Web Development")
        self.assertContains(response, "Resend email otomatis")
        self.assertContains(response, "Tailwind CSS")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, self.project.live_url)

    def test_empty_project_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:project_list"))

        self.assertContains(response, "Belum ada proyek yang ditambahkan.")

    def test_project_model(self):
        self.assertEqual(str(self.project), "Sandbox")
        self.assertEqual(
            self.project.tech_list, ["Next.js", "Resend", "Tailwind CSS"]
        )
        self.assertEqual(len(self.project.highlight_list), 2)
        self.assertTrue(self.project.is_ongoing)

    def test_completed_project(self):
        self.project.ended_at = date(2026, 8, 1)
        self.project.save()
        response = self.client.get(reverse("main:project_list"))

        self.assertFalse(self.project.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    def test_github_button_hidden_when_url_empty(self):
        response = self.client.get(reverse("main:project_list"))

        self.assertNotContains(response, "GitHub")

    def test_navbar_links_to_main(self):
        response = self.client.get(reverse("main:project_list"))

        self.assertContains(response, f'href="{reverse("main:show_main")}"')