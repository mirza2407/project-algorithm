import psycopg2
from psycopg2 import Error
from datetime import datetime
import os
from tabulate import tabulate 

# Tahap Inisialisasi Variabel: Mengimpor modul yang diperlukan untuk koneksi database, tanggal, sistem operasi, dan tabel data.

def connect_database():
    # Tahap Proses dan Logika: Mencoba membuat koneksi ke database PostgreSQL dengan parameter yang ditentukan.
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='gymtio2402',
            host='127.0.0.1',
            port='5432',
            database='Project Akhir smstr 1'
        )
        # Tahap Output: Mengembalikan objek koneksi jika berhasil; jika gagal, cetak error dan return None.
        return connection
    except (Exception, Error) as error:
        print("error")
        return None

def menu_utama():
    # Tahap Inisialisasi Variabel: Menginisialisasi koneksi database dan cursor untuk query SQL.
    conn = connect_database()
    if not conn:
        return

    cursor = conn.cursor()

    # Tahap Perulangan: Loop utama untuk menampilkan menu hingga user keluar atau login berhasil.
    while True:
        os.system('cls')  # Membersihkan layar sebelum output menu.
        print("""
              

░██       ░██ ░██████████ ░██           ░██████    ░██████   ░███     ░███ ░██████████    ░██████████  ░██████        ░██████   ░██████░█████████  ░██████░██████████
░██       ░██ ░██         ░██          ░██   ░██  ░██   ░██  ░████   ░████ ░██                ░██     ░██   ░██      ░██   ░██    ░██  ░██     ░██   ░██      ░██    
░██  ░██  ░██ ░██         ░██         ░██        ░██     ░██ ░██░██ ░██░██ ░██                ░██    ░██     ░██    ░██           ░██  ░██     ░██   ░██      ░██    
░██ ░████ ░██ ░█████████  ░██         ░██        ░██     ░██ ░██ ░████ ░██ ░█████████         ░██    ░██     ░██     ░████████    ░██  ░█████████    ░██      ░██    
░██░██ ░██░██ ░██         ░██         ░██        ░██     ░██ ░██  ░██  ░██ ░██                ░██    ░██     ░██            ░██   ░██  ░██           ░██      ░██    
░████   ░████ ░██         ░██          ░██   ░██  ░██   ░██  ░██       ░██ ░██                ░██     ░██   ░██      ░██   ░██    ░██  ░██           ░██      ░██    
░███     ░███ ░██████████ ░██████████   ░██████    ░██████   ░██       ░██ ░██████████        ░██      ░██████        ░██████   ░██████░██         ░██████    ░██    
        """)
        print("\n=== Menu Login ===")
        print("1. Buat Akun Baru (Register Pelanggan)")
        print("2. Login")
        print("3. Keluar")
        # Tahap Pengambilan Input: Mengambil pilihan menu dari user.
        pilihan = input("Pilih opsi (1/2/3): ")

        # Tahap Perkondisian: Memeriksa pilihan user dan menjalankan aksi sesuai (registrasi, login, atau keluar).
        if pilihan == '1':
            if registrasi_pengguna(cursor):
                conn.commit()  # Tahap Proses dan Logika: Menyimpan perubahan registrasi ke database.
        elif pilihan == '2':
            result = login_pengguna(cursor)
            if result:
                id_pengguna, role = result  
                # Tahap Proses dan Logika: Jika login berhasil, break loop untuk masuk ke menu role.
                break
        elif pilihan == '3':
            # Tahap Output: Menampilkan pesan keluar dan menghentikan program.
            print("Keluar dari program.")
            break   
        else:
            # Tahap Output: Menampilkan pesan error jika pilihan invalid.
            print("Pilihan tidak valid!")

def registrasi_pengguna(cursor):
    # Tahap Perulangan: Loop untuk input ulang jika validasi gagal.
    while True:
        # Tahap Pengambilan Input: Mengambil data registrasi dari user.
        username = input("Buat username yang di inginkan: ")
        password = input("Buat password: ")
        email = input("Masukkan email anda: ")
        no_telpon = input("Masukkan nomor anda: ")
        nama = input("Nama lengkapmu: ")

        # Tahap Perkondisian: Memeriksa validasi input (field kosong, panjang password, username unik).
        if not nama or not username or not email or not no_telpon or not password:
            # Tahap Output: Menampilkan pesan error jika field kosong.
            print("Semua field harus diisi!")
            continue
        if len(password) < 8:
            # Tahap Output: Menampilkan pesan error jika password terlalu pendek.
            print("Password minimal 8 karakter!")
            continue

        # Tahap Proses dan Logika: Mengecek username unik di database.
        cursor.execute("SELECT id_pengguna FROM pengguna WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            # Tahap Output: Menampilkan pesan error jika username sudah ada.
            print("Username anda sudah tesedia.")
            continue
    
        print("\n=== Input Alamat ===")
        
        # Tahap Pengambilan Input: Mengambil input alamat dengan query database untuk opsi kabupaten/kecamatan/desa.
        cursor.execute("SELECT id_kabupaten, nama_kabupaten FROM kabupaten ORDER BY nama_kabupaten")
        kabupaten_list = cursor.fetchall()
        print("\nPilih Kabupaten:")
        for kab in kabupaten_list:
            print(f"{kab[0]}. {kab[1]}")
        kabupaten_id = input("Pilih ID Kabupaten: ")

        cursor.execute("SELECT id_kecamatan, nama_kecamatan FROM kecamatan WHERE kabupaten_id = %s ORDER BY nama_kecamatan", (kabupaten_id,))
        kecamatan_list = cursor.fetchall()
        if not kecamatan_list:
            # Tahap Output: Menampilkan pesan error jika tidak ada kecamatan.
            print("Tidak ada kecamatan di kabupaten ini!")
            continue
        print("\nPilih Kecamatan:")
        for kec in kecamatan_list:
            print(f"{kec[0]}. {kec[1]}")
        kecamatan_id = input("Pilih ID Kecamatan: ")

        cursor.execute("SELECT id_desa, nama_desa FROM desa WHERE kecamatan_id = %s ORDER BY nama_desa", (kecamatan_id,))
        desa_list = cursor.fetchall()
        if not desa_list:
            # Tahap Output: Menampilkan pesan error jika tidak ada desa.
            print("Tidak ada desa di kecamatan ini!")
            continue
        print("\nPilih Desa:")
        for ds in desa_list:
            print(f"{ds[0]}. {ds[1]}")
        desa_id = input("Pilih ID Desa: ")

        nama_jalan = input("Masukkan nama jalan & nomor rumah: ")
        rt_rw = input("Masukkan RT/RW (contoh: 02/05): ")
        kode_pos = input("Masukkan kode pos: ")
        catatan_alamat = input("Catatan alamat (opsional): ")

        # Tahap Proses dan Logika: Insert data alamat dan pengguna ke database, lalu commit.
        cursor.execute("""
            INSERT INTO alamat (nama_jalan, rt_rw, desa_id, kode_pos, catatan_alamat)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_alamat
        """, (nama_jalan, rt_rw, desa_id, kode_pos, catatan_alamat))
        alamat_id = cursor.fetchone()[0]
        
        created_at = datetime.now()
        cursor.execute("INSERT INTO pengguna (username, password, email, no_telpon, nama, alamat_id, user_role_id_role) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_pengguna", 
                    (username, password, email, no_telpon, nama, alamat_id, 4))
        id_pengguna = cursor.fetchone()[0]

        cursor.execute("INSERT INTO keranjang (pengguna_id_pengguna) VALUES (%s)", (id_pengguna,))

        cursor.connection.commit()

        # Tahap Output: Menampilkan pesan sukses registrasi.
        print("\n Akun Anda berhasil dibuat!")
        print(f"Username: {username}")
        print(f"Silakan login untuk melanjutkan.")
        input("\nTekan Enter untuk kembali ke menu...")
        # Tahap Proses dan Logika: Break loop jika registrasi berhasil.
        break

    return True

def login_pengguna(cursor):
    # Tahap Perulangan: Loop untuk input ulang jika login gagal.
    while True:
        # Tahap Pengambilan Input: Mengambil username dan password dari user.
        username = input("masukkan Username Anda: ")
        password = input("Masukkan password anda: ")

        # Tahap Proses dan Logika: Mengeksekusi query untuk validasi login dengan JOIN ke user_role.
        cursor.execute("""SELECT p.id_pengguna, ur.nama_role 
            FROM pengguna p 
            JOIN user_role ur ON p.user_role_id_role = ur.id_role 
            WHERE p.username = %s AND p.password = %s
        """, (username, password))
        pengguna = cursor.fetchone()
        # Tahap Perkondisian: Memeriksa apakah login berhasil.
        if not pengguna:
            # Tahap Output: Menampilkan pesan error jika username/password salah.
            print("Username atau password anda salah!")
            continue
        
        id_pengguna, role = pengguna

        # Tahap Output: Menampilkan pesan sukses login.
        print(f"Login berhasil!, Selamat dattang, {username}. Sebagai {role}")
        input("enter untuk melanjutkan...")
        # Tahap Perkondisian: Menentukan menu berdasarkan role user (Pelanggan, Admin, Teknisi, CEO).
        if role == 'Pelanggan':
            menu_pelanggan(cursor, id_pengguna, role)
        elif role == 'Admin':   
            fitur_admin(cursor,id_pengguna, role)
        elif role == 'Teknisi':
            fitur_teknisi(cursor, id_pengguna, role)
        elif role == 'Ceo':
            fitur_ceo(cursor,id_pengguna, role)
        else:
            # Tahap Output: Menampilkan pesan error jika role tidak dikenali.
            print("Role tidak dikenali!")
            continue
        
        # Tahap Proses dan Logika: Return None untuk menghentikan loop setelah login berhasil.
        return None 



def menu_pelanggan(cursor, id_pengguna, role):
    # Tahap Perulangan: Loop utama untuk menampilkan menu pelanggan hingga user logout.
    while True:
        os.system('cls')  # Tahap Proses dan Logika: Membersihkan layar sebelum output menu.
        print("=================================")
        print(f"n\=== menu pelanggan {id_pengguna} ===")
        print("=================================")
        print("1. Menu Ikan")
        print("2. Menu Keranjang")
        print("3. Transaksi")
        print("4. Melihat Bukti Pembayaran")
        print("5. Melihat Status Pengiriman")
        print("6. Menu profil")
        print("7. Logout")
        # Tahap Pengambilan Input: Mengambil pilihan menu dari user.
        pilihan = input("Pilih opsi: ")

        # Tahap Perkondisian: Memeriksa pilihan user dan menjalankan fungsi sesuai (menu ikan, keranjang, transaksi, dll.).
        if pilihan == '1':
            Menu_ikan(cursor)
            input("tekkan enter untuk kembali")  # Tahap Output: Pause untuk user melihat output sebelum kembali.
        elif pilihan == '2':
            Menu_Keranjang(cursor, id_pengguna)
        elif pilihan == '3':
            Transaksi(cursor, id_pengguna)
            input("enter untuk kembali")  # Tahap Output: Pause setelah transaksi.
        elif pilihan == '4':
            Bukti_pembayaran(cursor, id_pengguna)
            input("enter untuk kembali")  # Tahap Output: Pause setelah melihat bukti.
        elif pilihan == '5':
            lihat_Status_pengiriman(cursor, id_pengguna)
            input("enter untuk kembali")  # Tahap Output: Pause setelah melihat status.
        elif pilihan == '6':
            menu_profil(cursor, id_pengguna)
        elif pilihan == '7':
            # Tahap Output: Menampilkan pesan logout dan menghentikan loop.
            print("Anda telah keluar")
            break
        else:
            # Tahap Output: Menampilkan pesan error jika pilihan invalid.
            print("Pilihan tidak valid!")

def Menu_ikan(cursor):
    os.system('cls')  # Tahap Proses dan Logika: Membersihkan layar sebelum output daftar ikan.
    # Tahap Proses dan Logika: Mengeksekusi query untuk mengambil data ikan dengan JOIN ke jenis_ikan.
    cursor.execute("""
        SELECT ikan.id_ikan, jenis_ikan.nama_ikan AS jenis_ikan, ikan.nama_ikan, ikan.warna, ikan.ukuran, ikan.harga, ikan.stok, ikan.deskripsi 
        FROM ikan 
        JOIN jenis_ikan ON ikan.jenis_ikan_id_jenis_ikan = jenis_ikan.id_jenis_ikan
    """)
    list_ikan = cursor.fetchall()
    # Tahap Perkondisian: Memeriksa apakah ada data ikan untuk ditampilkan.
    if list_ikan: 
        # Tahap Output: Menampilkan daftar ikan dalam tabel.
        print("\nDaftar Ikan Hias:")
        print(tabulate(list_ikan, headers=['id_ikan', 'jenis ikan', 'nama ikan', 'warna', 'ukuran', 'Harga', 'Stok', 'Deskripsi'], tablefmt='fancy_grid'))

        # Tahap Proses dan Logika: Mengambil rekomendasi ikan berdasarkan stok dan harga.
        cursor.execute("SELECT nama_ikan FROM ikan WHERE stok > 50 ORDER BY harga ASC LIMIT 3")
        rekomendasi = cursor.fetchall()
        # Tahap Perkondisian: Memeriksa apakah ada rekomendasi untuk ditampilkan.
        if rekomendasi:
            # Tahap Output: Menampilkan rekomendasi ikan.
            print("\nRekomendasi Ikan:")
            for rec in rekomendasi:
                print(f"- {rec[0]}")
    else:
        # Tahap Output: Menampilkan pesan jika tidak ada ikan.
        print("ikan tidak tersedia")

def Menu_Keranjang(cursor, id_pengguna):
    Menu_ikan(cursor)  # Tahap Proses dan Logika: Menampilkan menu ikan terlebih dahulu.
    # Tahap Pengambilan Input: Mengambil ID ikan dan jumlah yang ingin dibeli.
    id_ikan = input("Masukkan id ikan yang ingin dibeli: ")
    jumlah = int(input("Masukkan Jumlah Ikan: "))

    # Tahap Proses dan Logika: Mengecek harga dan stok ikan dari database.
    cursor.execute("SELECT harga, stok FROM ikan WHERE id_ikan = %s", (id_ikan,))
    ikan = cursor.fetchone()
    # Tahap Perkondisian: Memeriksa apakah ikan tersedia.
    if not ikan:
        # Tahap Output: Menampilkan pesan error jika ikan tidak ditemukan.
        print("Ikan tidak tersedia")
        return
    harga, stok = ikan
    # Tahap Perkondisian: Memeriksa apakah stok cukup.
    if jumlah > stok:
        # Tahap Output: Menampilkan pesan error jika stok tidak cukup.
        print("Stok tidak cukup.")
        return
    

    # Tahap Proses dan Logika: Mengambil atau membuat ID keranjang untuk user.
    cursor.execute("SELECT id_keranjang FROM keranjang WHERE pengguna_id_pengguna = %s", (id_pengguna,))
    keranjang = cursor.fetchone()
    if not keranjang:
        cursor.execute("INSERT INTO keranjang(pengguna_id_pengguna) VALUES (%s) RETURNING id_keranjang", (id_pengguna,))
        id_keranjang = cursor.fetchone()[0]
    else:
        id_keranjang = keranjang[0]

    # Tahap Proses dan Logika: Mengecek apakah item sudah ada di keranjang untuk update atau insert.
    cursor.execute("SELECT jumlah_ikan FROM item_keranjang WHERE keranjang_id_keranjang = %s AND ikan_id_ikan = %s", (id_keranjang, id_ikan))
    existing_item = cursor.fetchone()
    # Tahap Perkondisian: Jika item sudah ada, update jumlah; jika tidak, insert baru.
    if existing_item:
        new_jumlah = existing_item[0] + jumlah
        cursor.execute("UPDATE item_keranjang SET jumlah_ikan = %s WHERE keranjang_id_keranjang = %s AND ikan_id_ikan = %s", (new_jumlah, id_keranjang, id_ikan))
        # Tahap Output: Menampilkan pesan sukses update.
        print("Jumlah ikan di keranjang berhasil ditambah!")
    else:
        cursor.execute("""
        INSERT INTO item_keranjang (jumlah_ikan, harga_satuan, keranjang_id_keranjang, ikan_id_ikan)
        VALUES (%s, %s, %s, %s)
    """, (jumlah, harga, id_keranjang, id_ikan))
        # Tahap Output: Menampilkan pesan sukses insert.
        print("item berhasil ditambahkan ke keranjang!")
    
    # Tahap Output: Menampilkan opsi lanjut transaksi atau kembali.
    print("1. lanjut transkasi")
    print("2. Kembali")
    # Tahap Pengambilan Input: Mengambil pilihan lanjutan.
    lanjutan = input("Pilih opsi: ")

    # Tahap Perkondisian: Menjalankan transaksi atau kembali berdasarkan pilihan.
    if lanjutan == '1':
        Transaksi(cursor, id_pengguna)
    elif lanjutan == '2':
        return
    else:
        # Tahap Output: Menampilkan pesan error jika pilihan invalid.
        print("pilihan tidak valid")

def Transaksi(cursor, id_pengguna):
    os.system('cls')  # Tahap Proses dan Logika: Membersihkan layar sebelum proses transaksi.
    # Tahap Proses dan Logika: Mengambil data keranjang user dengan JOIN untuk subtotal.
    cursor.execute("""
        SELECT i.nama_ikan, ik.jumlah_ikan, ik.harga_satuan, (ik.jumlah_ikan * ik.harga_satuan) as subtotal
        FROM item_keranjang ik
        JOIN ikan i ON ik.ikan_id_ikan = i.id_ikan
        JOIN keranjang k ON ik.keranjang_id_keranjang = k.id_keranjang
        WHERE k.pengguna_id_pengguna = %s
    """, (id_pengguna,))
    items = cursor.fetchall()
    # Tahap Perkondisian: Memeriksa apakah keranjang kosong.
    if not items:
        # Tahap Output: Menampilkan pesan jika keranjang kosong.
        print("keranjang kosong")
        return
    
    # Tahap Output: Menampilkan ringkasan keranjang dalam tabel.
    print("\n=== Ringkasan Keranjang ===")
    print(tabulate(items, headers=['Nama Ikan', 'Jumlah', 'Harga Satuan', 'Subtotal'], tablefmt='fancy_grid'))

    total_harga_ikan = sum(item[3] for item in items)  # Tahap Proses dan Logika: Menghitung total harga ikan.
    # Tahap Output: Menampilkan total harga ikan.
    print(f"\n Total Harga Ikan: Rp {total_harga_ikan:,}")

    # Tahap Output: Menampilkan opsi alamat pengiriman.
    print("\n=== Alamat Pengiriman ===")
    print("1. Gunakan alamat profil")
    print("2. Input alamat baru")
    # Tahap Pengambilan Input: Mengambil pilihan alamat.
    pilih_alamat = input("Pilih opsi (1/2): ")

    # Tahap Perkondisian: Memproses alamat berdasarkan pilihan user.
    if pilih_alamat == '1':
        cursor.execute("SELECT alamat_id FROM pengguna WHERE id_pengguna = %s", (id_pengguna,))
        alamat_result = cursor.fetchone()
        if alamat_result and alamat_result[0]:
            alamat_pengiriman_id = alamat_result[0]
        else:
            # Tahap Output: Menampilkan pesan error jika alamat profil kosong, lalu paksa input baru.
            print(" Alamat profil belum diisi! Silakan input alamat baru.")
            pilih_alamat = '2'

    # Tahap Pengambilan Input: Jika input alamat baru, ambil detail alamat dengan query database untuk opsi.
    if pilih_alamat == '2':
        print("\n--- Input Alamat Pengiriman ---")

        cursor.execute("SELECT id_kabupaten, nama_kabupaten, harga_ongkir FROM kabupaten ORDER BY nama_kabupaten")
        kabupaten_list = cursor.fetchall()
        # Tahap Output: Menampilkan daftar kabupaten dengan ongkir.
        print("\nPilih Kabupaten:")
        for kab in kabupaten_list:
            print(f"{kab[0]}. {kab[1]} (Ongkir: Rp {kab[2]:,})")
        kabupaten_id = input("Pilih ID Kabupaten: ")
        
        cursor.execute("SELECT id_kecamatan, nama_kecamatan FROM kecamatan WHERE kabupaten_id = %s ORDER BY nama_kecamatan", (kabupaten_id,))
        kecamatan_list = cursor.fetchall()
        if not kecamatan_list:
            # Tahap Output: Menampilkan pesan error jika tidak ada kecamatan.
            print(" Tidak ada kecamatan di kabupaten ini!")
            return
        # Tahap Output: Menampilkan daftar kecamatan.
        print("\nPilih Kecamatan:")
        for kec in kecamatan_list:
            print(f"{kec[0]}. {kec[1]}")
        kecamatan_id = input("Pilih ID Kecamatan: ")
        
        cursor.execute("SELECT id_desa, nama_desa FROM desa WHERE kecamatan_id = %s ORDER BY nama_desa", (kecamatan_id,))
        desa_list = cursor.fetchall()
        if not desa_list:
            # Tahap Output: Menampilkan pesan error jika tidak ada desa.
            print(" Tidak ada desa di kecamatan ini!")
            return
        # Tahap Output: Menampilkan daftar desa.
        print("\nPilih Desa:")
        for ds in desa_list:
            print(f"{ds[0]}. {ds[1]}")
        desa_id = input("Pilih ID Desa: ")
        
        nama_jalan = input("Masukkan nama jalan & nomor rumah: ")
        rt_rw = input("Masukkan RT/RW (contoh: 02/05): ")
        kode_pos = input("Masukkan kode pos: ")
        catatan_alamat = input("Catatan alamat (opsional): ")
        
        # Tahap Proses dan Logika: Insert alamat baru ke database.
        cursor.execute("""
            INSERT INTO alamat (nama_jalan, rt_rw, desa_id, kode_pos, catatan_alamat)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_alamat
        """, (nama_jalan, rt_rw, desa_id, kode_pos, catatan_alamat))
        alamat_pengiriman_id = cursor.fetchone()[0]

    # Tahap Proses dan Logika: Mengambil ongkir berdasarkan alamat.
    cursor.execute("""
        SELECT kab.harga_ongkir 
        FROM alamat a
        JOIN desa d ON a.desa_id = d.id_desa
        JOIN kecamatan k ON d.kecamatan_id = k.id_kecamatan
        JOIN kabupaten kab ON k.kabupaten_id = kab.id_kabupaten
        WHERE a.id_alamat = %s
    """, (alamat_pengiriman_id,))
    ongkir = cursor.fetchone()[0]

    total_pesanan = total_harga_ikan + ongkir  # Tahap Proses dan Logika: Menghitung total pesanan.
    
    # Tahap Output: Menampilkan ringkasan pembayaran.
    print(f"\n--- Ringkasan Pembayaran ---")
    print(f"Total Harga Ikan : Rp {total_harga_ikan:,}")
    print(f"Ongkos Kirim     : Rp {ongkir:,}")
    print(f"{'='*35}")
    print(f"TOTAL BAYAR      : Rp {total_pesanan:,}")
    
    # Tahap Pengambilan Input: Mengambil catatan dan metode pembayaran.
    catatan = input("\nMasukkan catatan pesanan (opsional): ")
    
    cursor.execute("SELECT id_metode, nama_metode FROM metode_pembayaran")
    metode_list = cursor.fetchall()
    # Tahap Output: Menampilkan daftar metode pembayaran.
    print("\n=== Metode Pembayaran ===")
    for metode in metode_list:
        print(f"{metode[0]}. {metode[1]}")
    metode_id = input("Pilih metode pembayaran: ")

    # Tahap Perkondisian: Memeriksa validitas metode pembayaran.
    if not metode_id.isdigit():
        # Tahap Output: Menampilkan pesan error jika metode invalid.
        print(" Metode tidak valid.")
        return
    

    # Tahap Proses dan Logika: Insert pesanan, item_pesanan, dan transaksi ke database, lalu commit.
    cursor.execute("""
        INSERT INTO pesanan (alamat_pengiriman_id, total_pesanan, catatan, pengguna_id_pengguna) 
        VALUES (%s, %s, %s, %s) RETURNING id_pesanan
    """, (alamat_pengiriman_id, total_pesanan, catatan, id_pengguna))
    id_pesanan = cursor.fetchone()[0]

    cursor.execute("""
        INSERT INTO item_pesanan (subtotal, pesanan_id_pesanan, ikan_id_ikan)
        SELECT (jumlah_ikan * harga_satuan), %s, ikan_id_ikan 
        FROM item_keranjang 
        WHERE keranjang_id_keranjang = (SELECT id_keranjang FROM keranjang WHERE pengguna_id_pengguna = %s)
    """, (id_pesanan, id_pengguna))

    no_transaksi = f"TXN{id_pesanan}{datetime.now().strftime('%Y%m%d%H%M%S')}"
    cursor.execute("""
        INSERT INTO transaksi (jumlah_dibayar, pengguna_id_pengguna, pesanan_id_pesanan, metode_pembayaran_id_metode, no_transaksi) 
        VALUES (%s, %s, %s, %s, %s)
    """, (total_pesanan, id_pengguna, id_pesanan, metode_id, no_transaksi))

    cursor.execute("DELETE FROM item_keranjang WHERE keranjang_id_keranjang = (SELECT id_keranjang FROM keranjang WHERE pengguna_id_pengguna = %s)", (id_pengguna,))
    
    cursor.connection.commit()
    # Tahap Output: Menampilkan pesan sukses transaksi.
    print(f"\n✅ Pembayaran berhasil! No Transaksi: {no_transaksi}")

def Bukti_pembayaran(cursor, id_pengguna):
    os.system('cls')  # Tahap Proses dan Logika: Membersihkan layar sebelum output bukti.
    # Tahap Proses dan Logika: Mengambil data transaksi dengan JOIN ke view untuk breakdown harga.
    cursor.execute("""
        SELECT DISTINCT t.no_transaksi, t.jumlah_dibayar, mp.nama_metode, 
            v.alamat_lengkap, p.catatan, p.status_pesanan,
            p.total_pesanan, vd.harga_ongkir, vd.total_harga_ikan_sebelum_ongkir
        FROM transaksi t
        JOIN metode_pembayaran mp ON t.metode_pembayaran_id_metode = mp.id_metode
        JOIN pesanan p ON t.pesanan_id_pesanan = p.id_pesanan
        JOIN v_alamat_lengkap v ON p.alamat_pengiriman_id = v.id_alamat
        JOIN v_pesanan_detail vd ON p.id_pesanan = vd.id_pesanan
        WHERE t.pengguna_id_pengguna = %s
    """, (id_pengguna,))
    list_transaksi = cursor.fetchall()
    # Tahap Perkondisian: Memeriksa apakah ada transaksi untuk ditampilkan.
    if list_transaksi:
        # Tahap Output: Menampilkan header bukti pembayaran.
        print("\n=== Bukti Pembayaran dan Pembelian ===")
        # Tahap Perulangan: Loop untuk menampilkan setiap transaksi dalam format invoice.
        for trx in list_transaksi:
            print(f"\n{'='*60}")
            print(f"No Transaksi      : {trx[0]}")
            print(f"Metode Pembayaran : {trx[2]}")
            print(f"Status Pesanan    : {trx[5]}")
            print(f"\nAlamat Pengiriman : {trx[3]}")
            print(f"Catatan           : {trx[4] if trx[4] else '-'}")
            print(f"\n--- Rincian Biaya ---")
            print(f"Total Harga Ikan  : Rp {int(trx[8]):,}")
            print(f"Ongkos Kirim      : Rp {int(trx[7]):,}")
            print(f"{'-'*35}")
            print(f"TOTAL DIBAYAR     : Rp {int(trx[1]):,}")
            print(f"{'='*60}")
    else:
        # Tahap Output: Menampilkan pesan jika tidak ada transaksi.
        print(" Tidak ada transaksi.")

def lihat_Status_pengiriman(cursor, id_pengguna):
    os.system('cls')  # Tahap Proses dan Logika: Membersihkan layar sebelum output status.
    # Tahap Proses dan Logika: Mengambil data pesanan dengan JOIN ke view alamat lengkap.
    cursor.execute("""
        SELECT p.id_pesanan, v.alamat_lengkap, p.status_pesanan, p.tanggal_pesanan
        FROM pesanan p
        JOIN v_alamat_lengkap v ON p.alamat_pengiriman_id = v.id_alamat
        WHERE p.pengguna_id_pengguna = %s
        ORDER BY p.tanggal_pesanan DESC
    """, (id_pengguna,))
    list_pesanan = cursor.fetchall()
    # Tahap Perkondisian: Memeriksa apakah ada pesanan untuk ditampilkan.
    if list_pesanan:
        # Tahap Output: Menampilkan status pengiriman dalam tabel.
        print("\n=== Status Pengiriman ===")
        print(tabulate(list_pesanan, headers=['ID Pesanan', 'Alamat Pengiriman', 'Status', 'Tanggal'], tablefmt='fancy_grid'))
    else:
        # Tahap Output: Menampilkan pesan jika tidak ada pesanan.
        print("Tidak ada pesanan.")





def fitur_admin(cursor, id_pengguna, role):
    """
    Fungsi menu utama untuk role Admin
    Parameter:
    - cursor: koneksi database
    - id_pengguna: ID admin yang login
    - role: role pengguna (Admin)
    """
    while True:
        os.system('cls')  # Clear screen (Windows: cls, Linux/Mac: clear)
        print(f"\n=== Menu Admin (ID: {id_pengguna}) ===")
        
        # Tampilkan menu pilihan admin
        print("1. Kelola Stok Ikan")
        print("2. Kelola Harga Ikan")
        print("3. Konfirmasi Pesanan")
        print("4. Lihat Status Pengiriman")
        print("5. Buat Laporan Penjualan")
        print("6. Lihat Inputan teknisi")
        print("7. Lihat Data Pengguna")  
        print("8. Menu profil")
        print("9. Logout ke Menu Utama")
        
        pilihan = input("Pilih opsi (1-9): ")

        # Routing berdasarkan pilihan user
        if pilihan == '1':
            kelola_stok_ikan(cursor)  # Panggil fungsi kelola stok
            input("enter untuk kembali")  # Pause sebelum kembali ke menu
        elif pilihan == '2':
            kelola_harga_ikan(cursor)  # Panggil fungsi kelola harga
            input("enter untuk kembali")
        elif pilihan == '3':
            konfirmasi_pesanan(cursor)  # Panggil fungsi konfirmasi pesanan
            input("enter untuk kembali")
        elif pilihan == '4':
            lihat_status_pengiriman_admin(cursor)  # Lihat semua status pengiriman
            input("enter untuk kembali")
        elif pilihan == '5':
            buat_laporan_penjualan(cursor)  # Generate laporan penjualan
            input("enter untuk kembali")
        elif pilihan == '6':
            lihat_baruan_teknisi(cursor)  # Lihat notifikasi dari teknisi
            input("enter untuk kembali")
        elif pilihan == '7':
            lihat_data_pengguna(cursor)  # Lihat semua data pengguna
            input("enter untuk kembali")  
        elif pilihan == '8':
            menu_profil(cursor, id_pengguna)  # Edit profil admin
        elif pilihan == '9':
            print("Logout berhasil. Kembali ke Menu Utama.")
            break  # Keluar dari loop, kembali ke menu login
        else:
            print("Pilihan tidak valid!")    


def kelola_stok_ikan(cursor):
    """
    Fungsi untuk mengelola stok ikan (tambah/kurangi/hapus)
    Admin bisa:
    1. Tambah stok ikan yang sudah ada
    2. Kurangi stok ikan
    3. Tambah ikan baru ke katalog
    4. Hapus ikan dari katalog
    """
    while True:
        os.system('cls')
        print("\n=== Kelola Stok Ikan ===")
        print("1. Tambah Stok")
        print("2. Kurangi Stok")
        print("3. Tambah Ikan")
        print("4. Hapus Ikan")
        print("5. Kembali")
        pilihan = input("Pilih opsi (1-5): ")
    
        if pilihan == '1':
            # === TAMBAH STOK IKAN YANG SUDAH ADA ===
            
            # Query JOIN untuk menampilkan daftar ikan dengan jenis
            # JOIN jenis_ikan agar bisa lihat kategori ikan (Arwana, Koi, dll)
            cursor.execute("""
                SELECT ikan.id_ikan, jenis_ikan.nama_ikan AS jenis_ikan, ikan.nama_ikan, 
                ikan.warna, ikan.ukuran, ikan.harga, ikan.stok, ikan.deskripsi 
                FROM ikan 
                JOIN jenis_ikan ON ikan.jenis_ikan_id_jenis_ikan = jenis_ikan.id_jenis_ikan
            """)
            list_ikan = cursor.fetchall()  # Ambil semua hasil query
            
            # Jika ada data ikan, tampilkan dalam bentuk tabel
            if list_ikan: 
                print(tabulate(list_ikan, 
                            headers=['ID Ikan', 'Jenis Ikan', 'Nama Ikan', 'Warna', 'Ukuran', 'Harga', 'Stok', 'Deskripsi'], 
                            tablefmt='fancy_grid'))
            else:
                print(" Tidak ada data ikan.")
                input("\nTekan Enter untuk kembali...")
                continue

            # Input ID ikan yang mau ditambah stoknya
            id_ikan = input("\nMasukkan ID Ikan: ").strip()
            
            # Validasi: Cek apakah ID ikan valid
            cursor.execute("SELECT nama_ikan, stok FROM ikan WHERE id_ikan = %s", (id_ikan,))
            ikan_data = cursor.fetchone()
            
            if not ikan_data:
                print(" ID Ikan tidak ditemukan!")
                input("\nTekan Enter untuk kembali...")
                continue
            
            nama_ikan, stok_lama = ikan_data
            print(f"\n Ikan: {nama_ikan}")
            print(f" Stok saat ini: {stok_lama}")
            
            # Input jumlah tambahan
            try:
                tambah_stock = int(input("Masukkan jumlah stok tambahan: "))
                
                # Validasi: jumlah harus positif
                if tambah_stock <= 0:
                    print(" Jumlah stok harus lebih dari 0!")
                    input("\nTekan Enter untuk kembali...")
                    continue
                
            except ValueError:
                print(" Input harus berupa angka!")
                input("\nTekan Enter untuk kembali...")
                continue
            
            # Hitung stok baru
            stok_baru = stok_lama + tambah_stock
            
            # Konfirmasi
            print(f"\n--- Konfirmasi Tambah Stok ---")
            print(f"Ikan: {nama_ikan}")
            print(f"Stok Lama: {stok_lama}")
            print(f"Tambahan: +{tambah_stock}")
            print(f"Stok Baru: {stok_baru}")
            
            konfirmasi = input("\n✅ Yakin ingin menambah stok? (Ya/Tidak): ").strip().lower()
            
            if konfirmasi == 'ya':
                try:
                    # UPDATE stok: stok lama + tambahan
                    cursor.execute("UPDATE ikan SET stok = stok + %s, waktu_update = CURRENT_TIMESTAMP WHERE id_ikan = %s", 
                                 (tambah_stock, id_ikan))
                    
                    # COMMIT: SIMPAN PERUBAHAN KE DATABASE
                    # Tanpa commit, perubahan hanya di memori (tidak tersimpan permanen)
                    cursor.connection.commit()
                    
                    print(f"\n✅ Stok berhasil ditambahkan!")
                    print(f" Stok {nama_ikan} sekarang: {stok_baru}")
                    
                except Exception as e:
                    # Jika error, rollback (batalkan perubahan)
                    cursor.connection.rollback()
                    print(f"\n❌ Error saat menambah stok: {e}")
            else:
                print("\n❌ Penambahan stok dibatalkan.")
            
        elif pilihan == '2':
            # === KURANGI STOK IKAN ===
            
            # Tampilkan daftar ikan
            cursor.execute("""
                SELECT ikan.id_ikan, jenis_ikan.nama_ikan AS jenis_ikan, ikan.nama_ikan, 
                    ikan.warna, ikan.ukuran, ikan.harga, ikan.stok 
                FROM ikan 
                JOIN jenis_ikan ON ikan.jenis_ikan_id_jenis_ikan = jenis_ikan.id_jenis_ikan
            """)
            list_ikan = cursor.fetchall()
            
            if list_ikan: 
                print(tabulate(list_ikan, 
                            headers=['ID Ikan', 'Jenis Ikan', 'Nama Ikan', 'Warna', 'Ukuran', 'Harga', 'Stok'], 
                            tablefmt='fancy_grid'))
            else:
                print(" Tidak ada data ikan.")
                input("\nTekan Enter untuk kembali...")
                continue
            
            # Input ID ikan
            id_ikan = input("\nMasukkan ID Ikan: ").strip()
            
            # Cek stok ikan dulu sebelum dikurangi
            cursor.execute("SELECT nama_ikan, stok FROM ikan WHERE id_ikan = %s", (id_ikan,))
            ikan_data = cursor.fetchone()  # Ambil 1 hasil (nama & stok saat ini)
            
            # Validasi: ikan ada atau tidak?
            if not ikan_data:
                print(" ID Ikan tidak ditemukan!")
                input("\nTekan Enter untuk kembali...")
                continue
            
            nama_ikan, stok_lama = ikan_data
            print(f"\n📦 Ikan: {nama_ikan}")
            print(f"📊 Stok saat ini: {stok_lama}")
            
            # Input jumlah pengurangan
            try:
                kurangi = int(input("Masukkan jumlah stok yang akan dikurangi: "))
                
                # Validasi: jumlah harus positif
                if kurangi <= 0:
                    print(" Jumlah pengurangan harus lebih dari 0!")
                    input("\nTekan Enter untuk kembali...")
                    continue
                
            except ValueError:
                print(" Input harus berupa angka!")
                input("\nTekan Enter untuk kembali...")
                continue
            
            # Validasi: stok cukup atau tidak?
            if stok_lama - kurangi < 0:
                print(f"\n❌ Stok tidak cukup!")
                print(f"Stok tersedia: {stok_lama}")
                print(f"Yang akan dikurangi: {kurangi}")
                print(f"Kekurangan: {kurangi - stok_lama}")
                input("\nTekan Enter untuk kembali...")
                continue
            
            # Hitung stok baru
            stok_baru = stok_lama - kurangi
            
            # Konfirmasi
            print(f"\n--- Konfirmasi Kurangi Stok ---")
            print(f"Ikan: {nama_ikan}")
            print(f"Stok Lama: {stok_lama}")
            print(f"Pengurangan: -{kurangi}")
            print(f"Stok Baru: {stok_baru}")
            
            konfirmasi = input("\n Yakin ingin mengurangi stok? (Ya/Tidak): ").strip().lower()
            
            if konfirmasi == 'ya':
                try:
                    # UPDATE stok: stok lama - pengurangan
                    cursor.execute("UPDATE ikan SET stok = stok - %s, waktu_update = CURRENT_TIMESTAMP WHERE id_ikan = %s", 
                                (kurangi, id_ikan))
                    
                    #  COMMIT: SIMPAN PERUBAHAN KE DATABASE
                    # Kenapa penting? Tanpa commit = perubahan hilang saat program close
                    cursor.connection.commit()
                    
                    print(f"\n  Stok berhasil dikurangi!")
                    print(f" Stok {nama_ikan} sekarang: {stok_baru}")
                    
                except Exception as e:
                    # Jika error (misal: constraint violation), rollback
                    cursor.connection.rollback()
                    print(f"\n  Error saat mengurangi stok: {e}")
            else:
                print("\n  Pengurangan stok dibatalkan.")
                
        elif pilihan == '3': 
            # === TAMBAH IKAN BARU KE KATALOG ===
            
            # Input data ikan baru
            nama_ikan = input("Masukkan nama ikan: ")
            jenis_ikan_nama = input("Masukkan jenis ikan: ")
            warna = input("Masukkan warna: ")
            ukuran = input("Masukkan ukuran: ")
            harga = int(input("Masukkan harga: "))
            stok = int(input("Masukkan stok awal: "))
            deskripsi = input("Masukkan deskripsi: ")
            link_gambar = input("Masukkan link gambar: ")
            
            # Cek apakah jenis ikan sudah ada di database
            cursor.execute("SELECT id_jenis_ikan FROM jenis_ikan WHERE nama_ikan = %s", (jenis_ikan_nama,))
            jenis = cursor.fetchone()
            
            if not jenis:
                # Jika jenis ikan belum ada, insert jenis baru
                cursor.execute("INSERT INTO jenis_ikan (nama_ikan) VALUES (%s) RETURNING id_jenis_ikan", (jenis_ikan_nama,))
                id_jenis_ikan = cursor.fetchone()[0]  # Ambil ID jenis yang baru dibuat
                cursor.connection.commit()  # Simpan perubahan ke database
                print(f"Jenis ikan '{jenis_ikan_nama}' berhasil ditambah.")
            else:
                # Jika sudah ada, pakai ID yang sudah ada
                id_jenis_ikan = jenis[0]
            
            # Insert ikan baru dengan jenis_ikan_id yang sudah didapat
            cursor.execute("""
                INSERT INTO ikan (nama_ikan, jenis_ikan_id_jenis_ikan, warna, ukuran, harga, stok, deskripsi, link_gambar) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (nama_ikan, id_jenis_ikan, warna, ukuran, harga, stok, deskripsi, link_gambar))
            cursor.connection.commit()  # Simpan ke database
            print("Ikan baru berhasil ditambah.")
            
        elif pilihan == '4':
            # === HAPUS IKAN DARI KATALOG ===
            
            # Tampilkan daftar ikan yang ada
            cursor.execute("SELECT id_ikan, nama_ikan, stok FROM ikan ORDER BY id_ikan")
            ikan_list = cursor.fetchall()
            
            # Validasi: apakah ada ikan di database?
            if not ikan_list:
                print("Tidak ada ikan di database.")
                input("\nTekan Enter untuk kembali...")
                continue  # Kembali ke menu pilihan
            
            # Tampilkan daftar ikan dalam tabel
            print("\n--- Daftar Ikan ---")
            print(tabulate(ikan_list, headers=['ID', 'Nama Ikan', 'Stok'], tablefmt='fancy_grid'))
            
            id_ikan = input("\nMasukkan ID Ikan yang ingin dihapus: ")
            
            # Cek apakah ID ikan ada di database
            cursor.execute("SELECT nama_ikan FROM ikan WHERE id_ikan = %s", (id_ikan,))
            ikan_data = cursor.fetchone()
            
            if not ikan_data:
                print(f" Ikan dengan ID {id_ikan} tidak ditemukan.")
                input("\nTekan Enter untuk kembali...")
                continue
            
            # Konfirmasi hapus (pastikan admin yakin)
            print(f"\n⚠ Anda akan menghapus: {ikan_data[0]} (ID: {id_ikan})")
            konfirmasi = input("Yakin ingin menghapus? (Ya/Tidak): ").strip().lower()
            
            if konfirmasi == 'ya':
                try:
                    # DELETE dari database
                    cursor.execute("DELETE FROM ikan WHERE id_ikan = %s", (id_ikan,))
                    cursor.connection.commit()  # Simpan perubahan
                    print(f" Ikan '{ikan_data[0]}' berhasil dihapus dari database!")
                except Exception as e:
                    # Jika error (misal: ikan masih ada di pesanan), rollback
                    cursor.connection.rollback()
                    print(f" Error saat menghapus: {e}")
            else:
                print(" Penghapusan dibatalkan.")
            
        elif pilihan == '5':
            break  # Kembali ke menu admin utama
        else:
            print("Pilihan tidak valid!")
        input("enter untuk kembali")


def kelola_harga_ikan(cursor):
    """
    Fungsi untuk update harga ikan
    Admin bisa mengubah harga ikan yang sudah ada
    """
    while True:
        os.system('cls')
        print("\n=== Kelola Harga Ikan ===")
        print("1. Update Harga")
        print("2. Kembali")
        pilihan = input("Pilih opsi (1-2): ")

        if pilihan == '1':
            # === UPDATE HARGA IKAN ===
            cursor.execute("""
                SELECT ikan.id_ikan, jenis_ikan.nama_ikan AS jenis_ikan, ikan.nama_ikan, 
                ikan.harga
                FROM ikan 
                JOIN jenis_ikan ON ikan.jenis_ikan_id_jenis_ikan = jenis_ikan.id_jenis_ikan
            """)
            list_ikan = cursor.fetchall()  # Ambil semua hasil query
            
            # Jika ada data ikan, tampilkan dalam bentuk tabel
            if list_ikan: 
                print(tabulate(list_ikan, 
                            headers=['ID Ikan', 'Jenis Ikan', 'Nama Ikan', 'Harga'], 
                            tablefmt='fancy_grid'))
            else:
                print(" Tidak ada data ikan.")
                input("\nTekan Enter untuk kembali...")
                continue

            id_ikan = input("Masukkan ID Ikan: ")
            new_harga = int(input("Masukkan harga baru: "))
            
            # Validasi: harga tidak boleh negatif
            if new_harga >= 0:
                # UPDATE harga di database
                cursor.execute("UPDATE ikan SET harga = %s WHERE id_ikan = %s", (new_harga, id_ikan))
                #Tambahkan commit untuk menyimpan perubahan ke database
                cursor.connection.commit()
                print("Harga berhasil diupdate.")
            else:
                print("Harga tidak boleh negatif.")
            input("enter untuk kembali")
        elif pilihan == '2':
            break  # Kembali ke menu admin utama
        else:
            print("Pilihan tidak valid!")



def konfirmasi_pesanan(cursor):
    """
    Fungsi untuk admin konfirmasi pesanan pelanggan
    Flow: Pending → Dikonfirmasi → Dikirim → Diterima
    Penting: Stok HANYA dikurangi saat status berubah ke "Dikonfirmasi"
    """
    os.system('cls')
    
    # Query pesanan yang belum selesai (belum "Diterima")
    cursor.execute("""
        SELECT p.id_pesanan, pg.nama, p.total_pesanan, p.catatan, p.status_pesanan, p.tanggal_pesanan
        FROM pesanan p
        JOIN pengguna pg ON p.pengguna_id_pengguna = pg.id_pengguna
        WHERE p.status_pesanan IN ('Pending', 'Dikonfirmasi', 'Dikirim')
        ORDER BY p.tanggal_pesanan DESC
    """)
    pesanan_list = cursor.fetchall()
    
    if not pesanan_list:
        print("❌ Tidak ada pesanan yang perlu dikonfirmasi.")
        input("\nTekan Enter untuk kembali...")
        return

    print("\n=== Daftar Pesanan ===")
    print(tabulate(pesanan_list, 
                headers=['ID Pesanan', 'Nama Pelanggan', 'Total', 'Catatan', 'Status', 'Tanggal'], 
                tablefmt='fancy_grid'))

    id_pesanan = input("\nMasukkan ID Pesanan untuk update status: ")
    
    cursor.execute("SELECT status_pesanan FROM pesanan WHERE id_pesanan = %s", (id_pesanan,))
    pesanan_data = cursor.fetchone()
    
    if not pesanan_data:
        print(f"❌ Pesanan ID {id_pesanan} tidak ditemukan.")
        input("\nTekan Enter untuk kembali...")
        return
    
    status_sekarang = pesanan_data[0]
    print(f"\n📋 Status saat ini: {status_sekarang}")
    
    print("\n=== Pilih Status Baru ===")
    print("1. Dikonfirmasi (Admin menerima pesanan)")
    print("2. Dikirim (Pesanan dalam pengiriman)")
    print("3. Diterima (Pelanggan sudah terima)")
    new_status_baru = input("Pilih status baru (1/2/3): ")
    
    status_map = {
        '1': 'Dikonfirmasi',
        '2': 'Dikirim',
        '3': 'Diterima'
    }
    
    new_status = status_map.get(new_status_baru)
    
    if not new_status:
        print("❌ Status tidak valid.")
        input("\nTekan Enter untuk kembali...")
        return
    
    # === PENTING: KURANGI STOK HANYA SAAT DIKONFIRMASI ===
    if new_status == 'Dikonfirmasi' and status_sekarang == 'Pending':
        # ✅ SOLUSI: Hitung jumlah ikan dari subtotal / harga_satuan
        # Ambil data dari item_pesanan dan ikan
        cursor.execute("""
            SELECT ip.ikan_id_ikan, ip.subtotal, i.harga
            FROM item_pesanan ip
            JOIN ikan i ON ip.ikan_id_ikan = i.id_ikan
            WHERE ip.pesanan_id_pesanan = %s
        """, (id_pesanan,))
        
        items = cursor.fetchall()
        
        # Loop setiap item dan kurangi stok
        for id_ikan, subtotal, harga_satuan in items:
            # Hitung jumlah ikan dari subtotal / harga_satuan
            jumlah_ikan = subtotal // harga_satuan  # Integer division
            
            # Update stok ikan
            cursor.execute("""
                UPDATE ikan 
                SET stok = stok - %s,
                    waktu_update = CURRENT_TIMESTAMP
                WHERE id_ikan = %s
            """, (jumlah_ikan, id_ikan))
        
        print("\n✅ Stok ikan berhasil dikurangi!")
    
    # Update status pesanan
    cursor.execute("""
        UPDATE pesanan 
        SET status_pesanan = %s, waktu_update = CURRENT_TIMESTAMP 
        WHERE id_pesanan = %s
    """, (new_status, id_pesanan))
    
    # COMMIT perubahan
    cursor.connection.commit()
    
    print(f"\n✅ Status pesanan berhasil diupdate menjadi '{new_status}'!")
    input("\nTekan Enter untuk kembali...")


def lihat_status_pengiriman_admin(cursor):
    """
    Fungsi untuk admin melihat status semua pengiriman
    Menggunakan VIEW v_alamat_lengkap untuk menampilkan alamat lengkap
    """
    os.system('cls')
    
    # Query JOIN dengan v_alamat_lengkap VIEW
    # Kenapa JOIN VIEW? Karena alamat sudah dinormalisasi (kabupaten → kecamatan → desa)
    # VIEW sudah CONCAT semua jadi 1 string alamat lengkap
    cursor.execute("""
        SELECT p.id_pesanan, pg.nama, v.alamat_lengkap, p.status_pesanan, p.tanggal_pesanan
        FROM pesanan p
        JOIN pengguna pg ON p.pengguna_id_pengguna = pg.id_pengguna
        JOIN v_alamat_lengkap v ON p.alamat_pengiriman_id = v.id_alamat
        ORDER BY p.tanggal_pesanan DESC
    """)
    pesanan_list = cursor.fetchall()
    
    # Tampilkan dalam tabel jika ada data
    if pesanan_list:
        print("\n=== Status Pengiriman Semua Pesanan ===")
        print(tabulate(pesanan_list, 
                      headers=['ID Pesanan', 'Nama Pelanggan', 'Alamat Pengiriman', 'Status', 'Tanggal'], 
                      tablefmt='fancy_grid'))
    else:
        print(" Tidak ada pesanan.")


def buat_laporan_penjualan(cursor):
    """
    Fungsi untuk generate laporan penjualan per bulan
    Admin bisa lihat total penjualan dan detail transaksi
    """
    os.system('cls')
    
    # Input bulan dan tahun yang mau dilihat
    bulan = input("Masukkan bulan (MM): ")
    tahun = input("Masukkan tahun (YYYY): ")
    
    # Query transaksi berdasarkan bulan & tahun
    # EXTRACT(MONTH FROM ...) = ambil bulan dari tanggal
    # EXTRACT(YEAR FROM ...) = ambil tahun dari tanggal
    cursor.execute("""
        SELECT t.no_transaksi, p.nama, t.jumlah_dibayar, t.tanggal_transaksi
        FROM transaksi t
        JOIN pengguna p ON t.pengguna_id_pengguna = p.id_pengguna
        WHERE EXTRACT(MONTH FROM t.tanggal_transaksi) = %s 
        AND EXTRACT(YEAR FROM t.tanggal_transaksi) = %s
    """, (bulan, tahun))
    list_transaksi = cursor.fetchall()
    
    if list_transaksi:
        # Hitung total penjualan dengan sum semua jumlah_dibayar
        # t[2] = index ke-2 (jumlah_dibayar) dari setiap row
        total_penjualan = sum(t[2] for t in list_transaksi)
        
        print(f"\n💰 Total Penjualan Bulan {bulan}/{tahun}: Rp {total_penjualan:,}")
        print("\n=== Daftar Transaksi ===")
        print(tabulate(list_transaksi, 
                      headers=['No Transaksi', 'Nama Pelanggan', 'Jumlah Dibayar', 'Tanggal'], 
                      tablefmt='fancy_grid'))
    else:
        print(" Tidak ada transaksi di bulan tersebut.")


def lihat_baruan_teknisi(cursor):
    """
    Fungsi untuk admin melihat notifikasi dari teknisi
    Teknisi bisa input "ikan siap jual" yang masuk notifikasi ke admin
    Data disimpan di list global: pending_stok_updates
    """
    os.system('cls')
    
    # Cek apakah ada notifikasi dari teknisi
    if pending_stok_updates:  # pending_stok_updates = list global
        print("\n=== Inputan Tambahan Stok dari Teknisi ===")
        data = []  # List untuk menyimpan data yang akan ditampilkan
        
        # Loop setiap notifikasi
        for item in pending_stok_updates:
            # Query nama ikan berdasarkan id_ikan
            cursor.execute("SELECT nama_ikan FROM ikan WHERE id_ikan = %s", (item['id_ikan'],))
            result_ikan = cursor.fetchone()
            nama_ikan = result_ikan[0] if result_ikan else "Tidak ditemukan"
            
            # Query nama teknisi berdasarkan id_teknisi
            cursor.execute("SELECT nama FROM pengguna WHERE id_pengguna = %s", (item['id_teknisi'],))
            result_teknisi = cursor.fetchone()
            nama_teknisi = result_teknisi[0] if result_teknisi else "Tidak ditemukan"
            
            # Append data ke list untuk ditampilkan dalam tabel
            data.append([
                item['id_ikan'], 
                nama_ikan, 
                item['tambah_siap_jual'],  # Jumlah ikan siap jual
                nama_teknisi, 
                item['tanggal']  # Kapan teknisi input
            ])
        
        # Tampilkan dalam bentuk tabel
        print(tabulate(data, 
                      headers=['ID Ikan', 'Nama Ikan', 'Tambah Siap Jual', 'Nama Teknisi', 'Tanggal'], 
                      tablefmt='fancy_grid'))
    else:
        print(" Tidak ada inputan tambahan stok dari teknisi.")

def fitur_teknisi(cursor, id_pengguna, role):
    """
    Fungsi menu utama untuk role Teknisi
    Teknisi bertugas:
    1. Monitoring kondisi ikan (suhu air, pH, kesehatan)
    2. Input stok ikan yang siap jual
    """
    while True:
        os.system('cls')  # Clear screen
        print(f"\n=== Menu Teknisi (ID: {id_pengguna}) ===")
        print("1. Menginput Data Pemeliharaan")
        print("2. Logout ke Menu Utama")
        pilihan = input("Pilih opsi (1-2): ")

        if pilihan == '1':
            input_data_pemeliharaan(cursor, id_pengguna)  # Panggil fungsi input data
        elif pilihan == '2':
            print("Logout berhasil. Kembali ke menu utama.")
            break  # Keluar dari loop, kembali ke menu login
        else:
            print("Pilihan tidak valid!")


# === GLOBAL VARIABLE: List untuk menyimpan notifikasi ke admin ===
# Kenapa global? Karena perlu diakses oleh teknisi (append) dan admin (read)
# Alternatif: bisa pakai database tabel notifikasi, tapi ini contoh sederhana
pending_stok_updates = []


def input_data_pemeliharaan(cursor, id_pengguna):
    """
    Fungsi utama untuk teknisi mengelola data pemeliharaan ikan
    Fitur:
    1. Tambah monitoring (suhu, pH, kondisi)
    2. Input stok ikan siap jual (notifikasi ke admin)
    3. Update monitoring
    4. Lihat data monitoring
    5. Hapus monitoring
    """
    while True:
        print("\n" + "="*50)
        print("=== Menu Teknisi - Data Pemeliharaan ===")
        print("="*50)
        print("1. Tambah Data Monitoring")
        print("2. Input Stok Ikan Siap Jual")
        print("3. Update Data Monitoring")
        print("4. Lihat Data Monitoring")
        print("5. Hapus Data Monitoring")
        print("6. Menu Profil")
        print("7. Kembali")
        pilihan = input("Pilih opsi (1-7): ")
        
        # Clear screen untuk pilihan 1-5 (tampilan lebih bersih)
        if pilihan in ['1', '2', '3', '4', '5']:
            os.system('cls')
            
        if pilihan == '1':
            # === TAMBAH DATA MONITORING IKAN ===
            print("\n=== Tambah Data Monitoring ===")
    
            # Query: Tampilkan daftar ikan dengan JOIN jenis_ikan
            # Kenapa JOIN? Supaya teknisi tahu jenis ikannya (Arwana, Koi, dll)
            cursor.execute("""
                SELECT i.id_ikan, j.nama_ikan AS jenis, i.nama_ikan, i.stok
                FROM ikan i
                JOIN jenis_ikan j ON i.jenis_ikan_id_jenis_ikan = j.id_jenis_ikan
                ORDER BY i.id_ikan
            """)
            ikan_list = cursor.fetchall()
            
            # Validasi: apakah ada ikan di database?
            if ikan_list:
                print("\n--- Daftar Ikan ---")
                print(tabulate(ikan_list, headers=['ID', 'Jenis', 'Nama Ikan', 'Stok'], tablefmt='fancy_grid'))
            else:
                print("Tidak ada data ikan.")
                input("\nTekan Enter untuk kembali...")
                return  # Keluar dari fungsi jika tidak ada ikan
            
            # === INPUT ID IKAN ===
            id_ikan = input("\nMasukkan ID Ikan: ").strip()
            
            # Validasi: cek apakah ID ikan ada di database
            cursor.execute("SELECT nama_ikan FROM ikan WHERE id_ikan = %s", (id_ikan,))
            ikan_data = cursor.fetchone()
            
            if not ikan_data:
                print(" ID Ikan tidak ditemukan.")
                input("\nTekan Enter untuk kembali...")
                return
            
            nama_ikan = ikan_data[0]  # Ambil nama ikan
            print(f" Ikan dipilih: {nama_ikan}")
            
            # === INPUT TANGGAL MONITORING ===
            tanggal = input("\nMasukkan tanggal monitoring (YYYY-MM-DD): ").strip()

            # Validasi format tanggal
            try:
                datetime.strptime(tanggal, '%Y-%m-%d')  # Cek apakah format benar
            except:
                print(" Format tanggal salah (YYYY-MM-DD).")
                input("\nTekan Enter untuk kembali...")
                return
            
            # === CEK DUPLIKASI DATA ===
            # Cek apakah sudah ada data monitoring untuk tanggal & ikan yang sama
            # Kenapa? Supaya tidak ada data ganda (1 ikan, 1 tanggal, 1 data monitoring)
            cursor.execute("""
                SELECT id_monitoring FROM monitoring 
                WHERE tanggal_monitoring = %s AND ikan_id_ikan = %s
            """, (tanggal, id_ikan))
            
            if cursor.fetchone():
                print(f" Data monitoring untuk {nama_ikan} pada {tanggal} sudah ada.")
                input("\nTekan Enter untuk kembali...")
                return
            
            # === INPUT SUHU AIR ===
            # float() = desimal (27.5°C, 28.2°C)
            # Ikan hias hidup optimal di suhu 24-30°C
            suhu_air = float(input("Masukkan suhu air (°C): "))
            
            # === INPUT pH AIR ===
            # pH = tingkat keasaman air (0-14, 7 = netral)
            # Ikan hias optimal di pH 6.5-7.5
            ph_air = float(input("Masukkan pH air: "))
            
            # === INPUT KONDISI IKAN ===
            kondisi_ikan = input("Masukkan kondisi ikan (Sehat/Sakit): ").strip()
            
            # === INPUT CATATAN ===
            catatan = input("Masukkan catatan: ").strip()

            # === RINGKASAN DATA ===
            print("\n--- Ringkasan Data Monitoring ---")
            print(f"Ikan: {nama_ikan}")
            print(f"Tanggal: {tanggal}")
            print(f"Suhu Air: {suhu_air}°C")
            print(f"pH Air: {ph_air}")
            print(f"Kondisi: {kondisi_ikan}")
            print(f"Catatan: {catatan}")
            
            # === KONFIRMASI SIMPAN ===
            konfirmasi = input("\n✅ Simpan data monitoring? (Ya/Tidak): ").strip().lower()
            
            if konfirmasi == 'ya':
                try:
                    # INSERT ke tabel monitoring
                    cursor.execute("""
                        INSERT INTO monitoring (tanggal_monitoring, suhu_air, ph_air, kondisi_ikan, catatan, pengguna_id_pengguna, ikan_id_ikan) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (tanggal, suhu_air, ph_air, kondisi_ikan, catatan, id_pengguna, id_ikan))
                    
                    # COMMIT = simpan perubahan ke database
                    cursor.connection.commit()
                    
                    print("\n✅ Data monitoring berhasil disimpan!")
                except Exception as e:
                    # Jika error (misal: constraint violation), rollback
                    cursor.connection.rollback()
                    print(f"\n❌ Error saat menyimpan: {e}")
            else:
                print("\n❌ Penyimpanan dibatalkan.")
            
            input("\nTekan Enter untuk kembali...")

        elif pilihan == '2':
            # === INPUT STOK IKAN SIAP JUAL ===
            # Fitur ini: teknisi notifikasi admin bahwa ada ikan siap jual
            # Admin nanti yang approve dan tambah stok resmi di database
            print("\n=== Input Stok Ikan Siap Jual ===")
    
            # Query: Tampilkan daftar ikan
            cursor.execute("""
                SELECT i.id_ikan, j.nama_ikan AS jenis, i.nama_ikan, i.stok
                FROM ikan i
                JOIN jenis_ikan j ON i.jenis_ikan_id_jenis_ikan = j.id_jenis_ikan
                ORDER BY i.id_ikan
            """)
            ikan_list = cursor.fetchall()
            
            if ikan_list:
                print("\n--- Daftar Ikan ---")
                print(tabulate(ikan_list, headers=['ID', 'Jenis', 'Nama Ikan', 'Stok Saat Ini'], tablefmt='fancy_grid'))
            else:
                print("Tidak ada data ikan.")
                input("\nTekan Enter untuk kembali...")
                return
            
            # Input ID Ikan
            id_ikan = input("\nMasukkan ID Ikan: ").strip()
            
            # Query: Ambil nama ikan dan stok saat ini
            cursor.execute("SELECT nama_ikan, stok FROM ikan WHERE id_ikan = %s", (id_ikan,))
            ikan_data = cursor.fetchone()
            
            if not ikan_data:
                print(" ID Ikan tidak ditemukan.")
                input("\nTekan Enter untuk kembali...")
                return
            
            nama_ikan, stok_sekarang = ikan_data  # Unpack tuple
            print(f"\n📦 Ikan: {nama_ikan}")
            print(f"📊 Stok saat ini: {stok_sekarang}")
            
            # === INPUT JUMLAH IKAN SIAP JUAL ===
            tambah_siap_jual = int(input("\nMasukkan jumlah ikan siap jual yang akan ditambahkan: "))
            
            # Validasi: jumlah harus > 0
            # BUG di kode asli: `if not tambah_siap_jual == 0:` salah logika
            # Seharusnya: `if tambah_siap_jual <= 0:`
            if tambah_siap_jual <= 0:
                print(" Jumlah harus lebih dari 0.")
                input("\nTekan Enter untuk kembali...")
                return
            
            # Hitung stok baru (proyeksi, belum di-save ke database)
            stok_baru = stok_sekarang + tambah_siap_jual
            print(f"\n📈 Stok setelah ditambah: {stok_baru}")
            
            # Catatan tambahan (opsional)
            catatan = input("Catatan tambahan (opsional): ").strip()
            
            # === RINGKASAN ===
            print("\n--- Ringkasan Tambahan Stok ---")
            print(f"Ikan: {nama_ikan}")
            print(f"Stok Saat Ini: {stok_sekarang}")
            print(f"Tambahan: +{tambah_siap_jual}")
            print(f"Stok Baru: {stok_baru}")
            if catatan:
                print(f"Catatan: {catatan}")
            
            # === KONFIRMASI KIRIM NOTIFIKASI ===
            konfirmasi = input("\n✅ Kirim notifikasi ke admin? (Ya/Tidak): ").strip().lower()
            
            if konfirmasi == 'ya':
                # === SIMPAN KE LIST PENDING (GLOBAL VARIABLE) ===
                # Kenapa tidak langsung update database?
                # Karena perlu approval admin dulu (quality control)
                pending_stok_updates.append({
                    'id_ikan': id_ikan,
                    'nama_ikan': nama_ikan,
                    'stok_lama': stok_sekarang,
                    'tambah_siap_jual': tambah_siap_jual,
                    'stok_baru': stok_baru,
                    'id_teknisi': id_pengguna,  # Siapa teknisi yang input
                    'tanggal': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Kapan di-input
                    'catatan': catatan
                })
                
                print("\n✅ Notifikasi berhasil dikirim ke admin!")  
            else:
                print("\n❌ Pengiriman dibatalkan.")
            
            input("\nTekan Enter untuk kembali...")

        elif pilihan == '3':
            # === UPDATE DATA MONITORING ===
            
            # Query: Ambil semua data monitoring milik teknisi ini
            # Kenapa WHERE pengguna_id? Supaya teknisi hanya bisa edit data sendiri
            cursor.execute("""
                SELECT m.id_monitoring, m.tanggal_monitoring, m.suhu_air, m.ph_air, 
                       m.kondisi_ikan, m.catatan, i.nama_ikan
                FROM monitoring m
                JOIN ikan i ON m.ikan_id_ikan = i.id_ikan
                WHERE m.pengguna_id_pengguna = %s
                ORDER BY m.id_monitoring
            """, (id_pengguna,))
            data_list = cursor.fetchall()
    
            # Validasi: apakah ada data?
            if not data_list:
                print("\n❌ Tidak ada data pemeliharaan untuk diupdate.")
                input("Tekan Enter untuk kembali...")
                continue  # Kembali ke menu pilihan

            # Tampilkan data monitoring
            print("\n=== Data Pemeliharaan Anda ===")
            print(tabulate(data_list, 
                    headers=['ID', 'Tanggal', 'Suhu (°C)', 'pH', 'Kondisi', 'Catatan', 'Nama Ikan'], 
                    tablefmt='fancy_grid'))
            
            id_monitoring = input("\n📝 Masukkan ID Monitoring yang ingin diupdate: ")
    
            # === CEK KEPEMILIKAN DATA ===
            # Cek apakah data monitoring ini milik teknisi yang login
            # Kenapa? Supaya teknisi A tidak bisa edit data teknisi B
            cursor.execute("""
                SELECT m.tanggal_monitoring, m.suhu_air, m.ph_air, m.kondisi_ikan, m.catatan, i.nama_ikan
                FROM monitoring m
                JOIN ikan i ON m.ikan_id_ikan = i.id_ikan
                WHERE m.id_monitoring = %s AND m.pengguna_id_pengguna = %s
            """, (id_monitoring, id_pengguna))
    
            data_lama = cursor.fetchone()

            if not data_lama:
                print(" Data tidak ditemukan atau bukan milik Anda.")
                input("Tekan Enter untuk kembali...")
                continue

            # Unpack data lama
            tanggal_lama, suhu_lama, ph_lama, kondisi_lama, catatan_lama, nama_ikan = data_lama
            
            # Tampilkan data saat ini
            print(f"\n--- Data Saat Ini ---")
            print(f"Ikan: {nama_ikan}")
            print(f"Tanggal: {tanggal_lama}")
            print(f"Suhu Air: {suhu_lama}°C")
            print(f"pH Air: {ph_lama}")
            print(f"Kondisi: {kondisi_lama}")
            print(f"Catatan: {catatan_lama}")

            # === INPUT DATA BARU ===
            # Jika kosongkan = pakai data lama (tidak berubah)
            print("\n=== Masukkan Data Baru (kosongkan jika tidak ingin diupdate) ===")

            tanggal_baru = input(f"Tanggal baru (YYYY-MM-DD) [{tanggal_lama}]: ").strip()
            suhu_baru = input(f"Suhu air baru (24-28°C) [{suhu_lama}]: ").strip()
            ph_baru = input(f"pH air baru (6.5-7.5) [{ph_lama}]: ").strip()
            kondisi_baru = input(f"Kondisi ikan baru (Sehat/Sakit) [{kondisi_lama}]: ").strip()
            catatan_baru = input(f"Catatan baru [{catatan_lama}]: ").strip()

            # === KONFIRMASI UPDATE ===
            konfirmasi = input("\n✅ Yakin ingin update? (Ya/Tidak): ").strip().lower()

            if konfirmasi == 'ya':
                try:
                    # UPDATE monitoring
                    # Jika input kosong, SQL akan set NULL (perlu handle di aplikasi)
                    # Solusi: bisa pakai COALESCE di SQL atau logic Python
                    cursor.execute("""
                        UPDATE monitoring 
                        SET tanggal_monitoring = %s, 
                            suhu_air = %s, 
                            ph_air = %s, 
                            kondisi_ikan = %s, 
                            catatan = %s,
                            waktu_dibuat = CURRENT_TIMESTAMP
                        WHERE id_monitoring = %s
                    """, (tanggal_baru or tanggal_lama,  # Jika kosong, pakai yang lama
                          suhu_baru or suhu_lama, 
                          ph_baru or ph_lama, 
                          kondisi_baru or kondisi_lama, 
                          catatan_baru or catatan_lama, 
                          id_monitoring))
            
                    # COMMIT perubahan
                    cursor.connection.commit()
            
                    print("\n✅ Data pemeliharaan berhasil diupdate!")
                except Exception as e:
                    # Rollback jika error
                    cursor.connection.rollback()
                    print(f"\n❌ Error saat update: {e}")
            else:
                print("\n❌ Update dibatalkan.")
            
            input("\nTekan Enter untuk kembali...")

        elif pilihan == '4':
            # === LIHAT DATA MONITORING ===
            
            # Query: Ambil semua data monitoring milik teknisi ini
            cursor.execute("""
                SELECT m.id_monitoring, m.tanggal_monitoring, m.suhu_air, m.ph_air, 
                       m.kondisi_ikan, m.catatan, i.nama_ikan
                FROM monitoring m
                JOIN ikan i ON m.ikan_id_ikan = i.id_ikan
                WHERE m.pengguna_id_pengguna = %s
            """, (id_pengguna,))
            data_list = cursor.fetchall()
            
            # Tampilkan dalam tabel
            if data_list:
                print("\n=== Data Pemeliharaan ===")
                print(tabulate(data_list, 
                              headers=['ID Monitoring', 'Tanggal', 'Suhu Air', 'pH Air', 'Kondisi Ikan', 'Catatan', 'Nama Ikan'], 
                              tablefmt='fancy_grid'))
            else:
                print(" Tidak ada data pemeliharaan.")

        elif pilihan == '5':
            # === HAPUS DATA MONITORING ===
            
            # Query: Ambil semua data monitoring
            # BUG di kode asli: variable `ikan_list` harusnya `monitoring_list`
            cursor.execute("SELECT id_monitoring, tanggal_monitoring, pengguna_id_pengguna FROM monitoring ORDER BY id_monitoring")
            monitoring_list = cursor.fetchall()
            
            if not monitoring_list:
                print(" Tidak ada data monitoring di database.")
                input("\nTekan Enter untuk kembali...")
                continue
            
            print("\n--- Daftar Monitoring ---")
            print(tabulate(monitoring_list, headers=['ID', 'Tanggal Monitoring', 'ID Pengguna'], tablefmt='fancy_grid'))
            
            # Input ID monitoring yang mau dihapus
            id_monitoring = input("\nMasukkan ID Monitoring yang ingin dihapus: ")
            
            try:
                # DELETE dari database
                cursor.execute("DELETE FROM monitoring WHERE id_monitoring = %s", (id_monitoring,))
                
                # COMMIT perubahan
                cursor.connection.commit()
                print(" Hapus data berhasil!")
            except Exception as e:
                # Rollback jika error
                cursor.connection.rollback()
                print(f" Error saat menghapus: {e}")

        elif pilihan == '6':
            # Menu profil (edit profil teknisi)
            menu_profil(cursor, id_pengguna)

        elif pilihan == '7':
            break  # Kembali ke menu teknisi utama
        else:
            print(" Pilihan tidak valid!")
        
        input("Tekan Enter untuk kembali...")






def fitur_ceo(cursor, id_pengguna, role):
    """
    Fungsi menu utama untuk role CEO
    CEO memiliki akses penuh untuk:
    1. Melihat dashboard/homepage bisnis
    2. Monitoring performa ikan (semua teknisi)
    3. Laporan penjualan
    4. Data semua pengguna
    5. Edit profil sendiri
    """
    while True:
        os.system('cls')  # Clear screen
        print(f"\n=== Menu CEO (ID: {id_pengguna}) ===")
        print("1. Homepage")
        print("2. Memantau Performa Ikan")
        print("3. Memantau Laporan Penjualan")
        print("4. Lihat Data Pengguna")  
        print("5. Menu profil")
        print("6. Logout ke Menu Utama")
        pilihan = input("Pilih opsi (1-6): ")

        # Routing berdasarkan pilihan
        if pilihan == '1':
            homepage_ceo(cursor)  # Dashboard CEO
            input("enter jika ingin kembali")
        elif pilihan == '2':
            pantau_performa_ikan(cursor)  # Monitoring ikan (semua teknisi)
        elif pilihan == '3':
            pantau_laporan_penjualan(cursor)  # Laporan penjualan per bulan
        elif pilihan == '4':
            lihat_data_pengguna(cursor)  # Data semua user (CEO/Admin/Teknisi/Pelanggan)
        elif pilihan == '5':
            menu_profil(cursor, id_pengguna)  # Edit profil CEO
        elif pilihan == '6':
            print("Logout berhasil. Kembali ke Menu Utama.")
            break  # Keluar dari loop, kembali ke menu login
        else:
            print("Pilihan tidak valid!")


def homepage_ceo(cursor):
    """
    Dashboard CEO: Ringkasan bisnis dalam 1 layar
    Menampilkan KPI (Key Performance Indicator):
    1. Total produk ikan yang tersedia
    2. Penjualan hari ini (real-time)
    3. Pesanan yang menunggu konfirmasi
    """
    os.system('cls')
    
    # === KPI 1: TOTAL IKAN ===
    # Query: Hitung jumlah total produk ikan di katalog
    cursor.execute("SELECT COUNT(*) FROM ikan")
    total_ikan = cursor.fetchone()[0]  # fetchone() return tuple, ambil index 0
    
    # === KPI 2: PENJUALAN HARI INI ===
    # Query: SUM semua transaksi yang tanggalnya = hari ini
    today = datetime.now().date()  # Ambil tanggal hari ini (tanpa waktu)
    cursor.execute("SELECT SUM(jumlah_dibayar) FROM transaksi WHERE DATE(tanggal_transaksi) = %s", (today,))
    penjualan_hari_ini = cursor.fetchone()[0] or 0  # Jika NULL (tidak ada transaksi), set 0
    
    # === KPI 3: PESANAN PENDING ===
    # Query: Hitung pesanan yang belum dikonfirmasi admin
    # Status 'Pending' = pelanggan sudah bayar, tapi admin belum approve
    cursor.execute("SELECT COUNT(*) FROM pesanan WHERE status_pesanan = 'Pending'")
    pesanan_pending = cursor.fetchone()[0]
    
    # === TAMPILKAN DASHBOARD ===
    print("\n=== Homepage CEO ===")
    print(f" Total Ikan: {total_ikan}")
    print(f"💰 Penjualan Hari Ini: Rp {penjualan_hari_ini:,}")
    print(f"⏳ Pesanan Pending: {pesanan_pending}")
    

def pantau_performa_ikan(cursor):
    """
    Fungsi untuk CEO memantau kondisi semua ikan
    CEO bisa lihat data monitoring dari SEMUA teknisi (tidak terbatas)
    Berbeda dengan teknisi yang hanya bisa lihat data sendiri
    """
    os.system('cls')
    
    # === Query: Ambil SEMUA data monitoring ===
    # JOIN ikan = untuk nama ikan
    # JOIN pengguna = untuk nama teknisi yang input
    # TIDAK ADA WHERE = CEO akses semua data (tidak filtered by user)
    cursor.execute("""
        SELECT m.id_monitoring, m.tanggal_monitoring, m.suhu_air, m.ph_air, 
               m.kondisi_ikan, m.catatan, i.nama_ikan, p.nama as nama_peternak
        FROM monitoring m
        JOIN ikan i ON m.ikan_id_ikan = i.id_ikan
        JOIN pengguna p ON m.pengguna_id_pengguna = p.id_pengguna
    """)
    data_list = cursor.fetchall()
    
    # Tampilkan dalam tabel
    if data_list:
        print("\n=== Data Performa Ikan (Semua Teknisi) ===")
        print(tabulate(data_list, 
                      headers=['ID', 'Tanggal', 'Suhu (°C)', 'pH', 'Kondisi', 'Catatan', 'Nama Ikan', 'Teknisi'], 
                      tablefmt='fancy_grid'))
    else:
        print(" Tidak ada data performa ikan.")
    
    input("Tekan Enter untuk kembali...")


def pantau_laporan_penjualan(cursor):
    """
    Fungsi untuk CEO melihat laporan penjualan per bulan
    Fitur:
    1. Input bulan & tahun
    2. Tampilkan total penjualan
    3. Detail semua transaksi di bulan tersebut
    """
    os.system('cls')
    
    # Input periode laporan
    bulan = input("Masukkan bulan (MM): ")
    tahun = input("Masukkan tahun (YYYY): ")
    
    # === Query: Ambil transaksi berdasarkan bulan & tahun ===
    # EXTRACT(MONTH FROM ...) = ekstrak bulan dari tanggal (1-12)
    # EXTRACT(YEAR FROM ...) = ekstrak tahun dari tanggal (2025, 2024, dll)
    cursor.execute("""
        SELECT t.no_transaksi, p.nama, t.jumlah_dibayar, t.tanggal_transaksi
        FROM transaksi t
        JOIN pengguna p ON t.pengguna_id_pengguna = p.id_pengguna
        WHERE EXTRACT(MONTH FROM t.tanggal_transaksi) = %s 
        AND EXTRACT(YEAR FROM t.tanggal_transaksi) = %s
    """, (bulan, tahun))
    transaksi_list = cursor.fetchall()
    
    if transaksi_list:
        # === Hitung Total Penjualan ===
        # sum() = jumlahkan semua nilai
        # t[2] = index ke-2 dari tuple (jumlah_dibayar)
        total_penjualan = sum(t[2] for t in transaksi_list)
        
        print(f"\n💰 Total Penjualan Bulan {bulan}/{tahun}: Rp {total_penjualan:,}")
        print("\n=== Daftar Transaksi ===")
        print(tabulate(transaksi_list, 
                      headers=['No Transaksi', 'Nama Pelanggan', 'Jumlah Dibayar', 'Tanggal'], 
                      tablefmt='fancy_grid'))
    else:
        print(f" Tidak ada transaksi di bulan {bulan}/{tahun}.")
    
    input("Tekan Enter untuk kembali...")


def menu_profil(cursor, id_pengguna):
    """
    Fungsi untuk semua user (CEO/Admin/Teknisi/Pelanggan) mengelola profil
    Fitur:
    1. Lihat profil (dengan alamat lengkap dari VIEW)
    2. Update data profil (nama, email, password)
    3. Update alamat (terpisah karena struktur kompleks)
    """
    while True:
        os.system('cls')
        print("\n=== Menu Profil ===")
        print("1. Lihat Profil")
        print("2. Update Profil")
        print("3. Update Alamat")
        print("4. Kembali")
        pilihan = input("Pilih opsi (1-4): ")
        
        if pilihan == '1':
            # === LIHAT PROFIL ===
            
            # Query: JOIN dengan VIEW v_alamat_lengkap
            # LEFT JOIN = karena user baru belum tentu isi alamat (nullable)
            # COALESCE(..., 'Belum diisi') = jika NULL, tampilkan "Belum diisi"
            cursor.execute("""
                SELECT p.nama, p.username, p.email, p.no_telpon, 
                       COALESCE(v.alamat_lengkap, 'Belum diisi') as alamat,
                       ur.nama_role, p.waktu_dibuat, p.waktu_update 
                FROM pengguna p
                JOIN user_role ur ON p.user_role_id_role = ur.id_role
                LEFT JOIN v_alamat_lengkap v ON p.alamat_id = v.id_alamat
                WHERE p.id_pengguna = %s
            """, (id_pengguna,))  
    
            profil = cursor.fetchone()
            
            if profil:
                # Unpack tuple hasil query
                nama, username, email, no_telpon, alamat, role, waktu_dibuat, waktu_update = profil
                
                # Tampilkan profil
                print("\n--- Profil Anda ---")
                print(f"👤 Nama: {nama}")
                print(f"🔑 Username: {username}")
                print(f"📧 Email: {email}")
                print(f"📱 No Telpon: {no_telpon}")
                print(f"🏠 Alamat: {alamat}")
                print(f"👔 Role: {role}")
                print(f"📅 Waktu Dibuat: {waktu_dibuat}")
                print(f"🔄 Waktu Update Terakhir: {waktu_update}")
            
        elif pilihan == '2':
            # === UPDATE PROFIL (Nama, Email, Password) ===
            
            print("\n=== Update Profil ===")
            print("Kosongkan jika tidak ingin mengubah")
            
            # Input data baru (optional - bisa dikosongkan)
            nama_baru = input("Nama baru: ").strip()
            email_baru = input("Email baru: ").strip()
            password_baru = input("Password baru (minimal 8 karakter): ").strip()
            
            # === VALIDASI PASSWORD BARU ===
            if password_baru:
                # Validasi 1: Minimal 8 karakter
                if len(password_baru) < 8:
                    print(" Password minimal 8 karakter!")
                    continue  # Kembali ke menu profil
                
                # Validasi 2: Password baru tidak boleh sama dengan password lama
                cursor.execute("SELECT password FROM pengguna WHERE id_pengguna = %s", (id_pengguna,))
                password_lama_row = cursor.fetchone()
                password_lama = password_lama_row[0] if password_lama_row else None
                
                # Loop sampai password baru berbeda dengan password lama
                while password_baru == password_lama:
                    print(" Password baru tidak boleh sama dengan password lama!")
                    password_baru = input("Password baru (minimal 8 karakter): ").strip()
                    if not password_baru or len(password_baru) < 8:
                        print(" Password minimal 8 karakter!")
                        break
            
            # === VALIDASI EMAIL BARU ===
            if email_baru:
                # Validasi 1: Email baru tidak boleh sama dengan email lama
                cursor.execute("SELECT email FROM pengguna WHERE id_pengguna = %s", (id_pengguna,))
                email_lama_row = cursor.fetchone()
                email_lama = email_lama_row[0] if email_lama_row else None
                
                while email_baru == email_lama:
                    print(" Email baru tidak boleh sama dengan email lama!")
                    email_baru = input("Email baru: ").strip()
                    if not email_baru:
                        print(" Email tidak boleh kosong!")
                        break
                
                # Validasi 2: Email harus unik (tidak dipakai user lain)
                cursor.execute("SELECT id_pengguna FROM pengguna WHERE email = %s AND id_pengguna != %s", 
                             (email_baru, id_pengguna))
                if cursor.fetchone():
                    print(" Email sudah digunakan oleh user lain!")
                    continue
            
            # === KONFIRMASI UPDATE ===
            konfirmasi = input("\n✅ Yakin ingin update profil? (Ya/Tidak): ").strip().lower()
            if konfirmasi != 'ya':
                print(" Update dibatalkan.")
                continue
            
            # === UPDATE DATABASE ===
            # COALESCE(%s, nama) = jika %s NULL, pakai nilai 'nama' yang lama
            # Kenapa pakai COALESCE? Karena ada field yang mungkin tidak diisi (dikosongkan)
            waktu_update = datetime.now()
            cursor.execute("""
                UPDATE pengguna 
                SET nama = COALESCE(%s, nama), 
                    email = COALESCE(%s, email),  
                    password = COALESCE(%s, password), 
                    waktu_update = %s 
                WHERE id_pengguna = %s
            """, (nama_baru or None,  # Jika kosong, kirim None ke SQL
                  email_baru or None, 
                  password_baru or None, 
                  waktu_update, 
                  id_pengguna))
            
            # COMMIT perubahan ke database
            cursor.connection.commit()
            print(" Profil berhasil diupdate!")

        elif pilihan == '3':
            # === UPDATE ALAMAT ===
            # Kenapa terpisah? Karena struktur alamat kompleks (hierarki wilayah)
            
            print("\n--- Update Alamat ---")
            
            # === CEK APAKAH USER SUDAH PUNYA ALAMAT ===
            cursor.execute("SELECT alamat_id FROM pengguna WHERE id_pengguna = %s", (id_pengguna,))
            alamat_result = cursor.fetchone()
            alamat_id_lama = alamat_result[0] if alamat_result else None
            
            # === PILIH KABUPATEN ===
            cursor.execute("SELECT id_kabupaten, nama_kabupaten FROM kabupaten ORDER BY nama_kabupaten")
            kabupaten_list = cursor.fetchall()
            print("\nPilih Kabupaten:")
            for kab in kabupaten_list:
                print(f"{kab[0]}. {kab[1]}")
            kabupaten_id = input("Pilih ID Kabupaten: ")
            
            # === PILIH KECAMATAN (filtered by kabupaten) ===
            cursor.execute("SELECT id_kecamatan, nama_kecamatan FROM kecamatan WHERE kabupaten_id = %s ORDER BY nama_kecamatan", 
                         (kabupaten_id,))
            kecamatan_list = cursor.fetchall()
            
            # Validasi: apakah ada kecamatan di kabupaten ini?
            if not kecamatan_list:
                print(" Tidak ada kecamatan di kabupaten ini!")
                continue
            
            print("\nPilih Kecamatan:")
            for kec in kecamatan_list:
                print(f"{kec[0]}. {kec[1]}")
            kecamatan_id = input("Pilih ID Kecamatan: ")
            
            # === PILIH DESA (filtered by kecamatan) ===
            cursor.execute("SELECT id_desa, nama_desa FROM desa WHERE kecamatan_id = %s ORDER BY nama_desa", 
                         (kecamatan_id,))
            desa_list = cursor.fetchall()
            
            # Validasi: apakah ada desa di kecamatan ini?
            if not desa_list:
                print(" Tidak ada desa di kecamatan ini!")
                continue
            
            print("\nPilih Desa:")
            for ds in desa_list:
                print(f"{ds[0]}. {ds[1]}")
            desa_id = input("Pilih ID Desa: ")
            
            # === INPUT DETAIL ALAMAT ===
            nama_jalan = input("Masukkan nama jalan & nomor rumah: ")
            rt_rw = input("Masukkan RT/RW (contoh: 02/05): ")
            kode_pos = input("Masukkan kode pos: ")
            catatan_alamat = input("Catatan alamat (opsional): ")
            
            # === UPDATE ATAU INSERT? ===
            if alamat_id_lama:
                # Jika sudah punya alamat, UPDATE alamat yang lama
                cursor.execute("""
                    UPDATE alamat 
                    SET nama_jalan = %s, rt_rw = %s, desa_id = %s, kode_pos = %s, 
                        catatan_alamat = %s, waktu_update = %s
                    WHERE id_alamat = %s
                """, (nama_jalan, rt_rw, desa_id, kode_pos, catatan_alamat, datetime.now(), alamat_id_lama))
                print(" Alamat berhasil diupdate!")
            else:
                # Jika belum punya alamat, INSERT alamat baru
                cursor.execute("""
                    INSERT INTO alamat (nama_jalan, rt_rw, desa_id, kode_pos, catatan_alamat)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id_alamat
                """, (nama_jalan, rt_rw, desa_id, kode_pos, catatan_alamat))
                alamat_id_baru = cursor.fetchone()[0]  # Ambil ID alamat yang baru dibuat
                
                # Update tabel pengguna: link user ke alamat baru
                cursor.execute("UPDATE pengguna SET alamat_id = %s, waktu_update = %s WHERE id_pengguna = %s", 
                             (alamat_id_baru, datetime.now(), id_pengguna))
                print(" Alamat berhasil ditambahkan!")
            
            # COMMIT perubahan
            cursor.connection.commit()
            
        elif pilihan == '4':
            break  # Kembali ke menu utama (CEO/Admin/Teknisi/Pelanggan)
        else:
            print(" Pilihan tidak valid!")
        
        input("Tekan Enter untuk kembali...")


def lihat_data_pengguna(cursor):
    """
    Fungsi untuk CEO/Admin melihat data semua pengguna
    Fitur:
    1. Lihat semua pengguna
    2. Filter berdasarkan role (CEO/Admin/Teknisi/Pelanggan)
    3. Search by username
    4. Filter berdasarkan kabupaten
    """
    while True:
        os.system('cls')
        print("\n=== Data Pengguna Terdaftar ===")
        print("1. Lihat Semua Pengguna")
        print("2. Cari Pengguna Berdasarkan Role")
        print("3. Cari Pengguna Berdasarkan Username")
        print("4. Cari Berdasarkan Kabupaten")
        print("5. Kembali")
        pilihan = input("Pilih opsi (1-5): ")
        
        if pilihan == '1':
            # === LIHAT SEMUA PENGGUNA ===
            
            # Query: JOIN dengan VIEW v_alamat_lengkap
            # LEFT JOIN = karena tidak semua user isi alamat
            # COALESCE = jika alamat NULL, tampilkan "Belum diisi"
            cursor.execute("""
                SELECT p.id_pengguna, p.nama, p.username, p.email, p.no_telpon, 
                       COALESCE(v.alamat_lengkap, 'Belum diisi') as alamat,
                       ur.nama_role, p.waktu_dibuat, p.waktu_update
                FROM pengguna p
                JOIN user_role ur ON p.user_role_id_role = ur.id_role
                LEFT JOIN v_alamat_lengkap v ON p.alamat_id = v.id_alamat
                ORDER BY p.id_pengguna
            """)
            pengguna_list = cursor.fetchall()
            
            if pengguna_list:
                print("\n--- Daftar Semua Pengguna ---")
                print(tabulate(pengguna_list, 
                             headers=['ID', 'Nama', 'Username', 'Email', 'No Telpon', 'Alamat', 
                                     'Role', 'Waktu Dibuat', 'Update Terakhir'], 
                             tablefmt='fancy_grid'))
                print(f"\n📊 Total Pengguna: {len(pengguna_list)}")
            else:
                print(" Tidak ada pengguna terdaftar.")
                
        elif pilihan == '2':
            # === FILTER BERDASARKAN ROLE ===
            
            # Tampilkan pilihan role
            print("\n=== Pilih Role ===")
            cursor.execute("SELECT id_role, nama_role FROM user_role")
            roles = cursor.fetchall()
            for role in roles:
                print(f"{role[0]}. {role[1]}")
            
            role_id = input("Masukkan ID Role: ").strip()
            
            # Query: Filter pengguna by role_id
            # WHERE p.user_role_id_role = %s = hanya ambil user dengan role tertentu
            cursor.execute("""
                SELECT p.id_pengguna, p.nama, p.username, p.email, p.no_telpon, 
                       COALESCE(v.alamat_lengkap, 'Belum diisi') as alamat,
                       ur.nama_role, p.waktu_dibuat, p.waktu_update
                FROM pengguna p
                JOIN user_role ur ON p.user_role_id_role = ur.id_role
                LEFT JOIN v_alamat_lengkap v ON p.alamat_id = v.id_alamat
                WHERE p.user_role_id_role = %s
                ORDER BY p.id_pengguna
            """, (role_id,))
            pengguna_list = cursor.fetchall()
            
            if pengguna_list:
                print(f"\n--- Pengguna dengan Role {pengguna_list[0][6]} ---")
                print(tabulate(pengguna_list, 
                             headers=['ID', 'Nama', 'Username', 'Email', 'No Telpon', 'Alamat', 
                                     'Role', 'Waktu Dibuat', 'Update Terakhir'], 
                             tablefmt='fancy_grid'))
                print(f"\n📊 Total: {len(pengguna_list)} pengguna")
            else:
                print(" Tidak ada pengguna dengan role tersebut.")
            input("Tekan Enter untuk kembali...")
            
        elif pilihan == '3':
            # === SEARCH BY USERNAME ===
            
            username_cari = input("Masukkan username yang dicari: ").strip()
            
            # Query: ILIKE = case-insensitive LIKE (tidak peduli huruf besar/kecil)
            # %{username_cari}% = wildcard search (cari yang mengandung keyword)
            # Contoh: cari "admin" → ketemu "admin123", "superadmin", dll
            cursor.execute("""
                SELECT p.id_pengguna, p.nama, p.username, p.email, p.no_telpon, 
                       COALESCE(v.alamat_lengkap, 'Belum diisi') as alamat,
                       ur.nama_role, p.waktu_dibuat, p.waktu_update
                FROM pengguna p
                JOIN user_role ur ON p.user_role_id_role = ur.id_role
                LEFT JOIN v_alamat_lengkap v ON p.alamat_id = v.id_alamat
                WHERE p.username ILIKE %s
            """, (f'%{username_cari}%',))
            pengguna_list = cursor.fetchall()
            
            if pengguna_list:
                print(f"\n--- Hasil Pencarian '{username_cari}' ---")
                print(tabulate(pengguna_list, 
                             headers=['ID', 'Nama', 'Username', 'Email', 'No Telpon', 'Alamat', 
                                     'Role', 'Waktu Dibuat', 'Update Terakhir'], 
                             tablefmt='fancy_grid'))
            else:
                print(f" Tidak ada pengguna dengan username '{username_cari}'.")
            input("Tekan Enter untuk kembali...")

        elif pilihan == '4':
            # === FILTER BERDASARKAN KABUPATEN ===
            
            # Tampilkan pilihan kabupaten
            cursor.execute("SELECT id_kabupaten, nama_kabupaten FROM kabupaten ORDER BY nama_kabupaten")
            kabupaten_list = cursor.fetchall()
            print("\nPilih Kabupaten:")
            for kab in kabupaten_list:
                print(f"{kab[0]}. {kab[1]}")
            
            kabupaten_id = input("Masukkan ID Kabupaten: ").strip()
            
            # Query: Filter user by kabupaten
            # Trik: JOIN v_alamat_lengkap untuk akses nama_kabupaten
            # WHERE v.nama_kabupaten = (SELECT ...) = filter by nama kabupaten
            cursor.execute("""
                SELECT p.id_pengguna, p.nama, p.username, p.email, p.no_telpon, 
                       v.alamat_lengkap, ur.nama_role
                FROM pengguna p
                JOIN user_role ur ON p.user_role_id_role = ur.id_role
                JOIN v_alamat_lengkap v ON p.alamat_id = v.id_alamat
                WHERE v.nama_kabupaten = (SELECT nama_kabupaten FROM kabupaten WHERE id_kabupaten = %s)
                ORDER BY p.id_pengguna
            """, (kabupaten_id,))
            pengguna_list = cursor.fetchall()
            
            if pengguna_list:
                print(f"\n--- Pengguna di Kabupaten ---")
                print(tabulate(pengguna_list, 
                             headers=['ID', 'Nama', 'Username', 'Email', 'No Telpon', 'Alamat', 'Role'], 
                             tablefmt='fancy_grid'))
                print(f"\n📊 Total: {len(pengguna_list)} pengguna")
            else:
                print(" Tidak ada pengguna di kabupaten tersebut.")

        elif pilihan == '5':
            break  # Kembali ke menu CEO/Admin
        else:
            print(" Pilihan tidak valid!")
        
        input("Tekan Enter untuk kembali...")


if __name__ == "__main__":
    """
    Entry point program
    Jika file ini dijalankan langsung (bukan di-import), maka jalankan menu_utama()
    """
    menu_utama()  # Panggil fungsi menu login/registrasi
