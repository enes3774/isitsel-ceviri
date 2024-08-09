# İşitsel Çeviri

İşitsel Çeviri, herhangi bir Türkçe videonun sesini işleyerek sürekli bir şekilde Türkçe işaret diline çeviren [Progressive Transformer mimarisine](https://arxiv.org/pdf/2004.14874) dayalı bir yapay zeka modelidir.

![örnek_grafik](https://github.com/user-attachments/assets/9712cd36-baf5-4355-8ac6-6ac494f72aed)

# Projenin Motivasyonu
İşitme engelliler, çevresiyle iletişim kurmada ve günümüz internet çağında bilgiye ulaşmada işaret dilini kullanmak zorundadırlar. Fakat onların diline çeviri sunan kaynaklar neredeyse yok denebilir. Bu, toplumdan işitme engellilerin soyutlanması ve onların bilgiye erişimini kısıtlamaktadır. Projemizin asıl motivasyonu, işitme engelli bireylerin herhangi bir videoyu veya metni kendi dillerinde, yani işaret diliyle anlayabilmeleri için videoları işaret diline çeviren bir yapay zeka sistemi geliştirilmiştir.

Amacımız, işitme engelli bireylerin dijital dünyada daha bağımsız olmalarını sağlamak, bilgiye erişimlerini kolaylaştırmak ve onların da kendi dillerinde bilgiye erişmesine olanak vermektir.

Projemiz Veriseti üretimi ve üretilen verisetini Progressive Transformer modeli ile eğitim yapmak olarak 2'ye ayrılmıştır. 

# Veriseti Üretimi
![openpose ile pose çıkarımı](https://github.com/user-attachments/assets/d115ebfd-4f09-411c-b5af-720d7597713f)



Youtube'da Türkçe işaret dili içeren birçok video bulunabileceğinden verisetini istenilen videolar üzerinden çıkarmak ve kendi verisetleri ile yapay zeka modelini eğitmek isteyenler için verilen videolardan veriseti oluşturma yöntemini paylaşıyoruz.

## Youtube Üzerinden Seçilen Videoları İndirmek ve Her Frame için İstenilen İnsan İskeletini(Pozlarını) Çıkarmak
Kaliteli işaret dili ve açıklayıcı ses içeren videoalr bulabilmek prjenin ana sorunlarından biri olmuştu. Bunun nedenleri; poz ve ses arası gecikmeler, işaret dili çeviricisinin ekranın çok küçük bir alanında kalması(mesela haber kanallarında sağ köşede çok küçük bir alan barındırıyor), işaret diliyle her sesin çevirilmemesiydi.
İnternet üzerinde birçok video araştırıldıktan sonra TRT Haber'in işitme engelliler için özel yaptığı [İşitme Engelliler Haber Bülteni](https://www.youtube.com/playlist?list=PLZ5AxhlnKvj5PGmTHgFPyv7N1X3ScdpWh) yayınıyla karşılaştık. Burada ekranın yarısını işaret dili çevirmeni karşılıyor, diğer yarısı da haberi anlatıyordu. Yayındaki 114 haber ile bir veriseti oluşturulmaya başlandı. 

Karşılaşılan bir diğer zorluk ise videolarda isklete pozlarını çıkarmak oldu. Burada [**OpenPose**](https://github.com/CMU-Perceptual-Computing-Lab/openpose/tree/v1.7.0) kütüphanesi ve [**MediaPipe**](https://github.com/google-ai-edge/mediapipe) kütüphanneleri denenmiştir. Openpose kütüphanesi kullanırken el+poz verisi için 10gb VRAM gerekmekte ve 10dk'lık video için 30dk process sürmekteydi. Mediapipe ise tam zamanlı ve CPU'da bile çalışabilmekte ama ürettiği sonuçlar openpose kadar doğru ve tutarlı olmuyor.

Geliştirdiğimiz verisetinde OpenPose kütüphanesi kullanılarak cloud'da GPU kiralayarak pozları çıkarma yoluna gittik. Bu işlemin normalden 3 kat daha yavaş olması nedeniyle videoların sadece bir bölümü verisetine katıldı. Fakat paylaşılan kodlarla tüm videolardan  poz çıkarımı yapılabilir.
## Whisper_large_v3 ile Türkçe seslerden metin çıkarımı yapılması
Geliştirilen yapay zeka modeli metin alıp poz verisi ürettiğinden youtube videolarının metin verisine çevirilmesi lazımdı. Bunun için OpenAI'ın Whiper modeli kullanıldı. Çıkarılan metinler ile o aralıktaki pozlar eşlenerek train, test ve val verisetleri kaydedildi.



data_creation klasorune gidip videos.txt dosyasına 
