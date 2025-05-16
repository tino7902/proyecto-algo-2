import tkinter as tk
from tkinter import ttk


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
    ttk.Label(coso, text=f"Bienvenido, {user} !").grid(row=0, column=1)
    ttk.Label(coso, text="Elegí el juego que quieras jugar !").grid(row=1, column=1)
    ttk.Button(coso, text="Juego 1").grid(row=2, column=0)
    ttk.Button(coso, text="Juego 2").grid(row=2, column=2)
    coso.mainloop()

def login(entry_user, entry_pw):
    existe_user, pw_correcta = check_user_pw(entry_user.get(), entry_pw.get())
    if not existe_user:
        print("no existe usuario")
    elif not pw_correcta:
        print("contraseña equivocada")
    else:
        print("login correcto")
        elegir_juego(entry_user.get())

def crear_user(entry_user, entry_pw):
    global usuarios
    existe_user, pw_correcta = check_user_pw(entry_user.get(), entry_pw.get())
    if existe_user:
        print("el usuario ya existe")
    else:
        usuarios.append(Usuario(entry_user.get(), entry_pw.get()))
        actualizar_usuarios_txt()
        print("usuario creado")

def main():
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
    entry_user = tk.StringVar()
    entry_pw = tk.StringVar()
    ttk.Label(main, text="Usuario", justify="right")
    ttk.Label(main, text="Contraseña", justify="right")
    ttk.Entry(main, textvariable=entry_user).grid(column=1, row=0)
    ttk.Entry(main, textvariable=entry_pw).grid(column=1, row=1)
    ttk.Button(main, text="iniciar sesión", command=lambda: login(entry_user, entry_pw)).grid(column=0, row=2)
    ttk.Button(main, text="crear cuenta", command=lambda: crear_user(entry_user, entry_pw)).grid(column=2, row=2)

    main.mainloop()

if __name__ == '__main__':
    main()