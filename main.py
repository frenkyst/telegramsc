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

# Impor semua variabel konfigurasi dari file config.py
import config

# =========================================================================
# 1. Inisialisasi Klien & Cache
# =========================================================================

# Cache untuk melacak pengguna yang baru saja dilaporkan untuk mencegah spam
REPORT_CACHE = {}

# Membuat instance klien Telethon
session_name = 'userbot_session'
client = TelegramClient(session_name, config.api_id, config.api_hash)


# =========================================================================
# 2. Fungsi Helper
# =========================================================================

async def clear_cache(username):
    """Menghapus username dari cache setelah waktu cooldown berakhir."""
    await asyncio.sleep(config.COOLDOWN_SECONDS)
    if username in REPORT_CACHE:
        del REPORT_CACHE[username]
        print(f"🔄 Cooldown selesai untuk @{username}. Siap dilaporkan kembali.")


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
    
    # 1. ⛔️ Pengecekan Username Dikecualikan
    if username_lower and username_lower in config.EXCLUDED_USERNAMES:
        print(f"➖ Pesan dilewati: @{username_lower} ada dalam daftar pengecualian.")
        return

# ... (kode di atas tidak berubah) ...

    # 📝 Melakukan Pencarian Kata Kunci Lebih Awal 📝
    found_keyword = None
    # ... (proses pencarian kata kunci dan penyimpanan found_keyword) ...
    for keyword_pattern in config.KEYWORDS:
        # Cek Pengecualian Grup/Kata Kunci (Live/Daftar)
        is_excluded_group = event.chat_id in config.EXCLUDED_KEYWORD_GROUPS
        is_excluded_keyword = keyword_pattern in config.EXCLUDED_KEYWORDS
        
        if is_excluded_group and is_excluded_keyword:
            continue

        match = re.search(keyword_pattern, message_text, re.IGNORECASE)
        if match:
            found_keyword = match.group(0)
            break # Hentikan loop keyword setelah ditemukan satu

    # Jika tidak ada kata kunci yang ditemukan, abaikan
    if not found_keyword:
        return
        
    # 📌 🟢 LOGGING BARU: Pengecekan Tanpa Username (Diletakkan di sini setelah keyword ditemukan) 🟢
    if not username_lower:
        # Format waktu ke string yang mudah dibaca, lalu cetak log
        timestamp = event.date.strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"[{timestamp}] ➖ [ID:{event.chat_id}] Pesan dilewati di '{chat.title}': Pengirim '{sender.first_name}' tidak memiliki username. Keyword ditemukan: '{found_keyword}'.")
        return
        
    # 3. ⛔️ Pengecekan Cooldown (Pencegahan Spam)
    if username_lower in REPORT_CACHE:
        # Tambahkan juga timestamp dan chat ID di sini untuk konsistensi
        timestamp = event.date.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ⏳ [ID:{event.chat_id}] Pesan dari @{username_lower} dilewati (cooldown). Keyword ditemukan: '{found_keyword}'.")
        return
    
    # --- PROSES LAPORAN (lanjut ke sini) ---
# ... (sisa kode pengiriman laporan) ...
        
    # --- Proses Pencarian Kata Kunci (lanjut ke sini jika semua filter terlewati) ---
    for keyword_pattern in config.KEYWORDS:
        # ... (Sisa kode tidak berubah)
        is_excluded_group = event.chat_id in config.EXCLUDED_KEYWORD_GROUPS
        is_excluded_keyword = keyword_pattern in config.EXCLUDED_KEYWORDS
        
        if is_excluded_group and is_excluded_keyword:
            continue
        # ... (Sisa kode pencarian dan pengiriman laporan) ...

        match = re.search(keyword_pattern, message_text, re.IGNORECASE)
        if match:
            try:
                link = f"https://t.me/c/{abs(event.message.peer_id.channel_id)}/{event.message.id}"
                link_text = f"[➡️ Lompat ke Pesan]({link})"
            except AttributeError:
                link_text = "(Tautan pesan tidak tersedia)"

            # =============================================================
            # PERBAIKAN FINAL: USER ID DIKEMBALIKAN KE FORMAT LAPORAN
            # =============================================================
            report_message = (
                f"⚡️ **Laporan Kata Kunci** ⚡️\n\n"
                f"**🗝️ Ditemukan:** `{match.group(0)}`\n"
                f"**👥 Grup:** `{chat.title}`\n\n"
                f"--- **Info Pengirim** ---\n"
                f"**🗣️ Nama:** `{sender.first_name}`\n"
                f"**👤 Username:** @{sender.username}\n"
                f"**🆔 User ID:** `{sender.id}`\n\n"
                f"--- **Pesan Asli** ---\n"
                f"```\n{event.text.replace('`', '’')}\n```\n"
                f"{link_text}"
            )

            try:
                await client.send_message(config.RECIPIENT_ID, report_message, parse_mode='md')
                print(f"✅ Laporan terkirim: '{match.group(0)}' dari @{sender.username}")
                REPORT_CACHE[username_lower] = True
                client.loop.create_task(clear_cache(username_lower))
            except Exception as e:
                print(f"❌ Gagal mengirim laporan: {e}")
            
            break

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
        entity_type = "User" if isinstance(entity, User) else "Grup/Channel"
        name = entity.first_name if isinstance(entity, User) else entity.title
        username = f"@{entity.username}" if entity.username else "(tidak ada)"

        user_info = (
            f"**🔎 Info Entitas**\n\n"
            f"**Input:** `{target_input}`\n"
            f"**Tipe:** `{entity_type}`\n"
            f"**Nama:** `{name}`\n"
            f"**Username:** `{username}`\n"
            f"**ID Unik:** `{entity.id}`"
        )
        await event.reply(user_info, parse_mode='md')
    except (ValueError, TypeError):
        await event.reply(f"❌ **Tidak Ditemukan:** Entitas '{target_input}' tidak dapat ditemukan.")
    except Exception as e:
        await event.reply(f"❌ **Error:** {type(e).__name__}: {e}")

# =========================================================================
# 5. FUNGSI UTAMA DAN STARTUP BOT
# =========================================================================

async def main():
    """Fungsi ini berjalan setelah klien berhasil terhubung."""
    me = await client.get_me()
    
    print("==================================================")
    print(f"✅ UserBot Terhubung sebagai: @{me.username} ({me.id})")
    print("--------------------------------------------------")
    print(f"👥 Memantau {len(config.TARGET_GROUP_IDS)} grup.")
    print(f"🗝️ {len(config.KEYWORDS)} kata kunci dipantau.")
    print(f"⏳ Cooldown: {config.COOLDOWN_SECONDS / 60:.0f} menit per pengguna.")
    
    if config.EXCLUDED_KEYWORD_GROUPS and config.EXCLUDED_KEYWORDS:
        print(f"🚫 Kata kunci {config.EXCLUDED_KEYWORDS} dikecualikan di {len(config.EXCLUDED_KEYWORD_GROUPS)} grup.")
    
    print("==================================================")
    print("Bot sekarang berjalan. Menunggu pesan baru...")

if __name__ == '__main__':
    print("🤖 Memulai bot...")
    with client:
        client.loop.run_until_complete(main())
        client.run_until_disconnected()
    
    print("\n🔌 Bot telah dihentikan.")
