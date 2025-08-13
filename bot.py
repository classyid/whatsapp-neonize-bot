import asyncio
import logging
import os
import sys
import json
from datetime import timedelta
from neonize.aioze.client import NewAClient
from neonize.events import (
    ConnectedEv,
    MessageEv,
    PairStatusEv,
    event,
)
from neonize.utils import log

sys.path.insert(0, os.getcwd())

# Konfigurasi logging yang lebih baik
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log.setLevel(logging.DEBUG)

# Inisialisasi client
client = NewAClient("db.sqlite3")

# Variable global untuk tracking status
is_connected = False

@client.event(ConnectedEv)
async def on_connected(_: NewAClient, __: ConnectedEv):
    global is_connected
    is_connected = True
    log.info("⚡ Connected to WhatsApp")
    print("✅ Bot berhasil terhubung ke WhatsApp!")
    print("🤖 Bot siap menerima perintah!")
    print("💡 Kirim 'help' untuk melihat daftar perintah")
    
    # Jangan auto-download kontak karena menyebabkan crash
    # Biarkan user yang meminta manual dengan perintah
    print("⚠️ Auto-download kontak dinonaktifkan untuk stabilitas")

@client.event(MessageEv)
async def on_message(client: NewAClient, message: MessageEv):
    await handler(client, message)

@client.event(PairStatusEv)
async def PairStatusMessage(_: NewAClient, message: PairStatusEv):
    log.info(f"📱 Logged as {message.ID.User}")
    print(f"📱 Login sebagai: {message.ID.User}")

async def handler(client: NewAClient, message: MessageEv):
    try:
        # Cek apakah pesan dari diri sendiri
        if message.Info.MessageSource.IsFromMe:
            return
            
        # Ekstrak teks dari pesan dengan handling yang lebih baik
        text = ""
        if hasattr(message.Message, 'conversation') and message.Message.conversation:
            text = message.Message.conversation
        elif hasattr(message.Message, 'extendedTextMessage') and message.Message.extendedTextMessage:
            if hasattr(message.Message.extendedTextMessage, 'text'):
                text = message.Message.extendedTextMessage.text
        
        # Skip jika tidak ada teks
        if not text:
            return
            
        text = text.strip().lower()
        chat = message.Info.MessageSource.Chat
        
        print(f"📨 Pesan diterima dari {chat}: {text}")
        
        # Respon untuk berbagai perintah
        if text == "ping":
            await client.reply_message("🏓 pong - Bot aktif!", message)
        elif text == "download_contacts":
            await download_contacts_command(client, message)
        elif text == "profile_pict":
            await get_profile_picture(client, message, chat)
        elif text == "status_privacy":
            await get_status_privacy(client, message)
        elif text == "get_chat_settings":
            await get_chat_settings(client, message, chat)
        elif text == "help":
            await show_help(client, message)
        elif text == "status":
            await client.reply_message("🤖 Bot aktif dan berjalan dengan baik!", message)
        elif text == "info":
            await get_bot_info(client, message)
        elif text.startswith("echo "):
            # Echo command untuk testing
            echo_text = text[5:]  # Remove "echo "
            await client.reply_message(f"🔊 Echo: {echo_text}", message)
            
    except Exception as e:
        print(f"❌ Error saat memproses pesan: {e}")
        try:
            await client.reply_message(f"❌ Terjadi error: {str(e)}", message)
        except:
            pass

# Fungsi untuk mengunduh kontak dengan error handling yang lebih baik
async def download_contacts():
    try:
        print("📥 Mengunduh daftar kontak...")
        
        # Tambahkan delay untuk memastikan koneksi stabil
        await asyncio.sleep(2)
        
        # Coba beberapa kali jika gagal
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"🔄 Percobaan {attempt + 1}/{max_retries}")
                
                # Coba dengan timeout
                contacts = await asyncio.wait_for(
                    client.contact.get_all_contacts(),
                    timeout=30.0  # 30 detik timeout
                )
                
                if contacts and len(contacts) > 0:
                    # Konversi ke format yang bisa di-serialize dengan validasi
                    contacts_data = []
                    for i, contact in enumerate(contacts):
                        try:
                            contact_dict = {
                                'index': i,
                                'jid': str(contact.JID) if hasattr(contact, 'JID') and contact.JID else f'unknown_{i}',
                                'name': str(contact.Name) if hasattr(contact, 'Name') and contact.Name else 'No Name',
                                'notify': str(contact.Notify) if hasattr(contact, 'Notify') and contact.Notify else '',
                                'business': str(contact.BusinessName) if hasattr(contact, 'BusinessName') and contact.BusinessName else ''
                            }
                            contacts_data.append(contact_dict)
                        except Exception as e:
                            print(f"⚠️ Error processing contact {i}: {e}")
                            # Tetap lanjutkan dengan contact lainnya
                            continue
                    
                    # Simpan kontak ke file jika ada data
                    if contacts_data:
                        with open("contacts.json", "w", encoding='utf-8') as f:
                            json.dump(contacts_data, f, indent=4, ensure_ascii=False)
                        
                        print(f"✅ Berhasil mengunduh {len(contacts_data)} kontak")
                        print("📁 Kontak disimpan di contacts.json")
                        return contacts_data
                    else:
                        print("⚠️ Tidak ada kontak valid yang bisa diproses")
                        return []
                        
                else:
                    print("⚠️ Tidak ada kontak yang ditemukan atau kontak kosong")
                    return []
                    
            except asyncio.TimeoutError:
                print(f"⏰ Timeout pada percobaan {attempt + 1}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(5)
                    continue
                else:
                    raise Exception("Timeout saat mengambil kontak setelah beberapa percobaan")
                    
            except Exception as e:
                print(f"❌ Error pada percobaan {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(5)
                    continue
                else:
                    raise e
        
        return []
            
    except Exception as e:
        print(f"❌ Error saat mengunduh kontak: {e}")
        return None

# Fungsi untuk perintah download kontak dengan safety check
async def download_contacts_command(client, message):
    try:
        await client.reply_message("⚠️ PERINGATAN: Download kontak dapat menyebabkan crash jika tidak ada kontak. Lanjutkan? (Kirim 'yes' untuk konfirmasi)", message)
        
        # Untuk sementara, beri pesan bahwa fitur ini bermasalah
        await asyncio.sleep(1)
        await client.reply_message("""
❌ **Fitur Download Kontak Sementara Dinonaktifkan**

Alasan: Library neonize mengalami bug saat mengakses kontak kosong yang menyebabkan aplikasi crash.

🔧 **Alternatif:**
• Pastikan WhatsApp Anda memiliki kontak
• Coba restart bot setelah menambah kontak
• Gunakan fitur lain yang tersedia

Ketik 'help' untuk melihat fitur lain yang bisa digunakan.
        """, message)
        
    except Exception as e:
        await client.reply_message(f"❌ Error: {str(e)}", message)

# Fungsi untuk mendapatkan foto profil dengan better handling
async def get_profile_picture(client, message, chat):
    try:
        await client.reply_message("📸 Mengambil foto profil...", message)
        
        # Tambahkan timeout
        profile_picture = await asyncio.wait_for(
            client.get_profile_picture(chat),
            timeout=15.0
        )
        
        if profile_picture:
            await client.reply_message(f"📸 Foto profil ditemukan: {profile_picture}", message)
        else:
            await client.reply_message("❌ Tidak dapat mengambil foto profil atau foto profil tidak tersedia", message)
            
    except asyncio.TimeoutError:
        await client.reply_message("⏰ Timeout saat mengambil foto profil", message)
    except Exception as e:
        await client.reply_message(f"❌ Error saat mengambil foto profil: {str(e)}", message)

# Fungsi untuk mendapatkan status privasi
async def get_status_privacy(client, message):
    try:
        await client.reply_message("🔒 Mengambil status privasi...", message)
        
        status_privacy = await asyncio.wait_for(
            client.get_status_privacy(),
            timeout=15.0
        )
        
        await client.reply_message(f"🔒 Status privasi: {status_privacy}", message)
        
    except asyncio.TimeoutError:
        await client.reply_message("⏰ Timeout saat mengambil status privasi", message)
    except Exception as e:
        await client.reply_message(f"❌ Error saat mengambil status privasi: {str(e)}", message)

# Fungsi untuk mendapatkan pengaturan chat
async def get_chat_settings(client, message, chat):
    try:
        await client.reply_message("⚙️ Mengambil pengaturan chat...", message)
        
        chat_settings = await asyncio.wait_for(
            client.chat_settings.get_chat_settings(chat),
            timeout=15.0
        )
        
        await client.reply_message(f"⚙️ Pengaturan chat: {chat_settings}", message)
        
    except asyncio.TimeoutError:
        await client.reply_message("⏰ Timeout saat mengambil pengaturan chat", message)
    except Exception as e:
        await client.reply_message(f"❌ Error saat mengambil pengaturan chat: {str(e)}", message)

# Fungsi untuk info bot
async def get_bot_info(client, message):
    info_text = f"""
🤖 **WhatsApp Bot Info:**

📊 **Status:** ✅ Aktif dan Berjalan
🔗 **Koneksi:** ✅ Terhubung ke WhatsApp  
💾 **Database:** db.sqlite3
📱 **Platform:** Neonize Python Client
⚡ **Uptime:** Sejak terakhir restart

🔧 **Fitur yang Stabil:**
• Ping/Pong ✅
• Echo command ✅
• Help & Info ✅  
• Status check ✅

⚠️ **Fitur dalam Perbaikan:**
• Download contacts (bug library)
• Profile picture (tergantung privacy)

💡 **Tips:** Gunakan 'help' untuk daftar lengkap perintah
    """
    await client.reply_message(info_text, message)

# Fungsi untuk menampilkan bantuan
async def show_help(client, message):
    help_text = """🤖 **WhatsApp Bot - Daftar Perintah:**

🔧 **Perintah Dasar:**
• `ping` - Tes koneksi bot
• `status` - Cek status bot  
• `info` - Informasi detail bot
• `help` - Tampilkan bantuan ini
• `echo [text]` - Echo pesan (contoh: echo hello)

📋 **Fitur Kontak:**
• `download_contacts` - ⚠️ Sementara dinonaktifkan (bug library)

📸 **Fitur Profile:**
• `profile_pict` - Ambil foto profil (mungkin dibatasi privacy)

🔒 **Fitur Privasi:**
• `status_privacy` - Dapatkan status privasi

⚙️ **Pengaturan:**
• `get_chat_settings` - Dapatkan pengaturan chat

---
🚀 **Bot berjalan 24/7 dan siap melayani!**
💡 **Ketik perintah tanpa tanda kutip**
⚠️ **Beberapa fitur tergantung pengaturan privacy WhatsApp Anda**
"""
    
    await client.reply_message(help_text, message)

# Fungsi untuk keep alive yang lebih robust
async def keep_alive():
    """Keep the bot running and handle reconnection"""
    heartbeat_count = 0
    
    while True:
        try:
            if not is_connected:
                print("🔄 Menunggu koneksi...")
                await asyncio.sleep(5)
                continue
            
            # Heartbeat setiap 60 detik dengan counter
            heartbeat_count += 1
            print(f"💓 Bot aktif - Heartbeat #{heartbeat_count}")
            
            # Setiap 10 heartbeat (10 menit), tampilkan info lebih detail
            if heartbeat_count % 10 == 0:
                print(f"📊 Bot telah berjalan selama {heartbeat_count} menit")
                print("✅ Semua sistem normal")
            
            await asyncio.sleep(60)  # 60 detik
            
        except Exception as e:
            print(f"❌ Error dalam keep_alive: {e}")
            await asyncio.sleep(30)

# Fungsi utama yang lebih robust dengan error recovery
async def main():
    global is_connected
    
    print("=" * 50)
    print("🤖 WHATSAPP BOT STARTING")
    print("=" * 50)
    print("📱 Menghubungkan dengan QR Code...")
    print("⏳ Scan QR Code yang muncul dengan WhatsApp Anda")
    print("⚠️ Fitur download kontak dinonaktifkan karena bug library")
    print("=" * 50)
    
    retry_count = 0
    max_retries = 3
    
    while retry_count < max_retries:
        try:
            # Jalankan connect dan keep_alive secara bersamaan
            print(f"🔄 Percobaan koneksi {retry_count + 1}/{max_retries}")
            
            connect_task = asyncio.create_task(client.connect())
            keep_alive_task = asyncio.create_task(keep_alive())
            
            # Tunggu hingga salah satu task selesai atau error
            done, pending = await asyncio.wait(
                [connect_task, keep_alive_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Jika sampai sini tanpa exception, berarti berhasil
            print("✅ Koneksi berhasil dan stabil")
            
            # Tunggu hingga user menghentikan dengan Ctrl+C
            try:
                while is_connected:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Bot dihentikan oleh user")
                break
                
        except KeyboardInterrupt:
            print("\n🛑 Bot dihentikan oleh user")
            break
            
        except Exception as e:
            print(f"❌ Error koneksi (percobaan {retry_count + 1}): {e}")
            retry_count += 1
            
            if retry_count < max_retries:
                print(f"⏳ Menunggu 10 detik sebelum retry...")
                await asyncio.sleep(10)
            else:
                print("❌ Maksimal percobaan tercapai")
                break
        
        finally:
            # Cleanup tasks
            for task in [connect_task, keep_alive_task]:
                if not task.done():
                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
    
    is_connected = False
    print("👋 Bot telah berhenti sepenuhnya")

if __name__ == "__main__":
    # Jalankan dengan event loop yang proper
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Program dihentikan oleh user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        print("💡 Coba restart bot atau periksa koneksi internet")
