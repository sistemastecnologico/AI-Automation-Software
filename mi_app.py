import tkinter as tk

app = tk.Tk()
app.title("Mi primera app")
app.geometry("300x200")

label = tk.Label(app, text="Hola mundo 👋")
label.pack(pady=20)

app.mainloop()
