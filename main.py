import tkinter as tk
from tkinter import ttk, messagebox
import juego1 as j1
import juego2 as j2


global usuarios

COLOR_FONDO = "#f0f4f8"
COLOR_BOTON = "#6fbf73"
COLOR_TEXTO = "#333333"
FUENTE_TITULO = ("Segoe UI", 36, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 20)
FUENTE_BOTON = ("Segoe UI", 16, "bold")

# Clase usuario
class Usuario:
    def __init__(self, user, pw):
        self.user = user
        self.pw = pw

    def __str__(self):
        return f"{self.user};{self.pw}"

def actualizar_usuarios_txt():  # Actualiza lista de usuarios
    global usuarios
    with open("usuarios.txt", mode="w") as f:
        for usuario in usuarios:
            f.write(f"{usuario}\n")


def check_user_pw(user, pw):    # Verifica la contraseña
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


def iniciarJuego1(user):
    global root, menu
    mostrar_cargando("Cargando Letras...")
    menu.withdraw()
    root.after(50, lambda: lanzar_juego1(user))

def lanzar_juego1(user):
    global menu
    juego1 = j1.JuegoLetras(user, root)
    menu.wait_window(juego1.juego)
    ocultar_cargando()
    menu.deiconify()
    menu.lift()
    menu.focus_force()

def iniciarJuego2(user):
    global root, menu
    mostrar_cargando("Cargando LexiReto...")
    menu.withdraw()
    root.after(50, lambda: lanzar_juego2(user))

def lanzar_juego2(user):
    global menu
    juego2 = j2.LexiReto(user, root)
    menu.wait_window(juego2.juego)
    ocultar_cargando()
    menu.deiconify()
    menu.lift()
    menu.focus_force()


def elegir_juego(user): # Menú elegir juego
    global root
    global menu
    menu = tk.Toplevel()
    menu.attributes("-fullscreen", True)
    menu.configure(bg=COLOR_FONDO)

    frame = tk.Frame(menu, bg=COLOR_FONDO)

    # Textos y botones
    tk.Label(
        frame,
        text=f"🎮 Bienvenido a LexiManía, {user}!",
        font=FUENTE_TITULO,
        fg=COLOR_TEXTO,
        bg=COLOR_FONDO,
    ).pack(pady=(30, 10))
    tk.Label(
        frame,
        text="Desafía tu mente con dos modos de juego únicos:",
        font=FUENTE_SUBTITULO,
        fg=COLOR_TEXTO,
        bg=COLOR_FONDO,
    ).pack(pady=(0, 30))

    tk.Button(
        frame,
        text="🧩 Letras",
        command=lambda: iniciarJuego1(user),
        bg=COLOR_BOTON,
        font=FUENTE_BOTON,
        width=20,
    ).pack(pady=10)

    tk.Button(
        frame,
        text="🧠 LexiReto",
        command=lambda: iniciarJuego2(user),
        bg=COLOR_BOTON,
        font=FUENTE_BOTON,
        width=20,
    ).pack(pady=10)

    tk.Button(
        frame,
        text="🚪 Cerrar sesión",
        command=menu.destroy,
        bg="#e57373",
        font=FUENTE_BOTON,
        width=20,
    ).pack(pady=30)

    tk.Label(
        frame,
        text="Grupo S.A.N.G.A — 2025",
        font=("Segoe UI", 12),
        bg=COLOR_FONDO,
        fg="#888",
    ).pack(pady=10)

    frame.pack(expand=True)
    # ventana.protocol("WM_DELETE_WINDOW", cerrar_menu)
    root.wait_window(menu)
    root.deiconify()
    root.lift()
    root.focus_force()


def login(entry_user, entry_pw):    # Función inciar sesión
    existe_user, pw_correcta = check_user_pw(entry_user.get(), entry_pw.get())
    if not existe_user:
        messagebox.showerror(title="error !", message="No existe el usuario !")
    elif not pw_correcta:
        messagebox.showerror(title="error !", message="Contraseña incorrecta !")
    else:
        elegir_juego(entry_user.get())


def crear_user(entry_user, entry_pw):   # Función crear usuario
    global usuarios
    existe_user, pw_correcta = check_user_pw(entry_user.get(), entry_pw.get())
    if existe_user:
        messagebox.showerror(
            title="error !", message="El usuario ingresado ya está registrado!"
        )
    else:
        messagebox.showinfo(title="¡Éxito!", message="Cuenta creada con éxito!")
        usuarios.append(Usuario(entry_user.get(), entry_pw.get()))
        actualizar_usuarios_txt()

def mostrar_cargando(mensaje="Cargando..."):
    pantalla_carga.config(text=mensaje)
    pantalla_carga.place(relx=0, rely=0, relwidth=1, relheight=1)
    pantalla_carga.lift()

def ocultar_cargando():
    pantalla_carga.place_forget()


def main(): # Función principal
    global usuarios

    with open("usuarios.txt", mode="r") as f:
        lineas_usuarios_txt = f.readlines()
    lineas_usuarios_txt = [linea.replace("\n", "") for linea in lineas_usuarios_txt]

    usuarios = [Usuario(*linea.split(";")) for linea in lineas_usuarios_txt]    # Crea lista de usuarios

    global root
    root = tk.Tk()  # Ventana root
    root.attributes("-fullscreen", True)

    # Capa negra de carga
    global pantalla_carga
    pantalla_carga = tk.Label(
        root,
        bg="black",
        fg="white",
        font=("Segoe UI", 32, "bold"),
        text="Cargando...",
        anchor="center"
    )
    pantalla_carga.place(relx=0, rely=0, relwidth=1, relheight=1)
    pantalla_carga.lower()  # lo manda al fondo
    pantalla_carga.place_forget()  # lo oculta al inicio

    framePrincipal = tk.Frame(root)
    entry_user = tk.StringVar()
    entry_pw = tk.StringVar()

    ttk.Label(
        framePrincipal,
        text="Usuario: ",
        font=FUENTE_SUBTITULO,
        justify="right",
        width=12,
    ).grid(column=0, row=0, padx=15, pady=15)
    ttk.Label(
        framePrincipal,
        text="Contraseña: ",
        font=FUENTE_SUBTITULO,
        justify="right",
        width=12,
    ).grid(column=0, row=1, padx=15, pady=15)
    ttk.Entry(
        framePrincipal, textvariable=entry_user, font=FUENTE_SUBTITULO, width=10
    ).grid(column=1, row=0)
    ttk.Entry(
        framePrincipal, textvariable=entry_pw, font=FUENTE_SUBTITULO, width=10, show="*"
    ).grid(column=1, row=1)

    # Botones con estilo personalizado
    tk.Button(
        framePrincipal,
        text="Iniciar sesión",
        command=lambda: login(entry_user, entry_pw),
        bg=COLOR_BOTON,
        font=FUENTE_BOTON,
        relief="groove",
        bd=2,
    ).grid(column=0, row=2, padx=10, pady=10)

    tk.Button(
        framePrincipal,
        text="Crear cuenta",
        command=lambda: crear_user(entry_user, entry_pw),
        bg=COLOR_BOTON,
        font=FUENTE_BOTON,
        relief="groove",
        bd=2,
    ).grid(column=1, row=2, padx=10, pady=10)

    # Botón de salir
    tk.Button(
        framePrincipal,
        text="Salir",
        command=root.destroy,
        bg=COLOR_BOTON,
        font=FUENTE_BOTON,
        relief="groove",
        bd=2,
    ).grid(column=0, columnspan=2, row=3, pady=25)

    framePrincipal.pack(anchor="center", expand=1)
    root.mainloop()


if __name__ == "__main__":
    main()
