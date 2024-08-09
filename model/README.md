
https://github.com/user-attachments/assets/17160628-174e-407e-844c-4584a83adee6
# Autoregressive Model Mimarisi Kurulumu ve Eğitimi
Geliştirdiğimiz model giriş olarak aldığı metin cümlesini işleyerek encodera aktarır, decoder modeli ise pose verilerini üretir. Üretilen poz verileri giriş cümlesinin işaret diline çevrilmiş halidir.

<img src="https://github.com/user-attachments/assets/9980cb33-2947-43a8-b54d-63581d861fdd" alt="model_architecture" width="600" height="600">



Model geliştirilirken öğrenmeyi hızlandırmak için embedding katmanının ağırlıklarını sıfırdan başlatmak yerine FastText_large modeli ile verisetindeki kelimelere vektörlere dönüştürülmüştür.
Bu klasorun içerisine fasttext_large modelini buradan indirmeniz ve kurmanız gerekmektedir.
Modeli başlatmadan önce aşağıdaki klasor yapısına sahip olduğunuzadan emin olun. 


https://github.com/user-attachments/assets/14b8fbec-30db-4d3b-9126-f43c394151ab


## Proje Yapısı

- **Configs/**: Konfigürasyon dosyalarını içerir.
- **Data/**: Verisetleri bu dizinde olmalıdır. Örnek veriseti `tr` klasörü altında verilmiştir.
- **Models/**: Önceden eğitilmiş modeller ve yeni oluşturulan modeller burada saklanır.
- **external_metrics/**: Modelleri değerlendirmek için kullanılan dış metrik betikleri veya dosyaları içerir.
- **optim/**: Optimizasyon ile ilgili betikler ve dosyalar.
- **scripts/**: Genel amaçlı betikler ve yardımcı fonksiyonlar:
  - `batch.py`: Batch işleme işlemlerini yönetir.
  - `builders.py`: Modeller ve diğer yapıları oluşturur.
  - `constants.py`: Proje genelinde kullanılan sabit değerler.
  - `data.py`: Veri işleme ve ön işleme işlevleri.
  - `dtw.py`: Dynamic Time Warping (DTW) ile ilgili işlevler.
  - `embeddings.py`: Gömme (embedding) modelleri ve araçları.
  - `encoders.py`: Encoder katmanları ve işlevleri.
  - `helpers.py`: Yardımcı fonksiyonlar ve araçlar.
  - `initialization.py`: Modellerin ve parametrelerin başlatılması.
  - `loss.py`: Eğitimde kullanılan kayıp fonksiyonları.
  - `metrics.py`: Metriği hesaplayan fonksiyonlar ve araçlar.
  - `model.py`: Model tanımları.
  - `plot_videos.py`: Video verilerini çizmek veya görselleştirmek için kullanılan betikler.
  - `prediction.py`: Tahmin ve çıkarım betikleri.
  - `search.py`: Model çıktıları veya verilerde arama yapmak için.
  - `transformer_layers.py`: Transformer katmanlarının implementasyonu.
  - `training.py`: Eğitim döngüsü ve ilgili fonksiyonlar.
  - `vocabulary.py`: Kelime hazinesi yönetimi ve araçlar.

- **checkpoints/**: Model kontrol noktalarının kaydedildiği dizin.
- **FastText_large.model**: Önceden eğitilmiş FastText modeli ve ilgili dosyalar.
- **LICENSE.md**: Projenin hangi lisans altında dağıtıldığını belirten dosya.
- **README.md**: Bu belge.
- **requirements.txt**: Progressive Transformers'ların çalışması için gereken kütüphaneler.


Yukarıdaki yapıya sahipseniz ve skel, text ve files dosyalarını oluşturup config düzenlemesi yaptıysanız. Pose üreten modeli eğitmek için aşağıdaki kodu çalıştırın.

 ```
python __main__.py train ./Configs/Base.yaml
 ```

Modelin kaç epoch ve kaçıncı steplerde görsel olarak sonuç çıkarmasını istediğinizi config dosyasından ayarlayabilirsiniz. 



![output_gif](https://github.com/user-attachments/assets/87ac29d6-a278-4498-8512-9f98c3168229)

