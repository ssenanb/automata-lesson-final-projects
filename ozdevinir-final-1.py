import time
import sys

class TuringMakinesi:
    def __init__(self, sayi1, sayi2):
        self.sayi1 = sayi1
        self.sayi2 = sayi2

        sonuc_uzunlugu = len(sayi1) + len(sayi2) + 2
        bant_girisi = f"{sayi1}*{sayi2}=" + "0" * sonuc_uzunlugu
        self.bant = list(bant_girisi) + ['B'] * 30 

        self.kafa = 0
        
        self.durum = "q_find_star"         
        self.kabul_durumu = "q_accept" 
        self.red_durumu = "q_reject" 
        
        self.adim = 0
        self.islenen_bit_sirasi = 0
        self.kaydirilmis_sayi = sayi1

    def bant_metni(self):
        ham_bant = ''.join(self.bant).rstrip('B')
        if self.kafa >= len(ham_bant):
            ham_bant = ham_bant.ljust(self.kafa + 1, 'B')
        return ham_bant

    def adim_yazdir(self, okunan_sembol, yazilan_sembol, hareket):
        bant_gorunumu = self.bant_metni()
        
        onsorgu = f"Adım {self.adim:03d} | Durum: {self.durum:<15} | O: {okunan_sembol} | Y: {yazilan_sembol} | H: {hareket} | Bant: "
        
        print(f"{onsorgu}{bant_gorunumu}")
        
        print(" " * len(onsorgu) + " " * self.kafa + "^")
        
        time.sleep(0.01)  

    def kafa_hareket_ettir(self, yon):
        if yon == 'R':
            self.kafa += 1
        elif yon == 'L':
            self.kafa -= 1
        self.adim += 1
    def banta_ekle(self, eklenecek_sayi):
            eski_durum = self.durum
            
            self.durum = "q_go_to_equals"
            while self.bant[self.kafa] != '=':
                self.adim_yazdir(self.bant[self.kafa], self.bant[self.kafa], 'R')
                self.kafa_hareket_ettir('R')

            self.durum = "q_go_to_result"
            while self.bant[self.kafa] in ['=', '0', '1']:
                self.adim_yazdir(self.bant[self.kafa], self.bant[self.kafa], 'R')
                self.kafa_hareket_ettir('R')

            self.adim_yazdir('B', 'B', 'L')
            self.kafa_hareket_ettir('L')

            for bit in reversed(eklenecek_sayi):
                if bit == '1':
                    self.durum = "q_add_1"
                    mevcut = self.bant[self.kafa]
                    if mevcut == '0':
                        self.bant[self.kafa] = '1'
                        self.adim_yazdir('0', '1', 'L')
                        self.kafa_hareket_ettir('L')
                    elif mevcut == '1':
                        self.bant[self.kafa] = '0'
                        self.adim_yazdir('1', '0', 'L')
                        self.kafa_hareket_ettir('L')

                        self.durum = "q_carry_1"
                        geri_adim = 0
                        
                        while self.bant[self.kafa] == '1':
                            self.bant[self.kafa] = '0'
                            self.adim_yazdir('1', '0', 'L')
                            self.kafa_hareket_ettir('L')
                            geri_adim += 1

                        self.bant[self.kafa] = '1'
                        self.adim_yazdir('0', '1', 'R')
                        self.kafa_hareket_ettir('R')

                        self.durum = "q_return"
                        for _ in range(geri_adim):
                            self.adim_yazdir(self.bant[self.kafa], self.bant[self.kafa], 'R')
                            self.kafa_hareket_ettir('R')

                        self.adim_yazdir(self.bant[self.kafa], self.bant[self.kafa], 'L')
                        self.kafa_hareket_ettir('L')

                else:
                    self.durum = "q_add_0"
                    self.adim_yazdir(self.bant[self.kafa], self.bant[self.kafa], 'L')
                    self.kafa_hareket_ettir('L')

            self.durum = "q_return_equals"
            while self.bant[self.kafa] != '=':
                self.adim_yazdir(self.bant[self.kafa], self.bant[self.kafa], 'L')
                self.kafa_hareket_ettir('L')

            self.durum = eski_durum
            
        
    def calistir(self):

        while self.durum not in [self.kabul_durumu, self.red_durumu]:
            okunan_sembol = self.bant[self.kafa]
            yazilan_sembol = okunan_sembol
            yon = "N"
            
            if self.durum == "q_find_star":
                if okunan_sembol in ['0', '1']:
                    yon = "R"
                elif okunan_sembol == '*':
                    print(f"\n>>> BİLGİ: '*' bulundu -> Operandlar ayrıştırıldı.")
                    print(f"    Sol Taraf (1. Sayı) : {self.sayi1}")
                    print(f"    Sağ Taraf (2. Sayı) : {self.sayi2}\n")
                    print("-" * 80)
                    self.durum = "q_find_equals"
                    yon = "R"
                else:
                    self.durum = self.red_durumu
            
            elif self.durum == "q_find_equals":
                if okunan_sembol in ['0', '1', 'X']:
                    yon = "R"
                elif okunan_sembol == '=':
                    self.durum = "q_find_bit"
                    yon = "L"
                else:
                    self.durum = self.red_durumu
            
            elif self.durum == "q_find_bit":
                if okunan_sembol == 'X':
                    yon = "L"
                elif okunan_sembol == '0':
                    yazilan_sembol = 'X'
                    self.bant[self.kafa] = 'X'
                    self.adim_yazdir(okunan_sembol, 'X', 'R')
                    self.kafa_hareket_ettir('R')
                    
                    self.islenen_bit_sirasi += 1
                    print("-" * 80)
                    print(f">>> BİLGİ: Sağdan {self.islenen_bit_sirasi}. bit = 0 -> Sadece kaydırma yapılacak, ekleme yok.")
                    print("-" * 80)
                    
                    self.kaydirilmis_sayi += '0' 
                    self.durum = "q_find_equals"
                    continue
                    
                elif okunan_sembol == '1':
                    yazilan_sembol = 'X'
                    self.bant[self.kafa] = 'X'
                    self.adim_yazdir(okunan_sembol, 'X', 'R')
                    self.kafa_hareket_ettir('R')
                    
                    self.islenen_bit_sirasi += 1
                    print("-" * 80)
                    print(f">>> BİLGİ: Sağdan {self.islenen_bit_sirasi}. bit = 1 -> {self.kaydirilmis_sayi} sola kaydırıldı ve banta eklenecek.")
                    print("-" * 80)
                    
                    self.banta_ekle(self.kaydirilmis_sayi) 
                    self.kaydirilmis_sayi += '0'
                    
                    self.durum = "q_find_equals"
                    continue
                    
                elif okunan_sembol == '*':
                    self.durum = self.kabul_durumu
                    yon = "N"
                else:
                    self.durum = self.red_durumu
            
            if self.durum == self.red_durumu:
                print("\n>>> HATA: Beklenmeyen sembol okundu! Makine Red Durumuna (q_reject) geçti.")
                sys.exit()
                
            if self.durum != self.kabul_durumu:
                self.bant[self.kafa] = yazilan_sembol
                self.adim_yazdir(okunan_sembol, yazilan_sembol, yon)
                self.kafa_hareket_ettir(yon)

        sonuc_str = "".join(self.bant).split('=')[1].replace('B', '').replace(' ', '')
        temiz_sonuc = sonuc_str.lstrip('0') or "0"

        print("\n" + "="*50)
        print(f"DURUM: {self.durum.upper()}")
        print(f"Final Bant: {''.join(self.bant).rstrip('B')}")
        print(f"Binary Sonuç: {temiz_sonuc}")
        print(f"Decimal Sonuç: {int(temiz_sonuc, 2)}")
        print("="*50)

def binary_kontrol(metin):
    return all(karakter in '01' for karakter in metin) and metin != ""


def main():
    print("** Turing Makinesi ile Binary Çarpma **\n")

    while True:
        sayi1 = input("1. sayı: ").strip()
        sayi2 = input("2. sayı: ").strip()

        if binary_kontrol(sayi1) and binary_kontrol(sayi2):
            break
        print("HATA: sadece 0 ve 1 girilmeli!\n")

    tm = TuringMakinesi(sayi1, sayi2)
    tm.calistir()


if __name__ == "__main__":
    main()
