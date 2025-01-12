import math
import random
import tkinter as tk
from tkinter import messagebox


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


def update_game_state(gramezi, max_picks, depth, player_turn, frame, inputs):
    if sum(gramezi) <= 0:
        if player_turn:
            messagebox.showinfo("Joc terminat", "Ai pierdut! Botul a câștigat.")
        else:
            messagebox.showinfo("Joc terminat", "Felicitări! Ai câștigat împotriva botului.")
        frame.destroy()
        setup_game(frame.master)
        return

    display_gramezi(gramezi, frame)

    if not player_turn:
        bot_choice, grămadă_idx = bot_decide(gramezi, max_picks, depth)
        gramezi[grămadă_idx] -= bot_choice
        messagebox.showinfo("Botul a mutat", f"Botul a luat {bot_choice} bețe din grămada {grămadă_idx + 1}.")
        update_game_state(gramezi, max_picks, depth, True, frame, inputs)
    else:
        for widget in inputs.values():
            widget.destroy()

        tk.Label(frame, text="Introduceți grămada și numărul de bețe:", font=("Arial", 12), bg="lightblue").pack(pady=5)
        pile_input = tk.Entry(frame, font=("Arial", 12))
        pile_input.pack(pady=5)
        stick_input = tk.Entry(frame, font=("Arial", 12))
        stick_input.pack(pady=5)

        inputs['pile_input'] = pile_input
        inputs['stick_input'] = stick_input

        tk.Button(frame, text="Mutare", font=("Arial", 12), command=lambda: on_player_move(gramezi, max_picks, depth, frame, inputs)).pack(pady=10)
        tk.Button(frame, text="Înapoi", font=("Arial", 12), command=lambda: [frame.pack_forget(), show_menu()]).pack(pady=5)
        tk.Button(frame, text="Exit", font=("Arial", 14), command=root.destroy).pack(pady=10)


def on_player_move(gramezi, max_picks, depth, frame, inputs):
    try:
        grămadă_idx = int(inputs['pile_input'].get()) - 1
        sticks_to_remove = int(inputs['stick_input'].get())

        if 0 <= grămadă_idx < len(gramezi) and 1 <= sticks_to_remove <= min(max_picks, gramezi[grămadă_idx]):
            gramezi[grămadă_idx] -= sticks_to_remove
            update_game_state(gramezi, max_picks, depth, False, frame, inputs)
        else:
            messagebox.showerror("Eroare", "Introdu o grămadă validă și un număr valid de bețe.")
    except ValueError:
        messagebox.showerror("Eroare", "Introdu o grămadă validă și un număr de bețe.")


def bot_decide(gramezi, max_picks, depth):
    for grămadă_idx, sticks in enumerate(gramezi):
        for i in range(1, min(max_picks, sticks) + 1):
            gramezi_test = gramezi[:]
            gramezi_test[grămadă_idx] -= i
            if minimax(depth, False, sum(gramezi_test), -math.inf, math.inf, max_picks) == 1:
                return i, grămadă_idx
    return 1, 0


def display_gramezi(gramezi, frame):
    for widget in frame.winfo_children():
        widget.destroy()

    for grămadă_idx, sticks in enumerate(gramezi):
        row_frame = tk.Frame(frame)
        row_frame.pack()
        tk.Label(row_frame, text=f"Grămada {grămadă_idx + 1}:", font=("Arial", 12)).pack(side=tk.LEFT)
        for _ in range(sticks):
            tk.Label(row_frame, text="■", font=("Arial", 12), fg="green").pack(side=tk.LEFT)


def generate_gramezi(total_bete, num_gramezi):
    # Generăm intervale de valori posibile pentru fiecare grămadă.
    min_sticks = 1
    max_sticks = total_bete // num_gramezi
    gramezi = []

    # Calculăm o sumă aleatorie mai variabilă
    bete_ramase = total_bete

    for i in range(num_gramezi - 1):
        # Alegem o valoare aleatorie între 1 și max_sticks (dar asigurăm că nu depășim bețele rămase)
        max_possible = min(max_sticks, bete_ramase - (num_gramezi - i - 1))  # Evită dublările la final
        betele = random.randint(min_sticks, max_possible)
        gramezi.append(betele)
        bete_ramase -= betele

    gramezi.append(bete_ramase)

    # Opțional: Reordonăm aleatoriu grămezile pentru a distribui mai random
    random.shuffle(gramezi)

    return gramezi



def start_game(frame, total_bete, num_gramezi, max_picks):
    gramezi = generate_gramezi(total_bete, num_gramezi)
    depth = max(1, min(10, total_bete // 3))

    frame.pack_forget()
    game_frame = tk.Frame(frame.master, bg="lightblue")
    game_frame.pack(fill=tk.BOTH, expand=True)

    inputs = {}
    update_game_state(gramezi, max_picks, depth, True, game_frame, inputs)


def show_menu():
    for widget in root.winfo_children():
        widget.destroy()

    frame = tk.Frame(root, bg="lightblue")
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Jocul Nim", font=("Arial", 20), bg="lightblue").pack(pady=20)

    tk.Button(frame, text="Joacă", font=("Arial", 14), command=lambda: show_settings(frame)).pack(pady=10)
    tk.Button(frame, text="Info", font=("Arial", 14), command=lambda: messagebox.showinfo("Info", "Acesta este jocul Nim!")).pack(pady=10)
    tk.Button(frame, text="Creatori", font=("Arial", 14), command=lambda: messagebox.showinfo("Creatori", "Creat de [Nume].")).pack(pady=10)
    tk.Button(frame, text="Exit", font=("Arial", 14), command=root.destroy).pack(pady=10)


def show_settings(frame):
    frame.pack_forget()
    settings_frame = tk.Frame(root, bg="lightblue")
    settings_frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(settings_frame, text="Reguli de Joc", font=("Arial", 16), bg="lightblue").pack(pady=10)

    tk.Label(settings_frame, text="Număr total de bețe:", font=("Arial", 12), bg="lightblue").pack(pady=5)
    sticks_entry = tk.Entry(settings_frame, font=("Arial", 12))
    sticks_entry.pack()
    sticks_entry.insert(0, "15")

    tk.Label(settings_frame, text="Număr de grămezi:", font=("Arial", 12), bg="lightblue").pack(pady=5)
    piles_entry = tk.Entry(settings_frame, font=("Arial", 12))
    piles_entry.pack()
    piles_entry.insert(0, "3")

    tk.Label(settings_frame, text="Număr maxim de bețe per mutare:", font=("Arial", 12), bg="lightblue").pack(pady=5)
    max_picks_entry = tk.Entry(settings_frame, font=("Arial", 12))
    max_picks_entry.pack()
    max_picks_entry.insert(0, "3")

    tk.Button(settings_frame, text="Înapoi", font=("Arial", 12), command=lambda: [settings_frame.pack_forget(), show_menu()]).pack(pady=5)

    tk.Button(settings_frame, text="Începe", font=("Arial", 12),
              command=lambda: start_game(
                  settings_frame,
                  int(sticks_entry.get()),
                  int(piles_entry.get()),
                  int(max_picks_entry.get())
              )).pack(pady=20)


def setup_game(root):
    show_menu()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Jocul Nim")
    root.geometry("400x500")
    root.resizable(False, False)
    setup_game(root)
    root.mainloop()
