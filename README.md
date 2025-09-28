Link Toko Sofita : https://ahsan-parvez-tokosofita.pbp.cs.ui.ac.id/

## **Penjelasan Checklist**
**Checklist 1**
- > Start yang dimana dilakukan dengan langkah meenyiapkan hal hal yang dibutuhkan seperti env dengan menstup env kemudian melakukan setup di settings.py dan juga mencoba me run server django
1. Persiapan Proyek Django
    1. Buat direktori baru untuk proyek: 
        buat direktori baru dengan nama Toko Sofita
    2. Buka terminal di dalam VSCode kemudian jalankan Command
        python -m venv env
        env\Scripts\activate
    3. Buat file requirements.txt berisi dependency utama yang berisi:
        django
        gunicorn
        whitenoise
        psycopg2-binary
        requests
        urllib3
        python-dotenv
    4. Lalu install dengan cara (jika belum)
        pip install -r requirements.txt
    

2. Setup Proyek Django
    1. Buat proyek Django:
        django-admin startproject toko_sofita .
    2. Buat file .env (development):
        PRODUCTION=False
       Buat juga file .env.prod:
        DB_NAME=<nama database>
        DB_HOST=<host database>
        DB_PORT=<port database>
        DB_USER=<username database>
        DB_PASSWORD=<password database>
        SCHEMA=tugas_individu
        PRODUCTION=True
    3. Edit settings.py:
        Tambahkan:
            import os
            from dotenv import load_dotenv
            load_dotenv()
       Set ALLOWED_HOSTS awalnya ke:
        ALLOWED_HOSTS = ["localhost", "127.0.0.1"] // awal awal
       Tambahkan flag production:
        PRODUCTION = os.getenv('PRODUCTION', 'False').lower() == 'true'

3. Jalankan Server Lokal
    1. Migrasi database:
        python manage.py migrate
    2. Jalankan server:
        python manage.py runserver
        Pastikan django berjalan normal sebelum lanjut ke github atau PWS

4. Setup Github
    1. Inisialisasi Git:
        git init
    2. Tambahkan .gitignore (untuk menghindari commit file sensitif/env/db).
    3. Hubungkan ke repository GitHub:
        git remote add origin https://github.com/ahsanparvezz/toko-sofita.git
        git branch -M master
    4. Commit dan push
        git add .
        git commit -m "Commit awal untuk django"
        git push origin master

5. Deploy ke PWS
    1. Buat project baru di PWS → simpan username/password credential.
    2. Update ALLOWED_HOSTS di settings.py:
        ALLOWED_HOSTS = ["localhost", "127.0.0.1", "ahsan-parvez-tokosofita.pbp.cs.ui.ac.id"]
    3. Hubungkan repo ke PWS:
        git remote add pws https://pbp.cs.ui.ac.id/ahsan.parvez/tokosofita
        git branch -M master
        git push pws master
        → Saat push, masukkan username/password PWS.

**Checklist 2**
- > membuat main dengan python manage.py startapp main lalu menambahkannya kedalam installed apps dan menambahkan folder templates untuk menyimpan file html
6. Membuat Aplikasi main
    1. Buat app baru:
        python manage.py startapp main
    2. Tambahkan 'main' ke INSTALLED_APPS di settings.py.
    3. Buat folder templates dalam app main untuk menyimpan file HTML.

**Checklist 3**
- > Routing URL untuk aplikasi main
7. Routing
    1. Routing utama (urls.py di toko_sofita):
        from django.urls import path, include

        urlpatterns = [
            path('', include('main.urls')),
        ]

**Checklist 4**
- > membuat model yang diperlukan di models.py dengan menambahkan atribut wajib dan juga atribut tambahan
8. Di models.py app main:
    class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=100)
    is_featured = models.BooleanField(default=False)
    stock = models.IntegerField(default=0)
    rating = models.FloatField(null=True, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

**Checklist 5**
- > membuat funciton untuk digunakan ke template main html yang berisi nama app, nama, dan kelas
9. Views (views.py):
        from django.shortcuts import render
        def show_main(request):
            context = {
                'app_name': 'Toko Sofita',
                'name': 'Ahsan Parvez',
                'class': 'PBP E',
            }
            return render(request, "main.html", context)

**Checklist 6**
- > mengatur routing url pada proyek di folder main
10. URLs app (urls.py di folder main):
    from django.urls import path
    from main.views import show_main

    app_name = 'main'

    urlpatterns = [
        path('', show_main, name='show_main'),
    ]

**Checklist 7**
- > melakukan deployment ke pws
11. Deployment
    git add .
    git commit -m "Add main app with Product model and routing"
    git push origin master
    git push pws master

## **Link Bagan**
https://drive.google.com/file/d/1TS_KleMlmTl0XTZwwVW1RCUE4QC2tyK5/view?usp=sharing

## **Peran settings.py pada Django**
settings.py itu bisa dibilang pusat konfigurasi dari proyek Django. Semua pengaturan penting ada di sana, mulai dari database yang dipakai, daftar aplikasi yang aktif, konfigurasi keamanan (kayak secret key, debug mode, allowed hosts), sampai pengaturan static file dan template. Jadi, kalau kita mau ngubah perilaku proyek Django, biasanya yang pertama kali diutak-atik ya file settings.py ini.

## **Cara kerja migrasi database di Django**
Migrasi di Django itu intinya cara buat nyamain struktur database dengan model yang kita definisikan di kode.

Prosesnya:

Waktu kita bikin atau ubah model di models.py, Django belum otomatis ubah database.

Kita jalankan python manage.py makemigrations, Django akan bikin file migrasi yang isinya instruksi perubahan (misalnya bikin tabel baru, nambah kolom, atau hapus kolom).

Lalu pakai python manage.py migrate, instruksi itu dijalankan ke database, jadi database bener-bener punya struktur yang sama kayak model di kode.

Jadi singkatnya: makemigrations = bikin rencana, migrate = eksekusi rencana ke database.

## **Kenapa Django?**
Menurut saya, Django dipilih menjadi permulaan adalah karena Django udah kayak pake all in one hampir komplit dan ramah buat pemula. Dibangun diatas python yang notabennya mudah dimengerti. Dokumentasinya juga lengkap, komunitasnya besar dan banyak dipakai di industri. Jadi cukup relevan juga di praktik real world

## **Feedback**
Untuk feedback dari saya, tutorialnya sudah cukup bagus, lengkap dan mudah dimengerti. Mungkin tambahan dari saya, tambahkan saran aktivasi auto save karena saya dan teman2 saya lebih dari sekali error karena autosave tidak on.


## Tugas 3
1.  Jelaskan mengapa kita memerlukan data delivery dalam pengimplementasian sebuah platform?
    Karena kita memerlukan data delivery agar data yang ada di platform bisa disajikan ke pengguna atau sistem lain secara aman, tepat waktu, dan dalam format yang sesuai, sehingga data bisa benar-benar dimanfaatkan untuk keputusan, integrasi, dan pengalaman pengguna.

2. Menurutmu, mana yang lebih baik antara XML dan JSON? Mengapa JSON lebih populer dibandingkan XML?
    JSON lebih populer dibandingkan XML karena lebih ringan, mudah dibaca, cepat diproses, dan langsung cocok dengan web/API modern. Sedangkan XML lebih berat karena banyak tag dan biasanya dipakai di sistem lama atau dokumen kompleks.

3.  Jelaskan fungsi dari method is_valid() pada form Django dan mengapa kita membutuhkan method tersebut?
    is_valid() pada form Django berfungsi untuk memeriksa apakah data input sudah sesuai aturan validasi. Kita membutuhkannya agar hanya data yang benar dan bersih yang diproses atau disimpan ke database.

4. Mengapa kita membutuhkan csrf_token saat membuat form di Django? Apa yang dapat terjadi jika kita tidak menambahkan csrf_token pada form     Django? Bagaimana hal tersebut dapat dimanfaatkan oleh penyerang?
    csrf_token dibutuhkan di Django untuk melindungi form dari serangan Cross-Site Request Forgery (CSRF), csrf_token dibutuhkan untuk mencegah serangan CSRF. Tanpa token, penyerang bisa memalsukan form agar user melakukan aksi berbahaya tanpa disadari. Token ini memastikan bahwa request yang dikirim benar-benar berasal dari user yang sah, bukan dari pihak luar.

    Jika tidak ditambahkan, penyerang bisa membuat form palsu di luar aplikasi lalu memancing user yang sedang login untuk mengirim request berbahaya, misalnya mengubah data, mengganti password, atau melakukan transaksi tanpa sepengetahuan user. Dengan adanya csrf_token, request palsu tersebut akan ditolak karena tidak memiliki token yang valid.

5. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).
    **Checklist 1**
    Tambahkan 4 fungsi views baru untuk melihat objek yang sudah ditambahkan dalam format XML, JSON, XML by ID, dan JSON by ID.

    Membuka views.py pada app main.

    Menambahkan import yang dibutuhkan (HttpResponse, serializers, dan model Product).

    Membuat fungsi baru:

    show_xml → menampilkan semua data dalam format XML.

    show_json → menampilkan semua data dalam format JSON.

    show_xml_by_id → menampilkan data berdasarkan ID dalam format XML.

    show_json_by_id → menampilkan data berdasarkan ID dalam format JSON.

    **Checklist 2**
    Membuat routing URL untuk masing-masing views yang telah ditambahkan pada poin 1.

    Membuka urls.py pada app main.

    Menambahkan path untuk:

    /xml/ → menuju fungsi show_xml.

    /json/ → menuju fungsi show_json.

    /xml/<int:id>/ → menuju fungsi show_xml_by_id.

    /json/<int:id>/ → menuju fungsi show_json_by_id.

    **Checklist 3**
    Membuat halaman yang menampilkan data objek model.

    Halaman daftar produk (main.html) menampilkan semua data produk.

    Terdapat tombol "Add" untuk redirect ke halaman form input produk.

    Terdapat tombol "Detail" di setiap produk untuk membuka halaman detail produk.

    **Checklist 4**
    Membuat halaman form untuk menambahkan objek model.

    File yang digunakan: create_product.html.

    Form ini terhubung dengan forms.py dan fungsi create_product pada views.py.

    Tombol Add di main.html akan mengarahkan ke halaman create_product.html.

    **Checklist 5**
    Membuat halaman yang menampilkan detail dari setiap data objek model.

    File yang digunakan: product_detail.html.

    Halaman ini menampilkan detail lengkap dari satu produk.

    Tombol Detail di main.html mengarahkan ke halaman product_detail.html berdasarkan ID produk.


6. Apakah ada feedback untuk asdos di tutorial 2 yang sudah kalian kerjakan?
    Untuk tutorial 2 sudah cukup baik, tapi saya lihat lihat masih belum ada reminder untuk menyalakan auto save atau men save file tiap 5 menit misalnnya, mungkin itu saja.

7. Mengakses keempat URL di poin 2 menggunakan Postman, membuat screenshot dari hasil akses URL pada Postman, dan menambahkannya ke dalam README.md.
###  Data XML
![XML All](images/1.png)

###  Data JSON
![JSON All](images/2Json.png)

### XML by ID
![XML by ID](images/3XML.png)

### JSON by ID
![JSON by ID](images/4Json.png)


## Tugas 4
1. Apa itu Django AuthenticationForm? Jelaskan juga kelebihan dan kekurangannya.
    Authenticastion form di Django adalah form bawaan yang dipakai untuk proses login user. Form ini otomatis menangani validasi username dan password, kemudian memeriksa kredensialnya terhadap database pengguna yang terdaftar. Jadi, alih alih kita harus membuat form login dari nol, Django sudah menyiapkan tools yang siap untuk dipakai
    
    Kelebihan utamanya adalah kemudahan dan keamanan. Kita bisa menggunakannya dengan cepat, sudah mencakupi validasi dasar dan keamanananya yang cukup baik. Namun kekurangnnya terletak pada kekakuannya, form ini sangat dasar dan tidak fleksibel jika mau menambahkan field lain seperti login dengan email atau mau ubah tampilannya.

2. Apa perbedaan antara autentikasi dan otorisasi? Bagaiamana Django mengimplementasikan kedua konsep tersebut?
    Perbedaan antara autentikasi dan otorisasi terletak pada tujuannya. Autentikasi adalah proses untuk memverifikasi identitas pengguna, atau menjawab pertanyaan "Siapa kamu?", dengan memastikan kredensial seperti username dan password sesuai dengan data yang tersimpan. Sedangkan, otorisasi terjadi setelah pengguna berhasil terautentikasi dan bertujuan untuk menentukan hak akses atau tindakan apa yang diizinkan untuk pengguna tersebut, menjawab pertanyaan "Apa yang boleh kamu lakukan?".

    Django mengimplementasikan autentikasi melalui modul django.contrib.auth yang menyediakan sistem untuk mengelola user, group, dan izin. Untuk otorisasi, Django menggunakan mekanisme permissions yang dapat ditetapkan pada level user atau group, serta decorator seperti @login_required dan @permission_required yang memungkinkan developer membatasi akses ke view berdasarkan status login atau hak akses spesifik pengguna.


3. Apa saja kelebihan dan kekurangan session dan cookies dalam konteks menyimpan state di aplikasi web?
    Cookies dan session sama-sama digunakan untuk menyimpan state di aplikasi web, namun punya kelebihan dan kekurangan masing-masing. Cookies disimpan di browser pengguna sehingga ringan bagi server dan mudah digunakan untuk menyimpan data sederhana, tetapi kurang aman karena bisa dilihat atau dimodifikasi oleh user jika tidak dienkripsi. Sementara itu, session disimpan di server dan hanya menyimpan ID session di browser, sehingga lebih aman untuk data sensitif dan sulit dimanipulasi langsung oleh user, namun membebani server karena perlu menyimpan data setiap user yang aktif.

4. Apakah penggunaan cookies aman secara default dalam pengembangan web, atau apakah ada risiko potensial yang harus diwaspadai? Bagaimana Django menangani hal tersebut?
    Penggunaan cookies tidak aman secara default karena data yang disimpan di sisi klien rentan terhadap serangan seperti pencurian data atau pemalsuan (cross-site scripting). Risiko utama termasuk pencurian informasi sensitif dan session hijacking dimana penyerang dapat menyamar sebagai pengguna yang sah. Django sendiri sudah menyediakan mekanisme untuk meminimalkan risiko ini, misalnya dengan opsi HttpOnly agar cookie tidak bisa diakses lewat JavaScript, Secure agar hanya terkirim lewat HTTPS, serta CSRF token untuk mencegah serangan cross-site request forgery. Jadi, cookies bisa relatif aman digunakan asalkan dikonfigurasi dengan benar sesuai praktik keamanan yang disarankan.

5. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial).
    **Checklist 1**
    Di views.py, import modul yang diperlukan
    Buat fungsi register yang menangani pembuatan akun baru dengan UserCreationForm. Simpan user dan login otomatis setelah registrasi.
    Buat fungsi login_user untuk autentikasi dengan authenticate() dan login().
    Buat fungsi logout_user untuk logout menggunakan logout().
    Di main.html, tambahkan tombol kondisional untuk me logout login dan juga register
    Kemudian tambahkan path yang dibutuhkan di urls.py

    **Checklist 2**
    Meregister 2 akun dummy dan membuat 3 product masing masing

    **Checklist 3**
    Di models.py, tambahkan user di class models jalankan makemigrations dan migrate kemudian modifikasi di views.py sehingga bisa membedakan show product all dan show product per user dan juga Di views.py, modifikasi fungsi create_product dengan dengan untuk product per usernya menggunakan form.is_valid()
    lalu tambahkan di main.html button all product dan button untuk product sendiri

    **Checklist 4**
    Di show_main, tambahkan context:
    'username': request.user.username,
    'last_login': request.COOKIES.get('last_login', 'Not available')
    kemudian meng set cookie di views.py dengan menggunakan .set_cookie()

## Tugas 5
1. Jika terdapat beberapa CSS selector untuk suatu elemen HTML, jelaskan urutan prioritas pengambilan CSS selector tersebut!
    Dalam penerapan CSS, urutan prioritas pengambilan style untuk suatu elemen HTML ditentukan oleh tingkat spesifisitas (specificity) yang dihitung berdasarkan jenis selektornya, di mana aturan yang memiliki spesifisitas lebih tinggi akan selalu mengalahkan aturan dengan spesifisitas lebih rendah, dengan urutan kekuatan dari yang terkuat yaitu deklarasi !important, diikuti oleh inline style yang ditulis langsung pada elemen, kemudian ID selector, lalu class selector, attribute selector, dan pseudo-class, serta yang terlemah adalah element selector dan pseudo-element; namun jika beberapa selector memiliki tingkat spesifisitas yang persis sama, maka aturan yang dideklarasikan terakhir dalam stylesheet-lah yang akan diterapkan.

2. Mengapa responsive design menjadi konsep yang penting dalam pengembangan aplikasi web? Berikan contoh aplikasi yang sudah dan belum menerapkan responsive design, serta jelaskan mengapa!
    Responsive design penting dalam pengembangan aplikasi web karena memungkinkan tampilan menyesuaikan diri secara otomatis dengan berbagai ukuran layar, mulai dari desktop, tablet, hingga smartphone, sehingga pengalaman pengguna tetap nyaman tanpa harus melakukan zoom in atau scroll berlebihan. Contoh aplikasi yang sudah menerapkan responsive design adalah Tokopedia, di mana layout, menu, dan gambar menyesuaikan ukuran layar sehingga tetap mudah diakses di perangkat apapun. Sebaliknya, beberapa website lama instansi pemerintahan sering kali belum menerapkan responsive design, sehingga ketika dibuka di smartphone tampilannya mengecil, teks sulit dibaca, dan navigasi jadi kurang praktis. Hal ini menunjukkan bahwa tanpa responsive design, aksesibilitas dan kenyamanan pengguna akan sangat berkurang.

3. Jelaskan perbedaan antara margin, border, dan padding, serta cara untuk mengimplementasikan ketiga hal tersebut!
    Margin, border, dan padding adalah tiga properti CSS yang mengatur box model dari sebuah elemen, di mana padding adalah ruang transparan di antara konten elemen dan batasnya (border), berfungsi untuk memberi jarak di dalam elemen, sementara border sendiri adalah garis dekoratif yang mengelilingi padding dan konten, sedangkan margin adalah ruang transparan di luar border yang berfungsi untuk membuat jarak antara elemen tersebut dengan elemen-elemen di sekitarnya, untuk mengimplementasikannya, ketiganya dapat didefinisikan dalam deklarasi CSS menggunakan properti seperti padding: 20px; untuk memberi jarak dalam, border: 2px solid black; untuk membuat garis batas berwarna hitam, dan margin: 10px; untuk memberi jarak luar.

4. Jelaskan konsep flex box dan grid layout beserta kegunaannya!
    Flexbox dan Grid Layout adalah dua sistem tata letak modern dalam CSS yang digunakan untuk mengatur posisi elemen secara lebih fleksibel dan efisien. Flexbox berfokus pada pengaturan elemen dalam satu dimensi, baik horizontal (row) maupun vertikal (column), sehingga cocok digunakan untuk menyusun navigasi, tombol, atau elemen yang berjajar rapi dalam satu baris atau kolom. Sementara itu, Grid Layout bekerja dalam dua dimensi (baris dan kolom) sekaligus, sehingga lebih cocok untuk membuat struktur halaman yang kompleks seperti dashboard atau layout majalah online. Contoh penerapan Flexbox adalah display: flex; justify-content: center; align-items: center; untuk merapikan elemen di tengah, sedangkan Grid dapat diterapkan dengan display: grid; grid-template-columns: repeat(3, 1fr); untuk membuat tiga kolom yang seimbang. Kedua konsep ini membantu developer mengatur desain web agar lebih responsif, terstruktur, dan mudah disesuaikan dengan berbagai perangkat.

5. Jelaskan bagaimana cara kamu mengimplementasikan checklist di atas secara step-by-step (bukan hanya sekadar mengikuti tutorial)!
**Checklist 1**
Implementasikan fungsi untuk menghapus dan mengedit product.
    Tambahkan script untuk Tailwind CSS di file base.html agar memudahkan kustomisasi

    Buat fungsi edit_product dan delete_product di views.py.

    Tambahkan file baru edit_product.html untuk form edit product.

    Daftarkan URL untuk edit_product dan delete_product di urls.py.

    Ubah card_product.html agar setiap card product menampilkan button Edit dan Delete.

**Checklist 2**
Kustomisasi halaman login, register, tambah product, edit product, dan detail product semenarik mungkin.
    Halaman login, register, tambah product, edit product, dan detail product

    Login: ubah login.html agar tampilan sesuai dengan yang diinginkan

    Register: ubah register.html dengan styling serupa login agar konsisten.

    Tambah product dan Edit product: gunakan desain form card di card_product.

    Detail product: lakukan styling di product_detail.html agar informasi lebih rapi.

**Checklist 3**
Kustomisasi halaman daftar product menjadi lebih menarik dan responsive. Kemudian, perhatikan kondisi berikut:
    Jika pada aplikasi belum ada product yang tersimpan, halaman daftar product akan menampilkan gambar dan pesan bahwa belum ada product yang terdaftar.
    Jika sudah ada product yang tersimpan, halaman daftar product akan menampilkan detail setiap product dengan menggunakan card (tidak boleh sama persis dengan desain pada Tutorial!).
        Pertama menyiapkan gambar atau logo yang ingin ditampilkan jika product tidak ada, kemudian menambahkan di kondisi jika tidak ada product maka akan menampilkan itu di card_product.html, kemudian mendesain card_product sesuai dengan apa yang diinginkan

**Checklist 4**
Untuk setiap card product, buatlah dua buah button untuk mengedit dan menghapus product pada card tersebut!
    Setiap card product menampilkan dua button:

    Edit → menuju halaman edit_product.html.

    Delete → menghapus product langsung dari card.

**Checklist 5**
Buatlah navigation bar (navbar) untuk fitur-fitur pada aplikasi yang responsive terhadap perbedaan ukuran device, khususnya mobile dan desktop.
    Buat file baru navbar.html di folder templates.

    Tautkan navbar.html ke main.html agar tampil di setiap halaman.

    Styling navbar dengan Tailwind agar responsive di desktop maupun mobile.

