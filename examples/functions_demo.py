# Functions Demo
# Fonksiyon tanımlama örnekleri

# Basit fonksiyon
def selamla():
    print("Merhaba!")

# Parametreli fonksiyon
def kisisel_selamlama(isim):
    print(f"Merhaba {isim}!")

# Döndürme (return) fonksiyonu
def topla(a, b):
    return a + b

# Çoklu parametre
def hesapla(sayi1, sayi2, islem):
    if islem == "topla":
        return sayi1 + sayi2
    elif islem == "cikar":
        return sayi1 - sayi2
    elif islem == "carp":
        return sayi1 * sayi2
    elif islem == "bol":
        if sayi2 != 0:
            return sayi1 / sayi2
        else:
            return "Sıfıra bölme hatası!"
    else:
        return "Geçersiz işlem"

# Varsayılan parametre
def guc(taban, us=2):
    return taban ** us

# Fonksiyonları test et
print("=== Fonksiyon Örnekleri ===\n")

selamla()
kisisel_selamlama("Erol")

print(f"\n5 + 3 = {topla(5, 3)}")
print(f"10 - 4 = {hesapla(10, 4, 'cikar')}")
print(f"6 * 7 = {hesapla(6, 7, 'carp')}")
print(f"20 / 4 = {hesapla(20, 4, 'bol')}")

print(f"\n2^3 = {guc(2, 3)}")
print(f"5^2 = {guc(5)}")  # Varsayılan us=2
