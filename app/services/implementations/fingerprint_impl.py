from app.hardware.fingerprint_sensor import FingerprintSensor

class FingerprintImpl:
    def __init__(self):
        self.fingerprintSensor = FingerprintSensor()

    def capture_fingerprint(self) -> bool:
        self.fingerprintSensor.capture_image()
        return self.fingerprintSensor.check_duplicate() == -1
    def match_and_store(self):
        self.fingerprintSensor.wait_second_finger()
        try:
            return self.fingerprintSensor.match_and_store()
        except Exception as e:
            print(f"Error storing fingerprint: {e}")
            return None
