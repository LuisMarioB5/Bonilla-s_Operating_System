from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication
import threading
import sys
import os

class Process:
    def __init__(self, name, tid, cpu=None, memory=None):
        self.pid = os.getpid()
        self.tid = tid
        self.name = name
        self.cpu = cpu
        self.memory = memory


class Worker(QObject):
    # Señal para indicar que la aplicación está lista para ser mostrada
    app_ready = pyqtSignal(object)

    def run(self, app):
        # Emitir la señal para indicar que la aplicación está lista
        self.app_ready.emit(app)


class TaskManager(QMainWindow):
    
    def __init__(self, parent = None):
        super().__init__(parent)
        self.main = parent
        #self.active_process = []

    @pyqtSlot(object)
    def open_application(self, app):

        # Agregar a la lista de ventanas abiertas
        self.main.open_windows.append(app)

        # Añadir al tool bar e iniciar el metodo show
        self.main.add_app_action(app_name=app.name, icon_path=app.icon_path, app_instance=app)
        
        # Mostrar la interfaz de usuario desde el hilo principal
        app.instance.show()

        print('Aplicación abierta desde el administrador de tareas')            

    def close_aplication(self, app):
        new_process = []

        for process in self.active_process:
            if process.name != app.name:
                new_process.append(process)
            else:
                app.instance.close()

        self.active_process = new_process
        # Deberia cerrar la app

    def run_process_thread(self, app):
        
        # Creamos y configuramos un objeto Worker
        worker = Worker()

        # Conectar la señal app_ready al método open_application
        worker.app_ready.connect(self.open_application)

        # Creamos y configuramos un objeto Thread 
        process_thread = threading.Thread(target=worker.run, args=(app,))

        # Iniciamos el hilo
        process_thread.start()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    task_manager = TaskManager()
    #task_manager.show()
    sys.exit(app.exec_())
