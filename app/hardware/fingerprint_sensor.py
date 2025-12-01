from pyfingerprint.pyfingerprint import PyFingerprint
from app.core.exceptions.fingerprint_exceptions import SensorStorageException
import time
from pyfingerprint.pyfingerprint import PyFingerprint
from app.core.exceptions.fingerprint_exceptions import SensorStorageException
import time

class FingerprintSensor():

    """
    Clase que encapsula la lógica del sensor de huellas AS608 usando la librería pyfingerprint.
    Ofrece métodos para capturar, verificar, registrar y limpiar datos de huellas dactilares.
class FingerprintSensor():

    """

    def __init__(self):
        """
        Inicializa la conexión con el sensor y define los buffers de trabajo.
        """
        self.sensor = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)
        if not self.sensor.verifyPassword():
            raise SensorStorageException("Sensor no responde con el password esperado")
        self.buffer1 = 0x01
        self.buffer2 = 0x02
        """
        Inicializa la conexión con el sensor y define los buffers de trabajo.
        """
        self.sensor = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)
        if not self.sensor.verifyPassword():
            raise SensorStorageException("Sensor no responde con el password esperado")
        self.buffer1 = 0x01
        self.buffer2 = 0x02

    def capture_image(self):
        """
        Espera a que se coloque un dedo en el sensor, captura la imagen y la convierte en buffer1.
        """
        while not self.sensor.readImage():
            pass
        self.sensor.convertImage(self.buffer1)
        """
        Espera a que se coloque un dedo en el sensor, captura la imagen y la convierte en buffer1.
        """
        while not self.sensor.readImage():
            pass
        self.sensor.convertImage(self.buffer1)

    def check_duplicate(self):
        """
        Verifica si la huella ya está registrada en el sensor.
        
        Returns:
            int: Posición de la huella si ya existe; -1 si no hay coincidencias.
        """
        position, _ = self.sensor.searchTemplate()
        if position >= 0:
            self.clear_buffer(self.buffer1)
        return position # -1 si no existe
        """
        Verifica si la huella ya está registrada en el sensor.
        
        Returns:
            int: Posición de la huella si ya existe; -1 si no hay coincidencias.
        """
        position, _ = self.sensor.searchTemplate()
        if position >= 0:
            self.clear_buffer(self.buffer1)
        return position # -1 si no existe

    def wait_second_finger(self):
        """
        Solicita que el usuario retire y vuelva a colocar el dedo.
        Captura una segunda imagen y la convierte en buffer2.
        """
        self.clear_buffer(self.buffer2)
        while not self.sensor.readImage():
            pass
        self.sensor.convertImage(0x02)
        """
        Solicita que el usuario retire y vuelva a colocar el dedo.
        Captura una segunda imagen y la convierte en buffer2.
        """
        self.clear_buffer(self.buffer2)
        while not self.sensor.readImage():
            pass
        self.sensor.convertImage(0x02)

    def match_and_store(self):
        """
        Compara los datos en buffer1 y buffer2. Si coinciden, crea y almacena la plantilla.
        
        Returns:
            int | None: Posición donde fue almacenada la huella si todo fue exitoso, None si no hubo coincidencia.
        
        Side effects:
            Limpia los buffers si no hay coincidencia.
        """
        if self.sensor.compareCharacteristics() == 0:
            self.clear_buffer(self.buffer1)
            self.clear_buffer(self.buffer2)
            return None
        self.sensor.createTemplate()
        try:
            position = self.sensor.storeTemplate()
        except Exception as e:
            raise SensorStorageException("No se pudo almacenar la huella: " + str(e))
        return position
    
        """
        Compara los datos en buffer1 y buffer2. Si coinciden, crea y almacena la plantilla.
        
        Returns:
            int | None: Posición donde fue almacenada la huella si todo fue exitoso, None si no hubo coincidencia.
        
        Side effects:
            Limpia los buffers si no hay coincidencia.
        """
        if self.sensor.compareCharacteristics() == 0:
            self.clear_buffer(self.buffer1)
            self.clear_buffer(self.buffer2)
            return None
        self.sensor.createTemplate()
        try:
            position = self.sensor.storeTemplate()
        except Exception as e:
            raise SensorStorageException("No se pudo almacenar la huella: " + str(e))
        return position
    
    def clear_buffer(self, buffer_id):
        """
        Limpia manualmente un buffer del sensor cargando datos vacíos.
        
        Args:
            buffer_id (int): Identificador del buffer a limpiar (0x01 o 0x02).
        """
        empty_characteristics = [0] * 512 
        self.sensor.uploadCharacteristics(buffer_id, empty_characteristics)
        """
        Limpia manualmente un buffer del sensor cargando datos vacíos.
        
        Args:
            buffer_id (int): Identificador del buffer a limpiar (0x01 o 0x02).
        """
        empty_characteristics = [0] * 512 
        self.sensor.uploadCharacteristics(buffer_id, empty_characteristics)

    def check_fingerprint(self):
        """
        Captura una imagen y busca si la huella existe en la base del sensor.
        
        Returns:
            int: Posición donde se encuentra la huella o -1 si no está registrada.
        """
        self.capture_image()
        pos = self.sensor.searchTemplate()[0]
        self.clear_buffer(self.buffer1)
        return pos