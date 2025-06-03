import tkinter as tk
from tkinter import ttk, messagebox
from juego1 import iniciarJuego1
from juego2 import iniciarJuego2

global labelStyle
global entryStyle
global buttonStyle


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
    global labelStyle
    global entryStyle
    global buttonStyle

    coso = tk.Toplevel()
    coso.attributes("-fullscreen", True)
    frame = tk.Frame(coso)
    ttk.Label(frame, text=f"Bienvenido, {user} !").grid(row=0, column=1)
    ttk.Label(frame, text="Elegí el juego que quieras jugar !").grid(row=1, column=1)
    ttk.Button(frame, text="Juego 1", command=lambda: iniciarJuego1(user)).grid(
        row=2, column=0, padx=15, pady=15
    )
    ttk.Button(frame, text="Juego 2", command=lambda: iniciarJuego2(user)).grid(
        row=2, column=2, padx=15, pady=15
    )
    frame.pack(anchor="center", expand=1)
    coso.mainloop()


def login(entry_user, entry_pw):
    existe_user, pw_correcta = check_user_pw(entry_user.get(), entry_pw.get())
    if not existe_user:
        messagebox.showerror(title="error !", message="No existe el usuario !")
        print("no existe usuario")
    elif not pw_correcta:
        messagebox.showerror(title="error !", message="Contraseña incorrecta !")
        print("contraseña equivocada")
    else:
        print("login correcto")
        elegir_juego(entry_user.get())


def crear_user(entry_user, entry_pw):
    global usuarios
    existe_user, pw_correcta = check_user_pw(entry_user.get(), entry_pw.get())
    if existe_user:
        messagebox.showerror(title="error !", message="el usuario ingresado ya esta registrado !")
        print("el usuario ya existe")
    else:
        messagebox.showinfo(title="no error !", message="cuenta creada con exito !")
        usuarios.append(Usuario(entry_user.get(), entry_pw.get()))
        actualizar_usuarios_txt()
        print("usuario creado")


def main():
    global labelStyle
    global entryStyle
    global buttonStyle

    with open("usuarios.txt", mode="r") as f:
        lineas_usuarios_txt = f.readlines()
    lineas_usuarios_txt = [linea.replace("\n", "") for linea in lineas_usuarios_txt]

    global usuarios
    usuarios = []
    for linea in lineas_usuarios_txt:
        aux = linea.split(";")
        usuario = Usuario(aux[0], aux[1])
        usuarios.append(usuario)

    main = tk.Tk()
    main.attributes('-fullscreen', True)
    # main.geometry("1300x800")
    # Styles
    entryStyle = ttk.Style()
    entryStyle.configure("TEntry", font=("Helvetica", 24))
    labelStyle = ttk.Style()
    labelStyle.configure("TLabel", font=("Helvetica", 24))
    buttonStyle = ttk.Style()
    buttonStyle.configure("TButton", font=("Helvetica", 18, "bold"))
    
    framePrincipal = tk.Frame(main)
    entry_user = tk.StringVar()
    entry_pw = tk.StringVar()
    ttk.Label(framePrincipal, text="Usuario: ", justify="right", width=12).grid(column=0, row=0, padx=15, pady=15)
    ttk.Label(framePrincipal, text="Contraseña: ", justify="right", width=12).grid(column=0, row=1, padx=15, pady=15)
    ttk.Entry(framePrincipal, textvariable=entry_user, width=10, font=("Helvetica", 24)).grid(column=1, row=0)
    ttk.Entry(framePrincipal, textvariable=entry_pw, width=10, font=("Helvetica", 24)).grid(column=1, row=1)
    ttk.Button(
        framePrincipal, text="iniciar sesión", command=lambda: login(entry_user, entry_pw)
    ).grid(column=0, row=2)
    ttk.Button(
        framePrincipal, text="crear cuenta", command=lambda: crear_user(entry_user, entry_pw)
    ).grid(column=1, row=2)
    framePrincipal.pack(anchor="center", expand=1)
    main.mainloop()


if __name__ == "__main__":
    main()
