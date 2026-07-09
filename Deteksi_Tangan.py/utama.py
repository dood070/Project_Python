from HandDetection import HandDetector
import cv2
import time
from gtts import gTTS
import os
import pygame
import threading
import uuid  # ✅ agar nama file suara unik

# --- Inisialisasi pygame untuk memutar suara ---
pygame.mixer.init(frequency=22050, size=-16, channels=2)
pygame.mixer.music.set_volume(1.0)

def speak_gtts(text):
    """Fungsi untuk mengucapkan teks menggunakan suara Google Translate"""
    try:
        tts = gTTS(text=text, lang='id')
        filename = f"temp_voice_{uuid.uuid4().hex}.mp3"
        tts.save(filename)
        time.sleep(0.4)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        print(f"🔊 Mengucapkan: {text}")
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        # hapus file sementara
        time.sleep(0.3)
        os.remove(filename)
    except Exception as e:
        print("⚠️ Error saat memutar suara:", e)

def speak_in_thread(text):
    """Jalankan suara di thread agar webcam tidak lag"""
    threading.Thread(target=speak_gtts, args=(text,), daemon=True).start()

# --- Inisialisasi deteksi tangan ---
print("⏳ Memuat model Mediapipe, mohon tunggu...")
detector = HandDetector()
print("✅ Model siap, membuka webcam...")

# --- Buka webcam ---
webcam = cv2.VideoCapture(0)
time.sleep(2)  # beri waktu kamera menyala

if not webcam.isOpened():
    print("❌ Kamera gagal dibuka. Pastikan tidak digunakan aplikasi lain.")
    exit()

# Variabel kontrol
last_word = ""
last_speak_time = 0
speak_interval = 2  # detik

try:
    while True:
        success, frame = webcam.read()
        if not success:
            print("❌ Tidak dapat membaca frame webcam.")
            break

        frame = cv2.flip(frame, 1)
        hands = detector.findHandsLandMarks(frame, draw=True)
        word = ""

        if hands:
            for hand in hands:
                if len(hand) < 21:
                    continue  # pastikan titik lengkap

                # Ambil posisi y setiap jari
                thumb_y = hand[4][2]
                index_y = hand[8][2]
                middle_y = hand[12][2]
                ring_y = hand[16][2]
                pinky_y = hand[20][2]

                # Posisi referensi (sendi bawah)
                thumb_base = hand[3][2]
                index_base = hand[6][2]
                middle_base = hand[10][2]
                ring_base = hand[14][2]
                pinky_base = hand[18][2]

                # Fungsi untuk cek apakah jari terangkat
                def is_up(finger_y, base_y, tol=15):
                    return finger_y < base_y - tol

                # Deteksi jari mana yang terangkat
                fingers_up = [
                    is_up(thumb_y, thumb_base),   # jempol
                    is_up(index_y, index_base),   # telunjuk
                    is_up(middle_y, middle_base), # tengah
                    is_up(ring_y, ring_base),     # manis
                    is_up(pinky_y, pinky_base),   # kelingking
                ]

                # Kombinasi jari & kata
                if fingers_up == [False, True, False, False, False]:
                    word = "HALO"
                elif fingers_up == [False, True, True, False, False]:
                    word = "PERKENALKAN"
                elif fingers_up == [True, False, False, False, True]:
                    word = "NAMA SAYA"
                elif fingers_up == [True, True, False, False, True]:
                    word = "RIDHO PRIBADI"
                elif fingers_up == [False, True, False, False, True]:
                    word = "AL ISLAMI"
                elif fingers_up == [True, True, False, False, False]:
                    word = "TERIMA KASIH"  # 👈 tambahan baru: jempol + telunjuk

        # --- Tampilkan dan ucapkan kata ---
        if word:
            cv2.putText(frame, word, (50, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)

            current_time = time.time()
            if word == last_word:
                if current_time - last_speak_time >= speak_interval:
                    speak_in_thread(word)
                    last_speak_time = current_time
            else:
                speak_in_thread(word)
                last_word = word
                last_speak_time = current_time

        cv2.imshow("Hand Detection", frame)

        # Tekan Q untuk keluar
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

webcam.release()
cv2.destroyAllWindows()
