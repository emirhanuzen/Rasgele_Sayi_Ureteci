# Özgün Rastgele Sayı Üreteci (ÖzgünRNG)

Bu proje, özel bir algoritma kullanarak rastgele sayılar üreten bir Python sınıfı içermektedir.

## 📋 İçindekiler

- [Genel Bakış](#genel-bakış)
- [Algoritma Açıklaması](#algoritma-açıklaması)
- [Çalışma Mantığı](#çalışma-mantığı)
- [Kullanım](#kullanım)
- [Teknik Detaylar](#teknik-detaylar)

## 🎯 Genel Bakış

`ÖzgünRNG` sınıfı, hibrit bir yaklaşım kullanarak rastgele sayılar üretir. Algoritma, **XOR-Shift** ve **Linear Congruential Generator (LCG)** tekniklerini birleştirerek yüksek kaliteli rastgele sayılar üretmeyi hedefler.

## 🔬 Algoritma Açıklaması

### Temel Bileşenler

1. **Tohum (Seed)**: Rastgele sayı üretiminin başlangıç noktası
2. **XOR-Shift Karıştırma**: Bit seviyesinde karıştırma işlemi
3. **LCG (Linear Congruential Generator)**: Çarpma ve mod alma işlemleri
4. **Normalizasyon ve Ölçekleme**: İstenen aralığa dönüştürme

## ⚙️ Çalışma Mantığı

### 1. Başlatma (Initialization)

```python
rng = OzgunRNG(seed=None)
```

- Eğer `seed` verilmezse, sistem zamanı (milisaniye cinsinden) kullanılır
- Eğer `seed` verilirse, o değer başlangıç durumu olarak ayarlanır
- Bu sayede aynı seed ile aynı rastgele sayı dizisi üretilebilir (tekrarlanabilirlik)

### 2. Rastgele Sayı Üretimi (next_random)

Algoritma üç ana adımdan oluşur:

#### Adım 1: XOR ve SHIFT (Karıştırma)

```python
x = self.state
x ^= (x << 13) & 0xFFFFFFFF  # Sola 13 bit kaydır ve XOR
x ^= (x >> 17)                # Sağa 17 bit kaydır ve XOR
x ^= (x << 5) & 0xFFFFFFFF    # Sola 5 bit kaydır ve XOR
```

**Ne yapıyor?**
- Sayının bitlerini karıştırarak daha rastgele bir dağılım sağlar
- XOR işlemi bitleri tersine çevirir, SHIFT işlemi bitleri hareket ettirir
- Bu kombinasyon, sayının bit yapısını tamamen değiştirir
- `0xFFFFFFFF` maskesi, 32-bit sınırlar içinde kalmayı garanti eder

**Örnek:**
```
Başlangıç: 10101010
<< 13:     01010000... (sola kaydır)
XOR:       11111010... (bitler karıştı)
```

#### Adım 2: LCG Mantığı (Çarpma ve Mod)

```python
self.state = (x * self.MULTIPLIER) % self.MODULUS
```

**Ne yapıyor?**
- Karıştırılmış sayıyı bir katsayı ile çarpar (`MULTIPLIER = 48271`)
- Sonucu bir modülüs ile sınırlar (`MODULUS = 2147483647`, yani 2³¹ - 1)
- Bu işlem, sayıyı belirli bir aralıkta tutar ve bir sonraki durumu oluşturur

**Neden bu sayılar?**
- `48271`: Standart LCG katsayısı, iyi dağılım özellikleri sağlar
- `2147483647`: Mersenne asalı (2³¹ - 1), maksimum periyot uzunluğu sağlar

#### Adım 3: İstenen Aralığa Ölçekleme

```python
normalized = self.state / self.MODULUS  # 0-1 arası değer
return int(min_val + (normalized * (max_val - min_val)))
```

**Ne yapıyor?**
- Durumu 0 ile 1 arasında normalize eder
- Bu değeri istenen min-max aralığına ölçekler
- Sonucu tam sayıya çevirir

**Örnek:**
```
state = 1,073,741,823
normalized = 1,073,741,823 / 2,147,483,647 ≈ 0.5
min_val = 0, max_val = 100
sonuç = 0 + (0.5 * 100) = 50
```

## 💻 Kullanım

### Temel Kullanım

```python
from rsagele import OzgunRNG

# Otomatik seed (zaman tabanlı)
rng = OzgunRNG()

# 0-100 arası rastgele sayı
sayi = rng.next_random(0, 100)
print(sayi)
```

### Özel Seed ile Kullanım

```python
# Belirli bir seed ile (tekrarlanabilir sonuçlar)
rng = OzgunRNG(seed=12345)

# Her çalıştırmada aynı diziyi üretir
sayi1 = rng.next_random(0, 100)
sayi2 = rng.next_random(0, 100)
```

### Birden Fazla Sayı Üretme

```python
rng = OzgunRNG()

for i in range(10):
    sayi = rng.next_random(1, 100)
    print(f"{i+1}. Sayı: {sayi}")
```

## 🔧 Teknik Detaylar

### Algoritma Özellikleri

- **Periyot**: 2³¹ - 1 (yaklaşık 2.1 milyar sayı)
- **Hız**: Çok hızlı (bit işlemleri ve basit matematik)
- **Bellek**: Minimal (sadece bir durum değişkeni)
- **Kalite**: XOR-Shift ve LCG kombinasyonu ile yüksek kalite

### Avantajlar

✅ **Hızlı**: Bit işlemleri ve basit matematik işlemleri  
✅ **Hafif**: Minimal bellek kullanımı  
✅ **Tekrarlanabilir**: Aynı seed ile aynı sonuçlar  
✅ **Özelleştirilebilir**: Seed ve parametreler ayarlanabilir  

### Kullanım Alanları

- Oyun geliştirme
- Simülasyonlar
- Test verisi üretimi
- Kriptografik olmayan rastgele sayı gereksinimleri

## 📝 Notlar

- Bu algoritma **kriptografik amaçlar için uygun değildir**
- Güvenlik gerektiren uygulamalar için Python'un `secrets` modülü kullanılmalıdır
- Algoritma, eğlence ve öğrenme amaçlıdır

## 🎓 Algoritma Türleri

Bu kod şu algoritmaları birleştirir:

1. **XOR-Shift**: Hızlı ve basit bit karıştırma
2. **LCG (Linear Congruential Generator)**: Klasik rastgele sayı üretimi
3. **Hibrit Yaklaşım**: İkisinin avantajlarını birleştirme

## 📊 Örnek Çıktı

```
Üretilen Rastgele Sayılar (0-100 arası):
----------------------------------------
1. Sayı: 42
2. Sayı: 17
3. Sayı: 89
...
----------------------------------------
Liste: [42, 17, 89, ...]
```

---

**Geliştirici Notu**: Bu algoritma, rastgele sayı üretimi konusunda eğitici bir örnektir. Gerçek uygulamalarda Python'un `random` modülü veya daha gelişmiş algoritmalar tercih edilmelidir.

