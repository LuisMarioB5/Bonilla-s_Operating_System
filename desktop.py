from PyQt5.QtWidgets import QToolBar, QScrollArea, QDialog, QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QAction, QMenu, QInputDialog, QMessageBox
from apps.taskmanager import taskmanager
from PyQt5.QtGui import QPixmap, QIcon
from apps.notepad import notepad
from PyQt5.QtCore import Qt
import sys
import os



class ButtonStartMenu(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setObjectName("ButtonStartMenu")


class NewUser:
    def __init__(self, name, user, password, image):
        self.name = name
        self.user = user
        self.password = password
        self.image = image


class ContextMenu(QMenu):
    def __init__(self, element=None, option1=False, option2=False, option3=False, win=False, instance=None, parent=None):
        super().__init__(parent)

        self.element = element
        self.instance = instance
        
        if option1:

            # Agrega acciones al menú contextual
            open = QAction("Open", self)
            rename = QAction("Rename", self)
            delete = QAction("Delete", self)

            # Conecta las acciones a sus respectivos métodos
            open.triggered.connect(self.on_open_triggered)
            rename.triggered.connect(self.on_rename_triggered)
            delete.triggered.connect(self.on_delete_triggered)
            
            # Agrega las acciones al menú
            self.addAction(open)
            self.addAction(rename)
            self.addAction(delete)
        
        if option2:
            # Crear el menú "new"
            new = QMenu("New", self)

            # Crear las acciones para el submenú
            folder = QAction("Folder", self)
            notepad = QAction("Notepad", self)

            # Agregar las acciones al submenú
            new.addAction(folder)
            new.addAction(notepad)

            # Agregar el submenú al menú principal
            self.addMenu(new)

            # Conectar las acciones a sus respectivos métodos
            folder.triggered.connect(self.on_folder_triggered)
            notepad.triggered.connect(self.on_notepad_triggered)        

        if option3:

            # Crear una acción para "Open"
            open = QAction("Open", self)
            self.addAction(open)

            # Crear el menú "Send to"
            sendto_menu = QMenu("Send to", self)

            # Crear las acciones para el submenú
            desktop = QAction("Desktop", self)
            taskbar = QAction("Taskbar", self)

            # Agregar las acciones al submenú
            sendto_menu.addAction(desktop)
            sendto_menu.addAction(taskbar)

            # Agregar el submenú al menú principal
            self.addMenu(sendto_menu)

            # Conectar las acciones a sus respectivos métodos
            open.triggered.connect(self.on_open_triggered)
            desktop.triggered.connect(self.on_desktop_triggered)
            taskbar.triggered.connect(self.on_taskbar_triggered)
            
        if win:
            # Agrega acciones al menú contextual
            signout = QAction("Sign out", self)
            shutdown = QAction("Shut down", self)
            restart = QAction("Restart", self)
            desktop = QAction("Desktop", self)

            # Conecta las acciones a sus respectivos métodos
            signout.triggered.connect(self.on_signout_triggered)
            shutdown.triggered.connect(self.on_shutdown_triggered)
            restart.triggered.connect(self.on_restart_triggered)
            desktop.triggered.connect(self.on_showdesktop_triggered)  
            
            # Agrega las acciones al menú
            self.addAction(signout)
            self.addAction(shutdown)
            self.addAction(restart)
            self.addAction(desktop)

    def on_open_triggered(self):
        # Define los métodos que se ejecutarán cuando se seleccione una acción
        if self.element.name == 'Folder':
            print("OpenOption selected for:", self.element.alias)
        else:
            print("OpenOption selected for:", self.element.name)

    def on_rename_triggered(self):
        MainWindow.rename_file(self=self, file=self.element, file_path=self.element.get_file_path())


    def on_delete_triggered(self):
        if self.element.name == 'Folder':
            print("DeleteOption selected for:", self.element.alias)
        else:
            print("DeleteOption selected for:", self.element.name)

    
    def on_desktop_triggered(self):
        print("SendtoDesktopOption selected for: Startmenu")
    
    def on_taskbar_triggered(self):
        print("SendtoTaskbarOption selected for: Startmenu")
    
    def on_folder_triggered(self):
        print("NewFolderOption selected for: Desktop")
        MainWindow.create_new_folder(self.instance)
    
    def on_notepad_triggered(self):
        print("NewNotepadOption selected for: Desktop")

    # Funciones para win
    def on_signout_triggered(self):
        print("SignOutOption selected for: Win Icon Toolbar. On instance:", self.instance)
    
    def on_shutdown_triggered(self):
        print("ShutdownOption selected for: Win Icon Toolbar. On instance:", self.instance)
    
    def on_restart_triggered(self):
        print("RestartOption selected for: Win Icon Toolbar. On instance:", self.instance)
    
    def on_showdesktop_triggered(self):
        print("DesktopOption selected for: Win Icon Toolbar. On instance:", self.instance)


class App:
    def __init__(self, name, icon_path, instance, file_path = None, alias = None):
        self.name = name
        self.icon_path = icon_path
        self.instance = instance
        self.file_path = file_path

        if alias is None:
            self.alias = name
        else:
            self.alias = alias
    
    def get_file_path(self):
        # Devuelve el file path de la app
        print('app_file_path:', self.file_path)
        return self.file_path


class Folder:
    def __init__(self, file_path = None, alias = None):
        self.name = 'Folder'
        self.icon_path = './img/icons/folder.png'  # Ruta del ícono de la carpeta
        self.file_path = file_path
        self.alias = alias

    def get_file_path(self):
        # Devuelve el file path del folder
        print('folder_file_path:', self.file_path)
        return self.file_path


class DesktopIcon(QWidget):
    def __init__(self, app, parent=None):
        super().__init__(parent)

        self.app = app

        # Configurar el diseño vertical para el icono
        layout = QVBoxLayout()

        # Crear una etiqueta para la imagen del icono
        self.label_icon = QLabel()
        pixmap = QPixmap(app.icon_path)
        self.label_icon.setPixmap(pixmap.scaledToHeight(40, Qt.SmoothTransformation)) # Escalar la imagen a 40px de ancho, manteniendo la relación de aspecto
        layout.addWidget(self.label_icon, alignment=Qt.AlignCenter)
        
        # Crear una etiqueta para el texto del icono
        self.label_text = QLabel(app.alias)
            
        
        self.label_text.setStyleSheet("font-family: Segoe UI; font-size: 14px; color: white;")
        layout.addWidget(self.label_text, alignment=Qt.AlignCenter)

        # Establecer el tooltip con el nombre de la aplicación
        self.label_icon.setToolTip(app.name)

        # Conectar el doble clic para abrir la aplicación
        self.label_icon.mouseDoubleClickEvent = self.open_application
        self.label_text.mouseDoubleClickEvent = self.open_application

        # Conectar el clic derecho para abrir el menú contextual
        self.label_icon.setContextMenuPolicy(Qt.CustomContextMenu)
        self.label_icon.customContextMenuRequested.connect(self.show_desktop_icon_context_menu)
        self.label_text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.label_text.customContextMenuRequested.connect(self.show_desktop_icon_context_menu)


        self.setLayout(layout)

    def open_application(self, event):
        print(f"Abrir aplicación: {self.app.name}")

    def show_desktop_icon_context_menu(self, pos):
        # Crear instancia del menú contextual en los iconos del escritorio
        menu = ContextMenu(element=self.app, option1=True)

        # Mostrar el menú en la posición del clic derecho
        menu.exec_(self.mapToGlobal(pos))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Titulo del sistema operativo (OS)
        self.setWindowTitle("Bonilla's Operating System")
        
        # Establecer tamaño mínimo y posicion de la ventana
        self.setMinimumSize(1536, 864)
        self.setGeometry(192, 108, 1536, 864)

        # Crear una etiqueta para la imagen de fondo
        self.background_label = QLabel(self)
        self.background_label.setAlignment(Qt.AlignCenter)
        self.set_background_image("./img/background_edited.png")

        # Lista para mantener un registro de las ventanas abiertas
        self.open_windows = []
       
        # Crear un layout de cuadrícula para los iconos en el escritorio
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setHorizontalSpacing(0)
        self.grid_layout.setVerticalSpacing(0)


        self.num_cols = 14 # Minimizado en 14, en Pantalla completa en 17
        self.num_rows = 9 # Minimizado en 9, en Pantalla completa en 11

        # Creamos una matriz de None (espacios vacíos) para inicializar el grid layout
        self.grid_widgets = [[None for _ in range(self.num_cols)] for _ in range(self.num_rows)]

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                widget = QWidget()
                #widget.setStyleSheet("background-color: grey; border: 1px solid red")
                self.grid_layout.addWidget(widget, row, col)
                self.grid_widgets[row][col] = widget


        # Crear un widget contenedor para el layout de cuadrícula
        desktop_widget = QWidget()
        desktop_widget.setLayout(self.grid_layout)

        # Establecer el widget contenedor como el widget central de la ventana
        self.setCentralWidget(desktop_widget)

        # Descomentar el codigo siguiente para saber los limites de los objetos del escritorio
        #desktop_widget.setStyleSheet("border: 2px solid yellow;")

        # Conectar el clic derecho para abrir el menú contextual
        desktop_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        desktop_widget.customContextMenuRequested.connect(lambda pos: self.show_context_menu(pos=pos, option2=True, instance=desktop))

        # Barra de tarea - Taskbar - Task Bar
        self.create_bottom_toolbar()

        # Agregar acciones (botones) a la barra de herramientas (La estoy utilizando como barra de tareas)
        self.add_app_action(app_name="Win", icon_path="./img/icons/window.png")

        # Conecta el evento de movimiento
        self.moveEvent = self.on_move_event  

        # Menú de inicio - Startbar - Start Bar
        self.start_menu = StartMenu(self)

        self.show_created_folders()

        # Contador para mostrar u ocultar las apps en el toolbar
        self.show_counter = 1

    def closeEvent(self, event):
        # Cerrar todas las ventanas secundarias cuando se cierra la ventana principal
        open_windows = self.return_open_windows()
        
        if open_windows is not None:
            for i in open_windows:
                i.instance.close()
        else:
            print('La lista {open_windows} esta vacía.')

    # Función para crear Barra de tarea (Taskbar - Task Bar) en el área de abajo
    def create_bottom_toolbar(self):
        # Crear una barra de herramientas
        self.toolbar = QToolBar()

        # Mostrar texto debajo de los iconos
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  
        
        # Colocar la barra de herramientas en la parte inferior
        self.addToolBar(Qt.BottomToolBarArea, self.toolbar)  
        
        # Desactivar el menú contextual de la barra de herramientas
        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)

    def count_folders(self, directory):
        # Obtener la lista de archivos y directorios en el directorio dado
        files_and_folders = os.listdir(directory)

        # Inicializar el contador de folders
        folder_count = 0

        # Iterar sobre cada elemento en la lista
        for item in files_and_folders:
            # Comprobar si el elemento es un directorio
            if os.path.isdir(os.path.join(directory, item)):
                folder_count += 1

        return folder_count

    def show_created_folders(self):
        folder_path = './folder'
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            folder_names = os.listdir(folder_path)

            row = 0
            col = 0

            for folder_name in folder_names:
                if row // self.num_rows == 1:
                    row = 0 
                    col += 1

                folder_full_path = folder_path + '/' + folder_name
                if os.path.isdir(folder_full_path):
                    folder_app = Folder(folder_full_path, folder_name)
                    folder_icon = DesktopIcon(folder_app)
                    self.place_icon_on_desktop(folder_icon, row, col)
                    row += 1
    
    # Creacion de carpetas (folders)  
    def create_new_folder(self):
        folder_name, ok = QInputDialog.getText(self, "Create New Folder", "Enter folder name:")
        if ok and folder_name:
            folder_path = './folder'
            
            # Verificar si el directorio existe
            if not os.path.exists(folder_path):
                try:
                    # Intentar crear el directorio
                    os.makedirs(folder_path)
                except OSError as e:
                    # Capturar errores al intentar crear el directorio
                    print(f"No se pudo crear el directorio '{folder_path}': {e}")


            self.folder = Folder(folder_path + '/' + folder_name, folder_name)

            if folder_path:
                try:
                    # Crear la carpeta en la ubicación seleccionada y añadirla visualmente al programa
                    os.mkdir(folder_path + '/' + folder_name)
                    QMessageBox.information(self, "Success", f"Folder '{folder_name}' created successfully.")

                    #
                    self.icon = DesktopIcon(self.folder)

                    self.grid_found = False
                    for col in range(self.num_cols):
                        for row in range(self.num_rows):
                            if self.grid_widgets[row][col] is not None:
                                MainWindow.place_icon_on_desktop(self, self.icon, row, col)
                                self.grid_found = True
                                break  # Salir del bucle interno
                        else:
                            continue  # Este else se ejecuta si el bucle interno no se interrumpe con break
                        
                        if self.grid_found:
                                break  # Salir del bucle externo si se encontro la celda para ingresar el icono
                    #
                    
                except OSError as e:
                    QMessageBox.critical(self, "Error", f"Failed to create folder: {e}")

    def rename_file(self, file, file_path):
        self.file = file

        if file_path:
            # Obtener el nombre del archivo actual
            file_name = os.path.basename(file_path)
            
            # Solicitar al usuario un nuevo nombre para el archivo
            new_name, ok = QInputDialog.getText(self, "Rename File", "Enter new file name:", text=file_name)
            if ok and new_name:
                # Obtener la ruta del directorio del archivo
                file_dir = os.path.dirname(file_path)
                
                # Construir la nueva ruta completa del archivo
                new_path = file_dir + '/' + new_name
                
                try:
                    # Renombrar el archivo
                    os.rename(file_path, new_path)

                    # Guardando el nuevo nombre del archivo
                    if self.file.name == 'Folder':
                        self.file.alias = new_name
                    else:
                        self.file.name = new_name

                    # Guardando el nuevo directorio
                    self.file.file_path = new_path

                    QMessageBox.information(self, "Success", f"File '{file_name}' renamed to '{new_name}' successfully.")
                except OSError as e:
                    QMessageBox.critical(self, "Error", f"Failed to rename file: {e}")

    # Coloca iconos en el escritorio
    def place_icon_on_desktop(self, icon, row, col):
        self.icon = icon

        # Recorre la matriz de widgets para encontrar un espacio vacío
        if self.grid_widgets[self.num_rows - 1][self.num_cols - 1] is not None:                
            # Elimina el espacio en blanco (None)
            self.grid_layout.removeWidget(self.grid_widgets[row][col])
            
            # Agrega el icono y actualizar la matriz de widgets
            self.grid_layout.addWidget(self.icon, row, col)
            self.grid_widgets[row][col] = self.icon
            return True
        
        else:
            # Si no se encuentra ningún espacio vacío
            print("No hay espacio disponible para ejecutar la acción.")
            return False

    # Devuelve la lista de apps abiertas
    def return_open_windows(self):
        return self.open_windows
        
    def show_context_menu(self, pos, option1=False, option2=False, option3=False, win=False, instance=None, parent=None):
        # Crea instancia del menú contextual
        menu = ContextMenu(element=self, option1=option1, option2=option2, option3=option3, win=win, instance=instance, parent=parent)

        # Muestra el menú en la posición del clic derecho
        if self.toolbar.rect().contains(self.toolbar.mapFromGlobal(pos)) or win == True:
            # El click se realizó en el QToolBar
            toolbar_pos = self.toolbar.mapToGlobal(pos) # Guarda la posición del boton que se clickeo en el QToolBar
            menu.exec_(toolbar_pos)

        else:
            # El click se realizó fuera del QToolBar
            menu.exec_(self.mapToGlobal(pos))
      
    def set_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.background_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding))
        self.background_label.setGeometry(0, 0, self.width(), self.height())  # Ajustar tamaño de la etiqueta al de la ventana
    
    def resizeEvent(self, event):
        # Redimensionar la imagen de fondo cuando se redimensiona la ventana
        self.set_background_image("./img/background_edited.png")

    def add_app_action(self, app_name, icon_path, app_instance=None):
        # Verificar si la acción ya existe en el toolbar
        for button in self.toolbar.findChildren(QPushButton):
            if button.text == app_name:
                # La acción ya existe, no se agrega de nuevo
                return

        # Si la acción no existe, se agrega al toolbar
            
        # Crea el botón y establece su tamaño máximo y minimo
        width = 30
        height = 30
        button = QPushButton(self)
        button.setMinimumSize(width, height) 
        button.setMaximumSize(width, height) 


        # Crea un icono y establecer su tamaño
        icon = QIcon(icon_path)
        icon_size = button.size()
        icon.addPixmap(QPixmap(icon.pixmap(icon_size)))
        
        # Establece el icono y su tamaño para el botón
        button.setIcon(icon)
        button.setIconSize(icon_size)

        # Establece el ToolTip (el texto que aparece si el cursor esta sobre el botón)
        button.setToolTip(app_name)
        
        # Establece un texto al botón, el cual se emplea para mostrar el context menu
        button.text = app_name

        # Establece un id al botón para poder seleccionarlo en css
        button.setObjectName("ButtonToolbar")

        # Permite que el botón tenga un context menu
        button.setContextMenuPolicy(Qt.CustomContextMenu)

        # Añade el boton al toolbar
        self.toolbar.addWidget(button)
        
        # Hoja de estilo CSS
        with open("style.css", "r") as f:
            self.setStyleSheet(f.read())
        

        # Crea un menu contextual, para las action (button) del toolbar
        if button.text == 'Win':
            button.customContextMenuRequested.connect(lambda pos: self.show_context_menu(pos=pos, win=True, instance=desktop))
        else:
            # EN ESTA PARTE SE QUIERE EMPLEAR UN CONTEXT MENU QUE PERMITA ABRIR, FIJAR, O CERRAR LA APP (EN CASO DE QUE ESTE FIJADA Y CERRADA SOLO DEBERIA SALIR LAS OPCIONES DE ABRIR Y DESFIJAR)
            #button.customContextMenuRequested.connect(lambda pos: self.show_context_menu(pos=pos, win=True, instance=desktop))
            pass

        if app_instance is None:
            button.clicked.connect(lambda: self.open_application(app_name))
        else:
            button.clicked.connect(lambda: self.open_application(app_name, app_instance=app_instance))
            
    def remove_app_action(self, app_name):# icon_path, app_instance=None):
        for button in self.toolbar.findChildren(QPushButton):
            if button.text == app_name:
                # Si el button estan en el toolbar eliminalo
                button.deleteLater()
                return True
        else:
            print('No se encontro el objeto en la barra de tareas.')
            return False

    def open_application(self, app_name, app_instance=None):

        if app_name == 'Win':
            # Contador para alternar la visibilidad
            self.start_menu.toggle_dialog()
        
        if app_instance:
            self.toggle_app(app_instance=app_instance)
    
    def toggle_app(self, app_instance):
        # Incrementar el contador cada vez que se presiona el botón
        self.show_counter += 1

        # Si el contador es par, mostrar el QDialog; si es impar, ocultarlo
        if self.show_counter % 2 == 0:
            app_instance.instance.hide()
        else:
            app_instance.instance.show()

    def on_move_event(self, event):
        # Captura el evento de movimiento de la ventana del sistema operativo
        super().moveEvent(event)

        # Mueve todas las ventanas secundarias junto con la ventana del sistema operativo
        for widget in self.findChildren(QDialog):
            widget.move(event.pos() + widget.pos() - event.oldPos())

        for widget in self.findChildren(QMainWindow):
            widget.move(event.pos() + widget.pos() - event.oldPos())


class StartMenu(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main = main_window
        
        # Centro el menu de inicio - start menu
        x= 857
        y= 335
        self.move(x, y)

        # Desactiva la barra de titulo(minimizar, maximizar, cerrar ventana)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint) 


        # Inicialmente, el QDialog está oculto
        self.hide()

        # Crear capa inferior con botones e iconos
        bottom_layer = QWidget()
        bottom_layout = QVBoxLayout(bottom_layer)
        self.add_buttons(bottom_layout)

        # Crear capa media con scroll
        middle_layer = QWidget()
        middle_layout = QVBoxLayout(middle_layer)
        self.add_content(middle_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(middle_layer)

        # Crear capa superior con imagen y etiqueta
        top_layer = QWidget()
        top_layout = QHBoxLayout(top_layer)
        self.add_user_info(top_layout)

        # Colocar las capas en la ventana principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(top_layer)
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(bottom_layer)
        self.setLayout(main_layout)
        
        self.show_counter = 1
        
  

        
    def toggle_dialog(self):
        # Incrementar el contador cada vez que se presiona el botón
        self.show_counter += 1

        # Si el contador es par, mostrar el QDialog; si es impar, ocultarlo
        if self.show_counter % 2 == 0:
            self.show()
        else:
            self.hide()


    def add_buttons(self, layout):
        button_icons = [
            ("Icon path for Sign out", "Sign out"),
            ("Icon path for Shut down", "Shut down"), 
            ("Icon path for Restart", "Restart")
        ]
        
        for icon_path, text in button_icons:
            button = ButtonStartMenu(text)
            # Descomentar el siguiente codigo para colocarles iconos a los botones, asegurate de colocar la rutas corespondientes en la lista de tuplas
            #button.setIcon(QIcon(icon_path))
            #button.setIconSize(button.sizeHint())  # Ajustar el tamaño del icono al del botón
            
            # Agrega el boton al menu de inicio
            layout.addWidget(button)

            # Conectar la señal clicked del botón a una función
            button.clicked.connect(lambda checked, action=text: self.power(action))

            # Hoja de estilo CSS
            with open("style.css", "r") as f:
                self.setStyleSheet(f.read())

    def power(self, action):

        if action == 'Shut down':
            print('Shutting down...')

        elif action == 'Restart':
            print('Restaring...')
        
        elif action == 'Sign out':
            print('Signing out...')


    def add_content(self, layout):
        # Creación de las instacias para ejecutar las apps
        
        # Instanciar el bloc de notas - Notepad
        self.notepad = notepad.Notepad(parent=self.main)
        
        # Instanciar el administrador de tareas - Task manager
        self.taskmanager = taskmanager.TaskManager(parent=self.main)


        # Lista de aplicaciones     
        self.apps = [
            App("Notepad", "./img/icons/notepad.png", self.notepad),
            App("Web Nav.", "./img/icons/chrome.png", "web.exe"),
            App("Task Manager", "./img/icons/taskmanager.png", self.taskmanager)
        ]

        for i, name in enumerate(self.apps):
            self.app = self.apps[i]
            self.button = QPushButton(self.app.name)
            layout.addWidget(self.button)
            self.button.setObjectName("AppStartMenu")
            self.button.clicked.connect(lambda _, app=self.app: self.open_application(app))        
            
    def open_application(self, app):
        print('Abrir app:', app.name)
        
        if app.name == 'Task Manager':
            pass

        if app.name == 'Notepad':
            self.taskmanager.run_process_thread(app=app)    


    def add_user_info(self, layout):
        self.users =[
            NewUser('Luis Mario Bonilla Madera', 'LuisMBonilla', 'pass', './img/icons/user.png'),
            NewUser('Luis Bonilla', 'Admin', 'pass', './img/icons/user.png'),
        ]

        index = 0
        user = self.users[index]

        # Configurando y colocando la informacion del usuario en la parte superior del menu de inicio
        user_image_label = QLabel()
        user_image_label.setPixmap(QPixmap(user.image))
        layout.addWidget(user_image_label)

        user_name_label = QLabel(user.name)
        layout.addWidget(user_name_label)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    desktop = MainWindow()
    desktop.show()

    sys.exit(app.exec_())