ClipGoat: Video Hikaye Oluşturucu
ClipGoat, mevcut bir arka plan videosu üzerine metin tabanlı hikayeler ekleyerek otomatik olarak yeni videolar oluşturan bir Python aracıdır. Proje, bir grafik kullanıcı arayüzü (GUI) ve video işleme için güçlü bir arka uç (backend) içerir. Kullanıcılar, arka plan videosunu seçebilir, hikaye metnini girebilir ve yazı tipi boyutu, rengi, kutu rengi ve opaklığı gibi çeşitli ayarları özelleştirebilir.

Temel Özellikler
Kullanıcı Dostu Arayüz: Proje, tkinter kütüphanesi kullanılarak geliştirilmiş basit ve sezgisel bir GUI'ye sahiptir. Bu arayüz, arka plan videosu ve hikaye metni girişini kolaylaştırır.

Özelleştirilebilir Ayarlar: Kullanıcılar;

Yazı tipi boyutunu ve rengini

Metin kutusunun rengini ve şeffaflığını

Altyazı konumunu (alt, üst, orta)

Metin okuma (TTS) hızını ve ses cinsiyetini (kadın, erkek) ayarlayabilir.

Otomatik Video Oluşturma: create_story_video fonksiyonu, arka plan videosunu, hikaye metnini ve ayarları alarak tüm video oluşturma sürecini otomatikleştirir.

TTS Entegrasyonu: Proje, metinden sese dönüştürme (TTS) işlemi için edge_tts kütüphanesini kullanır. TTS hız ayarı, potansiyel hataları önlemek için backend'de devre dışı bırakılmıştır.

Video ve Ses İşleme: moviepy kütüphanesi, ses ve altyazı kliplerini arka plan videosuyla birleştirmek için kullanılır. Bu, nihai video dosyasının oluşturulmasını sağlar.

Kurulum
Projenin çalışması için gerekli olan kütüphaneleri yüklemeniz gerekmektedir:

moviepy

edge_tts (backend dosyasında bahsedilen kütüphane)

Bu kütüphaneleri pip ile yükleyebilirsiniz:

pip install moviepy edge-tts

Ayrıca, moviepy ffmpeg'in yüklü olmasını gerektirir. ffmpeg'i resmi web sitesinden indirip sistem PATH'inize eklemeniz gerekmektedir.

Kullanım
clipgoat_local_gui.py dosyasını çalıştırın.

python clipgoat_local_gui.py

GUI'de bir arka plan videosu (.mp4, .mov, .avi, .mkv gibi formatlarda) seçin.

"Hikaye Metni" kutusuna videonuzda görünmesini ve seslendirilmesini istediğiniz metni yazın.

İstediğiniz ayarları düzenleyin.

"Videoyu Oluştur" düğmesine tıklayın.

Video oluşturulduktan sonra, çıktı dosyası orijinal video dosyasının bulunduğu klasörde video_adi_story.mp4 adıyla kaydedilecektir.
