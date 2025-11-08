# Loops Demo
# For ve While döngüleri

# FOR DÖNGÜSÜ ÖRNEKLERİ

print("=== For Döngüsü Örnekleri ===\n")

# 1-10 arası sayıları yazdır
print("1'den 10'a kadar sayılar:")
for i in range(10):
    print(i + 1, end=" ")
print("\n")

# Liste üzerinde döngü
meyveler = ["elma", "armut", "muz", "çilek"]
print("Meyveler:")
for meyve in meyveler:
    print(f"- {meyve}")
print()

# Enumerate ile index ve değer
print("Index ve değerler:")
for index, meyve in enumerate(meyveler):
    print(f"{index}: {meyve}")
print()


# WHILE DÖNGÜSÜ ÖRNEKLERİ

print("\n=== While Döngüsü Örnekleri ===\n")

# Basit sayaç
print("0'dan 5'e kadar:")
sayac = 0
while sayac <= 5:
    print(sayac, end=" ")
    sayac += 1
print("\n")

# Koşullu while
print("Çift sayılar (0-10):")
sayi = 0
while sayi <= 10:
    if sayi % 2 == 0:
        print(sayi, end=" ")
    sayi += 1
print("\n")

# Break kullanımı
print("Break örneği:")
i = 0
while True:
    if i >= 5:
        break
    print(i, end=" ")
    i += 1
print()
