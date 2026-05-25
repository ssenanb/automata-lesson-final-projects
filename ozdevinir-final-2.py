BLANK = "_"
START_STATE = "q0"
ACCEPT_STATE = "q7"
REJECT_STATE = "q8"

def is_digit(ch):
    return "0" <= ch <= "9"

def is_upper(ch):
    return "A" <= ch <= "Z"

def transition(state, symbol):
    if state == "q0":
        return ("q1", symbol, "R") if is_digit(symbol) else (REJECT_STATE, symbol, "S")
    if state == "q1":
        return ("q2", symbol, "R") if is_digit(symbol) else (REJECT_STATE, symbol, "S")
    if state == "q2":
        return ("q3", symbol, "R") if is_upper(symbol) else (REJECT_STATE, symbol, "S")
    if state == "q3":
        return ("q4", symbol, "R") if is_upper(symbol) else (REJECT_STATE, symbol, "S")
    if state == "q4":
        return ("q5", symbol, "R") if is_digit(symbol) else (REJECT_STATE, symbol, "S")
    if state == "q5":
        return ("q6", symbol, "R") if is_digit(symbol) else (REJECT_STATE, symbol, "S")
    if state == "q6":
        return (ACCEPT_STATE, symbol, "R") if is_digit(symbol) else (REJECT_STATE, symbol, "S")
    
    if state == ACCEPT_STATE:
        return (ACCEPT_STATE if symbol == BLANK else REJECT_STATE, symbol, "S")
    
    return (REJECT_STATE, symbol, "S")

def simulate_turing_machine(input_string, verbose=True):
    tape = list(input_string) + [BLANK]
    head = 0
    state = START_STATE
    step = 1
    
    print(f"Girdi: {input_string}")
    print(f"Başlangıç bandı: {''.join(tape)}")
    print("-" * 50)

    while True:
        current_symbol = tape[head]
        
        if state == ACCEPT_STATE and current_symbol == BLANK:
            formatted_tape = " ".join([f"[{t}]" if i == head else t for i, t in enumerate(tape)])
            print(f"Adım {step:02d} | Durum: {state} | Okunan: {current_symbol} | Kafa: S | Bant: {formatted_tape}")
            print("Sonuç: KABUL")
            return True
        
        if state == REJECT_STATE or (state == ACCEPT_STATE and current_symbol != BLANK):
            print("Sonuç: RED")
            return False

        new_state, written, move = transition(state, current_symbol)
        
        formatted_tape = " ".join([f"[{t}]" if i == head else t for i, t in enumerate(tape)])
        
        if verbose:
            print(f"Adım {step:02d} | Durum: {state} | Okunan: {current_symbol} | Yazılan: {written} | "
                  f"Kafa hareketi: {move} | Sonraki durum: {new_state} | Bant: {formatted_tape}")
        
        state = new_state
        if move == "R" and head < len(tape) - 1:
            head += 1

if __name__ == "__main__":
    plate = input("Plaka giriniz: ")
    simulate_turing_machine(plate)
