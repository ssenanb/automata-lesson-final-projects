BLANK = "_"

START_STATE = "q0"
ACCEPT_STATE = "q7"
REJECT_STATE = "q8"

EXPECTED = {
    "q0": "digit",   # 1. karakter
    "q1": "digit",   # 2. karakter
    "q2": "upper",   # 3. karakter
    "q3": "upper",   # 4. karakter
    "q4": "digit",   # 5. karakter
    "q5": "digit",   # 6. karakter
    "q6": "digit",   # 7. karakter
}

def symbol_class(ch: str) -> str:
    if "0" <= ch <= "9":
        return "digit"
    if "A" <= ch <= "Z":
        return "upper"
    if ch == BLANK:
        return "blank"
    return "other"

def tape_view(tape, head):
    shown = []
    for i, ch in enumerate(tape):
        if i == head:
            shown.append(f"[{ch}]")
        else:
            shown.append(f" {ch} ")
    return "".join(shown)

def next_state_from(state: str) -> str:
    """q0->q1, q1->q2, ... q6->q7."""
    if state.startswith("q") and state[1:].isdigit():
        n = int(state[1:])
        return f"q{n + 1}"
    return REJECT_STATE

def transition(state: str, symbol: str):
    if state == REJECT_STATE:
        return REJECT_STATE, symbol, "S", "Already rejected"

    if state == ACCEPT_STATE:
        if symbol == BLANK:
            return ACCEPT_STATE, symbol, "S", "End of tape reached"
        return REJECT_STATE, symbol, "S", "Extra character after 7 symbols"

    expected = EXPECTED.get(state)

    actual = symbol_class(symbol)

    if expected is not None and actual == expected:
        return next_state_from(state), symbol, "R", "Symbol matched"

    return REJECT_STATE, symbol, "S", "Symbol mismatch"

def simulate_turing_machine(input_string: str, verbose: bool = True) -> bool:
    tape = list(input_string) + [BLANK] 
    head = 0
    state = START_STATE
    step = 1

    if verbose:
        print("\n--- Turing Makinesi Simülasyonu Başladı ---")
        print(f"Girdi: {input_string}")
        print(f"Başlangıç bandı: {''.join(tape)}\n")

    while True:
        current_symbol = tape[head] if head < len(tape) else BLANK

        if state == ACCEPT_STATE:
            if verbose:
                print(
                    f"Adım {step:02d} | Durum: {state} | Okunan: {current_symbol} | "
                    f"Kafa: S | Bant: {tape_view(tape, head)}"
                )
            if current_symbol == BLANK:
                if verbose:
                    print("\nSonuç: KABUL")
                return True
            else:
                if verbose:
                    print("\nSonuç: RED")
                return False

        if state == REJECT_STATE:
            if verbose:
                print(f"Adım {step:02d} | Durum: {state} | Sonuç: RED")
            return False

        new_state, written_symbol, move, reason = transition(state, current_symbol)

        if head < len(tape):
            tape[head] = written_symbol
        else:
            tape.append(written_symbol)

        if verbose:
            print(
                f"Adım {step:02d} | Durum: {state} | Okunan: {current_symbol} | "
                f"Yazılan: {written_symbol} | Kafa hareketi: {move} | "
                f"Sonraki durum: {new_state} | Bant: {tape_view(tape, head)}"
            )

        state = new_state

        if state == REJECT_STATE:
            if verbose:
                print("\nSonuç: RED")
            return False

        if move == "R":
            head += 1
            if head >= len(tape):
                tape.append(BLANK)
        elif move == "L":
            head = max(0, head - 1)

        step += 1

def print_transition_table():
    print("\n--- Geçiş Tablosu ---")
    print("Durum | Beklenen | Doğruysa -> | Yanlışsa ->")
    print("---------------------------------------------")
    for state in ["q0", "q1", "q2", "q3", "q4", "q5", "q6"]:
        expected = EXPECTED[state]
        print(f"{state:5} | {expected:8} | {next_state_from(state):10} | q8")
    print(f"{ACCEPT_STATE:5} | blank     | kabul      | q8")
    print(f"{REJECT_STATE:5} | -         | -          | -")

if __name__ == "__main__":
    plate = input("Plaka giriniz: ")
    simulate_turing_machine(plate, verbose=True)