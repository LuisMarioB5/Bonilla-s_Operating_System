from PyQt5.QtWidgets import QToolBar, QScrollArea, QDialog, QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QAction, QMenu, QInputDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
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
    def __init__(self, app=None, option1 = False, option2 = False, option3 = False, option4 = False, instance = None, parent=None):
        super().__init__(parent)

        self.app = app
        self.instance = instance
        
        if option1 == True:

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
        
        if option2 == True:
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

        if option3 == True and app.name == 'Win':
            # Agrega acciones al menú contextual
            restart = QAction("Restart", self)
            shutdown = QAction("Shutdown", self)
            desktop = QAction("Desktop", self)

            # Conecta las acciones a sus respectivos métodos
            restart.triggered.connect(self.on_restart_triggered)
            shutdown.triggered.connect(self.on_shutdown_triggered)
            desktop.triggered.connect(self.on_desktop_triggered)  
            
            # Agrega las acciones al menú
            self.addAction(restart)
            self.addAction(shutdown)
            self.addAction(desktop)

        if option4 == True:

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
            
    # Define los métodos que se ejecutarán cuando se seleccione una acción
    def on_open_triggered(self):
        print("OpenOption selected for:", self.app.name)

    def on_rename_triggered(self):
        print("RenameOption selected for:", self.app.name)
        print("RenameOption selected for:", self.app.icon_path)
        print("RenameOption selected for:", self.app.file_path)
        print("RenameOption selected for:", self.app.alias)
        print("RenameOption selected for:", self.app.get_file_path())
        MainWindow.rename_file(self.instance, self.app.get_file_path())

    def on_delete_triggered(self):
        print("DeleteOption selected for:", self.app.name)

    def on_restart_triggered(self):
        print("RestartOption selected for:", self.app.name)

    def on_shutdown_triggered(self):
        print("ShutdownOption selected for:", self.app.name)
    
    def on_desktop_triggered(self):
        print("SendtoDesktopOption selected for: Startmenu")
    
    def on_taskbar_triggered(self):
        print("SendtoTaskbarOption selected for: Startmenu")
    
    def on_folder_triggered(self):
        print("NewFolderOption selected for: Desktop")
        MainWindow.create_new_folder(self.instance)
    
    def on_notepad_triggered(self):
        print("NewNotepadOption selected for: Desktop")

class App:
    def __init__(self, name, icon_path, file_path = None, alias = None):
        self.alias = alias
        self.name = name
        self.icon_path = icon_path
        self.file_path = file_path

    def get_file_path(self):
        self.complete_file_path = self.file_path + '/' + self.alias
        return self.complete_file_path

        
        

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
        if app.name == 'Folder':
            self.label_text = QLabel(app.alias)
        else:
            self.label_text = QLabel(app.name)
            
        
        self.label_text.setStyleSheet("font-family: Segoe UI; font-size: 14px; color: white;")
        layout.addWidget(self.label_text, alignment=Qt.AlignCenter)

        # Establecer el tooltip con el nombre de la aplicación
        self.label_icon.setToolTip(app.name)

        # Conectar el doble clic para abrir la aplicación
        self.label_icon.mouseDoubleClickEvent = self.open_application
        self.label_text.mouseDoubleClickEvent = self.open_application

        # Conectar el clic derecho para abrir el menú contextual
        self.label_icon.setContextMenuPolicy(Qt.CustomContextMenu)
        self.label_icon.customContextMenuRequested.connect(self.show_menu)
        self.label_text.setContextMenuPolicy(Qt.CustomContextMenu)
        self.label_text.customContextMenuRequested.connect(self.show_menu)


        self.setLayout(layout)

    def open_application(self, event):
        print(f"Abrir aplicación: {self.app.name}")
        # Aquí podrías ejecutar la aplicación utilizando el atributo 'self.app.file_path'

    def show_menu(self, pos):
        # Crear instancia del menú contextual
        menu = ContextMenu(self.app, True, False, False, False)

        # Mostrar el menú en la posición del clic derecho
        menu.exec_(self.mapToGlobal(pos))

# Termine eliminando el statusbar por lo que esto no sirve ahora
"""class TaskbarIcon(QPushButton):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.icon = QIcon(app.icon_path)
        self.setIcon(self.icon)
        self.setToolTip(app.name)
        self.clicked.connect(self.open_application)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)

    def open_application(self):
        print(f"Abrir aplicación: {self.app.name}")
        # Aquí podrías ejecutar la aplicación utilizando el atributo 'self.app.executable'

    def show_menu(self, pos):
        # Crear instancia del menú contextual
        menu = ContextMenu(self.app, False, False, True, False)

        # Mostrar el menú en la posición del clic derecho
        menu.exec_(self.mapToGlobal(pos))"""

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
        
        
        # Como tengo el escritorio sin archivos lo desactive para que no se ponan las apps predeterminadamente en el escritorio
        """
        for col in range(num_cols):
            for row in range(num_rows):

                i = col * num_rows + row  # Calcula el índice correspondiente en la lista 'apps'
                
                # Se cuentan los elementos de la lista apps en una variable numerica
                count = 0
                for i2 in enumerate(self.apps):
                    count += 1


                if i <= count - 1:
                    app = self.apps[i]  # Accede al elemento de la lista 'apps' utilizando el índice
                    icon = DesktopIcon(app)
                    grid_layout.removeWidget(grid_widgets[row][col])  # Elimina el widget vacío
                    grid_layout.addWidget(icon, row, col)  # Agrega el nuevo widget
                    grid_widgets[row][col] = icon  # Actualiza la matriz de widgets"
        """

        # Crear un widget contenedor para el layout de cuadrícula
        desktop_widget = QWidget()
        desktop_widget.setLayout(self.grid_layout)

        # Establecer el widget contenedor como el widget central de la ventana
        self.setCentralWidget(desktop_widget)

        #desktop_widget.setStyleSheet("border: 2px solid yellow;")

        # Conectar el clic derecho para abrir el menú contextual
        desktop_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        desktop_widget.customContextMenuRequested.connect(self.show_menu)     


        
        
        
        

        # Barra de tarea - Taskbar - Task Bar
        # Crear una barra de herramientas
        self.toolbar = QToolBar()
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # Mostrar texto debajo de los iconos
        self.addToolBar(Qt.BottomToolBarArea, self.toolbar)  # Colocar la barra de herramientas en la parte inferior
        # Desactivar el menú contextual de la barra de herramientas
        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)

        # Agregar acciones (botones) a la barra de herramientas (La estoy utilizando como barra de tareas)
        self.add_app_action("Win", "./img/icons/window.png")


        # Menú de inicio - Startbar - Start Bar
        self.start_menu = StartMenu()
        self.start_menu.hide()

        self.show_created_folders()

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


                folder_icon_path = './img/icons/folder.png'  # Ruta del ícono de la carpeta
                folder_full_path = folder_path + '/' + folder_name
                if os.path.isdir(folder_full_path):
                    folder_app = App('Folder', folder_icon_path, folder_full_path, folder_name)
                    folder_icon = DesktopIcon(folder_app)
                    self.place_icon_on_desktop(folder_icon, row, col)
                    row += 1
                    print('cantidad de folders:', self.count_folders(folder_path))
                    print('valor de col:', col)

    
    # Creacion de carpetas (folders)  
    def create_new_folder(self):
        folder_name, ok = QInputDialog.getText(self, "Create New Folder", "Enter folder name:")
        if ok and folder_name:
            # Pedir al usuario que seleccione la ubicación de la carpeta
            folder_path = './folder'
            icon_path = './img/icons/folder.png'
            

            self.folder = App('Folder', icon_path, folder_path, folder_name)

            if folder_path:
                # Crear la carpeta en la ubicación seleccionada y añadirla visualmente al programa
                folder_path = folder_path + '/' + folder_name
                try:
                    self.icon = DesktopIcon(self.folder)
                    MainWindow.place_icon_on_desktop(self, self.icon)
                    os.mkdir(folder_path)
                    QMessageBox.information(self, "Success", f"Folder '{folder_name}' created successfully.")
                except OSError as e:
                    QMessageBox.critical(self, "Error", f"Failed to create folder: {e}")


    def rename_file(self, file_path):
        # Obtener la ruta del archivo seleccionado en el escritorio

        if file_path:
            # Obtener el nombre del archivo actual
            file_name = os.path.basename(file_path)
            # Solicitar al usuario un nuevo nombre para el archivo
            new_name, ok = QInputDialog.getText(self, "Rename File", "Enter new file name:", text=file_name)
            if ok and new_name:
                # Obtener la ruta del directorio del archivo
                file_dir = os.path.dirname(file_path)
                # Construir la nueva ruta completa del archivo
                new_path = os.path.join(file_dir, new_name)
                try:
                    # Renombrar el archivo
                    os.rename(file_path, new_path)
                    QMessageBox.information(self, "Success", f"File '{file_name}' renamed to '{new_name}' successfully.")
                except OSError as e:
                    QMessageBox.critical(self, "Error", f"Failed to rename file: {e}")


    def place_icon_on_desktop(self, icon, row, col):

        self.icon = icon
        # Recorrer la matriz de widgets para encontrar un espacio vacío

        print(row, col)
        print(self.num_rows, self.num_cols)
        # Elimina el espacio en blanco (None)
        self.grid_layout.removeWidget(self.grid_widgets[row][col])
        # Agregar el icono y actualizar la matriz de widgets
        self.grid_layout.addWidget(self.icon, row, col)
        self.grid_widgets[row][col] = self.icon
            
        return
                
        # Si no se encuentra ningún espacio vacío
        self.show_message_to_user("No hay espacio disponible para ejecutar la acción.")
        return False
    
        

                


                    







    def show_message_to_user(self, message):
        # Mostrar un mensaje al usuario usando QMessageBox
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Mensaje")
        msg_box.setText(message)
        msg_box.exec_()













        
        
    def show_menu(self, pos):
        # Crear instancia del menú contextual
        menu = ContextMenu(None, False, True, False, False, desktop)

        # Mostrar el menú en la posición del clic derecho
        menu.exec_(self.mapToGlobal(pos))
           
    def set_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.background_label.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding))
        self.background_label.setGeometry(0, 0, self.width(), self.height())  # Ajustar tamaño de la etiqueta al de la ventana
    
    def resizeEvent(self, event):
        # Redimensionar la imagen de fondo cuando se redimensiona la ventana
        self.set_background_image("./img/background_edited.png")

    def add_app_action(self, app_name, icon_path):
        action = QAction(self)
        action.setIcon(QIcon(icon_path))
        action.triggered.connect(lambda: self.open_application(app_name))
        self.toolbar.addAction(action)

    def open_application(self, app_name):
        if app_name == 'Win':
            # Contador para alternar la visibilidad
            self.start_menu.toggle_dialog()










class StartMenu(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint) # Desactiva la barra de titulo(minimizar, maximizar, cerrar ventana)


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
            ("./img/icons/notepad.png", "Shut down"), 
            ("./img/icons/notepad.png", "Restart"), 
            ("./img/icons/notepad.png", "Sign off")
        ]
        
        for icon_path, text in button_icons:
            button = ButtonStartMenu(text)
            #button.setIcon(QIcon(icon_path))
            #button.setIconSize(button.sizeHint())  # Ajustar el tamaño del icono al del botón
            layout.addWidget(button)
            # Hoja de estilo CSS
            with open("start_menu.css", "r") as f:
                self.setStyleSheet(f.read())

    def add_content(self, layout):
        # Lista de aplicaciones
        self.apps = [
            App("Notepad", "./img/icons/notepad.png", "notepad.exe"),
            App("Web Nav.", "./img/icons/chrome.png", "web.exe"),
            App("Task Manager", "./img/icons/taskmanager.png", "taskmanager.exe")
        ]

        for i, name in enumerate(self.apps):
            app = self.apps[i]
            button = QPushButton(app.name)
            layout.addWidget(button)
            button.setObjectName("AppStartMenu")


    def add_user_info(self, layout):
        self.users =[
            NewUser('Luis Mario Bonilla Madera', 'LuisMBonilla', 'pass', './img/icons/user.png'),
            NewUser('Luis Bonilla', 'Admin', 'pass', './img/icons/user.png'),
        ]

        index = 0
        user = self.users[index]

        user_image_label = QLabel()
        user_image_label.setPixmap(QPixmap(user.image))  # Reemplaza "UserImage.png" con la ruta de la imagen del usuario
        layout.addWidget(user_image_label)

        user_name_label = QLabel(user.name)
        layout.addWidget(user_name_label)
   























if __name__ == "__main__":
    app = QApplication(sys.argv)
    desktop = MainWindow()
    desktop.show()
    sys.exit(app.exec_())
