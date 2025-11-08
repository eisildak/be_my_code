# Simple Calculator
# Basit hesap makinesi

def topla(a, b):
    return a + b

def cikar(a, b):
    return a - b

def carp(a, b):
    return a * b

def bol(a, b):
    if b == 0:
        return "Hata: Sıfıra bölme!"
    return a / b

def hesap_makinesi():
    print("=== Basit Hesap Makinesi ===")
    print("İşlemler: +, -, *, /")
    print("Çıkmak için 'q' yazın\n")
    
    while True:
        islem = input("İşlem seçin (+, -, *, /) veya 'q' çıkış: ")
        
        if islem.lower() == 'q':
            print("Hoşça kalın!")
            break
        
        if islem not in ['+', '-', '*', '/']:
            print("Geçersiz işlem! Lütfen +, -, *, / seçin.")
            continue
        
        try:
            sayi1 = float(input("Birinci sayı: "))
            sayi2 = float(input("İkinci sayı: "))
            
            if islem == '+':
                sonuc = topla(sayi1, sayi2)
            elif islem == '-':
                sonuc = cikar(sayi1, sayi2)
            elif islem == '*':
                sonuc = carp(sayi1, sayi2)
            elif islem == '/':
                sonuc = bol(sayi1, sayi2)
            
            print(f"\nSonuç: {sayi1} {islem} {sayi2} = {sonuc}\n")
            
        except ValueError:
            print("Hata: Lütfen geçerli bir sayı girin!\n")
        except Exception as e:
            print(f"Bir hata oluştu: {e}\n")

# Programı çalıştır
if __name__ == "__main__":
    hesap_makinesi()
