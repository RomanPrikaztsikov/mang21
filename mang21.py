import tkinter as tk
import random

BG = "#2E2E2E"
FG = "#FFFFFF"
BUTTON_BG = "#444444"
BUTTON_FG = "#FFFFFF"
BUTTON_ACTIVE_BG = "#555555"

deck = []

def loo_dekk():
    values = []
    for v in range(2, 10):
        values += [v] * 4
    values += [10] * 16
    values += [11] * 4
    random.shuffle(values)
    return values

def loe_kaart():
    return deck.pop()

def käsi_summa(kaardid):
    total = sum(kaardid)
    aces = kaardid.count(11)
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

def arvuta_tulemus(mängija_kaardid, arvuti_kaardid):
    mängija_summa = käsi_summa(mängija_kaardid)
    arvuti_summa  = käsi_summa(arvuti_kaardid)

    if mängija_summa > 21:
        return "Kaotus"
    if arvuti_summa > 21:
        return "Võit"
    if mängija_summa == arvuti_summa:
        return "Viik"
    if mängija_summa > arvuti_summa:
        return "Võit"
    return "Kaotus"



def salvesta_tulemus(nimi, tulemus, summa):
    with open("tulemused.txt", "a", encoding="utf-8") as f:
        f.write(f"{nimi};{tulemus};{summa}\n")

def näita_ajalugu():
    aken2 = tk.Toplevel(aken)
    aken2.title("Mängu ajalugu")
    aken2.configure(bg=BG)
    tekst = tk.Text(aken2, bg=BUTTON_BG, fg=FG, width=40, height=15, relief="flat")
    tekst.pack(padx=10, pady=10)
    try:
        with open("tulemused.txt", "r", encoding="utf-8") as f:
            for rida in f:
                tekst.insert(tk.END, rida)
    except FileNotFoundError:
        tekst.insert(tk.END, "Ühtki tulemust ei leitud.")

def kuva_arvuti_kaardid(hidden):
    if hidden:
        first = arvuti_kaardid[0]
        hidden_count = len(arvuti_kaardid) - 1
        return [first] + ['?'] * hidden_count
    else:
        return arvuti_kaardid

def uuenda_käed(hidden):
    silt_kaartide.config(text=f"Sinu kaardid: {mängija_kaardid}")
    silt_arviti_kaartide.config(text=f"Arvuti kaardid: {kuva_arvuti_kaardid(hidden)}")

def alusta_mängu():
    nimi = sisestus.get().strip()
    if not nimi:
        return
    sisestus.config(state="disabled")
    nupp_alusta.config(state="disabled")
    nupp_kaart.config(state="normal")
    nupp_peatu.config(state="normal")
    global deck, mängija_kaardid, arvuti_kaardid
    deck = loo_dekk()
    mängija_kaardid = []
    arvuti_kaardid = []
    for i in range(2):
        mängija_kaardid.append(loe_kaart())
        arvuti_kaardid.append(loe_kaart())
    uuenda_käed(hidden=True)
    silt_info.config(text="")
    if käsi_summa(mängija_kaardid) == 21 or käsi_summa(arvuti_kaardid) == 21:
        lõpetamise_loogika()

def lisa_kaart():
    mängija_kaardid.append(loe_kaart())
    uuenda_käed(hidden=True)
    if käsi_summa(mängija_kaardid) >= 21:
        lõpetamise_loogika()

def lõpetamise_loogika():
    nimi = sisestus.get().strip()
    while käsi_summa(arvuti_kaardid) < 17:
        arvuti_kaardid.append(loe_kaart())
    mängija_summa = käsi_summa(mängija_kaardid)
    arvuti_summa = käsi_summa(arvuti_kaardid)
    tulemus = arvuta_tulemus(mängija_summa)
    uuenda_käed(hidden=False)
    silt_info.config(
        text=f"Tulemus: {tulemus}! Sinu {mängija_summa}, arvuti {arvuti_summa}"
    )
    salvesta_tulemus(nimi, tulemus, mängija_summa)
    nupp_kaart.config(state="disabled")
    nupp_peatu.config(state="disabled")
    sisestus.config(state="normal")
    nupp_alusta.config(state="normal")

def peatu():
    lõpetamise_loogika()

aken = tk.Tk()
aken.title("Mäng 21")
aken.configure(bg=BG)
aken.geometry("400x300")

silt_nimi = tk.Label(aken, text="Mängija nimi:", bg=BG, fg=FG, font=("Arial", 12))
silt_nimi.place(x=20, y=20)
sisestus = tk.Entry(aken, bg=FG, fg=BG, font=("Arial", 12))
sisestus.place(x=160, y=20, width=200)

nupp_alusta = tk.Button(
    aken,
    text="Alusta mängu",
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    activebackground=BUTTON_ACTIVE_BG,
    font=("Arial", 12),
    command=alusta_mängu,
)
nupp_alusta.place(x=20, y=60, width=120)

nupp_kaart = tk.Button(
    aken,
    text="Võta kaart",
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    activebackground=BUTTON_ACTIVE_BG,
    font=("Arial", 12),
    state="disabled",
    command=lisa_kaart,
)
nupp_kaart.place(x=160, y=60, width=120)

nupp_peatu = tk.Button(
    aken,
    text="Peatu",
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    activebackground=BUTTON_ACTIVE_BG,
    font=("Arial", 12),
    state="disabled",
    command=peatu,
)
nupp_peatu.place(x=300, y=60, width=80)

silt_kaartide = tk.Label(
    aken, text="Sinu kaardid: []", bg=BG, fg=FG, font=("Arial", 12)
)
silt_kaartide.place(x=20, y=120)

silt_arviti_kaartide = tk.Label(
    aken, text="Arvuti kaardid: []", bg=BG, fg=FG, font=("Arial", 12)
)
silt_arviti_kaartide.place(x=20, y=150)

silt_info = tk.Label(aken, text="", bg=BG, fg=FG, font=("Arial", 12))
silt_info.place(x=20, y=180)

nupp_ajalugu = tk.Button(
    aken,
    text="Vaata ajalugu",
    bg=BUTTON_BG,
    fg=BUTTON_FG,
    activebackground=BUTTON_ACTIVE_BG,
    font=("Arial", 12),
    command=näita_ajalugu,
)
nupp_ajalugu.place(x=140, y=230, width=120)

aken.mainloop()
