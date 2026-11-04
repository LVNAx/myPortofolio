from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrReadOnly(BasePermission):
    """Semua pengunjung boleh membaca; hanya pemilik (superuser) yang boleh mengubah."""

    message = "Hanya pemilik portofolio yang dapat mengubah proyek."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_superuser
        )


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """Seperti di atas, tetapi grup Editor juga boleh PUT/PATCH (tidak boleh create/delete)."""

    message = "Kamu tidak memiliki izin untuk melakukan tindakan ini."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return (
            request.method in ("PUT", "PATCH")
            and request.user.groups.filter(name="Editor").exists()
        )
