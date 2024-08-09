# Video İndirme, Ses ve Poz Çıkarımı

Bu proje, **İşitme Engelliler Haber Bülteni** YouTube kanalındaki videoları işleyerek metin ve poz verisi çıkarmayı içerir. Bu videolar, işaret dilini gösteren kişinin ekranda büyük bir alan kaplaması nedeniyle seçilmiştir, bu da poz çıkarımındaki hataları azaltır.

## 1. Video İndirimi ve Whisper Kullanımı

Eğitilen model metinlerle çalıştığından, verisetindeki videolardan metinleri çıkarmamız gerekiyor. Bunun için OpenAI'ın en büyük modeli olan **Whisper_large** kullanılmıştır. Kullanmak istediğiniz videoları, bu klasör altında bulunan `videos.txt` dosyasına kaydediniz.

Videolardan metin çıkarmak için şu komutu çalıştırın:
  ```
python audio_to_text.py
  ```
Çıkarılan metin, başlangıç ve bitiş zamanlarıyla birlikte `out.csv` dosyasına kaydedilecektir.

Ayrıca, orijinal videolar `sign_videos` klasörüne indirilecek ve aşağıdaki kod kullanılarak videolar sadece insan kısmını içerecek şekilde kırpılacaktır. Kırpılan videolar `sign_videos_processed` klasöründe depolanacaktır.
  ```
python video_processing.py
  ```

## 2. Videolardan Poz Verilerinin Çıkarılması

Sisteminize ait GPU VRAM'e bağlı olarak, poz çıkarımı için iki seçenek sunuyoruz. İlk seçenek, hem el hem de vücut pozları için OpenPose kullanmak, bu yaklaşık 12GB VRAM gerektirir ve yaklaşık 6fps hızında çalışır. İkinci seçenek, vücut pozları için OpenPose ve el iskeletleri için Mediapipe kullanmak, bu 6GB VRAM altında çalışabilir ve yaklaşık 10fps hızında poz verisi üretebilir.

### Seçenek 1: OpenPose Full Body + Hands (12GB VRAM)
Öncelikle, [buradan](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/0_index.md#windows-portable-demo) OpenPose inference kütüphanesini indirip kurmanız gerekiyor.

Sonrasında, aşağıdaki kod ile poz verilerini kaydediniz:
  ```
python only_openpose.py
  ```

### Seçenek 2: OpenPose Full Body + Mediapipe Hands (4GB VRAM)
Bu seçenekte, OpenPose sadece vücut pozlarını çıkarmak için kullanılacak. Öncelikle OpenPose'u aynı bağlantıdan indirip kurunuz.

Ardından, şu kodu çalıştırın:
  ```
python openpose_body_process.py
  ```

Vücut anahtar noktaları çıkarıldıktan sonra, Mediapipe aynı verileri işleyerek el anahtar noktalarını dolduracaktır. Mediapipe kütüphanesi ve modellerinin önceden indirilmiş olduğundan emin olun. Poz çıkarımı gerçek zamanlı olduğundan, fazla zaman almaz. Tüm veriler `pose_results` klasörüne kaydedilir.
  ```
python mediapipe_hand_gesture_estimation.py
  ```

Mediapipe ve OpenPose'un uyumlu çalışmasını sağlamak için birkaç işlem eklenmiştir. Bunlar, verilerin normalize edilmesi, eksik poz verilerinin ağırlıklı bir algoritma ile doldurulması, OpenPose bilek verisi ile Mediapipe tarafından tespit edilen el başlangıç noktalarının aynı konuma getirilmesi ve düzeltilemeyen karelerin çıkarılması gibi işlemleri içerir.

Bu işlemleri çalıştırarak düzenlenmiş ve yapay zeka modeli için kullanılabilir formda veriler elde etmek için şu kodu çalıştırın:
python finalize_pose_data.py
