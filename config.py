# =========================================================================
# ⚠️ PENGATURAN KONFIGURASI BOT TELEGRAM ⚠️
# =========================================================================
# File ini berisi semua pengaturan untuk userbot Anda.
# Ubah nilai di bawah ini sesuai dengan kebutuhan Anda.
# =========================================================================

# Tambahkan impor pustaka yang diperlukan untuk Environment Variables
import os
from dotenv import load_dotenv

# Muat variabel dari file .env (Harus dijalankan paling atas!)
load_dotenv()

# =========================================================================
# 1. Credentials & Klien
# =========================================================================
# AMBIL DARI LINGKUNGAN (File .env) - JANGAN DISIMPAN DI SINI!
# Anda HARUS membuat file .env yang berisi API_ID, API_HASH, dan RECIPIENT_ID.
# Menggunakan int() dan strip() untuk memastikan tipe data yang benar
api_id = int(os.environ.get('API_ID', 0))
api_hash = os.environ.get('API_HASH', '').strip("'") # Hapus tanda kutip jika ada
RECIPIENT_ID = int(os.environ.get('RECIPIENT_ID', 0))

# ID Topik opsional. Hanya digunakan jika RECIPIENT_ID adalah ID Grup/Channel 
# yang memiliki fitur topik. Jika dikosongkan/tidak ada di .env, nilainya None.
# Nilai default adalah None.
try:
    REPORT_TOPIC_ID = int(os.environ.get('TOPIC_ID'))
except (TypeError, ValueError):
    REPORT_TOPIC_ID = None

# =========================================================================
# 2. Penargetan Grup & Kata Kunci
# =========================================================================
# Daftar ID numerik grup yang ingin dipantau.
TARGET_GROUP_IDS = [
    -1002985230022,  # Menther(test)
    -1002193793537,  # MOOTS TIKTOK MUTUALAN TT 30k
    -1002857426145,  # MOOTS TIKTOK MUTUALAN TT 12k
    -1002577291866,  # MUTUALAN TIKTOK MOOTS TT 46k
    -1001865044003,  # SALING FOLLOW TIKTOK 2025 2k
    -1001552376990,  # PATUNGAN AKRAB
    -1002502507665,  # job recehan chimmie💸
    -1001866571383,  # Job Review Gmaps
    -1001779205859,  # YOUTH BUZZER INDONESIA
    -1001263277654,  # LVL - Job Buzzer Instagram Tiktok Twitter
    -1001478453928,  # LVL | Job Endorse Buzzer KOL Indonesia
    -1001406072903,  # Job Receh Influencer Selebgram buzzer freelance
    -1002008842263,  # REVIEW MAPS BY CYLA PT 2🕊️
    -1002032063990,  # What'sApp Grup Freelance
    -1001861954287,  # FREELANCE JOB by @buzzerinaja
    -1001612143244,  # Google Reviews Maps GMB
    -1001197136417,  # 🌐 www.Gatcha.org 🇮🇩
    -1002838723963,  # 🍉☁️KMKFuyukiXT [RagumuRugimu]☁️🍉
    -1001949275318,  # BIRA MANAGEMENT
    -1002104861120,  # Freelance Job | Buzzer & Temen mabar
    -1002240742569,  # BUZZERKUY MG
    -1002377564532,  # MAROHELO MG | BUZZER JOB FREELANCE
]

# Daftar kata kunci (regex) yang akan dicari.
# Gunakan r'(?i)keyword' untuk pencarian case-insensitive.
KEYWORDS = [
    # --- Kata Kunci Utama ---
    r'(?i)gratis',
    r'(?i)anggersaputra',
    r'(?i)mentherg',
    r'(?i)regis',
    r'(?i)live',      # Kata kunci yang bisa dikecualikan per grup
    r'(?i)apk',
    r'(?i)playstore',
    r'(?i)registrasi',
    r'(?i)daftar',
    r'(?i)aplikasi',
    r'(?i)review',
    r'(?i)fb',
    r'(?i)foll',
    # r'(?i)like',
    # r'(?i)komen',
    # r'(?i)tiktok',

    # --- Pola Angka & Simbol (dipisahkan agar lebih mudah dibaca) ---
    r'>\s*1k', r'>\s*1\.5k', r'>\s*2k', r'>\s*2\.5k',
    r'>\s*3k', r'>\s*3\.5k', r'>\s*4k', r'>\s*4\.5k',
    r'1k✅', r'2k✅', r'3k✅', r'4k✅',
    r'\)\s*=\s*1k', r'\)\s*=\s*2k', r'\)\s*=\s*3k', r'\)\s*=\s*4k',
]


# =========================================================================
# 3. Pengaturan Pengecualian (Exclusion)
# =========================================================================
# Laporan dari username ini akan diabaikan (gunakan huruf kecil).
EXCLUDED_USERNAMES = [
    'usernameadmin1',
    'moderatorubot',
    'usernamelain',
]

# Di grup ini, kata kunci yang ada di EXCLUDED_KEYWORD akan diabaikan.
EXCLUDED_KEYWORD_GROUPS = [
    -1001552376990,  # PATUNGAN AKRAB
    -1001197136417,  # 🌐 www.Gatcha.org 🇮🇩
    -1002193793537,  # MOOTS TIKTOK MUTUALAN TT 30k
    -1002857426145,  # MOOTS TIKTOK MUTUALAN TT 12k
    -1002577291866,  # MUTUALAN TIKTOK MOOTS TT 46k
    -1001865044003,  # SALING FOLLOW TIKTOK 2025 2k
]

# Daftar kata kunci regex yang akan dikecualikan (Wajib sama persis dengan di KEYWORDS)
EXCLUDED_KEYWORDS = [
    r'(?i)live',
    r'(?i)daftar',
    r'(?i)review',
]

# =========================================================================
# 4. Pengaturan Cache & Cooldown
# =========================================================================
# Durasi (dalam detik) untuk mengabaikan laporan dari pengguna yang sama
# untuk mencegah spam laporan. Contoh: 3600 = 1 jam.
COOLDOWN_SECONDS = 23600

# Grup ini akan MENGABAIKAN SELURUH MEKANISME COOLDOWN/SPAM.
# Setiap pesan dari grup ini akan langsung dilaporkan jika mengandung kata kunci.
# Masukkan ID grup di sini.
EXCLUDED_COOLDOWN_GROUPS = [
    -1001552376990,  # PATUNGAN AKRAB
    -1002502507665,  # job recehan chimmie💸
    -1001866571383,  # Job Review Gmaps
    -1001779205859,  # YOUTH BUZZER INDONESIA
    -1001263277654,  # LVL - Job Buzzer Instagram Tiktok Twitter
    -1001478453928,  # LVL | Job Endorse Buzzer KOL Indonesia
    -1001406072903,  # Job Receh Influencer Selebgram buzzer freelance
    -1002008842263,  # REVIEW MAPS BY CYLA PT 2🕊️
    -1002032063990,  # What'sApp Grup Freelance
    -1001861954287,  # FREELANCE JOB by @buzzerinaja
    -1001612143244,  # Google Reviews Maps GMB
    -1001197136417,  # 🌐 www.Gatcha.org 🇮🇩
    -1002838723963,  # 🍉☁️KMKFuyukiXT [RagumuRugimu]☁️🍉
    -1001949275318,  # BIRA MANAGEMENT
    -1002104861120,  # Freelance Job | Buzzer & Temen mabar
    -1002240742569,  # BUZZERKUY MG
    -1002377564532,  # MAROHELO MG | BUZZER JOB FREELANCE
]
