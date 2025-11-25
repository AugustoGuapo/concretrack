# app/hardware/fingerprint_sensor.py

class FingerprintSensor:
    """
    Versión neutra para desarrollo visual.
    No accede a hardware. Todos los métodos son no-op o devuelven valores seguros.
    """

    def __init__(self):
        pass

    def capture_image(self):
        pass

    def check_duplicate(self):
        return -1  # No duplicado

    def wait_second_finger(self):
        pass

    def match_and_store(self):
        return None  # No almacena

    def clear_buffer(self, buffer_id):
        pass

    def check_fingerprint(self):
        return -1  # Huella no encontrada