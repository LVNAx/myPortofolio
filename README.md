# Website Portofolio Pribadi

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

## Pertanyaan Reflektif

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
