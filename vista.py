"""
Modulo Vista: Contiene la clase Ventana, cuya función es implementar la ventana que visualizara los
datos al usuario
se importa :
* tkinter: Librería
* modelo: Módulo creado
"""
from tkinter import PhotoImage, Label, LabelFrame, Entry, ttk, StringVar, Button, CENTER, Tk, N, S, E, W
from modelo import enviar_logs_al_salir


class Ventana:
    def __init__(self, root, modelo):
        """
        Constructor:Su función es especificar las forma y características que tendría la ventana en la que
        se van a presentar los datos de los usuarios.
        * root: variable de tkinter creada en el modulo controlador
        * modelo: objeto de clase traído desde el controlador
        """
        self.root = root

        self.icono = PhotoImage(file="icon.png")
        self.root.iconphoto(True, self.icono)

        self.modelo = modelo                            #Instancia de la clase modelo 

        self.imagen = PhotoImage(file='banner.png')    #Imagen de fondo           
        self.fondo = Label(self.root, image=self.imagen)
        self.fondo.place(x=0, y=0)

        #Titulo de la ventana
        self.titulo = Label(self.root, text="SALIDAS DE MICROS", font=("Bus", 27, "bold"))
        self.titulo.place(x=403, y=1)

        #Etiqueta que muesta la hora
        self.clock = Label(self.root, font=("hora", 50, "bold"))
        self.clock.place(x=400, y=47)

        #Etiqueta que muestra la fecha
        self.tiempo = Label(self.root, font=("fecha", 10, "bold"))
        self.tiempo.place(x=785, y=109)

        self.frame2 = LabelFrame(self.root, text="INGRESO SALIDAS", width=200,
                                 height=475, font=('Calibri', 12), fg='red')
        self.frame2.place(x=11, y=220, width=200, height=475)

        # variables de tkinter a travez de los cuales se tomaran los datos
        self.inte_val, self.chof_val, self.nume_val, self.reco_val, self.sali_val = (
            StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        )
        # Se crear etiquetas de entrada
        self.interno = Label(root, text="Interno")
        self.interno.place(x=13, y=245)
        self.numero = Label(root, text="Numero")
        self.numero.place(x=13, y=295)
        self.chofer = Label(root, text="Nombre Chofer")
        self.chofer.place(x=13, y=345)
        self.recorrido = Label(root, text="Recorrido")
        self.recorrido.place(x=13, y=395)
        self.salida = Label(root, text="Hora Salida(HH:MM)")
        self.salida.place(x=13, y=445)
        # Entradas
        self.entrada1 = Entry(self.root, textvariable=self.inte_val, width=10)  # Campos de entrada
        self.entrada1.place(x=13, y=265)
        self.entrada2 = Entry(self.root, textvariable=self.nume_val, width=10)
        self.entrada2.place(x=13, y=315)
        self.entrada3 = Entry(self.root, textvariable=self.chof_val, width=30)
        self.entrada3.place(x=13, y=365)
        self.entrada4 = Entry(self.root, textvariable=self.reco_val, width=30)
        self.entrada4.place(x=13, y=415)
        self.entrada5 = Entry(self.root, textvariable=self.sali_val, width=10)
        self.entrada5.place(x=13, y=465)
        # Treeview
        self.tree = ttk.Treeview(self.root, show='headings')  # Treeview
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=(None, 15))
        self.style.theme_use("default")
        self.style.configure('Treeview', rowheight=45, font=(None, 15))
        self.style.configure("Heading", font=(None, 15))
        self.style.map('Treeview', background=[('selected', 'blue')])
        self.tree["columns"] = ("col1", "col2", "col3", "col4", "col5")
        self.tree.column("#0", width=10)
        self.tree.column("col1", minwidth=110, anchor=CENTER)
        self.tree.column("col2", minwidth=100, anchor=CENTER)
        self.tree.column("col3", minwidth=110, anchor=CENTER)
        self.tree.column("col4", minwidth=110, anchor=CENTER)
        self.tree.column("col5", minwidth=110, anchor=CENTER)
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="Interno")
        self.tree.heading("col2", text="Numero")
        self.tree.heading("col3", text="Chofer")
        self.tree.heading("col4", text="Recorrido")
        self.tree.heading("col5", text="Hora Salida")
        self.tree.place(x=220, y=220)

        
        """ Botones de la aplicación
            * boton_alta:permite dar de alta en la base de datos los la información que está en los campos
            * boton_consulta: Permite actualizar la información en pantalla
            * boton_editar:Permite editar la información  seleccionada en la pantalla
            * boton_borrar:Permite borrar los datos seleccionados en la pantalla
            * boton_salir:Permite salir de la aplicación
        """

        self.boton_alta = Button(self.root, text="Ingresar", width=10, command=lambda: self.modelo.alta(self.entrada1, self.entrada2, self.entrada3, self.entrada4, self.entrada5, self.tree))
        self.boton_alta.place(x=13, y=500)

        self.boton_consulta = Button(self.root, text="Actualizar", width=10, command=self.actualizar_treeview)
        self.boton_consulta.place(x=13, y=530)

        self.boton_editar = Button(self.root, text="Editar", width=10, command=lambda: self.modelo.editar(self.entrada1, self.entrada2, self.entrada3, self.entrada4, self.entrada5, self.tree))
        self.boton_editar.place(x=13, y=560)

        self.boton_borrar = Button(self.root, text="Borrar", width=10, command=lambda: self.modelo.borrar(self.entrada1, self.entrada2, self.entrada3, self.entrada4, self.entrada5, self.tree))
        self.boton_borrar.place(x=13, y=590)

        self.boton_salir = Button(self.root, text="Salir", width=20, command=enviar_logs_al_salir)
        self.boton_salir.place(x=13, y=610)
        
        self.tree.bind('<ButtonRelease-1>', self.seleccion)

        
        self.hora()                 #Llama al método hora() que permite actualizar la hora cada 900 milisegundos
        self.actualizar_treeview()  #Llama al metodo actualizar_treeview que permite actualizar la información en pantalla cada 1 seg

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    # Se define funciones para traer desde modelo

    def hora(self):
        """
        Método que permite actualizar la hora, para esto hace una llamada al método de la clase modelo
        * self.clock: Label de la clase ventana
        * self.tiempo: Label de la clase ventana
        """
        self.modelo.actualizar_tiempo(self.clock, self.tiempo)
        self.clock.after(900, self.hora)

    def actualizar_treeview(self):
        """
        Método que permite actualizar la información contenida en la ventana que ve el usuario
        * self.tree: variable de la clase ventana
        """
        self.modelo.actualizar_treeview(self.tree)
        self.root.after(1000, self.actualizar_treeview)

    def seleccion(self, e):
        """
        Método selección:Este método tiene la función de obtener todos los valores de la selección realizada
        en la ventana de la aplicación
        * entrada1: interno del colectivo
        * entrada2: Número del recorrido
        * entrada3: nombre del recorrido
        * entrada4: Hora de salida
        * entrada5:Fecha
        * tree: Variable del treeview
        * e: Variable del la función
        """
        self.modelo.seleccion(e, self.tree, self.entrada1, self.entrada2, self.entrada3, self.entrada4, self.entrada5)
