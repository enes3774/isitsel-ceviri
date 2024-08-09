# İşitsel Çeviri

**İşitsel Çeviri**, herhangi bir Türkçe videonun sesini işleyerek sürekli bir şekilde Türkçe işaret diline çeviren, [Progressive Transformer mimarisine](https://arxiv.org/pdf/2004.14874) dayalı bir yapay zeka modelidir.

![Örnek Grafik](https://github.com/user-attachments/assets/9712cd36-baf5-4355-8ac6-6ac494f72aed)

## Projenin Motivasyonu

İşitme engelliler, çevresiyle iletişim kurmada ve günümüz internet çağında bilgiye ulaşmada işaret dilini kullanmak zorundadırlar. Fakat onların diline çeviri sunan kaynaklar neredeyse yok denecek kadar azdır. Bu durum, işitme engellilerin toplumdan soyutlanmasına ve bilgiye erişimlerinin kısıtlanmasına yol açmaktadır. Projemizin asıl motivasyonu, işitme engelli bireylerin herhangi bir videoyu veya metni kendi dillerinde, yani işaret diliyle anlayabilmeleri için bir yapay zeka sistemi geliştirmektir.

Amacımız, işitme engelli bireylerin dijital dünyada daha bağımsız olmalarını sağlamak, bilgiye erişimlerini kolaylaştırmak ve onların da kendi dillerinde bilgiye erişmelerine olanak vermektir.

![Output GIF](https://github.com/user-attachments/assets/87ac29d6-a278-4498-8512-9f98c3168229)

Projemiz, veriseti üretimi ve üretilen verisetini Progressive Transformer modeli ile eğitmek olmak üzere iki aşamaya ayrılmıştır.

## Veriseti Üretimi

![OpenPose ile Poz Çıkarımı](https://github.com/user-attachments/assets/d115ebfd-4f09-411c-b5af-720d7597713f)

İnternet üzerinde Türkçe işaret dili içeren kaynaklar araştırılarak farklı alanlardan işaret dili videoları bulunmuştur.

![Image](https://github.com/user-attachments/assets/1281ffc6-ad27-4cad-ac12-b0f655973a08)

Bu videoların toplam süresi 100 saati bulmaktadır ve aşağıdaki kodlarla gerekli tüm düzenlemeler yapılabilir hale getirilmiştir. YouTube'da Türkçe işaret dili içeren birçok video bulunduğundan, istenilen videolar üzerinden veriseti oluşturma yöntemini paylaşarak, kendi verisetlerinizi oluşturabilir ve yapay zeka modelini eğitebilirsiniz.

Kendi videolarınız üzerinde poz çıkarımı yapmak için `data_creation` klasörüne gidip `videos.txt` dosyasını kendi video URL'leri ile değiştirmeniz gerekir.
1. Video sesleri kullanılarak poz çıkarımı.
2. OpenPose modeli kullanılarak her frame için poz üretimi.
3. Üretilen pozlar üzerinde hatalar tespit edilip ağırlıklı bir algoritma ile yeniden işleme.
4. Verilerin normalize edilmesi ve poz cümleleri ile metinlerin eşlenmesi.

### YouTube Üzerinden Seçilen Videoları İndirmek ve Her Frame için İstenilen İnsan İskeletini (Pozlarını) Çıkarmak

Kaliteli işaret dili ve açıklayıcı ses içeren videolar bulmak projenin ana sorunlarından biri olmuştur. Bunun nedenleri; poz ve ses arasındaki gecikmeler, işaret dili çeviricisinin ekranın çok küçük bir alanında kalması (örneğin haber kanallarında sağ köşede çok küçük bir alanın kullanılması) ve işaret diliyle her sesin çevrilmemesiydi.

İnternet üzerinde birçok video araştırıldıktan sonra, TRT Haber'in işitme engelliler için özel olarak hazırladığı [İşitme Engelliler Haber Bülteni](https://www.youtube.com/playlist?list=PLZ5AxhlnKvj5PGmTHgFPyv7N1X3ScdpWh) yayını ile karşılaştık. Bu yayında ekranın yarısını işaret dili çevirmeni, diğer yarısını ise haber sunucusu kaplıyordu. Yayındaki 114 haber ile bir veriseti oluşturmaya başlandı.

Karşılaşılan bir diğer zorluk ise videolardan iskelet pozlarını çıkarmaktı. Burada [**OpenPose**](https://github.com/CMU-Perceptual-Computing-Lab/openpose/tree/v1.7.0) ve [**MediaPipe**](https://github.com/google-ai-edge/mediapipe) kütüphaneleri denenmiştir. OpenPose kütüphanesi kullanırken el+poz verisi için 10 GB VRAM gerekmekte ve 10 dakikalık bir video için 30 dakikalık işlem süresi gerekmekteydi. MediaPipe ise tam zamanlı olarak CPU'da bile çalışabilmekte, ancak ürettiği sonuçlar OpenPose kadar doğru ve tutarlı olmamaktadır.

Geliştirdiğimiz verisetinde, OpenPose kütüphanesi kullanılarak bulutta GPU kiralanıp pozlar çıkarıldı. Bu işlemin normalden üç kat daha yavaş olması nedeniyle videoların sadece bir bölümü veriseti olarak kullanıldı. Ancak paylaşılan kodlarla tüm videolardan poz çıkarımı yapılabilir.

### Whisper_large_v3 ile Türkçe Seslerden Metin Çıkarımı

Geliştirilen yapay zeka modeli, metin alıp poz verisi ürettiğinden, YouTube videolarının metin verisine çevrilmesi gerekiyordu. Bunun için OpenAI'ın Whisper modeli kullanıldı. Çıkarılan metinler ile o aralıktaki pozlar eşleştirilerek train, test ve val verisetleri kaydedildi.

## Model Üretimi

### Progressive Transformer Model Mimarisi Kurulumu ve Eğitimi

Geliştirdiğimiz model, giriş olarak aldığı metin cümlesini işleyerek encodera aktarır. Decoder modeli ise auto-regressive bir şekilde poz verilerini üretir. Üretilen poz verileri, giriş cümlesinin işaret diline çevrilmiş halidir.

<img src="https://github.com/user-attachments/assets/9980cb33-2947-43a8-b54d-63581d861fdd" alt="Model Mimarisi" width="600" height="600">

Verisetlerini elde ettikten sonra [bu adrese](https://github.com/enes3774/isitsel-ceviri/tree/main/model) gidebilir ve model eğitimine başlayabilirsiniz.

## Resimden Video Üretimi

Projemizin asıl amacı işitme engelliler için işaret dili konuşan insan videoları üretmek olduğundan, bu hedef üzerinde stable diffusion modellerini kendi poz verimiz ile çalışır hale getirdik. Burada elde ettiğimiz bir örnek videoyu paylaşıyoruz.

[Örnek Video](https://github.com/user-attachments/assets/6787617b-467d-4e9d-bcf8-e202f7c707cd)
