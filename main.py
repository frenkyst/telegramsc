# =========================================================================
# 🐦 USERBOT TELEGRAM PENCARI KATA KUNCI (VERSI LENGKAP & STABIL) 🐦
# =========================================================================
# Deskripsi: 
# Userbot ini memantau grup-grup yang ditentukan untuk kata kunci tertentu 
# dan mengirimkan laporan ke akun pribadi Anda.
# =========================================================================

# Impor pustaka yang diperlukan
from telethon import TelegramClient, events
from telethon.tl.types import User, Channel, Chat
from telethon.errors.rpcerrorlist import UserNotParticipantError
import re
import asyncio
from datetime import datetime, timedelta
import json
import time

# Impor semua variabel konfigurasi dari file config.py
import config

# =========================================================================
# 1. Inisialisasi Klien & Cache
# =========================================================================

REPORT_CACHE = {}
CACHE_FILE = 'report_cache.json'

session_name = 'userbot_session'
client = TelegramClient(session_name, config.api_id, config.api_hash)

# =========================================================================
# 2. Fungsi Helper & Persistensi Cache
# =========================================================================

def save_cache():
    """Menyimpan REPORT_CACHE ke file JSON."""
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(REPORT_CACHE, f, indent=4)
    except Exception as e:
        print(f"❌ Gagal menyimpan cache: {e}")

def load_cache():
    """Memuat REPORT_CACHE dari file JSON dan membersihkan yang kedaluwarsa."""
    global REPORT_CACHE
    try:
        with open(CACHE_FILE, 'r') as f:
            data = json.load(f)
            current_time = time.time()
            REPORT_CACHE = {
                k: v for k, v in data.items()
                if (current_time - v) < config.COOLDOWN_SECONDS
            }
            print(f"✅ Cache laporan dimuat. {len(REPORT_CACHE)} entri aktif.")
    except FileNotFoundError:
        print("ℹ️ File cache tidak ditemukan, memulai dengan cache kosong.")
        REPORT_CACHE = {}
    except json.JSONDecodeError:
        print("⚠️ File cache rusak, memulai dengan cache kosong.")
        REPORT_CACHE = {}
    except Exception as e:
        print(f"❌ Gagal memuat cache: {e}")
        REPORT_CACHE = {}

# =========================================================================
# 2B. Fungsi Logger File
# =========================================================================

def log_to_file(log_message):
    """Menulis pesan log ke file teks harian."""
    try:
        log_filename = f"log_{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(log_filename, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    except Exception as e:
        print(f"❌ Gagal menyimpan log ke file: {e}")

# =========================================================================
# 3. Event Handler untuk Pesan Baru (Pencari Kata Kunci)
# =========================================================================

@client.on(events.NewMessage(chats=config.TARGET_GROUP_IDS))
async def keyword_handler(event):
    """Dipicu setiap kali ada pesan baru di grup yang dipantau."""
    message_text = event.text
    if not message_text: return

    try:
        chat = await event.get_chat()
        sender = await event.get_sender()
    except UserNotParticipantError:
        return

    if not sender or sender.bot:
        return

    username_lower = sender.username.lower() if sender.username else None
    
    if username_lower and username_lower in config.EXCLUDED_USERNAMES:
        print(f"➖ Pesan dilewati: @{username_lower} ada dalam daftar pengecualian.")
        return

    found_keyword = None
    for keyword_pattern in config.KEYWORDS:
        is_excluded_group = event.chat_id in config.EXCLUDED_KEYWORD_GROUPS
        is_excluded_keyword = keyword_pattern in config.EXCLUDED_KEYWORDS
        
        if is_excluded_group and is_excluded_keyword:
            continue

        if (match := re.search(keyword_pattern, message_text, re.IGNORECASE)):
            found_keyword = match.group(0)
            break

    if not found_keyword:
        return

    user_identifier = username_lower if username_lower else str(sender.id)
    
    if event.chat_id not in config.EXCLUDED_COOLDOWN_GROUPS:
        current_time = time.time()
        last_reported_time = REPORT_CACHE.get(user_identifier)
        
        if last_reported_time and (current_time - last_reported_time) < config.COOLDOWN_SECONDS:
            timestamp = datetime.fromtimestamp(current_time).strftime("%Y-%m-%d %H:%M:%S")
            display_name = f"@{username_lower}" if username_lower else f"[{sender.first_name} ID:{sender.id}]"
            remaining_seconds = config.COOLDOWN_SECONDS - (current_time - last_reported_time)
            remaining_time = str(timedelta(seconds=int(remaining_seconds)))
            cleaned_text = message_text.strip().replace('"', '""')

            log_message = f"""[{timestamp}] ⏳ [ID:{event.chat_id}] [COOLDOWN] Pesan dari {display_name} dilewati di '{chat.title}'.
    Keyword ditemukan: '{found_keyword}'. Sisa Cooldown: {remaining_time}.
    Pesan Asli: "{cleaned_text}"""
            
            print(f"[{timestamp}] ⏳ [ID:{event.chat_id}] Pesan dari {display_name} dilewati (cooldown). Sisa: {remaining_time}")
            log_to_file(log_message)
            return
    
    try:
        link = f"https://t.me/c/{abs(event.message.peer_id.channel_id)}/{event.message.id}"
        link_text = f"[➡️ Lompat ke Pesan]({link})"
    except AttributeError:
        link_text = "(Tautan pesan tidak tersedia)"

    username_link = f"[@{sender.username}](https://t.me/{sender.username})" if sender.username else f"[{sender.first_name} (Tanpa Username)](tg://user?id={sender.id})"
    message_content = message_text.replace('`', '’')
    
    report_message = f"""⚡️ **Laporan Kata Kunci** ⚡️

**🗝️ Ditemukan:** `{found_keyword}`
**👥 Grup:** `{chat.title}`

--- **Info Pengirim** ---
**🗣️ Nama:** `{sender.first_name}`
**👤 Profil:** {username_link}
**🆔 User ID:** `{sender.id}`

--- **Pesan Asli** ---
```
{message_content}
```
{link_text}"""

    try:
        await client.send_message(config.RECIPIENT_ID, report_message, parse_mode='md')
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        display_name = f"@{username_lower}" if username_lower else f"[{sender.first_name} ID:{sender.id}]"
        cleaned_text = message_text.strip().replace('"', '""')

        # DEFINITIVE FIX for line 197
        success_log = f"""[{timestamp}] ✅ [ID:{event.chat_id}] LAPORAN TERKIRIM: '{found_keyword}' dari {display_name} di '{chat.title}'.
    Pesan Asli: "{cleaned_text}"""
        
        print(f"[{timestamp}] ✅ Laporan terkirim: '{found_keyword}' dari {display_name}")
        log_to_file(success_log)
        
        if event.chat_id not in config.EXCLUDED_COOLDOWN_GROUPS:
            REPORT_CACHE[user_identifier] = time.time()
            save_cache()
        
    except Exception as e:
        print(f"❌ Gagal mengirim laporan: {e}")

# =========================================================================
# 4. Perintah /whois
# =========================================================================

@client.on(events.NewMessage(pattern=r'/whois(?: |$)(.*)', from_users=config.RECIPIENT_ID))
async def whois_handler(event):
    """Memberikan informasi detail tentang username atau user ID."""
    target_input = event.pattern_match.group(1).strip()
    if not target_input:
        await event.reply("ℹ️ **Guna:** `/whois <username/user_id>`")
        return

    try:
        entity = await client.get_entity(target_input)
    except Exception as e:
        await event.reply(f"❌ **Error saat mengambil entitas:** {e}")
        return

    entity_type = "User" if isinstance(entity, User) else "Grup/Channel"
    name = entity.first_name if isinstance(entity, User) else entity.title
    username = f"@{entity.username}" if entity.username else "(tidak ada)"

    user_info = f"""**🔎 Info Entitas**

**Input:** `{target_input}`
**Tipe:** `{entity_type}`
**Nama:** `{name}`
**Username:** `{username}`
**ID Unik:** `{entity.id}`"""
    await event.reply(user_info, parse_mode='md')

# =========================================================================
# 5. FUNGSI UTAMA DAN STARTUP BOT
# =========================================================================

async def main():
    """Fungsi ini berjalan setelah klien berhasil terhubung."""
    load_cache()
    me = await client.get_me()
    
    print("==================================================")
    print(f"✅ UserBot Terhubung sebagai: @{me.username} ({me.id})")
    print("--------------------------------------------------")
    print(f"👥 Memantau {len(config.TARGET_GROUP_IDS)} grup.")
    print(f"🗝️ {len(config.KEYWORDS)} kata kunci dipantau.")
    print(f"⏳ Cooldown: {config.COOLDOWN_SECONDS / 60:.0f} menit per pengguna.")
    print(f"💾 Cache Cooldown dimuat: {len(REPORT_CACHE)} entri aktif.")
    
    if config.EXCLUDED_KEYWORD_GROUPS and config.EXCLUDED_KEYWORDS:
        print(f"🚫 Kata kunci {config.EXCLUDED_KEYWORDS} dikecualikan di {len(config.EXCLUDED_KEYWORD_GROUPS)} grup.")
    
    if config.EXCLUDED_COOLDOWN_GROUPS:
        print(f"⚠️ {len(config.EXCLUDED_COOLDOWN_GROUPS)} grup DIKECUALIKAN dari Cooldown.")
    
    print("==================================================")
    print("Bot sekarang berjalan. Menunggu pesan baru...")

if __name__ == '__main__':
    print("🤖 Memulai bot...")
    with client:
        client.loop.run_until_complete(main())
        client.run_until_disconnected()
    
    print("\n🔌 Bot telah dihentikan.")
