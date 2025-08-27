import tkinter as tk
from tkinter import ttk, messagebox
from services.zkteco import Zkteco
import requests

class MainWindow:
    def __init__(self):
        self.service = None
        self.ip_entry = '192.168.1.155'
        self.port_entry = '4370'
    
        # ----- Ventana principal -----
        self.root = tk.Tk()
        self.root.title("Control Biométrico V1")
        self.root.geometry("800x600")

        # ⚡ Estado del modo
        self.is_dark = False  

        # 🎨 Estilo
        self.style = ttk.Style(self.root)
        self.set_light_mode()  # iniciar en modo claro

        # Botón para cambiar tema
        toggle_btn = ttk.Button(self.root, text="🌙 Modo Oscuro", command=self.toggle_theme)
        toggle_btn.pack(pady=10)

        # ----- Frame Principal -----
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill="both", expand=True)

        # ----- Frame Configuración -----
        device_frame = ttk.LabelFrame(frame, text="Conexión con Dispositivo Biométrico", padding=15)
        device_frame.pack(fill="x", pady=10)

        ttk.Label(device_frame, text="IP del dispositivo:").grid(row=0, column=0, sticky="w")
        self.ip_entry = ttk.Entry(device_frame, width=20)
        self.ip_entry.grid(row=0, column=1, padx=5)

        ttk.Label(device_frame, text="Puerto:").grid(row=0, column=2, sticky="w")
        self.port_entry = ttk.Entry(device_frame, width=10)
        self.port_entry.grid(row=0, column=3, padx=5)

        connect_btn = ttk.Button(device_frame, text="Conectar", command=self.connect_device)
        connect_btn.grid(row=0, column=4, padx=10)

        # ----- Notebook (Pestañas) -----
        notebook = ttk.Notebook(frame)
        notebook.pack(fill="both", expand=True, pady=10)

        # ----- Tab 1: Acciones -----
        actions_tab = ttk.Frame(notebook)
        notebook.add(actions_tab, text="Acciones")

        btn_check = ttk.Button(actions_tab, text="Probar conexión Flask", command=self.check_flask)
        btn_check.grid(row=0, column=0, padx=10, pady=10)

        btn_status = ttk.Button(actions_tab, text="Obtener Estado", command=self.get_device_status)
        btn_status.grid(row=0, column=1, padx=10, pady=10)

        btn_users = ttk.Button(actions_tab, text="Listar Usuarios", command=self.get_users)
        btn_users.grid(row=0, column=2, padx=10, pady=10)

        btn_att = ttk.Button(actions_tab, text="Listar Asistencias", command=self.get_attendance)
        btn_att.grid(row=0, column=3, padx=10, pady=10)

        # Text box de logs
        self.log_text = tk.Text(actions_tab, height=15, width=110, wrap="word", state="disabled")
        self.log_text.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # ----- Tab 2: Usuarios -----
        users_tab = ttk.Frame(notebook)
        notebook.add(users_tab, text="Usuarios")

        self.users_tree = ttk.Treeview(users_tab, columns=("id", "name", "privilege"), show="headings", height=20)
        self.users_tree.heading("id", text="ID")
        self.users_tree.heading("name", text="Nombre")
        self.users_tree.heading("privilege", text="Privilegio")
        self.users_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # ----- Tab 3: Asistencias -----
        att_tab = ttk.Frame(notebook)
        notebook.add(att_tab, text="Asistencias")

        self.att_tree = ttk.Treeview(att_tab, columns=("user_id", "timestamp", "status"), show="headings", height=20)
        self.att_tree.heading("user_id", text="Usuario")
        self.att_tree.heading("timestamp", text="Fecha / Hora")
        self.att_tree.heading("status", text="Estado")
        self.att_tree.pack(fill="both", expand=True, padx=10, pady=10)

    # ---- Métodos ----
    def check_flask(self):
        try:
            r = requests.get("http://127.0.0.1:5000/")
            self.log(f"Flask: {r.json()['message']}")
            messagebox.showinfo("Respuesta Flask", r.json()["message"])
        except Exception as e:
            self.log(f"Error Flask: {e}")
            messagebox.showerror("Error", f"No se pudo conectar: {e}")

    def connect_device(self):
        ip = self.ip_entry.get().strip()
        port = int(self.port_entry.get().strip())
        self.service = Zkteco(ip, port)
        ok, msg = self.service.connect()
        self.log(msg)

    def get_device_status(self):
        if not self.service:
            self.log("Advertencia, Debes conectar primero")
            return
        ok, result = self.service.get_status()
        if ok:
            info = "\n".join([f"{k}: {v}" for k, v in result.items()])
            self.log(f"Estado del dispositivo: {info}")
        else:
            self.log(f"Error: {result}")

    def get_users(self):
        try:
            success, result = self.service.get_users()
            if success:
                self.log("Usuarios obtenidos correctamente ✅")
                if not result:
                    self.log("No hay usuarios registrados en el dispotivo")
                    return
                formatted = []
                for u in result:
                    user_id = getattr(u, "user_id", None)
                    name = getattr(u, "name", "Sin Nobre")
                    privilege= getattr(u, "privilege", "N/A")
            
                    line = f"ID: {user_id} | Nombre: {name} | Privilegio: {privilege}"
                    self.log(line)
                    formatted.append(line)
            else:
                self.log(f"Error: {result}")
        except Exception as e:
            self.log(f"Excepción en UI al obtener usuarios: {e}")

    def get_attendance(self):
        try:
            success, result = self.service.get_attendance()
            if success:
                if not result:
                    self.log("No hay asistencias registradas en el dispotivo")
                    return
                formatted = []
                for a in result:
                    user_id = getattr(a, "user_id", None)
                    timestamp = getattr(a, "timestamp", None)
                    status = getattr(a, "status", "-")

                    line = f"ID: {user_id} | Fecha: {timestamp} | Estado: {status}"
                    self.log(line)
                    formatted.append(line)
            else:
                self.log(f"Error: {result}")
        except Exception as e:
            self.log(f"Excepción en UI al obtener asistencias: {e}")

    def log(self, text):
        self.log_text.config(state="normal")
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def set_dark_mode(self):
        self.style.theme_use("clam")

        # Colores suaves en gris oscuro
        bg_color = "#2e2e2e"      # gris oscuro suave
        frame_color = "#3a3a3a"   # gris medio
        text_color = "#e0e0e0"    # blanco suave (no blanco puro)
        button_color = "#505050"  # gris tirando a plomo
        entry_bg = "#404040"      # gris intermedio

        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabelFrame", background=frame_color, foreground=text_color)
        self.style.configure("TLabel", background=bg_color, foreground=text_color)
        self.style.configure("TButton", background=button_color, foreground=text_color)
        self.style.configure("TEntry", fieldbackground=entry_bg, foreground=text_color)

        self.root.configure(bg=bg_color)


    def set_light_mode(self):
        self.style.theme_use("clam")

        # Colores claros neutros (sin ser blanco puro)
        bg_color = "#f5f5f5"      # gris claro suave
        frame_color = "#eaeaea"   # un poco más oscuro que el fondo
        text_color = "#222222"    # casi negro, pero no puro
        button_color = "#d6d6d6"  # gris claro plomo
        entry_bg = "#ffffff"      # blanco puro en campos de entrada

        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabelFrame", background=frame_color, foreground=text_color)
        self.style.configure("TLabel", background=bg_color, foreground=text_color)
        self.style.configure("TButton", background=button_color, foreground=text_color)
        self.style.configure("TEntry", fieldbackground=entry_bg, foreground=text_color)

        self.root.configure(bg=bg_color)


    def toggle_theme(self):
        self.is_dark = not self.is_dark
        if self.is_dark:
            self.set_dark_mode()
        else:
            self.set_light_mode()

    def run(self):
        self.root.mainloop()