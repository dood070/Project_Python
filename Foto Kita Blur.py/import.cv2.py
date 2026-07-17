import cv2
import mediapipe as mp

# ---------------------------------------------------------
# Setup MediaPipe Hands
# ---------------------------------------------------------
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,          # deteksi 1 tangan saja (bisa diubah)
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6,
)

# Index landmark ujung jari (tip) dan sendi bawahnya (pip)
# urutan: [thumb, index, middle, ring, pinky]
TIP_IDS = [4, 8, 12, 16, 20]


def hitung_jari_terangkat(hand_landmarks, handedness_label):
    """
    Mengembalikan list boolean (5 elemen) menunjukkan jari mana saja
    yang sedang terangkat: [ibu jari, telunjuk, tengah, manis, kelingking]
    """
    landmarks = hand_landmarks.landmark
    jari_naik = []

    # Ibu jari (thumb) -> dicek berdasarkan posisi x, tergantung tangan kiri/kanan
    if handedness_label == "Right":
        jari_naik.append(landmarks[TIP_IDS[0]].x < landmarks[TIP_IDS[0] - 1].x)
    else:
        jari_naik.append(landmarks[TIP_IDS[0]].x > landmarks[TIP_IDS[0] - 1].x)

    # 4 jari lainnya -> dicek berdasarkan posisi y (tip lebih tinggi dari pip = terangkat)
    for id in range(1, 5):
        tip_y = landmarks[TIP_IDS[id]].y
        pip_y = landmarks[TIP_IDS[id] - 2].y
        jari_naik.append(tip_y < pip_y)

    return jari_naik


def is_pose_dua_jari(jari_naik):
    """
    Cek apakah pose saat ini adalah "2 jari" (telunjuk + tengah terangkat,
    jari lain turun) -> seperti simbol peace/victory.
    """
    ibu_jari, telunjuk, tengah, manis, kelingking = jari_naik
    return telunjuk and tengah and not manis and not kelingking


def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Tidak bisa membuka webcam. Cek koneksi/permission kamera.")
        return

    print("Tekan 'q' untuk keluar.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal membaca frame dari webcam.")
            break

        frame = cv2.flip(frame, 1)  # efek cermin biar natural
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        pose_terdeteksi = False

        if result.multi_hand_landmarks and result.multi_handedness:
            for hand_landmarks, handedness in zip(
                result.multi_hand_landmarks, result.multi_handedness
            ):
                label = handedness.classification[0].label  # "Left" / "Right"
                jari_naik = hitung_jari_terangkat(hand_landmarks, label)

                if is_pose_dua_jari(jari_naik):
                    pose_terdeteksi = True

        # Kalau pose 2 jari terdeteksi -> blur seluruh frame
        if pose_terdeteksi:
            frame = cv2.GaussianBlur(frame, (35, 35), 0)

        cv2.imshow("Hand Gesture Blur", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()