from datetime import datetime

tugas_list = []


class Tugas:
    def __init__(self, nama, matkul, deadline, prioritas, jenis, tipe):
        self.nama = nama
        self.matkul = matkul
        self.deadline = deadline
        self.prioritas = int(prioritas)
        self.jenis = jenis
        self.tipe = tipe

    def hitung_skor(self):
        skor = self.prioritas * 10

        hari_tersisa = (self.deadline - datetime.now()).days

        if hari_tersisa <= 1:
            skor += 50
        elif hari_tersisa <= 3:
            skor += 30
        elif hari_tersisa <= 7:
            skor += 15

        if self.tipe == 'besar':
            skor += 10
        if self.jenis == 'mandiri':
            skor += 5

        return skor

    def __str__(self):
        return (f"{self.nama} ({self.matkul}) | "
                f"Deadline: {self.deadline.strftime('%d/%m/%Y')} | "
                f"Prioritas: {self.prioritas} | {self.jenis.title()} | "
                f"Tipe: {self.tipe.title()} | Skor: {self.hitung_skor()}")


def tampilkan_menu():
    print("\n" + "=" * 50)
    print("    PENJADWAL TUGAS KULIAH - GREEDY ALGORITHM")
    print("=" * 50)
    print("1. Tambah Tugas Baru")
    print("2. Lihat Semua Tugas")
    print("3. Lihat Jadwal Prioritas (Greedy)")
    print("4. Cek Deadline Mendesak")
    print("5. Hapus Tugas")
    print("6. Keluar")
    print("=" * 50)
    print("💡 Tips: Ketik '0' atau 'menu' untuk kembali ke menu utama kapan saja")


def kembali_ke_menu():
    """Fungsi untuk menangani input kembali ke menu"""
    while True:
        pilihan = input("\n📍 Tekan Enter untuk kembali ke menu utama, atau ketik 'x' untuk keluar: ").strip().lower()
        if pilihan == '' or pilihan == '0' or pilihan == 'menu':
            return 'menu'
        elif pilihan == 'x' or pilihan == 'exit' or pilihan == 'keluar':
            return 'exit'
        else:
            print("❌ Input tidak valid! Tekan Enter untuk menu utama atau 'x' untuk keluar.")


def input_dengan_escape(prompt, allow_empty=False):
    """Input dengan kemampuan escape ke menu utama"""
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() in ['0', 'menu']:
            return 'BACK_TO_MENU'
        if user_input.lower() in ['x', 'exit', 'keluar']:
            return 'EXIT'
        if not allow_empty and not user_input:
            print("❌ Input tidak boleh kosong! (Ketik '0' untuk kembali ke menu)")
            continue
        return user_input


def input_tanggal():
    while True:
        try:
            print("Format tanggal: DD/MM/YYYY (contoh: 31/12/2025)")
            tanggal_str = input_dengan_escape("Masukkan deadline: ")

            if tanggal_str in ['BACK_TO_MENU', 'EXIT']:
                return tanggal_str

            tanggal = datetime.strptime(tanggal_str, "%d/%m/%Y")

            if tanggal < datetime.now():
                print("❌ Tanggal tidak boleh di masa lalu!")
                continue

            return tanggal
        except ValueError:
            print("❌ Format tanggal salah! Gunakan DD/MM/YYYY")


def tambah_tugas():
    print("\n📝 TAMBAH TUGAS BARU")
    print("-" * 25)
    print("💡 Ketik '0' untuk kembali ke menu utama")

    nama = input_dengan_escape("Nama tugas: ")
    if nama in ['BACK_TO_MENU', 'EXIT']:
        return nama

    matkul = input_dengan_escape("Mata kuliah: ")
    if matkul in ['BACK_TO_MENU', 'EXIT']:
        return matkul

    deadline = input_tanggal()
    if deadline in ['BACK_TO_MENU', 'EXIT']:
        return deadline

    while True:
        try:
            prioritas_input = input_dengan_escape("Prioritas (1-5, 5=sangat penting): ")
            if prioritas_input in ['BACK_TO_MENU', 'EXIT']:
                return prioritas_input

            prioritas = int(prioritas_input)
            if 1 <= prioritas <= 5:
                break
            else:
                print("❌ Prioritas harus antara 1-5!")
        except ValueError:
            print("❌ Masukkan angka yang valid!")

    while True:
        jenis_input = input_dengan_escape("Jenis tugas (m=mandiri, k=kelompok): ").lower()
        if jenis_input in ['BACK_TO_MENU', 'EXIT']:
            return jenis_input
        if jenis_input in ['m', 'mandiri']:
            jenis = 'mandiri'
            break
        elif jenis_input in ['k', 'kelompok']:
            jenis = 'kelompok'
            break
        print("❌ Pilih 'm' untuk mandiri atau 'k' untuk kelompok!")

    while True:
        tipe_input = input_dengan_escape("Tipe tugas (b=biasa, g=besar): ").lower()
        if tipe_input in ['BACK_TO_MENU', 'EXIT']:
            return tipe_input
        if tipe_input in ['b', 'biasa']:
            tipe = 'biasa'
            break
        elif tipe_input in ['g', 'besar']:
            tipe = 'besar'
            break
        print("❌ Pilih 'b' untuk biasa atau 'g' untuk besar!")

    tugas_baru = Tugas(nama, matkul, deadline, prioritas, jenis, tipe)
    tugas_list.append(tugas_baru)

    print(f"✅ Tugas '{nama}' berhasil ditambahkan!")
    return kembali_ke_menu()


def lihat_semua_tugas():
    if not tugas_list:
        print("\n📋 Belum ada tugas yang ditambahkan.")
        return kembali_ke_menu()

    print(f"\n📋 SEMUA TUGAS ({len(tugas_list)} tugas)")
    print("-" * 80)

    for i, tugas in enumerate(tugas_list, 1):
        print(f"{i}. {tugas}")

    return kembali_ke_menu()


def jadwal_prioritas():
    if not tugas_list:
        print("\n📋 Belum ada tugas untuk dijadwalkan.")
        return kembali_ke_menu()

    tugas_terurut = sorted(tugas_list, key=lambda x: x.hitung_skor(), reverse=True)

    print(f"\n🎯 JADWAL PRIORITAS - GREEDY ALGORITHM")
    print("📊 Tugas diurutkan berdasarkan: prioritas + deadline + tipe")
    print("-" * 80)

    for i, tugas in enumerate(tugas_terurut, 1):
        if tugas.hitung_skor() >= 60:
            status = "🔴 SANGAT URGENT"
        elif tugas.hitung_skor() >= 40:
            status = "🟡 PENTING"
        else:
            status = "🟢 NORMAL"

        print(f"{i}. {status}")
        print(f"   {tugas}")
        print()

    return kembali_ke_menu()


def cek_deadline_mendesak():
    if not tugas_list:
        print("\n📋 Belum ada tugas untuk dicek.")
        return kembali_ke_menu()

    sekarang = datetime.now()
    tugas_mendesak = []

    for tugas in tugas_list:
        hari_tersisa = (tugas.deadline - sekarang).days
        if 0 <= hari_tersisa <= 3:
            tugas_mendesak.append((tugas, hari_tersisa))

    if not tugas_mendesak:
        print("\n✅ Tidak ada tugas dengan deadline mendesak!")
        return kembali_ke_menu()

    print(f"\n⚠️  DEADLINE MENDESAK ({len(tugas_mendesak)} tugas)")
    print("-" * 60)

    tugas_mendesak.sort(key=lambda x: x[1])

    for tugas, hari in tugas_mendesak:
        if hari == 0:
            status = "🔴 HARI INI!"
        elif hari == 1:
            status = "🟠 BESOK"
        else:
            status = f"🟡 {hari} hari lagi"

        print(f"{status}")
        print(f"   {tugas}")
        print()

    return kembali_ke_menu()


def hapus_tugas():
    if not tugas_list:
        print("\n📋 Tidak ada tugas untuk dihapus.")
        return kembali_ke_menu()

    lihat_semua_tugas()

    try:
        nomor_input = input_dengan_escape(f"\nPilih nomor tugas yang akan dihapus (1-{len(tugas_list)}): ")

        if nomor_input in ['BACK_TO_MENU', 'EXIT']:
            return nomor_input

        nomor = int(nomor_input)
        if 1 <= nomor <= len(tugas_list):
            tugas_dihapus = tugas_list.pop(nomor - 1)
            print(f"✅ Tugas '{tugas_dihapus.nama}' berhasil dihapus!")
        else:
            print("❌ Nomor tidak valid!")
    except ValueError:
        print("❌ Masukkan nomor yang valid!")

    return kembali_ke_menu()


def main():
    print("🎓 Selamat datang di Penjadwal Tugas Kuliah!")
    print("📚 Menggunakan Greedy Algorithm untuk prioritas optimal")

    while True:
        tampilkan_menu()

        try:
            pilihan = input("Pilih menu (1-6): ").strip()

            result = None

            if pilihan == '1':
                result = tambah_tugas()
            elif pilihan == '2':
                result = lihat_semua_tugas()
            elif pilihan == '3':
                result = jadwal_prioritas()
            elif pilihan == '4':
                result = cek_deadline_mendesak()
            elif pilihan == '5':
                result = hapus_tugas()
            elif pilihan == '6':
                print("\n👋 Terima kasih! Semangat mengerjakan tugas!")
                break
            else:
                print("❌ Pilihan tidak valid! Pilih 1-6.")
                continue

            # Handle hasil dari fungsi menu
            if result == 'EXIT':
                print("\n👋 Terima kasih! Semangat mengerjakan tugas!")
                break

        except KeyboardInterrupt:
            print("\n\n👋 Program dihentikan. Sampai jumpa!")
            break
        except Exception as e:
            print(f"❌ Terjadi error: {e}")
            input("\nTekan Enter untuk melanjutkan...")


if __name__ == "__main__":
    main()