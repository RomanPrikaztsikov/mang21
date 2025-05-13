import tkinter as tk
from tkinter import messagebox
import random
import os

TAUST = "#2E2E2E"
FOREGROUND = "#FFFFFF"
NUPP_BG = "#444444"
NUPP_FG = "#FFFFFF"
NUPP_ACTIVE_BG = "#555555"

deck = []
mängija_kaardid = []
arvuti_kaardid = []
kaart_pildid = {}

def loo_dekk():
    suits = ["clubs", "diamonds", "hearts", "spades"]
    ranks = ["A"] + [str(v) for v in range(2, 11)] + ["J", "Q", "K"]
    kaardid = [f"{suit}_{rank}" for suit in suits for rank in ranks]
    random.shuffle(kaardid)
    return kaardid

def loe_kaart():
    if not deck:
        raise ValueError("Kaardipakk on tühi!")
    return deck.pop()

def kaardi_vaartus(kaart):
    rank = kaart.split("_")[1]
    if rank in ["J", "Q", "K", "10"]:
        return 10
    if rank == "A":
        return 11
    return int(rank)

def käsi_summa(kaardid):
    väärtused = [kaardi_vaartus(k) for k in kaardid]
    total = sum(väärtused)
    aces = väärtused.count(11)
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total

def arvuta_tulemus(mängija_summa):
    arvuti_summa = käsi_summa(arvuti_kaardid)
    if mängija_summa > 21 and arvuti_summa > 21:
        return "Viik"
    if mängija_summa == arvuti_summa:
        return "Viik"
    if mängija_summa > 21:
        return "Kaotus"
    if arvuti_summa > 21:
        return "Võit"
    if mängija_summa == 21:
        return "Võit"
    if arvuti_summa == 21:
        return "Kaotus"
    if arvuti_summa <= mängija_summa:
        return "Võit"
    return "Kaotus"

def salvesta_tulemus(nimi, tulemus, summa):
    try:
        with open("tulemused.txt", "a", encoding="utf-8") as f:
            f.write(f"{nimi};{tulemus};{summa}\n")
    except Exception as e:
        messagebox.showerror("Viga", f"Tulemuse salvestamine ebaõnnestus: {e}")

def näita_ajalugu():
    aken2 = tk.Toplevel(aken)
    aken2.title("Mängu ajalugu")
    aken2.configure(bg=TAUST)
    tekst = tk.Text(aken2, bg=NUPP_BG, fg=FOREGROUND, width=40, height=15, relief="flat")
    tekst.pack(padx=10, pady=10)
    try:
        with open("tulemused.txt", "r", encoding="utf-8") as f:
            for rida in f:
                tekst.insert(tk.END, rida)
    except FileNotFoundError:
        tekst.insert(tk.END, "Ühtki tulemust ei leitud.")
    except Exception as e:
        tekst.insert(tk.END, f"Viga faili lugemisel: {e}")

def laadi_pildid():
    try:
        base = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        base = os.getcwd()
    
    suits = ["clubs", "diamonds", "hearts", "spades"]
    ranks = ["A"] + [str(v) for v in range(2, 11)] + ["J", "Q", "K"]
    missing_files = []
    
    for suit in suits:
        for rank in ranks:
            key = f"{suit}_{rank}"
            path = os.path.join(base, f"{key}.png")
            try:
                img = tk.PhotoImage(file=path)
                kaart_pildid[key] = img.subsample(2, 2)
            except Exception as e:
                missing_files.append(f"{key}.png")
    
    back_path = os.path.join(base, "back_dark.png")
    try:
        img = tk.PhotoImage(file=back_path)
        kaart_pildid["back_dark"] = img.subsample(2, 2)
    except Exception:
        missing_files.append("back_dark.png")
    
    if missing_files:
        messagebox.showerror("Viga", f"Pildifailid puuduvad: {', '.join(missing_files)}")
        raise FileNotFoundError("Mõned kaardipildid puuduvad!")

def kuva_arvuti_kaardid(hidden):
    if not arvuti_kaardid:
        return []
    if hidden:
        return [arvuti_kaardid[0]] + ["back_dark"] * (len(arvuti_kaardid) - 1)
    return arvuti_kaardid

def uuenda_käed(hidden):
    for w in raam_mängija.winfo_children():
        w.destroy()
    for w in raam_arvuti.winfo_children():
        w.destroy()
    
    for k in mängija_kaardid:
        img = kaart_pildid.get(k, kaart_pildid["back_dark"])
        lbl = tk.Label(raam_mängija, image=img, bg=TAUST)
        lbl.image = img
        lbl.pack(side=tk.LEFT, padx=5)
    
    for k in kuva_arvuti_kaardid(hidden):
        img = kaart_pildid.get(k, kaart_pildid["back_dark"])
        lbl = tk.Label(raam_arvuti, image=img, bg=TAUST)
        lbl.image = img
        lbl.pack(side=tk.LEFT, padx=5)

def alusta_mängu():
    nimi = sisestus.get().strip()
    if not nimi:
        messagebox.showwarning("Hoiatus", "Palun sisesta mängija nimi!")
        return
    
    sisestus.config(state="disabled")
    nupp_alusta.config(state="disabled")
    nupp_kaart.config(state="normal")
    nupp_peatu.config(state="normal")
    
    global deck, mängija_kaardid, arvuti_kaardid
    deck = loo_dekk()
    mängija_kaardid = []
    arvuti_kaardid = []
    
    try:
        for _ in range(2):
            mängija_kaardid.append(loe_kaart())
            arvuti_kaardid.append(loe_kaart())
    except ValueError as e:
        messagebox.showerror("Viga", str(e))
        return
    
    uuenda_käed(True)
    silt_info.config(text="")
    
    if käsi_summa(mängija_kaardid) == 21 or käsi_summa(arvuti_kaardid) == 21:
        lõpetamise_loogika()

def lisa_kaart():
    try:
        mängija_kaardid.append(loe_kaart())
        uuenda_käed(True)
        if käsi_summa(mängija_kaardid) >= 21:
            lõpetamise_loogika()
    except ValueError as e:
        messagebox.showerror("Viga", str(e))

def lõpetamise_loogika():
    nimi = sisestus.get().strip()
    try:
        while käsi_summa(arvuti_kaardid) < 17:
            arvuti_kaardid.append(loe_kaart())
    except ValueError as e:
        messagebox.showerror("Viga", str(e))
        return
    
    mängija_summa = käsi_summa(mängija_kaardid)
    arvuti_summa = käsi_summa(arvuti_kaardid)
    tulemus = arvuta_tulemus(mängija_summa)
    
    uuenda_käed(False)
    silt_info.config(text=f"Tulemus: {tulemus}! Sinu {mängija_summa}, arvuti {arvuti_summa}")
    salvesta_tulemus(nimi, tulemus, mängija_summa)
    
    nupp_kaart.config(state="disabled")
    nupp_peatu.config(state="disabled")
    sisestus.config(state="normal")
    nupp_alusta.config(state="normal")

def peatu():
    lõpetamise_loogika()

aken = tk.Tk()
aken.title("Mäng 21")
aken.configure(bg=TAUST)
aken.geometry("900x700")

try:
    laadi_pildid()
except Exception as e:
    messagebox.showerror("Käivitusviga", f"Piltide laadimine ebaõnnestus: {e}")
    aken.destroy()
    exit()

silt_nimi = tk.Label(aken, text="Mängija nimi:", bg=TAUST, fg=FOREGROUND, font=("Arial", 14))
silt_nimi.place(x=20, y=20)
sisestus = tk.Entry(aken, bg=FOREGROUND, fg=TAUST, font=("Arial", 14))
sisestus.place(x=160, y=20, width=200)

nupp_alusta = tk.Button(aken, text="Alusta mängu", bg=NUPP_BG, fg=NUPP_FG,
                       activebackground=NUPP_ACTIVE_BG, font=("Arial", 12),
                       command=alusta_mängu)
nupp_alusta.place(x=20, y=60, width=120)

nupp_kaart = tk.Button(aken, text="Võta kaart", bg=NUPP_BG, fg=NUPP_FG,
                      activebackground=NUPP_ACTIVE_BG, font=("Arial", 12),
                      state="disabled", command=lisa_kaart)
nupp_kaart.place(x=160, y=60, width=120)

nupp_peatu = tk.Button(aken, text="Peatu", bg=NUPP_BG, fg=NUPP_FG,
                      activebackground=NUPP_ACTIVE_BG, font=("Arial", 12),
                      state="disabled", command=peatu)
nupp_peatu.place(x=300, y=60, width=80)

nupp_ajalugu = tk.Button(aken, text="Vaata ajalugu", bg=NUPP_BG, fg=NUPP_FG,
                        activebackground=NUPP_ACTIVE_BG, font=("Arial", 12),
                        command=näita_ajalugu)
nupp_ajalugu.place(x=380, y=60, width=100)

raam_arvuti = tk.Frame(aken, bg=TAUST)
raam_arvuti.place(x=20, y=120)
raam_mängija = tk.Frame(aken, bg=TAUST)
raam_mängija.place(x=20, y=320)

silt_info = tk.Label(aken, text="", bg=TAUST, fg=FOREGROUND, font=("Arial", 16, "bold"), pady=10)
silt_info.place(x=20, y=600)

aken.mainloop()
