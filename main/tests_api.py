import uuid
from datetime import date, datetime, timezone as dt_timezone

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Certification, Experience, Project


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", role="Fullstack Developer", category="web",
            description="My website", tech_stack="Django", started_at=date(2026, 9, 1),
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "role": "Backend Developer", "category": "course",
            "description": "A useful app", "highlights": "", "tech_stack": "Python",
            "live_url": "https://example.com/", "github_url": "",
            "started_at": "2026-10-01", "ended_at": None,
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"live_url": "javascript:alert(1)"}, "live_url"),
            ({"started_at": "2026-10-01", "ended_at": "2026-09-01"}, "ended_at"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Changed")
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CertificationAPITest(APITestCase):
    """Bagian pilihan tugas: pengunjung baca, user biasa star, Editor PUT/PATCH, pemilik semua."""

    def setUp(self):
        self.owner = User.objects.create_superuser(username="owner", password="test-password")
        self.regular = User.objects.create_user(username="regular", password="test-password")
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.certification = Certification.objects.create(
            title="Meta Backend Developer", issuer="Coursera",
            category="swe", issued_at=date(2026, 1, 15),
        )
        self.list_url = reverse("api:certification-list")
        self.detail_url = reverse("api:certification-detail", args=[self.certification.id])
        self.star_url = reverse("api:certification-star", args=[self.certification.id])
        self.payload = {
            "title": "Google Data Analytics", "issuer": "Google", "category": "dsai",
            "issued_at": "2026-02-01", "credential_url": "",
        }

    def test_public_list_search_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.certification.id))
        self.assertEqual(response.data[0]["category_display"], "Software Engineering")
        self.assertEqual(len(self.client.get(self.list_url, {"q": "coursera"}).data), 1)
        self.assertEqual(self.client.get(self.list_url, {"q": "tidakada"}).data, [])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_guest_and_regular_cannot_write(self):
        for user in (None, self.regular):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "X"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
            self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 403)
        # Pastikan database benar-benar tidak berubah, bukan hanya statusnya 403
        self.assertEqual(Certification.objects.count(), 1)
        self.assertFalse(Certification.objects.filter(title="Google Data Analytics").exists())
        self.certification.refresh_from_db()
        self.assertEqual(self.certification.title, "Meta Backend Developer")
        self.assertEqual(self.certification.issuer, "Coursera")

    def test_staff_without_editor_group_cannot_patch(self):
        self.regular.is_staff = True
        self.regular.save()
        self.client.force_authenticate(user=self.regular)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.certification.refresh_from_db()
        self.assertEqual(self.certification.title, "Meta Backend Developer")

    def test_missing_certification_returns_404(self):
        url = reverse("api:certification-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(
            self.client.patch(url, {"title": "X"}, format="json").status_code,
            status.HTTP_404_NOT_FOUND,
        )
        star_url = reverse("api:certification-star", args=[uuid.uuid4()])
        self.assertEqual(self.client.post(star_url).status_code, status.HTTP_404_NOT_FOUND)

    def test_editor_can_patch_and_put(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"title": "Meta Backend Pro"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.certification.refresh_from_db()
        self.assertEqual(self.certification.title, "Meta Backend Pro")
        self.assertEqual(self.certification.issuer, "Coursera")
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_editor_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertTrue(Certification.objects.filter(pk=self.certification.pk).exists())
        self.assertEqual(Certification.objects.count(), 1)
        self.assertFalse(Certification.objects.filter(title="Google Data Analytics").exists())

    def test_editor_patch_is_validated_and_stripped(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"title": "<i>Meta</i> Backend"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.certification.refresh_from_db()
        self.assertEqual(self.certification.title, "Meta Backend")
        response = self.client.patch(self.detail_url, {"issuer": "<script></script>"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("issuer", response.data)
        self.certification.refresh_from_db()
        self.assertEqual(self.certification.issuer, "Coursera")

    def test_owner_can_create_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(Certification.objects.get(pk=response.data["id"]).credential_url)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Certification.objects.filter(pk=self.certification.pk).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "<b></b>"}, "title"),
            ({"issuer": "   "}, "issuer"),
            ({"credential_url": "javascript:alert(1)"}, "credential_url"),
            ({"category": "unknown"}, "category"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Certification.objects.count(), 1)

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.certification.starred_by.count(), 0)
        self.client.force_authenticate(user=self.regular)
        self.assertEqual(self.client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(self.certification.starred_by.exists())

    def test_star_uses_request_user_only(self):
        # Klien tidak bisa memberi star atas nama akun lain lewat body request
        self.client.force_authenticate(user=self.regular)
        self.client.post(self.star_url, {"user": self.owner.id, "starred_by": [self.owner.id]}, format="json")
        self.assertEqual(list(self.certification.starred_by.all()), [self.regular])

    def test_editor_and_regular_can_star(self):
        for user in (self.editor, self.regular):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.certification.starred_by.count(), 2)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Certification.objects.count(), 1)

        # Editor juga ditolak saat PATCH tanpa token CSRF
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="editor", password="test-password"))
        response = client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.certification.refresh_from_db()
        self.assertEqual(self.certification.title, "Meta Backend Developer")

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        page = client.get(reverse("main:show_certification"))
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Certification.objects.count(), 2)


class ExperienceAPITest(APITestCase):
    """Tugas 6: pengunjung baca, user biasa star, Editor PUT/PATCH, pemilik semua."""

    def setUp(self):
        self.owner = User.objects.create_superuser(username="owner", password="test-password")
        self.regular = User.objects.create_user(username="regular", password="test-password")
        self.editor = User.objects.create_user(username="editor", password="test-password")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP", description="Membantu mahasiswa memahami Django.",
            category="part-time", started_at=datetime(2026, 2, 1, tzinfo=dt_timezone.utc),
        )
        self.other = Experience.objects.create(
            title="Magang Data", description="Analisis data penjualan.",
            category="internship", started_at=datetime(2025, 6, 1, tzinfo=dt_timezone.utc),
            ended_at=datetime(2025, 8, 31, tzinfo=dt_timezone.utc),
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.star_url = reverse("api:experience-star", args=[self.experience.id])
        self.payload = {
            "title": "Staff Multimedia", "category": "volunteer",
            "description": "Membangun dan merawat situs BEM.", "thumbnail": "",
            "started_at": "2026-03-01", "ended_at": None,
        }

    def assertExperienceUnchanged(self):
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Dosen PBP")
        self.assertEqual(self.experience.description, "Membantu mahasiswa memahami Django.")
        self.assertEqual(Experience.objects.count(), 2)
        self.assertFalse(Experience.objects.filter(title="Staff Multimedia").exists())

    # Membaca data
    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["title"] for item in response.data], ["Asisten Dosen PBP", "Magang Data"])

        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["category_display"], "Part-Time")
        self.assertTrue(response.data["is_ongoing"])
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_response_has_explicit_fields_without_sensitive_data(self):
        self.experience.starred_by.add(self.regular)
        data = self.client.get(self.detail_url).data

        self.assertEqual(set(data), {
            "id", "title", "category", "category_display", "description", "thumbnail",
            "started_at", "ended_at", "is_ongoing", "star_count", "is_starred", "starred_by_names",
        })
        self.assertEqual(data["starred_by_names"], "regular")
        self.assertNotIn("starred_by", data)
        self.assertNotIn("password", str(data))

    def test_search_filter_and_sort_query_params(self):
        def titles(params):
            return [item["title"] for item in self.client.get(self.list_url, params).data]

        self.assertEqual(titles({"q": "dosen"}), ["Asisten Dosen PBP"])
        self.assertEqual(titles({"q": "PENJUALAN"}), ["Magang Data"])  # deskripsi, tidak peka huruf besar
        self.assertEqual(titles({"q": "tidakada"}), [])
        self.assertEqual(titles({"category": "internship"}), ["Magang Data"])
        self.assertEqual(titles({"category": "ngawur"}), ["Asisten Dosen PBP", "Magang Data"])
        self.assertEqual(titles({"sort": "oldest"}), ["Magang Data", "Asisten Dosen PBP"])

    def test_missing_experience_returns_404(self):
        missing = uuid.uuid4()
        self.assertEqual(
            self.client.get(reverse("api:experience-detail", args=[missing])).status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(
            self.client.delete(reverse("api:experience-detail", args=[missing])).status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.assertEqual(
            self.client.post(reverse("api:experience-star", args=[missing])).status_code,
            status.HTTP_404_NOT_FOUND,
        )

    # Pengunjung dan pengguna biasa
    def test_visitor_and_regular_user_cannot_write(self):
        for user in (None, self.regular):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Curang"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        # Pastikan database benar-benar tidak berubah, bukan hanya statusnya 403
        self.assertExperienceUnchanged()

    def test_staff_without_editor_group_cannot_patch(self):
        self.regular.is_staff = True
        self.regular.save()
        self.client.force_authenticate(user=self.regular)

        response = self.client.patch(self.detail_url, {"title": "Curang"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertExperienceUnchanged()

    # Editor
    def test_editor_can_patch_and_put(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.patch(self.detail_url, {"title": "Asisten Dosen PBP 2026"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Dosen PBP 2026")
        self.assertEqual(self.experience.category, "part-time")  # PATCH tidak menyentuh field lain

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Staff Multimedia")
        self.assertEqual(self.experience.category, "volunteer")
        self.assertEqual(Experience.objects.count(), 2)

    def test_editor_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)

        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())
        self.assertExperienceUnchanged()

    # Pemilik
    def test_owner_can_create_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Experience.objects.get(pk=response.data["id"])
        self.assertEqual(created.title, "Staff Multimedia")
        self.assertIsNone(created.thumbnail)  # string kosong disimpan sebagai None
        self.assertTrue(response.data["is_ongoing"])

        response = self.client.delete(reverse("api:experience-detail", args=[created.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Experience.objects.filter(pk=created.pk).exists())

    def test_client_cannot_set_read_only_fields(self):
        self.client.force_authenticate(user=self.owner)
        payload = {**self.payload, "id": str(uuid.uuid4()), "star_count": 99, "is_starred": True}

        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data["id"], payload["id"])
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(Experience.objects.get(pk=response.data["id"]).starred_by.exists())

    # Validasi input
    def test_html_tags_are_stripped(self):
        self.client.force_authenticate(user=self.owner)
        payload = {
            **self.payload,
            "title": "<b>Staff</b> Multimedia",
            "description": "<script>x</script>Membangun situs",
        }

        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = Experience.objects.get(pk=response.data["id"])
        self.assertEqual(created.title, "Staff Multimedia")
        self.assertNotIn("<", created.description)

    def test_invalid_input_returns_400(self):
        self.client.force_authenticate(user=self.owner)
        without_title = {key: value for key, value in self.payload.items() if key != "title"}
        invalid_payloads = [
            ({**self.payload, "title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({**self.payload, "description": "   "}, "description"),
            ({**self.payload, "category": "bukan-kategori"}, "category"),
            ({**self.payload, "thumbnail": "bukan url"}, "thumbnail"),
            ({**self.payload, "started_at": "kemarin"}, "started_at"),
            ({**self.payload, "ended_at": "2026-01-01"}, "ended_at"),  # sebelum started_at
            (without_title, "title"),
        ]
        for payload, field in invalid_payloads:
            with self.subTest(field=field):
                response = self.client.post(self.list_url, payload, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(field, response.data)
        self.assertExperienceUnchanged()

    def test_editor_patch_is_validated(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.patch(self.detail_url, {"title": "<script></script>"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

        # ended_at dibandingkan dengan started_at yang sudah tersimpan
        response = self.client.patch(self.detail_url, {"ended_at": "2025-01-01"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ended_at", response.data)
        self.assertExperienceUnchanged()
        self.assertIsNone(self.experience.ended_at)

    # Star
    def test_star_requires_login(self):
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(self.experience.starred_by.exists())

    def test_star_toggles_for_request_user(self):
        self.client.force_authenticate(user=self.regular)
        self.assertEqual(self.client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertEqual(list(self.experience.starred_by.all()), [self.regular])

        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(self.experience.starred_by.exists())

    def test_star_uses_request_user_only(self):
        # Klien tidak bisa memberi star atas nama akun lain lewat body request
        self.client.force_authenticate(user=self.regular)
        self.client.post(self.star_url, {"user": self.owner.id, "starred_by": [self.owner.id]}, format="json")
        self.assertEqual(list(self.experience.starred_by.all()), [self.regular])

    def test_every_logged_in_role_can_star(self):
        for user in (self.regular, self.editor, self.owner):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_200_OK)
        self.assertEqual(self.experience.starred_by.count(), 3)

    # CSRF dengan login sungguhan (bukan force_authenticate)
    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="editor", password="test-password"))
        response = client.patch(self.detail_url, {"title": "Curang"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="regular", password="test-password"))
        self.assertEqual(client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)

        self.assertExperienceUnchanged()
        self.assertFalse(self.experience.starred_by.exists())

    def test_session_write_with_csrf_from_page_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="editor", password="test-password")
        # Halaman Experience memasang cookie csrftoken (@ensure_csrf_cookie)
        page = client.get(reverse("main:show_experience"))
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value

        response = client.patch(
            self.detail_url, {"title": "Asisten Dosen PBP (Editor)"},
            format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Dosen PBP (Editor)")
