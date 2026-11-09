from django.templatetags.static import static
from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Certification, Experience, Project


class StarFieldsMixin(serializers.Serializer):
    """Field hasil perhitungan untuk fitur star (read-only, tidak bisa diisi klien)."""

    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    def get_star_count(self, obj):
        return len(obj.starred_by.all())

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class ProjectSerializer(StarFieldsMixin, serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    is_ongoing = serializers.BooleanField(read_only=True)
    highlight_list = serializers.ListField(child=serializers.CharField(), read_only=True)

    class Meta:
        model = Project
        fields = [
            "id", "title", "role", "category", "category_display",
            "description", "highlights", "highlight_list", "tech_stack",
            "thumbnail_url", "live_url", "github_url",
            "started_at", "ended_at", "is_ongoing",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Nama proyek tidak boleh kosong atau hanya berisi tag HTML.")
        return value

    def validate_role(self, value):
        return strip_tags(value).strip()

    def validate_description(self, value):
        return strip_tags(value).strip()

    def validate_highlights(self, value):
        return strip_tags(value)

    def validate_tech_stack(self, value):
        return strip_tags(value).strip()

    def validate(self, attrs):
        started_at = attrs.get("started_at", getattr(self.instance, "started_at", None))
        ended_at = attrs.get("ended_at", getattr(self.instance, "ended_at", None))
        if started_at and ended_at and ended_at < started_at:
            raise serializers.ValidationError(
                {"ended_at": "Tanggal selesai tidak boleh sebelum tanggal mulai."}
            )
        return attrs

    def get_thumbnail_url(self, obj):
        return static(obj.thumbnail) if obj.thumbnail else ""


class CertificationSerializer(StarFieldsMixin, serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = Certification
        fields = [
            "id", "title", "issuer", "category", "category_display",
            "issued_at", "credential_url",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Nama sertifikat tidak boleh kosong atau hanya berisi tag HTML.")
        return value

    def validate_issuer(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Nama penerbit tidak boleh kosong atau hanya berisi tag HTML.")
        return value

    def validate_credential_url(self, value):
        # Model memakai null=True, jadi string kosong disimpan sebagai None
        return value or None


class ExperienceSerializer(StarFieldsMixin, serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    is_ongoing = serializers.BooleanField(read_only=True)
    # Model memakai DateTimeField, tetapi form/halaman cukup mengirim tanggal (YYYY-MM-DD)
    started_at = serializers.DateTimeField(input_formats=["iso-8601", "%Y-%m-%d"])
    ended_at = serializers.DateTimeField(
        input_formats=["iso-8601", "%Y-%m-%d"], required=False, allow_null=True,
    )

    class Meta:
        model = Experience
        fields = [
            "id", "title", "category", "category_display", "description",
            "thumbnail", "started_at", "ended_at", "is_ongoing",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Judul pengalaman tidak boleh kosong atau hanya berisi tag HTML.")
        return value

    def validate_description(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Deskripsi tidak boleh kosong atau hanya berisi tag HTML.")
        return value

    def validate_thumbnail(self, value):
        # Model memakai null=True, jadi string kosong disimpan sebagai None
        return value or None

    def validate(self, attrs):
        started_at = attrs.get("started_at", getattr(self.instance, "started_at", None))
        ended_at = attrs.get("ended_at", getattr(self.instance, "ended_at", None))
        if started_at and ended_at and ended_at < started_at:
            raise serializers.ValidationError(
                {"ended_at": "Tanggal selesai tidak boleh sebelum tanggal mulai."}
            )
        return attrs
