import time

class OzgunRNG:
    def __init__(self, seed=None):
        """
        Başlangıç tohumunu (seed) ayarlar.
        Eğer seed verilmezse, o anki zamanı kullanır.
        """
        if seed is None:
            # Zamanı milisaniye cinsinden alıp tamsayıya çeviriyoruz
            self.state = int(time.time() * 1000)
        else:
            self.state = seed
        
        # Algoritma için sabitler (Büyük asal sayılar seçmek güvenliği artırır)
        self.MULTIPLIER = 48271  # Standart bir LCG katsayısı (veya sevdiğiniz bir asal sayı)
        self.MODULUS = 2147483647 # 2^31 - 1 (Mersenne Asalı)

    def next_random(self, min_val, max_val):
        """
        Belirtilen aralıkta rastgele bir sayı üretir.
        """
        # 1. ADIM: XOR ve SHIFT (Karıştırma)
        # Sayıyı kendisinin sola kaydırılmış haliyle XOR'luyoruz.
        # Bu işlem bitleri karman çorman eder.
        x = self.state
        x ^= (x << 13) & 0xFFFFFFFF # 32 bit sınırı içinde kalması için
        x ^= (x >> 17)
        x ^= (x << 5) & 0xFFFFFFFF
        
        # 2. ADIM: LCG Mantığı (Çarpma ve Mod)
        # Karışan sayıyı bir katsayı ile çarpıp mod alıyoruz.
        self.state = (x * self.MULTIPLIER) % self.MODULUS
        
        # 3. ADIM: İstenen Aralığa Ölçekleme
        # 0 ile 1 arasında normalize edilmiş bir değer elde et
        normalized = self.state / self.MODULUS
        
        # Min-Max aralığına oturt
        return int(min_val + (normalized * (max_val - min_val)))

# --- TEST KISMI ---

rng = OzgunRNG() # Tohum otomatik olarak zamandan alınır

print("Üretilen Rastgele Sayılar (0-100 arası):")
print("-" * 40)

# 10 tane rastgele sayı üretelim
dagilim = []
for i in range(1):
    sayi = rng.next_random(0, 100)
    dagilim.append(sayi)
    print(f"{i+1}. Sayı: {sayi}")

print("-" * 40)
print(f"Liste: {dagilim}")