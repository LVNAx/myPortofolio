# Website Portofolio Pribadi
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)

`Nama: Nugraha Kautsarrizqi Caksana`
`Kelas: PBP-B`
`NPM: 2506541250`

Website portofolio pribadi yang dibangun menggunakan **Django (Python)**, **HTML**, dan **CSS**. Website ini terdiri dari beberapa section utama, yaitu About, Experience, dan Education.

## Fitur

- Section **About**
- Section **Experience** (dengan styling CSS custom)
- Section **Education**
- Ikon GitHub & LinkedIn menggunakan [Devicon](https://devicon.dev/)

## Tech Stack

- Python (Django)
- HTML5 & CSS3
- Devicon

## Instruksi Setup

1. Clone repository ini
   ```bash
   git clone [URL_REPO_ANDA]
   cd [nama-folder-proyek]
   ```

2. (Opsional, disarankan) Buat virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate      # untuk Mac/Linux
   venv\Scripts\activate         # untuk Windows
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Jalankan migrasi database
   ```bash
   python manage.py migrate
   ```

5. Jalankan development server
   ```bash
   python manage.py runserver
   ```

6. Buka browser dan akses `http://127.0.0.1:8000/`

# Tugas-1
## Progress Mingguan

| Hari / Tanggal | Progress |
|---|---|
| Selasa, 1 September | Menyelesaikan tutorial 1 dan memahami syntax yang diberikan; bagian yang belum familiar terus digali secara mandiri. |
| Rabu, 2 September | Mengikuti tutorial bersama asisten dosen, deep dive lebih lanjut terkait syntax dan istilah seperti *child*, *parent*, *inline*, dst. |
| Kamis, 3 September | Mencari referensi desain dari kakak tingkat (Kak Kevin, Kak Vincent, Kak Hakim). |
| Jumat, 4 September | Sudah memiliki gambaran desain yang ingin dibuat, namun memutuskan istirahat setelah kuliah. |
| Sabtu, 5 September | Menyelesaikan section Experience dan mengganti ikon GitHub & LinkedIn menggunakan Devicon. |
| Minggu, 6 September | Menambahkan section About dan Education. |

## Referensi

- [cornellius.dev](https://www.cornellius.dev/) --> referensi utama, khususnya untuk section Experience
- [Tutorial YouTube](https://www.youtube.com/watch?v=t5AE66WgQD0) --> referensi khusus untuk section Education
- [vinren.id](https://vinren.id/) --> referensi tambahan
- [hakimnizami.dev](https://hakimnizami.dev/) --> referensi tambahan

## AI Disclosure

Selama pengerjaan proyek ini, saya menggunakan Claude AI sebagai alat bantu belajar dan debugging:

- **[Chat 1-Model: Claude Sonnet-5 Medium](https://claude.ai/share/6ab852d3-616f-43c0-827b-87ff9f941c42)** yang digunakan untuk membantu menulis kode CSS pada section Experience. 
- **[Chat 2-Model: Claude Sonnet-5 Medium](https://claude.ai/share/38ad5efd-cb8e-459f-a989-0f88d101908b)** yang digunakan untuk berdiskusi mengenai maksud dari suatu syntax agar pemahaman saya jauh lebih mendalam, bukan sekadar copy-paste.
- **[Chat 3-Model: Claude Opus-5 High](https://claude.ai/share/b40b3597-574c-4d17-af71-14b73221fd57)** yang digunakan untuk membuat section `contact` untuk mengetahui jika AI yang full membuat akan bagaimana. Di sini saya juga mencoba menggunakan animejs.com dan juga formspree.com agar ia benar-benar akan terkirim ke dalam email saya.
- **[Chat 4-Model: Claude Sonnet-5 High](https://claude.ai/share/3343ab50-f83d-44b5-9ff0-3bb20246ba08)** digunakan untuk membuat hamburger stack karena navbar belum responsive untuk tampilan mobile

**Refleksi penggunaan AI:**
AI cukup membantu saya dalam memahami kode lebih lanjut, khususnya untuk mengecek syntax kode mana yang bermasalah beserta solusinya. Namun, kekurangannya terletak pada seberapa jelas konteks permasalahan yang diberikan, sesuai prinsip *garbage-in, garbage-out*, jadi seperti kalo kita memberi konteks yang kurang jelas, hasil yang diberikan AI juga kurang tepat. Selain itu juga, berdasarkan chat untuk section `contact`, saya temukan kalo tampilan dari website yang dibuat oleh AI itu akan selalu mirip (jika tidak menggunakan Skill-skill tertentu -> Informasi dari internet). Oleh karena itu, kita perlu menyesuaikan lagi keinginan kita seperti apa dan jangan sampai kita yang dikendalikan gitu.

## Permasalahan yang Ditemukan

Tantangan terbesar dalam proses ini adalah menentukan tata letak (layout) elemen-elemen pada halaman, yang melibatkan banyak trial and error. Ganti syntax (maupun style) serta juga reload dan `python manage.py runserver` menjadi makanan saya hampir setiap jam.

## Pertanyaan Reflektif Tugas-1

**1. Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti `section`, `article`, atau `aside`? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?**

Jawaban: Iya, saya menggunakan itu terutama untuk tag `section`, sedangkan `article` dan `aside` belum ada. Untuk `section` sendiri memudahkan saya untuk 'mempartisi' bagian-bagian yang ada dalam sebuah website sehingga saya bisa menerapkan style yang berbeda-beda dan yang saya inginkan di setiap section. Nah, jika tidak menurutku mungkin ada tag yang lebih cocok, misalnya di sini saya menemukan tag `details` dan juga `summary` yang saya gunakan di section `experience` di mana ia bisa menampilkan informasi intinya di depan dan untuk yang lebih lengkap bisa dengan diklik (untuk kasus saya seperti itu).

**2. Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?**

Jawaban: Ini lagi-lagi adalah bagaimana dalam menentukan tata letak yang sesuai dengan ukuran yang enak juga, jadi ambil contoh di section `education` yang mana tampilan antara di laptop dan juga hp itu perlu disesuaikan lagi dengan card sama arrownya menjadi rata kiri agar lebih nyaman untuk dilihat. Nah, lagi-lagi masalah yang seperti ini itu saya temukan di section `education` di mana intinya dari card yang sebelumnya ada 2 sisi, sekarang dijadikan sama rata dari kiri semua dan juga sejauh ini solusi yang diambil adalah dikecilkan / dicompactkan agar tetap nyaman dilihat.

Setelah mengikuti perkuliahan pada hari Senin, saya disarankan oleh teman saya untuk menggunakan Hamburger Stack terkait dengan navbar saya yang masih kurang responsive juga :D


**3. Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?**

Jawaban: Menurutku sendiri adalah ia kurang interaktif dengan user (jika dibandingkan dengan referensi yang saya temui) yang membuat ia kurang menarik dan membosankan, meskipun saya sudah menambahkan section `experience` yang bisa terbuka ke bawah dan ada garis yang melebar. Nah, terkait fungsionalitas dinamis ada beberapa (ada beberapa yang ngga feasible utk proyek selanjutnya):
- Kotak yang lebih rapi dan clean, di mana ia kayak ada outer line yang bagus juga,
- Background yang interaktif seperti milik Kak Kevin Cornellius,
- Font yang menurutku masih kurang menarik,
- Scroll down / up yang agak di-delay agar terkesan mewah gtu,
- Dan mungkin cursor yang keren juga :D

# Tugas-2
## Progress Mingguan

| Hari / Tanggal | Progress |
|---|---|
| Selasa, 8 September | Menyelesaikan Handson |
| Rabu, 9 September | Menyelesaikan Tutorial 2 |
| Kamis, 10 September | Memahami kembali kode-kode yang telah dibuat |
| Jumat, 11 September | Planning akan membuat sebuah entitias dengan attribute apa aja |
| Sabtu, 12 September | Menyelesaikan bagian Experience |
| Minggu, 13 September | Menyelesaikan bagian Projects dan juga Journey sambil Refactor besar-besaran agar kodenya jauh lebih rapi |
| Senin, 14 September | Refactor Experience, menyelesaikan Testing dan juga menambahkan README.md |


## AI Disclosure

Selama pengerjaan proyek ini, saya menggunakan Claude AI sebagai alat bantu belajar dan debugging:

- **[Chat 1-Model: Claude Sonnet-5 Medium](https://claude.ai/share/0c60b902-a2e2-40db-881a-af5cedc899ce)** yang digunakan untuk berdiskusi mengenai maksud dari kodenya bagaimana.
- **[Chat 2-Model: Claude Sonnet-5 Medium](https://claude.ai/share/87a42ee4-f14a-4bc0-b35f-7aeeada8cb31)** sama dengan chat-1, ia digunakan untuk berdiskusi mengenai maksud dari kode bagaimana.
- **[Chat 3-Model: Claude Sonnet-5 High](https://claude.ai/share/e6abf363-d3d3-4b14-931e-f2fdfdd538e7)** ini adalah chat utama dengan AI di mana digunakan untuk brainstorming (desain websitenya bagiamana dan ada minta beberapa kode dari nya).


## Petanyaan Reflektif Tugas-2
**1. Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran urls.py proyek, urls.py aplikasi, view, model, dan template.**

Jawaban: Di sini kita coba ambil kasus untuk path journey/.
Jadi, ketika user buka halaman Journey misalnya dengan klik 'Journey' yang ada pada navbar, browser akan mengirimkan ***request*** `GET /journey/` ke server Django. Nah, pertama-tama Django akan membaca `urls.py` milik portofolio (`portofolio/urls.py`) yang memiliki fungsi sebagai gerbang masuk seluruh URL. File ini ngga tau tentang halaman Journey karena tugasnya hanya membagi request ke Django Apps yang tepat. Karena URL tersebut cocok dengan `path('', include('main.urls'))`, sisa dari URL-nya akan diteruskan ke `main/urls.py` yang di mana di sana kan ada `path("journey/", show_journey, name="show_journey")`, sehingga Django memanggil fungsi view  `show_journey` (dari `views.py`). Nama rute inilah yang dipakai pada navbar.

Kemudian, view `show_journey` berperan sebagai penghubung antara model dan juga template. View meminta data kepada model melalui `JourneyStage.objects.prefetch_related("activities").all()`, lalu hasilnya dimasukkan ke dalam `context` dengan data profil, kemudian memanggil `render()` dengan template `journey.html`. Model `JourneyStage` dan `StageActivity` yang terhubung menggunakan **KeyAttribute** berupa ID, akan menerjemahkan kode Python menjadi query SQL ke database. Nah, lalu template `journey.html` menyusun HTML dengan meng-extend dari `base.html` agar bagian head, navbar, dan footer dari sini dan berlaku untuk semua halaman sedangkan `journey.html` hanya mengisi bagian kontennya. Seperti:
1. `{% for %}` untuk menampilkan setiap jenjang dan aktivitasnya,
2. `{% empty %}` menampilkan pesan ketika data masih kosong,
3. `{% static %}` menghasilkan alamat berkas CSS serta gambar.
Kemudian, hasil render dikirim kembali ke browser sebagai `HttpResponse` berisi HTML. Kemudian proses untuk folder statis hingga akhirnya halaman akan tampil dengan utuh di milik user.

**2. Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.**

Jawaban: Kebetulan di sini untuk Profile saya tetap melakukan hardcoded juga dan salah satu yang saya temukan setelah menggunakan model ini adalah `datanya lebih baik  dan lebih nyaman jika disimpan pada model agar ia hanya ada satu sumber data`. Sehingga, ketika kita ingin mengubahnya ia cukup dari Model aja. Selain itu juga, dari sisi penggembangan, data pada model lebih mudah dites dan dipakai lagi. Untuk unit test pula, kita dapat membuat data percobaan lalu memeriksa apakah data tersebut tampil, ataupun menghapusnya untuk memeriksa pesan ketika datanya kosong --> ini tidak bisa dilakukan jika ia hardcoded di html nya langsung.

Kemudian yang terakhir, di admin/ kita juga bisa mengurutkan, memfilter, atau menampilkan datanya ke halaman lain **tanpa ditulis ulang**.

**3. Apa perbedaan fungsi `makemigrations` dan `migrate` pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.**

Jawaban: Selama tugas 2 ini, saya sadar kalo perbedaan antara keduanya adalah `makemigrations` adalah tahap 'membuat rencana', sedangkan `migrate` adalah tahap 'mengeksekusinya'. `makemigrations` akan membandingkan isi `models.py` dengan migrasi sebelumnya, lalu menuliskan perubahannya ke berkas migrasi baru yang ada di folder `migrations/`, *tanpa mengubah database kita sama sekali*. Berkas inilah yang akan dimasukkan ke github juga agar semua orang dan server memiliki rencana perubahan yang sama. `migrate` kemudian membaca rencana yang belum dijalankan, lalu **benar-benar menerapkannya ke database**, seperti membuat tabel atau menambah kolom.

Contohnya pada proyek ini, ketika saya menambahkan model `JourneyStage` dan `StageActivity`, `makemigrations` menghasilkan berkas `0005_journeystage_stageactivity.py`, lalu `migrate` membuat tabel `journeystage` dan `stageactivity` di database. Nah, Kedua perintah ini hanya diperlukan jika struktur tabel-nya berubah menambah `@property` seperti `tag_list` ngga memerlukan migrasi karena ngga ada kolom yang berubah.

# Tugas-3
## Progress Mingguan
| Hari / Tanggal | Progress |
|---|---|
| Senin, 14 September | Menyelesaikan Tutorial-3 dan Memahami kode dan juga alur untuk membuat form-nya bagaimana |
| Selasa, 15 September | - |
| Rabu, 16 September | - |
| Kamis, 17 September | - |
| Jumat, 18 September | - |
| Sabtu, 19 September | Mereview kembali Tutorial-3 kita sudah belajar apa aja dan menyusun rencana untuk Tugas-3 |
| Minggu, 20 September | Menyelesaikan experience dengan menambahkan form (Create dan Delete) dan juga filter Experience |
| Senin, 21 September | Memperbaiki dan juga merapikan apa yang masih bermasalah (Menambahkan Edit dan Thumbnail utk Experience) |

## AI Disclosure
> Untuk Tugas-3 ini, saya masih bisa banyak banget yang bisa diimprove lagi dan sangat banyak mengikuti Tutorial-3 dengan menambahkan filter pada Experience. 
- **[Chat 1-Model: Claude Sonnet-5 High](https://claude.ai/share/8b57bbb1-f26c-442d-9f5d-52ec80a5dd40)** digunakan untuk memahami kode, mengimprove kode, dan juga memperbaiki beberapa error

## Pertanyaan Reflektif Tugas-3
1. Jelaskan mengapa kita menggunakan ModelForm pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan {% csrf_token %} pada form tersebut!
Jawaban: 

2. Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?
Jawaban:

3. Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?
Jawaban: 