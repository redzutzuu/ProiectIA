import math
import random
import tkinter as tk
from tkinter import messagebox

def center_window(window, width_ratio=0.75, height_ratio=0.75):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    width = int(screen_width * width_ratio)
    height = int(screen_height * height_ratio)
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def minimax(depth, is_maximizing, sticks, alpha, beta, max_picks):
    if sticks == 0:
        return -1 if is_maximizing else 1

    if depth == 0:
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(1, min(max_picks, sticks) + 1):
            eval = minimax(depth - 1, False, sticks - i, alpha, beta, max_picks)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(1, min(max_picks, sticks) + 1):
            eval = minimax(depth - 1, True, sticks - i, alpha, beta, max_picks)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def bot_move(sticks, max_picks, max_depth, factor=3):
    depth = min(max_depth, max(1, sticks // factor))
    best_move = None
    best_value = -math.inf
    for i in range(1, min(max_picks, sticks) + 1):
        value = minimax(depth, False, sticks - i, -math.inf, math.inf, max_picks)
        if value > best_value:
            best_value = value
            best_move = i
    return best_move

def display_gramezi(gramezi, frame):
    for widget in frame.winfo_children():
        widget.destroy()

    max_per_row = 5
    for idx, sticks in enumerate(gramezi):
        row = idx // max_per_row
        col = idx % max_per_row
        pile_frame = tk.Frame(frame, bg="lightblue", bd=2, relief="groove")
        pile_frame.grid(row=row, column=col, padx=15, pady=15)

        tk.Label(
            pile_frame,
            text=f"Gramada {idx + 1}: {sticks} bete",
            font=("Arial", 12, "bold"),
            bg="lightblue"
        ).pack()

        # Afișare pe linii de câte 7 bețe
        stick_frame = tk.Frame(pile_frame, bg="lightblue")
        stick_frame.pack()
        for i in range(sticks):
            if i > 0 and i % 7 == 0:
                stick_frame = tk.Frame(pile_frame, bg="lightblue")
                stick_frame.pack()
            tk.Label(
                stick_frame,
                text="\u25A0",
                font=("Arial", 18),
                bg="green",
                width=2,
                height=1
            ).pack(side=tk.LEFT, padx=2)



def update_game_state(gramezi, max_picks, depth, player_turn, frame, inputs_frame):
    if sum(gramezi) <= 0:
        if player_turn:
            messagebox.showinfo("Joc terminat", "Ai pierdut! Botul a castigat.")
        else:
            messagebox.showinfo("Joc terminat", "Felicitari! Ai castigat impotriva botului.")
        frame.master.destroy()
        return

    display_gramezi(gramezi, frame)

    for widget in inputs_frame.winfo_children():
        widget.destroy()

    if not player_turn:
        bot_choice, grămadă_idx = bot_decide(gramezi, max_picks, depth)
        gramezi[grămadă_idx] -= bot_choice
        messagebox.showinfo("Botul a mutat", f"Botul a luat {bot_choice} bete din gramada {grămadă_idx + 1}.")
        update_game_state(gramezi, max_picks, depth, True, frame, inputs_frame)
    else:
        tk.Label(inputs_frame, text="Introduceti gramada :", font=("Arial", 12), bg="lightblue").pack(pady=5)
        pile_input = tk.Entry(inputs_frame, font=("Arial", 12))
        pile_input.pack(pady=5)
        tk.Label(inputs_frame, text="Introduceti numarul de bete:", font=("Arial", 12), bg="lightblue").pack(
            pady=5)
        stick_input = tk.Entry(inputs_frame, font=("Arial", 12))
        stick_input.pack(pady=5)

        def on_player_move():
            try:
                grămadă_idx = int(pile_input.get()) - 1
                sticks_to_remove = int(stick_input.get())

                if 0 <= grămadă_idx < len(gramezi) and 1 <= sticks_to_remove <= min(max_picks, gramezi[grămadă_idx]):
                    gramezi[grămadă_idx] -= sticks_to_remove
                    update_game_state(gramezi, max_picks, depth, False, frame, inputs_frame)
                else:
                    messagebox.showerror("Eroare", "Introdu o gramada valida si un numar valid de bete.")
            except ValueError:
                messagebox.showerror("Eroare", "Introdu o gramada valida si un numar de bete.")

        tk.Button(inputs_frame, text="Mutare", font=("Arial", 14), bg="#ADD8E6", command=on_player_move).pack(pady=10)
        tk.Button(inputs_frame, text="Înapoi", font=("Arial", 14),  bg="#ADD8E6",command=lambda: [inputs_frame.pack_forget(), show_menu()]).pack(pady=10)
        tk.Button(inputs_frame, text="Exit", font=("Arial", 14),  bg="#ADD8E6",command=root.destroy).pack(pady=10)

def bot_decide(gramezi, max_picks, depth):
    for grămadă_idx, sticks in enumerate(gramezi):
        for i in range(1, min(max_picks, sticks) + 1):
            gramezi_test = gramezi[:]
            gramezi_test[grămadă_idx] -= i
            if minimax(depth, False, sum(gramezi_test), -math.inf, math.inf, max_picks) == 1:
                return i, grămadă_idx
    return 1, 0


import random


def generate_gramezi(total_bete, num_gramezi):
    # Calculează distribuția inițială uniformă
    base_bete = total_bete // num_gramezi
    gramezi = [base_bete] * num_gramezi

    # Distribuie restul de bețe rămase
    bete_ramase = total_bete - sum(gramezi)
    for i in range(bete_ramase):
        gramezi[random.randint(0, num_gramezi - 1)] += 1

    # Introduce o variație aleatorie pentru diversitate
    for i in range(num_gramezi):
        if gramezi[i] > 1:  # Asigură-te că grămada nu devine 0
            schimb = random.randint(-1, 1)  # Mică variație: poate adăuga/scădea 1
            gramezi[i] += schimb
            # Ajustează altă grămadă pentru a păstra totalul constant
            alt_index = random.randint(0, num_gramezi - 1)
            while alt_index == i:
                alt_index = random.randint(0, num_gramezi - 1)
            gramezi[alt_index] -= schimb

    # Asigură-te că toate grămezile au cel puțin un băț
    for i in range(num_gramezi):
        if gramezi[i] <= 0:
            gramezi[i] = 1

    # Amestecă grămezile pentru diversitate suplimentară
    random.shuffle(gramezi)

    # Asigură-te că suma totală e corectă
    assert sum(gramezi) == total_bete, "Suma totală a bețelor nu este corectă!"

    return gramezi


def start_game(frame, total_bete, num_gramezi, max_picks):
    if total_bete <= 0 or num_gramezi <= 0 or max_picks <= 0:
        messagebox.showerror("Eroare", "Toate valorile trebuie să fie mai mari ca zero!")
        return

    if total_bete < num_gramezi:
        messagebox.showerror("Eroare", "Numărul total de bețe trebuie să fie cel puțin egal cu numărul de grămezi!")
        return
    if max_picks <= 0 or max_picks > (total_bete - num_gramezi):
        messagebox.showerror("Eroare", "Numărul maxim de bețe a unei mutări este prea mare!\n "
                                       "Vă rog sa aveți maxim: (total_bețe)-(număr_grămezi)")
        return
    gramezi = generate_gramezi(total_bete, num_gramezi)
    depth = max(1, min(10, total_bete // 3))

    frame.pack_forget()
    game_frame = tk.Frame(frame.master, bg="lightblue")
    game_frame.pack(fill=tk.BOTH, expand=True)

    inputs_frame = tk.Frame(frame.master, bg="lightblue")
    inputs_frame.pack(fill=tk.BOTH, expand=True)

    update_game_state(gramezi, max_picks, depth, True, game_frame, inputs_frame)

def show_menu():
    def reguli():
        info_text = (
            "Acesta este jocul Nim.\n\n"
            "Reguli:\n"
            "1. Jocul începe cu un număr de grămezi, fiecare conținând un anumit număr de obiecte.\n"
            "2. Jucătorii, pe rând, pot lua unul sau mai multe obiecte dintr-o singură grămadă.\n"
            "3. Scopul jocului poate varia:\n"
            "   - În varianta standard, pierde jucătorul care ia ultimul obiect.\n"
            "   - În varianta misère, câștigă jucătorul care ia ultimul obiect.\n"
            "\nBucurați-vă de acest joc de strategie simplu dar captivant!"
        )
        messagebox.showinfo("Despre", info_text)
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root, bg="#f0f8ff")
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Jocul Nim", font=("Arial", 24, "bold"), bg="#f0f8ff").pack(pady=40)

    tk.Button(frame, text="Joaca", font=("Arial", 16), bg="#87CEEB", command=lambda: show_settings(frame)).pack(pady=20)
    tk.Button(frame, text="Informatii", font=("Arial", 14), command=lambda: reguli()).pack(pady=20)
    tk.Button(frame, text="Creatori", font=("Arial", 14),bg="#87CEEB",command=lambda: messagebox.showinfo("Creatori", "Verșanu George-David \n Alexandru Spătaru")).pack(pady=20)
    tk.Button(frame, text="Exit", font=("Arial", 16), bg="#FF6347", command=root.destroy).pack(pady=20)

def show_settings(frame):
    frame.pack_forget()
    settings_frame = tk.Frame(root, bg="#f0f8ff")
    settings_frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(settings_frame, text="Setari Joc", font=("Arial", 20, "bold"), bg="#f0f8ff").pack(pady=20)

    tk.Label(settings_frame, text="Numar total de bete:", font=("Arial", 14), bg="#f0f8ff").pack(pady=5)
    sticks_entry = tk.Entry(settings_frame, font=("Arial", 14))
    sticks_entry.pack()
    sticks_entry.insert(0, "15")

    tk.Label(settings_frame, text="Numar de gramezi:", font=("Arial", 14), bg="#f0f8ff").pack(pady=5)
    piles_entry = tk.Entry(settings_frame, font=("Arial", 14))
    piles_entry.pack()
    piles_entry.insert(0, "3")

    tk.Label(settings_frame, text="Numar maxim de bete per mutare:", font=("Arial", 14), bg="#f0f8ff").pack(pady=5)
    max_picks_entry = tk.Entry(settings_frame, font=("Arial", 14))
    max_picks_entry.pack()
    max_picks_entry.insert(0, "3")

    tk.Button(settings_frame, text="Incepe", font=("Arial", 14), bg="#32CD32",
              command=lambda: start_game(
                  settings_frame,
                  int(sticks_entry.get()),
                  int(piles_entry.get()),
                  int(max_picks_entry.get())
              )).pack(pady=20)

    tk.Button(settings_frame, text="Inapoi", font=("Arial", 14), bg="#87CEEB",
              command=lambda: [settings_frame.pack_forget(), show_menu()]).pack(pady=10)

def setup_game(root):
    show_menu()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Jocul Nim")
    center_window(root, 0.75, 0.75)
    root.resizable(False, False)
    setup_game(root)
    root.mainloop()
