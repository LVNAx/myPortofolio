import json
from datetime import date, timedelta

from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, JourneyStage, Project, StageActivity, Certification


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
        # Tanpa password: force_login tidak butuh password, dan hashing password itu lambat
        self.admin = User.objects.create_superuser("admin")
        self.client.force_login(self.admin)

    def test_project_url_is_accessible(self):
        response = self.client.get(reverse("main:project_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")

    def test_project_page_displays_data(self):
        response = self.client.get(reverse("main:get_projects_json"))
        item = json.loads(response.content)[0]["fields"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(item["title"], self.project.title)
        self.assertEqual(item["role"], self.project.role)
        self.assertEqual(item["description"], self.project.description)
        self.assertEqual(item["category"], "Web Development")
        self.assertIn("Resend email otomatis", item["highlights"])
        self.assertEqual(item["live_url"], self.project.live_url)
        self.assertTrue(item["is_ongoing"])

    def test_project_page_is_a_skeleton(self):
        response = self.client.get(reverse("main:project_list"))

        # Data tidak dirender server, hanya wadah yang akan diisi JavaScript
        self.assertNotContains(response, self.project.title)
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, 'id="empty"')

    def test_empty_project_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:get_projects_json"))

        self.assertEqual(json.loads(response.content), [])

    def test_project_model(self):
        self.assertEqual(str(self.project), "Sandbox")
        self.assertEqual(
            self.project.tech_list, ["Next.js", "Resend", "Tailwind CSS"]
        )
        self.assertEqual(len(self.project.highlight_list), 2)
        self.assertTrue(self.project.is_ongoing)

    # def test_completed_project(self):
    #     self.project.ended_at = date(2026, 8, 1)
    #     self.project.save()
    #     response = self.client.get(reverse("main:project_list"))

    #     self.assertFalse(self.project.is_ongoing)
    #     self.assertContains(response, "Completed")
    #     self.assertNotContains(response, "Ongoing")

    def test_completed_project(self):
        self.project.ended_at = date(2026, 8, 1)
        self.project.save()
        response = self.client.get(reverse("main:get_projects_json"))
        item = json.loads(response.content)[0]["fields"]

        self.assertFalse(self.project.is_ongoing)
        self.assertFalse(item["is_ongoing"])

    def test_github_button_hidden_when_url_empty(self):
        response = self.client.get(reverse("main:get_projects_json"))
        item = json.loads(response.content)[0]["fields"]

        self.assertFalse(item["github_url"], "")

        

    def test_navbar_links_to_main(self):
        response = self.client.get(reverse("main:project_list"))

        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_owner_can_create_project(self):
        response = self.client.post(reverse("main:create_project"), {
            "title": "Proyek Baru", "role": "Dev", "category": "web",
            "description": "Deskripsi.", "tech_stack": "Django",
            "started_at": "2026-09-01",
        })

        self.assertRedirects(response, reverse("main:project_list"))
        self.assertTrue(Project.objects.filter(title="Proyek Baru").exists())

    def test_owner_can_delete_project(self):
        self.client.post(reverse("main:delete_project", args=[self.project.id]))

        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())


class JourneyTest(TestCase):
    def setUp(self):
        self.stage = JourneyStage.objects.create(
            name="SMA",
            school="SMA Negeri 1 Pontianak",
            start_year=2022,
            end_year=2025,
            tags="sains, kompetitif, mandiri",
            description=" ".join(["belajar"] * 60),  # 60 kata
            order=1,
        )

        self.activity = StageActivity.objects.create(
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

    # Navbar punya link Journey dan menandainya sebagai halaman yang sedang dilihat
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
        self.admin = User.objects.create_superuser("admin")
        self.client.force_login(self.admin)

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

    def test_create_experience(self):
        response = self.client.post(reverse("main:create_experience"), {
            "title": "Pengalaman Baru", "category": "freelance",
            "description": "Membuat web.", "started_at": "2026-01-01",
            "ended_at": "",
        })

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(Experience.objects.filter(title="Pengalaman Baru").exists())

    def test_delete_experience(self):
        target = Experience.objects.get(title="Magang Data")
        self.client.post(reverse("main:delete_experience", args=[target.id]))

        self.assertFalse(Experience.objects.filter(pk=target.pk).exists())

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

    def test_edit_experience(self):
        target = Experience.objects.get(title="Magang Data")
        response = self.client.post(reverse("main:edit_experience", args=[target.id]), {
            "title": "Magang Data (Diperbarui)", "category": "internship",
            "description": "Analisis data.", "started_at": "2026-02-01",
            "ended_at": "",
        })
        target.refresh_from_db()

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertEqual(target.title, "Magang Data (Diperbarui)")
        self.assertEqual(Experience.objects.count(), 3)


class ExperienceRoleTest(TestCase):
    """Menguji empat peran: pengunjung, pengguna biasa, editor, dan pemilik."""

    def setUp(self):
        self.experience = Experience.objects.create(
            title="Magang Data", description="Analisis data.", category="internship",
        )
        self.owner = User.objects.create_superuser("owner")
        self.editor = User.objects.create_user("editor")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.biasa = User.objects.create_user("biasa")

        self.edit_url = reverse("main:edit_experience", args=[self.experience.id])
        self.delete_url = reverse("main:delete_experience", args=[self.experience.id])
        self.star_url = reverse("main:toggle_experience_star", args=[self.experience.id])
        self.create_url = reverse("main:create_experience")
        self.list_url = reverse("main:show_experience")

    def edit_data(self, title):
        return {
            "title": title, "category": "internship", "description": "Analisis data.",
            "started_at": "2026-02-01", "ended_at": "",
        }

    # Pengunjung tanpa login
    def test_anonymous_can_read_without_action_buttons(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Magang Data")
        self.assertNotContains(response, "Tambah Pengalaman")
        self.assertNotContains(response, ">Ubah<")
        self.assertNotContains(response, "Hapus Pengalaman")

    def test_anonymous_redirected_to_login(self):
        for url in [self.create_url, self.edit_url, self.delete_url, self.star_url]:
            response = self.client.post(url)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/login/", response["Location"])

    # Pengguna biasa
    def test_regular_user_forbidden_to_change_data(self):
        self.client.force_login(self.biasa)

        self.assertEqual(self.client.get(self.create_url).status_code, 403)
        self.assertEqual(self.client.post(self.edit_url, self.edit_data("Curang")).status_code, 403)
        self.assertEqual(self.client.post(self.delete_url).status_code, 403)

        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Magang Data")

    def test_regular_user_sees_only_star(self):
        self.client.force_login(self.biasa)
        response = self.client.get(self.list_url)

        self.assertContains(response, "star-form")
        self.assertNotContains(response, "Tambah Pengalaman")
        self.assertNotContains(response, ">Ubah<")
        self.assertNotContains(response, "Hapus Pengalaman")

    def test_star_toggle_one_per_user(self):
        self.client.force_login(self.biasa)

        self.client.post(self.star_url)
        self.client.post(self.star_url)
        self.assertEqual(self.experience.starred_by.count(), 0)   # dua kali klik = batal

        self.client.post(self.star_url)
        self.client.force_login(self.editor)
        self.client.post(self.star_url)
        self.assertEqual(self.experience.starred_by.count(), 2)   # satu star per akun

    # Editor
    def test_editor_can_edit(self):
        self.client.force_login(self.editor)
        response = self.client.post(self.edit_url, self.edit_data("Magang Data (Editor)"))

        self.assertRedirects(response, self.list_url)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Magang Data (Editor)")

    def test_editor_cannot_create_or_delete(self):
        self.client.force_login(self.editor)

        self.assertEqual(self.client.get(self.create_url).status_code, 403)
        self.assertEqual(self.client.post(self.delete_url).status_code, 403)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_editor_sees_edit_but_not_create_or_delete(self):
        self.client.force_login(self.editor)
        response = self.client.get(self.list_url)

        self.assertContains(response, ">Ubah<")
        self.assertNotContains(response, "Tambah Pengalaman")
        self.assertNotContains(response, "Hapus Pengalaman")

    # Pemilik
    def test_owner_sees_all_buttons(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.list_url)

        self.assertContains(response, "Tambah Pengalaman")
        self.assertContains(response, ">Ubah<")
        self.assertContains(response, "Hapus Pengalaman")

    # API
    def test_json_shows_username_not_id(self):
        self.experience.starred_by.add(self.biasa)
        data = json.loads(self.client.get(reverse("main:get_experience_json")).content)

        self.assertEqual(data[0]["fields"]["starred_by"], [["biasa"]])

class CertificationTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser("owner")
        self.biasa = User.objects.create_user("biasa")
        self.sertifikat = Certification.objects.create(
            title="Meta Backend Developer",
            issuer="Coursera",
            category="swe",
            issued_at=date(2026, 1, 15),
        )
        self.data_valid = {
            "title": "Google Data Analytics",
            "issuer": "Google",
            "category": "dsai",
            "issued_at": "2026-02-01",
            "credential_url": "",
        }

    # Halaman dan JSON
    def test_page_is_accessible_by_visitor(self):
        response = self.client.get(reverse("main:show_certification"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "certifications.html")
        # Kerangka saja: data tidak dirender server
        self.assertNotContains(response, self.sertifikat.title)

    def test_json_returns_data_with_star_info(self):
        response = self.client.get(reverse("main:get_certifications_json"))
        item = json.loads(response.content)[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(item["fields"]["title"], "Meta Backend Developer")
        self.assertEqual(item["fields"]["star_count"], 0)
        self.assertFalse(item["fields"]["is_starred"])

    def test_json_search_matches_title_or_issuer(self):
        url = reverse("main:get_certifications_json")

        self.assertEqual(len(json.loads(self.client.get(url, {"q": "backend"}).content)), 1)
        self.assertEqual(len(json.loads(self.client.get(url, {"q": "coursera"}).content)), 1)
        self.assertEqual(json.loads(self.client.get(url, {"q": "tidakada"}).content), [])

    # Tambah data
    def test_visitor_cannot_add(self):
        response = self.client.post(reverse("main:create_certification_ajax"), self.data_valid)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Certification.objects.count(), 1)

    def test_normal_user_cannot_add(self):
        self.client.force_login(self.biasa)
        response = self.client.post(reverse("main:create_certification_ajax"), self.data_valid)

        self.assertEqual(response.status_code, 403)

    def test_owner_can_add(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse("main:create_certification_ajax"), self.data_valid)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Certification.objects.count(), 2)

    def test_invalid_data_returns_400_with_errors(self):
        self.client.force_login(self.owner)
        data = {**self.data_valid, "title": ""}
        response = self.client.post(reverse("main:create_certification_ajax"), data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("title", json.loads(response.content)["errors"])

    def test_get_method_is_not_allowed(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("main:create_certification_ajax"))

        self.assertEqual(response.status_code, 405)

    # XSS
    def test_tags_are_stripped_from_input(self):
        self.client.force_login(self.owner)
        data = {**self.data_valid, "title": "<b>Halo</b>"}
        self.client.post(reverse("main:create_certification_ajax"), data)

        self.assertTrue(Certification.objects.filter(title="Halo").exists())

    def test_title_with_only_tags_is_rejected(self):
        self.client.force_login(self.owner)
        data = {**self.data_valid, "title": '<img src="x" onerror="alert(1)">'}
        response = self.client.post(reverse("main:create_certification_ajax"), data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Certification.objects.count(), 1)

    # Star
    def test_star_requires_login(self):
        url = reverse("main:toggle_certification_star", args=[self.sertifikat.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)
        self.assertEqual(self.sertifikat.starred_by.count(), 0)

    def test_star_toggles_and_shows_in_json(self):
        self.client.force_login(self.biasa)
        url = reverse("main:toggle_certification_star", args=[self.sertifikat.id])

        self.client.post(url)
        item = json.loads(self.client.get(reverse("main:get_certifications_json")).content)[0]
        self.assertEqual(item["fields"]["star_count"], 1)
        self.assertTrue(item["fields"]["is_starred"])

        self.client.post(url)
        self.assertEqual(self.sertifikat.starred_by.count(), 0)