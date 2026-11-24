from rest_framework.authentication import SessionAuthentication, TokenAuthentication


class ApiSessionAuthentication(SessionAuthentication):
    """Sesi untuk web, dengan tantangan token bagi klien yang mengirim Authorization.

    DRF memutuskan 401 atau 403 dari ``authenticate_header`` milik autentikator
    pertama. SessionAuthentication bawaan tidak punya header itu, sehingga token
    yang salah dijawab 403 dan klien mobile tidak tahu bahwa ia harus login ulang.
    Di sini header hanya diberikan bila klien memang mengirim Authorization,
    sehingga pengguna web yang belum login tetap menerima 403 seperti sebelumnya.
    """

    def authenticate_header(self, request):
        return "Token" if request.META.get("HTTP_AUTHORIZATION") else None


# Web memakai sesi (cookie + CSRF), klien mobile memakai token.
API_AUTHENTICATION = [ApiSessionAuthentication, TokenAuthentication]
