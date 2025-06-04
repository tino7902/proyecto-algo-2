import tkinter as tk
from tkinter import ttk, messagebox
from juego1 import iniciarJuego1
from juego2 import iniciarJuego2


global usuarios

COLOR_FONDO = "#f0f4f8"
COLOR_BOTON = "#6fbf73"
COLOR_TEXTO = "#333333"
FUENTE_TITULO = ("Segoe UI", 36, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 20)
FUENTE_BOTON = ("Segoe UI", 16, "bold")

class Usuario:
    def __init__(self, user, pw):
        self.user = user
        self.pw = pw

    def __str__(self):
        return f"{self.user};{self.pw}"


def actualizar_usuarios_txt():
    global usuarios
    with open("usuarios.txt", mode="w") as f:
        for usuario in usuarios:
            f.write(f"{usuario}\n")


def check_user_pw(user, pw):
    global usuarios
    existe_user = False
    pw_correcta = False
    for usuario in usuarios:
        if user == usuario.user:
            existe_user = True
            if pw != usuario.pw:
                pw_correcta = False
                break
            pw_correcta = True
            break
    return existe_user, pw_correcta


menu_abierto = False  # Bandera global para evitar múltiples menús

def elegir_juego(user):
    global menu_abierto
    if menu_abierto:
        return
    menu_abierto = True

    ventana = tk.Toplevel()
    ventana.attributes("-fullscreen", True)
    ventana.configure(bg=COLOR_FONDO)

    def cerrar_menu():
        global menu_abierto
        menu_abierto = False
        ventana.destroy()

    frame = tk.Frame(ventana, bg=COLOR_FONDO)

    tk.Label(frame, text=f"🎮 Bienvenido a LexiManía, {user}!", font=FUENTE_TITULO, fg=COLOR_TEXTO, bg=COLOR_FONDO).pack(pady=(30, 10))
    tk.Label(frame, text="Desafía tu mente con dos modos de juego únicos:", font=FUENTE_SUBTITULO, fg=COLOR_TEXTO, bg=COLOR_FONDO).pack(pady=(0, 30))

    tk.Button(frame, text="🧩 Letras", command=lambda: iniciarJuego1(user),
              bg=COLOR_BOTON, font=FUENTE_BOTON, width=20).pack(pady=10)

    tk.Button(frame, text="🧠 LexiReto", command=lambda: iniciarJuego2(),
              bg=COLOR_BOTON, font=FUENTE_BOTON, width=20).pack(pady=10)

    tk.Button(frame, text="🚪 Cerrar sesión", command=cerrar_menu,
              bg="#e57373", font=FUENTE_BOTON, width=20).pack(pady=30)

    tk.Label(frame, text="Grupo S.A.N.G.A — 2025", font=("Segoe UI", 12), bg=COLOR_FONDO, fg="#888").pack(pady=10)

    frame.pack(expand=True)
    ventana.protocol("WM_DELETE_WINDOW", cerrar_menu)
    ventana.mainloop()


def login(entry_user, entry_pw):
    existe_user, pw_correcta = check_user_pw(entry_user.get(), entry_pw.get())
    if not existe_user:
        messagebox.showerror(title="error !", message="No existe el usuario !")
    elif not pw_correcta:
        messagebox.showerror(title="error !", message="Contraseña incorrecta !")
    else:
        elegir_juego(entry_user.get())


def crear_user(entry_user, entry_pw):
    global usuarios
    existe_user, pw_correcta = check_user_pw(entry_user.get(), entry_pw.get())
    if existe_user:
        messagebox.showerror(title="error !", message="El usuario ingresado ya está registrado!")
    else:
        messagebox.showinfo(title="¡Éxito!", message="Cuenta creada con éxito!")
        usuarios.append(Usuario(entry_user.get(), entry_pw.get()))
        actualizar_usuarios_txt()

def main():
    global usuarios

    with open("usuarios.txt", mode="r") as f:
        lineas_usuarios_txt = f.readlines()
    lineas_usuarios_txt = [linea.replace("\n", "") for linea in lineas_usuarios_txt]

    usuarios = [Usuario(*linea.split(";")) for linea in lineas_usuarios_txt]

    main = tk.Tk()
    main.attributes('-fullscreen', True)

    framePrincipal = tk.Frame(main)
    entry_user = tk.StringVar()
    entry_pw = tk.StringVar()

    ttk.Label(framePrincipal, text="Usuario: ", font=("Helvetica", 24), justify="right", width=12).grid(column=0, row=0, padx=15, pady=15)
    ttk.Label(framePrincipal, text="Contraseña: ", font=("Helvetica", 24), justify="right", width=12).grid(column=0, row=1, padx=15, pady=15)
    ttk.Entry(framePrincipal, textvariable=entry_user, font=("Helvetica", 24), width=10).grid(column=1, row=0)
    ttk.Entry(framePrincipal, textvariable=entry_pw, font=("Helvetica", 24), width=10, show="*").grid(column=1, row=1)

    # Botones con estilo personalizado
    tk.Button(framePrincipal, text="Iniciar sesión", command=lambda: login(entry_user, entry_pw),
              bg=COLOR_BOTON, font=("Helvetica", 16, "bold"), relief="groove", bd=2).grid(column=0, row=2, padx=10, pady=10)

    tk.Button(framePrincipal, text="Crear cuenta", command=lambda: crear_user(entry_user, entry_pw),
              bg=COLOR_BOTON, font=("Helvetica", 16, "bold"), relief="groove", bd=2).grid(column=1, row=2, padx=10, pady=10)

    # Botón de salir
    tk.Button(framePrincipal, text="Salir", command=main.destroy,
              bg=COLOR_BOTON, font=("Helvetica", 16, "bold"), relief="groove", bd=2).grid(column=0, columnspan=2, row=3, pady=25)

    framePrincipal.pack(anchor="center", expand=1)
    main.mainloop()


if __name__ == "__main__":
    main()