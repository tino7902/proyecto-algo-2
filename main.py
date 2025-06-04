import tkinter as tk
from tkinter import ttk, messagebox
from juego1 import iniciarJuego1
from juego2 import iniciarJuego2


global usuarios
btn_color = "#A9C9DD"

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


def elegir_juego(user):
    coso = tk.Toplevel()
    coso.attributes("-fullscreen", True)
    frame = tk.Frame(coso)

    ttk.Label(frame, text=f"Bienvenido, {user} !", font=("Helvetica", 20)).grid(row=0, column=1, pady=(20, 10))
    ttk.Label(frame, text="Elegí el juego que quieras jugar !", font=("Helvetica", 18)).grid(row=1, column=1, pady=(0, 20))

    tk.Button(frame, text="Juego 1", command=lambda: iniciarJuego1(user),
              bg=btn_color, relief="groove", font=("Helvetica", 16, "bold"), bd=2, highlightthickness=0).grid(row=2, column=0, padx=15, pady=15)

    tk.Button(frame, text="Juego 2", command=lambda: iniciarJuego2(user),
              bg=btn_color, relief="groove", font=("Helvetica", 16, "bold"), bd=2, highlightthickness=0).grid(row=2, column=2, padx=15, pady=15)

    # Botón para salir de la ventana de juegos
    tk.Button(frame, text="Salir", command=coso.destroy,
              bg=btn_color, font=("Helvetica", 16, "bold"), relief="groove", bd=2).grid(row=3, column=1, pady=30)

    frame.pack(anchor="center", expand=1)
    coso.mainloop()



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
              bg=btn_color, font=("Helvetica", 16, "bold"), relief="groove", bd=2).grid(column=0, row=2, padx=10, pady=10)

    tk.Button(framePrincipal, text="Crear cuenta", command=lambda: crear_user(entry_user, entry_pw),
              bg=btn_color, font=("Helvetica", 16, "bold"), relief="groove", bd=2).grid(column=1, row=2, padx=10, pady=10)

    # Botón de salir
    tk.Button(framePrincipal, text="Salir", command=main.destroy,
              bg=btn_color, font=("Helvetica", 16, "bold"), relief="groove", bd=2).grid(column=0, columnspan=2, row=3, pady=25)

    framePrincipal.pack(anchor="center", expand=1)
    main.mainloop()


if __name__ == "__main__":
    main()