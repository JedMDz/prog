import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import csv
import datetime
import os
from datetime import timedelta

# --- IMPORTACIONES PARA GRÁFICAS ---
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except ImportError:
    plt = None

# =============================================================================
#  DATOS COMPLETOS (EQUIPOS ELÉCTRICOS E INDUSTRIALES)
# =============================================================================

EQUIPOS_DATA = {
    "Medición Eléctrica": [
        {"nombre": "Megóhmetro Digital 1 kV", "precioHora": 35, "precioDia": 200},
        {"nombre": "Megóhmetro Digital 5 kV", "precioHora": 45, "precioDia": 260},
        {"nombre": "Multímetro Fluke 17B+", "precioHora": 22, "precioDia": 130},
        {"nombre": "Multímetro Fluke 87V TrueRMS", "precioHora": 30, "precioDia": 170},
        {"nombre": "Pinza Amperimétrica Fluke 325", "precioHora": 25, "precioDia": 140},
        {"nombre": "Pinza Amperimétrica UT210E", "precioHora": 18, "precioDia": 95},
        {"nombre": "Telurómetro 3 Hilos", "precioHora": 32, "precioDia": 180},
        {"nombre": "Telurómetro 4 Hilos Profesional", "precioHora": 45, "precioDia": 240},
        {"nombre": "Detector de Tensión Fluke 1AC II", "precioHora": 10, "precioDia": 60},
        {"nombre": "Megóhmetro Analógico 1000V", "precioHora": 28, "precioDia": 160}
    ],
    "Instrumentos Industriales": [
        {"nombre": "Tacómetro Láser Digital", "precioHora": 18, "precioDia": 100},
        {"nombre": "Luxómetro Digital", "precioHora": 15, "precioDia": 80},
        {"nombre": "Sonómetro Clase 2", "precioHora": 22, "precioDia": 120},
        {"nombre": "Manómetro Digital 600 PSI", "precioHora": 20, "precioDia": 110},
        {"nombre": "Termómetro Infrarrojo Fluke 62 MAX", "precioHora": 18, "precioDia": 95},
        {"nombre": "Termohigrómetro Digital", "precioHora": 12, "precioDia": 70},
        {"nombre": "Medidor de Vibraciones Industrial", "precioHora": 40, "precioDia": 230},
        {"nombre": "Anemómetro Digital", "precioHora": 18, "precioDia": 90},
        {"nombre": "Medidor de pH Portátil", "precioHora": 15, "precioDia": 85},
        {"nombre": "Escáner Térmico Compacto", "precioHora": 30, "precioDia": 180}
    ],
    "Ensayos y Seguridad": [
        {"nombre": "Cámara Termográfica Fluke PTi120", "precioHora": 55, "precioDia": 330},
        {"nombre": "Cámara Termográfica FLIR C5", "precioHora": 48, "precioDia": 290},
        {"nombre": "Medidor de Fugas de Corriente", "precioHora": 28, "precioDia": 160},
        {"nombre": "Analizador de Energía Trifásico", "precioHora": 65, "precioDia": 380},
        {"nombre": "Analizador de Calidad de Energía", "precioHora": 75, "precioDia": 420},
        {"nombre": "Detector de Rotación de Fases", "precioHora": 25, "precioDia": 120},
        {"nombre": "Probador de Diferenciales (RCD Tester)", "precioHora": 32, "precioDia": 170},
        {"nombre": "Registrador de Corriente 3 Canales", "precioHora": 40, "precioDia": 210},
        {"nombre": "Registrador de Voltaje 2 Canales", "precioHora": 32, "precioDia": 165},
        {"nombre": "Probador de Aislamiento de Guantes", "precioHora": 38, "precioDia": 200}
    ],
    "Herramientas Especializadas": [
        {"nombre": "Bomba de Vacío 1 Etapa 3CFM", "precioHora": 25, "precioDia": 130},
        {"nombre": "Bomba de Vacío 2 Etapas 5CFM", "precioHora": 35, "precioDia": 200},
        {"nombre": "Detector de Fugas Refrigerante", "precioHora": 22, "precioDia": 115},
        {"nombre": "Máquina de Termofusión 1200W", "precioHora": 20, "precioDia": 110},
        {"nombre": "Prensa Hidráulica 10T Portátil", "precioHora": 28, "precioDia": 150},
        {"nombre": "Extractor de Rulemanes Industrial", "precioHora": 25, "precioDia": 135},
        {"nombre": "Cortadora de Concreto 3200W", "precioHora": 30, "precioDia": 160},
        {"nombre": "Taladro Percutor Industrial", "precioHora": 18, "precioDia": 90},
        {"nombre": "Máquina de Soldar Inversora 200A", "precioHora": 25, "precioDia": 135},
        {"nombre": "Rotorbalanceador Ligero", "precioHora": 45, "precioDia": 250}
    ],
    "Equipos para Media y Baja Tensión": [
        {"nombre": "Detector de Tensión 10kV", "precioHora": 40, "precioDia": 220},
        {"nombre": "Detector de Tensión 30kV", "precioHora": 55, "precioDia": 310},
        {"nombre": "Medidor de Resistencia de Transformador", "precioHora": 70, "precioDia": 420},
        {"nombre": "Medidor de Relación de Transformadores (TTR)", "precioHora": 68, "precioDia": 400},
        {"nombre": "Probador de Interruptores BT", "precioHora": 60, "precioDia": 350},
        {"nombre": "Analizador de Relés de Protección", "precioHora": 85, "precioDia": 500},
        {"nombre": "Equipo de Prueba de Sobretensiones", "precioHora": 90, "precioDia": 520},
        {"nombre": "Medidor de Resistencia de Devanados", "precioHora": 75, "precioDia": 440},
        {"nombre": "Analizador de Armónicos Trifásico", "precioHora": 65, "precioDia": 360},
        {"nombre": "Equipo de Prueba de Inyección Primaria", "precioHora": 120, "precioDia": 700}
    ]
}

CATEGORIAS = list(EQUIPOS_DATA.keys())

# --- CONFIGURACIÓN DE ARCHIVOS ---
CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
ARCHIVOS = {
    "inventario": os.path.join(CARPETA_ACTUAL, "inventario.csv"),
    "reservas": os.path.join(CARPETA_ACTUAL, "reservas.csv"),
    "clientes": os.path.join(CARPETA_ACTUAL, "clientes.csv")
}

# =============================================================================
#  CAPA 1: LÓGICA DE DATOS Y NEGOCIO (BACKEND)
# =============================================================================

def inicializar_sistema():
    """Crea los archivos CSV necesarios si no existen."""
    
    # 1. INVENTARIO
    recrear = False
    if os.path.exists(ARCHIVOS["inventario"]):
        try:
            with open(ARCHIVOS["inventario"], 'r', encoding='utf-8') as f:
                if len(f.readlines()) < 15: recrear = True
        except: recrear = True
    else: recrear = True

    if recrear:
        if os.path.exists(ARCHIVOS["inventario"]):
            try: os.remove(ARCHIVOS["inventario"])
            except: pass
        
        datos_para_csv = []
        contador_id = 101
        for categoria, lista_equipos in EQUIPOS_DATA.items():
            for equipo in lista_equipos:
                id_unico = f"EQ-{contador_id}"
                fila = [id_unico, equipo["nombre"], categoria, "Disponible", str(equipo["precioHora"]), str(equipo["precioDia"]), "Equipo Certificado"]
                datos_para_csv.append(fila)
                contador_id += 1
        escribir_csv(ARCHIVOS["inventario"], datos_para_csv, modo='w')

    # 2. CLIENTES
    if not os.path.exists(ARCHIVOS["clientes"]):
        clientes_init = [["Empresa GeoIngenieros SAC"], ["Empresa SDL Ingenieros"], ["Empresa Tech SAC"], ["Ingenieros Romero SAC"],["Rimax"]]
        escribir_csv(ARCHIVOS["clientes"], clientes_init, modo='w')

    # 3. RESERVAS
    if not os.path.exists(ARCHIVOS["reservas"]):
        encabezado = ["cliente", "id_equipo", "nombre_equipo", "categoria", "inicio", "fin", "estado", "costo_hora", "costo_dia", "total"]
        escribir_csv(ARCHIVOS["reservas"], [encabezado], modo='w')


def leer_csv(ruta):
    datos = []
    if os.path.exists(ruta):
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                datos = list(reader)
        except Exception: return []
    return datos

def escribir_csv(ruta, filas, modo='a'):
    with open(ruta, modo, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(filas)

def reescribir_todo_csv(ruta, filas):
    with open(ruta, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(filas)

# --- Lógica de Productos ---
def logica_agregar_producto(nombre, categoria, costo_h, costo_d):
    id_unico = f"EQ-{datetime.datetime.now().strftime('%M%S')}"
    fila = [id_unico, nombre, categoria, "Disponible", str(costo_h), str(costo_d), "N/A"]
    escribir_csv(ARCHIVOS["inventario"], [fila], modo='a')
    return id_unico

# --- Lógica de Clientes ---
def logica_obtener_clientes():
    raw = leer_csv(ARCHIVOS["clientes"])
    lista = [r[0] for r in raw if len(r) > 0]
    return lista

def logica_agregar_cliente(nombre):
    escribir_csv(ARCHIVOS["clientes"], [[nombre]], modo='a')

def logica_eliminar_cliente(nombre):
    todos = leer_csv(ARCHIVOS["clientes"])
    nuevos = [r for r in todos if len(r) > 0 and r[0] != nombre]
    reescribir_todo_csv(ARCHIVOS["clientes"], nuevos)

def logica_validar_login(usuario):
    lista = logica_obtener_clientes()
    return usuario in lista

# --- Lógica de Reservas ---
def logica_calcular_fechas(fecha_str, horas):
    try:
        ini = datetime.datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
        fin = ini + timedelta(hours=int(horas))
        return True, ini, fin, fin.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return False, None, None, None

def logica_verificar_disponibilidad(id_eq, inicio_req, fin_req):
    if not os.path.exists(ARCHIVOS["reservas"]): return True, ""
    reservas = leer_csv(ARCHIVOS["reservas"])
    
    for row in reservas:
        if len(row) < 7: continue
        # IMPORTANTE: Si el estado es "Finalizado", no bloquea el equipo
        estado = row[6]
        if estado == "Finalizado": continue 

        if row[1] == id_eq:
            try:
                ini_exist = datetime.datetime.strptime(row[4], "%Y-%m-%d %H:%M")
                fin_exist = datetime.datetime.strptime(row[5], "%Y-%m-%d %H:%M")
                if inicio_req < fin_exist and fin_req > ini_exist:
                    return False, f"Ocupado por {row[0]} hasta {row[5]}"
            except: continue
    return True, ""

def logica_guardar_reserva(cliente, item_data, inicio_str, fin_str, horas):
    ch = int(item_data[3]) if str(item_data[3]).isdigit() else 0
    cd = int(item_data[4]) if str(item_data[4]).isdigit() else 0
    horas = int(horas)
    dias = horas // 24
    horas_rest = horas % 24
    total = dias * cd + horas_rest * ch

    # Se guarda con estado "OK". Esto queda fijo en el CSV.
    fila = [cliente, item_data[0], item_data[1], item_data[2], inicio_str, fin_str, "OK", str(ch), str(cd), str(total)]
    escribir_csv(ARCHIVOS["reservas"], [fila], modo='a')

def logica_devolver_equipo(cliente, id_equipo, fecha_inicio):
    """Busca la reserva activa y cambia estado a Finalizado, PERO NO BORRA LA FILA."""
    reservas = leer_csv(ARCHIVOS["reservas"])
    modificado = False
    nueva_lista = []
    
    for row in reservas:
        if len(row) > 6:
            if row[0] == cliente and row[1] == id_equipo and row[4] == fecha_inicio and row[6] == "OK":
                row[6] = "Finalizado" # Solo cambiamos el estado
                modificado = True
        nueva_lista.append(row)
    
    if modificado:
        reescribir_todo_csv(ARCHIVOS["reservas"], nueva_lista)
        return True
    return False

# =============================================================================
#  CAPA 2: INTERFAZ DE USUARIO (FRONTEND)
# =============================================================================

def util_centrar(ventana, w, h):
    x = int((ventana.winfo_screenwidth()/2) - (w/2))
    y = int((ventana.winfo_screenheight()/2) - (h/2))
    ventana.geometry(f"{w}x{h}+{x}+{y}")

# --- LOGIN (CON IMAGEN REDIMENSIONADA) ---
def gui_login(app_state):
    root = tk.Tk()
    root.title("Admin-Rent v4.0")
    root.configure(bg="#f4f6f7")
    util_centrar(root, 420, 600) # Ventana un poco más alta para que entre todo

    # Intento de Cargar Logo
    try:
        ruta_img = os.path.join(CARPETA_ACTUAL, "logo.png")
        if os.path.exists(ruta_img):
            img_raw = tk.PhotoImage(file=ruta_img)
            
            # --- AQUÍ ESTÁ EL TRUCO ---
            # subsample(x, y) reduce la imagen. 
            # (10, 10) significa que la hace 10 veces más pequeña.
            # Si sigue muy grande, cambia los 10 por 20.
            # Si queda muy chica, cambia los 10 por 5.
            img_chica = img_raw.subsample(10, 10) 
            
            lbl_img = tk.Label(root, image=img_chica, bg="#f4f6f7")
            lbl_img.image = img_chica 
            lbl_img.pack(pady=(20, 0))
    except Exception:
        pass

    tk.Label(root, text="SISTEMA DE ALQUILER", font=("Arial", 16, "bold"), bg="#f4f6f7", fg="#333").pack(pady=(10,10))
    
    frame = tk.Frame(root, bg="white", padx=30, pady=30, relief="raised")
    frame.pack()

    tk.Label(frame, text="Usuario Registrado:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
    
    lista_usuarios = logica_obtener_clientes()
    combo_users = ttk.Combobox(frame, values=lista_usuarios, font=("Arial", 11), width=23)
    combo_users.pack(pady=5)
    if lista_usuarios: combo_users.current(0)

    def on_ingresar():
        nombre = combo_users.get().strip()
        if logica_validar_login(nombre):
            app_state["usuario"] = nombre
            app_state["root"] = root
            root.withdraw()
            gui_inventario(app_state)
        else:
            messagebox.showerror("Acceso Denegado", "El usuario no está registrado en la base de datos.")

    def on_admin():
        pwd = simpledialog.askstring("Admin", "Clave de Administrador:", parent=root, show="*")
        if pwd == "1234":
            app_state["usuario"] = "ADMIN"
            app_state["root"] = root
            root.withdraw()
            gui_panel_admin(app_state)
        elif pwd:
            messagebox.showerror("Error", "Clave incorrecta")

    tk.Button(frame, text="INGRESAR", bg="#3498db", fg="white", font=("Arial", 10, "bold"), command=on_ingresar, height=2, width=25).pack(pady=15)
    tk.Button(root, text="Acceso Administrativo", command=on_admin, bd=0, bg="#f4f6f7", fg="#7f8c8d", cursor="hand2").pack(pady=10)

    def refresh_list():
        combo_users['values'] = logica_obtener_clientes()
    
    refresh_list()
    root.mainloop()

# --- VENTANA PRINCIPAL USUARIO ---
def gui_inventario(app_state):
    win = tk.Toplevel()
    win.title(f"Panel de Usuario - {app_state['usuario']}")
    util_centrar(win, 1100, 700)
    win.protocol("WM_DELETE_WINDOW", lambda: [app_state["root"].deiconify(), win.destroy()])

    nb = ttk.Notebook(win)
    nb.pack(fill="both", expand=True, padx=10, pady=10)

    # --- TAB 1: CATÁLOGO ---
    tab_cat = tk.Frame(nb)
    nb.add(tab_cat, text="Catálogo y Reservas")

    f_top = tk.Frame(tab_cat, bg="#ecf0f1", pady=10)
    f_top.pack(fill="x")
    
    # 1. Filtro Texto
    tk.Label(f_top, text="Buscar:", bg="#ecf0f1").pack(side="left", padx=(10, 5))
    entry_filt = tk.Entry(f_top, width=25)
    entry_filt.pack(side="left", padx=5)

    # 2. Filtro Categoría
    tk.Label(f_top, text="Categoría:", bg="#ecf0f1").pack(side="left", padx=(15, 5))
    lista_cats = ["Todas"] + CATEGORIAS
    cb_cat_filter = ttk.Combobox(f_top, values=lista_cats, state="readonly", width=25)
    cb_cat_filter.pack(side="left", padx=5)
    cb_cat_filter.current(0)
    
    frame_list = tk.Frame(tab_cat)
    frame_list.pack(fill="both", expand=True, padx=10, pady=5)
    scroll = tk.Scrollbar(frame_list); scroll.pack(side=tk.RIGHT, fill="y")
    lista_inv = tk.Listbox(frame_list, font=("Consolas", 10), yscrollcommand=scroll.set, height=15)
    lista_inv.pack(fill="both", expand=True); scroll.config(command=lista_inv.yview)

    def cargar_inv(*args):
        filtro_texto = entry_filt.get().lower()
        filtro_cat = cb_cat_filter.get()

        lista_inv.delete(0, tk.END)
        datos = leer_csv(ARCHIVOS["inventario"])
        
        for row in datos:
            if len(row) < 7: continue
            
            match_cat = (filtro_cat == "Todas" or row[2] == filtro_cat)
            texto = f"[{row[0]}] {row[1]:<35} | {row[2]:<25} | S/.{row[4]}/h"
            match_texto = (filtro_texto in texto.lower())

            if match_cat and match_texto:
                lista_inv.insert(tk.END, texto)
    
    entry_filt.bind("<KeyRelease>", cargar_inv)
    cb_cat_filter.bind("<<ComboboxSelected>>", cargar_inv)
    cargar_inv()

    def reservar():
        sel = lista_inv.curselection()
        if not sel: return messagebox.showwarning("!", "Seleccione un equipo")
        raw = lista_inv.get(sel[0])
        id_eq = raw.split("]")[0].replace("[", "").strip()
        
        full_data = next((r for r in leer_csv(ARCHIVOS["inventario"]) if r[0] == id_eq), None)
        if full_data:
            gui_popup_reserva(app_state, full_data, win)

    tk.Button(tab_cat, text="RESERVAR SELECCIONADO", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), command=reservar, height=2).pack(fill="x", padx=10, pady=10)

    # --- TAB 2: MIS RESERVAS ---
    tab_mis = tk.Frame(nb)
    nb.add(tab_mis, text="Mis Alquileres Activos")

    tk.Label(tab_mis, text="Selecciona un equipo para devolverlo antes de tiempo:", font=("Arial", 10), pady=10).pack()

    frame_mis = tk.Frame(tab_mis)
    frame_mis.pack(fill="both", expand=True, padx=10)
    scroll2 = tk.Scrollbar(frame_mis); scroll2.pack(side=tk.RIGHT, fill="y")
    lista_mis = tk.Listbox(frame_mis, font=("Consolas", 10), yscrollcommand=scroll2.set, bg="#fff8e1")
    lista_mis.pack(fill="both", expand=True); scroll2.config(command=lista_mis.yview)

    def cargar_mis_reservas():
        lista_mis.delete(0, tk.END)
        reservas = leer_csv(ARCHIVOS["reservas"])
        usuario = app_state["usuario"]
        hay = False
        for row in reservas:
            if len(row) > 6 and row[0] == usuario and row[6] == "OK":
                lista_mis.insert(tk.END, f"{row[1]} | {row[2]} | Inicio: {row[4]} | Fin: {row[5]}")
                hay = True
        if not hay:
            lista_mis.insert(tk.END, "No tienes reservas activas.")

    def devolver_item():
        sel = lista_mis.curselection()
        if not sel: return
        txt = lista_mis.get(sel[0])
        if "No tienes" in txt: return

        parts = txt.split("|")
        id_eq = parts[0].strip()
        inicio_str = parts[2].replace("Inicio:", "").strip()

        if messagebox.askyesno("Confirmar", f"¿Deseas devolver el equipo {id_eq} ahora?"):
            ok = logica_devolver_equipo(app_state["usuario"], id_eq, inicio_str)
            if ok:
                messagebox.showinfo("Éxito", "Equipo devuelto. El registro queda guardado en el historial histórico.")
                cargar_mis_reservas()
            else:
                messagebox.showerror("Error", "No se pudo procesar la devolución.")

    tk.Button(tab_mis, text="🔄 Actualizar Lista", command=cargar_mis_reservas).pack(pady=5)
    tk.Button(tab_mis, text="DEVOLVER EQUIPO", bg="#e67e22", fg="white", font=("Arial", 10, "bold"), command=devolver_item).pack(pady=10, fill="x", padx=20)
    
    tab_mis.bind("<Visibility>", lambda e: cargar_mis_reservas())


def gui_popup_reserva(app_state, item_data, parent):
    pop = tk.Toplevel(parent)
    pop.title("Reservar")
    util_centrar(pop, 350, 400)
    
    tk.Label(pop, text=item_data[1], font=("Arial", 12, "bold"), bg="#34495e", fg="white").pack(fill="x", ipady=10)
    
    f = tk.Frame(pop, padx=20, pady=20)
    f.pack()

    tk.Label(f, text="Fecha Inicio (YYYY-MM-DD HH:MM):").pack()
    var_f = tk.StringVar(value=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    tk.Entry(f, textvariable=var_f, width=20, justify="center").pack(pady=5)

    tk.Label(f, text="Horas de uso:").pack()
    var_h = tk.IntVar(value=24)
    tk.Spinbox(f, from_=1, to=720, textvariable=var_h, width=5).pack()

    lbl_info = tk.Label(f, text="...", fg="blue")
    lbl_info.pack(pady=10)

    def calc(*a):
        ok, i, fin, str_fin = logica_calcular_fechas(var_f.get(), var_h.get())
        if ok: lbl_info.config(text=f"Devolución: {str_fin}")
        else: lbl_info.config(text="Fecha inválida")
    var_h.trace_add("write", calc); calc()

    def confirmar():
        f_txt, h = var_f.get(), var_h.get()
        ok, ini, fin, str_fin = logica_calcular_fechas(f_txt, h)
        if not ok: return messagebox.showerror("Error", "Fecha mal")
        
        libre, msg = logica_verificar_disponibilidad(item_data[0], ini, fin)
        if libre:
            logica_guardar_reserva(app_state["usuario"], item_data, f_txt, str_fin, h)
            messagebox.showinfo("Hecho", "Reserva creada exitosamente.")
            pop.destroy()
        else:
            messagebox.showerror("Ocupado", msg)

    tk.Button(pop, text="CONFIRMAR", bg="#2980b9", fg="white", command=confirmar).pack(fill="x", padx=20, pady=10)

# --- ADMIN PANEL ---
def gui_panel_admin(app_state):
    win = tk.Toplevel()
    win.title("Administración")
    util_centrar(win, 900, 600)
    win.protocol("WM_DELETE_WINDOW", lambda: [app_state["root"].deiconify(), win.destroy()])

    nb = ttk.Notebook(win)
    nb.pack(fill="both", expand=True, padx=10, pady=10)

    # TAB 1: AGREGAR EQUIPO
    t1 = tk.Frame(nb); nb.add(t1, text="Inventario")
    
    fr = tk.LabelFrame(t1, text="Nuevo Equipo", padx=10, pady=10)
    fr.pack(padx=20, pady=20)
    
    tk.Label(fr, text="Nombre:").grid(row=0, column=0)
    e_n = tk.Entry(fr); e_n.grid(row=0, column=1)
    tk.Label(fr, text="Categoría:").grid(row=1, column=0)
    cb_c = ttk.Combobox(fr, values=CATEGORIAS); cb_c.grid(row=1, column=1); cb_c.current(0)
    
    def add_eq():
        if e_n.get():
            nid = logica_agregar_producto(e_n.get(), cb_c.get(), 10, 50)
            messagebox.showinfo("OK", f"Agregado ID: {nid}")
            e_n.delete(0, tk.END)
    tk.Button(fr, text="Guardar", command=add_eq).grid(row=2, columnspan=2, pady=10)

    # TAB 2: FINANZAS E HISTORIAL
    t2 = tk.Frame(nb); nb.add(t2, text="Finanzas e Historial")
    
    header_fin = tk.Frame(t2, bg="#ddd")
    header_fin.pack(fill="x", padx=10)
    tk.Label(header_fin, text="CLIENTE | EQUIPO | ESTADO | MONTO", font=("Consolas", 10, "bold"), bg="#ddd").pack()

    lst_fin = tk.Listbox(t2, font=("Consolas", 9))
    lst_fin.pack(fill="both", expand=True, padx=10)
    
    def load_fin():
        lst_fin.delete(0, tk.END)
        suma = 0
        for r in leer_csv(ARCHIVOS["reservas"]):
            if len(r)>9 and r[0] != "cliente":
                texto = f"{r[0]:<12} | {r[2]:<20} | {r[6]:<10} | S/.{r[9]}"
                lst_fin.insert(tk.END, texto)
                try: suma += float(r[9])
                except: pass
        t2_lbl.config(text=f"INGRESOS TOTALES (Activos + Finalizados): S/. {suma:.2f}")
    
    t2_lbl = tk.Label(t2, text="Total: S/. 0.00", font=("Arial", 12, "bold"), fg="#27ae60")
    t2_lbl.pack()
    tk.Button(t2, text="Actualizar Reporte", command=load_fin).pack(pady=5)
    load_fin()

    # TAB 3: GRÁFICOS
    t3 = tk.Frame(nb); nb.add(t3, text="Gráficos")
    def gen_graf():
        if not plt: return
        for w in t3.winfo_children(): w.destroy()
        data = {}
        for r in leer_csv(ARCHIVOS["reservas"]):
            if len(r)>9 and r[0]!="cliente":
                cat = r[3]
                try: val = float(r[9])
                except: val=0
                data[cat] = data.get(cat, 0) + val
        
        fig, ax = plt.subplots(figsize=(5,3), dpi=100)
        ax.bar(data.keys(), data.values(), color="#8e44ad")
        ax.set_title("Ingresos por Categoría")
        canvas = FigureCanvasTkAgg(fig, master=t3)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    tk.Button(t3, text="Generar", command=gen_graf).pack()

    # TAB 4: GESTIÓN CLIENTES
    t4 = tk.Frame(nb); nb.add(t4, text="Gestión Usuarios")
    
    f_add_u = tk.Frame(t4, pady=10)
    f_add_u.pack()
    tk.Label(f_add_u, text="Nuevo Usuario:").pack(side="left")
    e_new_u = tk.Entry(f_add_u); e_new_u.pack(side="left", padx=5)
    
    lst_users = tk.Listbox(t4)
    lst_users.pack(fill="both", expand=True, padx=20, pady=5)

    def refrescar_usuarios():
        lst_users.delete(0, tk.END)
        for u in logica_obtener_clientes():
            lst_users.insert(tk.END, u)

    def agregar_usuario_btn():
        nom = e_new_u.get().strip()
        if nom:
            logica_agregar_cliente(nom)
            e_new_u.delete(0, tk.END)
            refrescar_usuarios()
    
    def eliminar_usuario_btn():
        sel = lst_users.curselection()
        if sel:
            nom = lst_users.get(sel[0])
            if messagebox.askyesno("Eliminar", f"¿Borrar a {nom}?"):
                logica_eliminar_cliente(nom)
                refrescar_usuarios()

    tk.Button(f_add_u, text="Agregar", command=agregar_usuario_btn, bg="#27ae60", fg="white").pack(side="left")
    tk.Button(t4, text="Eliminar Seleccionado", command=eliminar_usuario_btn, bg="#c0392b", fg="white").pack(pady=10)
    
    refrescar_usuarios()

# --- MAIN ---
if __name__ == "__main__":
    inicializar_sistema()
    state = {"usuario": None, "root": None}
    gui_login(state)
