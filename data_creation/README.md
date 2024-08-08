
# Verisetindeki videoları indirip ses ve poz çıkarımı

Bu projede veriseti olarak internetten araştırıp bulduğumuz  İşitme Engelliler Haber Bülteni kanalındaki videoları çektik. Bu seçimin nedeni işaret dilini gösteren 
kişinin ekranda büyük bir alan kaplaması ve poz çıkarımında hataalrı azaltmak içindi.
1. Video indirimi ve Whisper kullanımı
   Eğitilen model metinler üzerinde çalıştığından verisetindeki videolardan metinleri çıkarmamız gerekiyor. Bunun için OpenAI'ın en büyük modeli olan
   Whisper_large modeli kullanılmıştır. Kullanmak istediğiniz videoları bu klasor altında "videos.txt" dosyasına kaydediniz.
```
python audio_to_text.py
```
Videoların metinlerin başlangıç ve bitiş aralıkalrı ile çıkarılmış hali "out.csv" dosyasında bulunacaktır.

Ayrıca orijinal videolar da "sign_videos" klasorune indirilip onların da sadece insan kısmını içeren kesitleri çıkarmak için de aşağdaıki kod kullanılacaktır. Kesilen videolar sign_videos_processed kısmında depolanır.
```
python video_processing.py
```

2. Videolardan poz verilerinin çıkarılması
Burada sizin sistem GPU VRAM'inize göre 2 özellik sunuyoruz. İlki, El ve vücut pozları için OpenPose kullanmak. Bu yaklaşık 12GB VRAM gerektiriyor ve poz çıkarımı yaklaşık 6fps ile çalışıyor.
İkinci yöntem ise Opeepose ile vücut pozlarını ve el iskeleti için Mediapipe kullanmak. BU sayede 6GB altında çalışabilir ve yaklaşık 10fps ile poz verisi üretebilirisiniz.

- OpenPose Full Body+ Hands(12GB VRAM)
Öncelikle openpose inference kütüphanesini [buradan](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/0_index.md#windows-portable-demo) yükleyip kurmanız gerekiyor. 
İndirdikten bu kod ile poz verilerini kaydediniz
  ```
  python only_openpose.py
  ```
- OpenPose Full Body+  Mediapipe Hands(4 VRAM)
Openpose'u sadece vücut pozlarını çıkarmak için kullannırken öncelikle aynı linkten OpenPose'u kurunuz.
  ```
  python openpsoe_body_process.py
  ```
  
  Vücut noktalarından sonra mediapipe aynı verileri işleyip el noktaları ile dolduruyor.
  Burada Mediapipe kütüphanesini ve modelleir indirmiş olmak gerekiyor. Poz çıkarımı tam zamanlı şekilde olduğundan çok zaman almamaktadır. Verilerin hepsi "pose_results" kısmına kaydediliyor.
  
  ```
  mediapipe_hand_gesture_estimation.py
  ```

  
    
  Mediapipe ve openpose'un birlikte çalışmasını sağlarken bunların uyumlu çalışması için birçok process eklenmiştir. Bunlar içerisinde verilerin normalize edilmesi,
   eksik poz verileri tespit edilip aralarının ağırlıklı bir algoritma ile doldurulması, openpose bilek verisi ve mediapipe ile tespit edilen elin başlangıcının aynı konuma getirilmesi ve düzeltilmesi mümkün olmayan kareler tespit edilip çıkartılması yer almaktadır.
  Tüm bunları aşağıdaki kod ile çalıştırıp verilein düzenlenmiş ve  yapay zeka modeli için kullanılabilir forma getirilmis hali "processed_poses" dosyasına kaydedilecektir.
  ```
  hand_body_data_processing.py
  ```
