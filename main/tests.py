from datetime import date
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.test import TestCase, override_settings
from main.models import Experience, Project, JourneyStage, StageActivity
import json
from datetime import date, timedelta


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
        self.assertContains(response, "Ongoing")
        self.assertContains(response, self.project.live_url)

    def test_empty_project_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:project_list"))

        self.assertContains(response, "No projects added yet.")

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
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")

    def test_github_button_hidden_when_url_empty(self):
        response = self.client.get(reverse("main:project_list"))

        self.assertNotContains(response, "GitHub")

    def test_navbar_links_to_main(self):
        response = self.client.get(reverse("main:project_list"))

        self.assertContains(response, f'href="{reverse("main:show_main")}"')


# Ini cuman penasaran
    @override_settings(PORTFOLIO_SECRET="rahasia-test")
    def test_delete_rejected_with_wrong_secret(self):
        url = reverse("main:delete_project", args=[self.project.id])
        self.client.post(url, {"secret": "salah"})

        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())

    @override_settings(PORTFOLIO_SECRET="rahasia-test")
    def test_delete_with_secret_header(self):
        url = reverse("main:delete_project", args=[self.project.id])
        self.client.post(url, headers={"X-Portfolio-Secret": "rahasia-test"})

        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    @override_settings(PORTFOLIO_SECRET="rahasia-test")
    def test_create_rejected_without_secret(self):
        self.client.post(reverse("main:create_project"), {
            "title": "Proyek Palsu",
            "role": "Penyusup",
            "category": "web",
            "description": "Tidak boleh tersimpan.",
            "tech_stack": "Django",
            "started_at": "2026-09-01",
        })

        self.assertFalse(Project.objects.filter(title="Proyek Palsu").exists())

class JourneyTest(TestCase):
    def setUp(self):
        self.stage = JourneyStage.objects.create(
            name="SMA",
            school="SMA Negeri 1 Pontianak",
            start_year=2022,
            end_year=2025,
            tags="sains, kompetitif, mandiri",
            description=" ".join(["belajar" * 60]), # Jadi ada 60 kata
            order=1,
        )

        self.activity=StageActivity.objects.create(
            stage=self.stage,
            title="Top 3 OSN Astronomi",
            category=StageActivity.Category.OLIMPIADE,
            description="Juara tingkat provinsi\nMewakili sekolah",
            order=1,
        )

    # URL bisa diakses dan pakai template yang benar
    def test_journey_url_is_accessible(self):
        response = self.client.get(reverse("main:show_journey"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "journey.html")
        self.assertTemplateUsed(response, "base.html")

    # Data dari model muncul di HTML
    def test_journey_page_displays_data(self):
        response = self.client.get(reverse("main:show_journey"))

        self.assertContains(response, self.stage.name)
        self.assertContains(response, self.stage.school)
        self.assertContains(response, "2022 sampai 2025")
        self.assertContains(response, "kompetitif")
        self.assertContains(response, self.activity.title)
        self.assertContains(response, "Olimpiade")
        self.assertContains(response, "Mewakili sekolah")

    def test_empty_journey_page(self):
        JourneyStage.objects.all().delete()
        response = self.client.get(reverse("main:show_journey"))

        self.assertContains(response, "No stages added yet.")
        self.assertNotContains(response, "SMA Negeri 1 Pontianak")

    # Navbar punya link Journey dan nandain sebagai halaman yang sedang dilihat
    def test_navbar_marks_journey_as_current(self):
        response = self.client.get(reverse("main:show_journey"))

        self.assertContains(response, f'href="{reverse("main:show_journey")}"')
        self.assertContains(response, 'aria-current="page">Journey</a>')

    # property di model
    def test_journey_model(self):
        self.assertEqual(str(self.stage), "SMA (SMA Negeri 1 Pontianak)")
        self.assertEqual(self.stage.tag_list, ["sains", "kompetitif", "mandiri"])
        self.assertEqual(len(self.activity.point_list), 2)

    # validator jumlah kata
    def test_description_word_count_validator(self):
        self.stage.description = "terlalu pendek"

        with self.assertRaises(ValidationError):
            self.stage.full_clean()

class ExperienceFeatureTest(TestCase):
    def setUp(self):
        now = timezone.now()
        Experience.objects.create(
            title="Magang Data", description="Analisis data.",
            category="internship", started_at=now - timedelta(days=200),
        )
        Experience.objects.create(
            title="Asisten Dosen", description="Mengajar.",
            category="part-time", started_at=now - timedelta(days=100),
        )
        Experience.objects.create(
            title="Staff Multimedia", description="Membangun web.",
            category="volunteer", started_at=now - timedelta(days=10),
        )

    def titles(self, response):
        return [item.title for item in response.context["experience_list"]]

    def test_default_sort_is_newest_first(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(
            self.titles(response),
            ["Staff Multimedia", "Asisten Dosen", "Magang Data"],
        )

    def test_sort_oldest_first(self):
        response = self.client.get(reverse("main:show_experience"), {"sort": "oldest"})

        self.assertEqual(
            self.titles(response),
            ["Magang Data", "Asisten Dosen", "Staff Multimedia"],
        )
        self.assertEqual(response.context["selected_sort"], "oldest")

    def test_invalid_sort_falls_back_to_newest(self):
        response = self.client.get(reverse("main:show_experience"), {"sort": "asal"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected_sort"], "newest")
        self.assertEqual(self.titles(response)[0], "Staff Multimedia")

    def test_filter_by_category(self):
        response = self.client.get(reverse("main:show_experience"), {"category": "part-time"})

        self.assertEqual(self.titles(response), ["Asisten Dosen"])
        self.assertEqual(response.context["selected_category"], "part-time")

    def test_invalid_category_shows_all(self):
        response = self.client.get(reverse("main:show_experience"), {"category": "ngawur"})

        self.assertEqual(len(self.titles(response)), 3)
        self.assertEqual(response.context["selected_category"], "")

    def test_filter_without_result_shows_message(self):
        response = self.client.get(reverse("main:show_experience"), {"category": "research"})

        self.assertContains(response, "Tidak ada pengalaman pada kategori ini.")

    def test_json_endpoint(self):
        response = self.client.get(
            reverse("main:get_experience_json"), {"sort": "oldest", "category": "internship"}
        )
        data = json.loads(response.content)

        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["title"], "Magang Data")

    @override_settings(PORTFOLIO_SECRET="rahasia-test")
    def test_create_experience_with_secret(self):
        response = self.client.post(reverse("main:create_experience"), {
            "title": "Pengalaman Baru", "category": "freelance",
            "description": "Membuat web.", "started_at": "2026-01-01",
            "ended_at": "", "secret": "rahasia-test",
        })

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(Experience.objects.filter(title="Pengalaman Baru").exists())

    @override_settings(PORTFOLIO_SECRET="rahasia-test")
    def test_create_experience_rejected_with_wrong_secret(self):
        response = self.client.post(reverse("main:create_experience"), {
            "title": "Tidak Boleh Masuk", "category": "freelance",
            "description": "Membuat web.", "started_at": "2026-01-01",
            "ended_at": "", "secret": "salah",
        })

        self.assertContains(response, "Kode rahasia salah.")
        self.assertFalse(Experience.objects.filter(title="Tidak Boleh Masuk").exists())

    @override_settings(PORTFOLIO_SECRET="rahasia-test")
    def test_delete_experience_with_secret(self):
        target = Experience.objects.get(title="Magang Data")
        self.client.post(
            reverse("main:delete_experience", args=[target.id]),
            {"secret": "rahasia-test"},
        )

        self.assertFalse(Experience.objects.filter(pk=target.pk).exists())

    @override_settings(PORTFOLIO_SECRET="rahasia-test")
    def test_delete_experience_rejected_with_wrong_secret(self):
        target = Experience.objects.get(title="Magang Data")
        self.client.post(
            reverse("main:delete_experience", args=[target.id]),
            {"secret": "salah"},
        )

        self.assertTrue(Experience.objects.filter(pk=target.pk).exists())

    def test_edit_page_is_prefilled(self):
        target = Experience.objects.get(title="Magang Data")
        response = self.client.get(reverse("main:edit_experience", args=[target.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertContains(response, "Magang Data")
        self.assertContains(response, "Ubah Pengalaman")

    def test_edit_page_unknown_id_returns_404(self):
        response = self.client.get(
            reverse("main:edit_experience", args=["00000000-0000-0000-0000-000000000000"])
        )

        self.assertEqual(response.status_code, 404)

    def test_experience_card_links_to_edit(self):
        target = Experience.objects.get(title="Magang Data")
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, reverse("main:edit_experience", args=[target.id]))

    @override_settings(PORTFOLIO_SECRET="rahasia-test")
    def test_edit_experience_with_secret(self):
        target = Experience.objects.get(title="Magang Data")
        response = self.client.post(reverse("main:edit_experience", args=[target.id]), {
            "title": "Magang Data (Diperbarui)", "category": "internship",
            "description": "Analisis data.", "started_at": "2026-02-01",
            "ended_at": "", "secret": "rahasia-test",
        })
        target.refresh_from_db()

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertEqual(target.title, "Magang Data (Diperbarui)")
        self.assertEqual(Experience.objects.count(), 3)

    @override_settings(PORTFOLIO_SECRET="rahasia-test")
    def test_edit_experience_rejected_with_wrong_secret(self):
        target = Experience.objects.get(title="Magang Data")
        response = self.client.post(reverse("main:edit_experience", args=[target.id]), {
            "title": "Judul Curang", "category": "internship",
            "description": "Analisis data.", "started_at": "2026-02-01",
            "ended_at": "", "secret": "salah",
        })
        target.refresh_from_db()

        self.assertContains(response, "Kode rahasia salah.")
        self.assertEqual(target.title, "Magang Data")