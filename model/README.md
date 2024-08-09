# Autoregressive Model Mimarisi Kurulumu ve Eğitimi
Geliştirdiğimiz model giriş olarak aldığı metin cümlesini işleyerek encodera aktarır, decoder modeli ise pose verilerini üretir. Üretilen poz verileri giriş cümlesinin işaret diline çevrilmiş halidir.

<img src="https://github.com/user-attachments/assets/9980cb33-2947-43a8-b54d-63581d861fdd" alt="model_architecture" width="400" height="400">


Model geliştirilirken öğrenmeyi hızlandırmak için embedding katmanının ağırlıklarını sıfırdan başlatmak yerine FastText_large modeli ile verisetindeki kelimelere vektörlere dönüştürülmüştür.
Bu klasorun içerisine fasttext_large modelini buradan indirmeniz ve kurmanız gerekmektedir.
Modeli başlatmadan önce aşağıdaki klasor yapısına sahip olduğunuzadan emin olun. 

    .
    ├── images                  # Github için kullanılan resimler burada 
    ├── datasets                # verisetleri ve kullanımı hakkında 
    ├── İmageCaptioning         # Projenin modeli bu dosyada bulunuyor
    ├── images_data                  #içerisinde kullandığın verisetinin fotoğrafları olmalı
    ├── .gitignore            
    ├── dataset.json             #images içindeki resimlerin dosya adları ve o resme karşılık gelen metinleri barındırıyor 
    ├── LICENSE
    ├── requirements.txt
    └── README.md


pose üretmek için modeli eğitmek için aşağıdaki kodu çalıştırın

 ```
python __main__.py train ./Configs/Base.yaml
 ```

Modelin kaç epoch ve kaçıncı steplerde görsel olarak sonuç çıkarmasını istediğinizi config dosyasından ayarlayabilirsiniz. 

<poz_example_video>
