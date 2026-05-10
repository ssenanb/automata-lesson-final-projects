class TuringMachineSimulator:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
        result_space = "0" * (len(num1) + len(num2))
        self.tape = list(f"{num1}*{num2}={result_space}")
        self.head = 0
        self.state = 'q_start'
        self.step_count = 0
        
    def print_step(self, read_sym, write_sym, move_dir, prev_state):
        tape_content = "".join(self.tape)
        print(f"Adım {self.step_count:03d} | Durum: {prev_state:<18} | Okunan: {read_sym:<2} | Yazılan: {write_sym:<2} | Hareket: {move_dir:<2} | Bant: {tape_content}")

    def run(self):
        print("\n--- Turing Makinesi Çalışmaya Başlıyor ---")
        
        while self.tape[self.head] != '*':
            self.step_count += 1
            read_sym = self.tape[self.head]
            self.print_step(read_sym, read_sym, 'R', self.state)
            self.head += 1
            
        self.step_count += 1
        self.state = 'q_star_found'
        self.print_step('*', '*', 'R', 'q_start')
        self.head += 1

        toplam_sonuc = 0
        shift_count = 0 # Her adımda num1'i kaydırmak için

        while True:
            self.state = 'q_find_equals'
            while self.tape[self.head] != '=':
                self.step_count += 1
                read_sym = self.tape[self.head]
                self.print_step(read_sym, read_sym, 'R', self.state)
                self.head += 1
            
            search_head = self.head - 1
            while search_head >= 0 and self.tape[search_head] == 'X':
                search_head -= 1
            
            if self.tape[search_head] == '*':
                break

            bit = self.tape[search_head]
            self.tape[search_head] = 'X' 
            
            self.step_count += 1
            self.state = 'q_process_bit'
            self.print_step('=', '=', 'R', 'q_find_equals')
            self.head += 1 
            
            if bit == '1':
                toplam_sonuc += int(self.num1, 2) << shift_count
                sonuc_bin = bin(toplam_sonuc)[2:].zfill(len(self.num1) + len(self.num2))
                
                self.state = 'q_add_and_write'
                for i, char in enumerate(sonuc_bin):
                    if self.head + i < len(self.tape):
                        self.step_count += 1
                        eski_deger = self.tape[self.head + i]
                        self.tape[self.head + i] = char
                        self.print_step(eski_deger, char, 'R', self.state)
                
                self.head += len(sonuc_bin) - 1
                print(f">>> BİLGİ: Bit = 1 -> Ekleme yapıldı.")
            else:
                print(">>> BİLGİ: Bit = 0 -> İşlem yapılmadan geri dönülüyor.")
                self.step_count += 1
                self.print_step(self.tape[self.head], self.tape[self.head], 'L', 'q_process_bit')
                self.head -= 1
            
            shift_count += 1 
            
            self.state = 'q_return_star'
            while self.tape[self.head] != '*':
                self.step_count += 1
                read_sym = self.tape[self.head]
                self.print_step(read_sym, read_sym, 'L', self.state)
                self.head -= 1
            self.head += 1 # Yıldızın sağından tekrar başla

        self.state = 'q_accept'
        final_tape_str = "".join(self.tape)
        final_result_str = final_tape_str.split('=')[1].lstrip('0') or "0"
        
        print("\n=== BEKLENEN ÇIKTI ===")
        print(f"Bantın Son Hali: {final_tape_str}")
        print(f"Binary Sonuç: {final_result_str}\nDecimal Sonuç: {int(final_result_str, 2)}")

def main():
    num1 = input("Birinci binary sayıyı giriniz: ").strip()
    num2 = input("İkinci binary sayıyı giriniz: ").strip()
    if num1 and num2:
        TuringMachineSimulator(num1, num2).run()
    else:
        print("Hata: Geçersiz giriş.")

if __name__ == "__main__":
    main()
