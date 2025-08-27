from zk import ZK

class Zkteco:
    def __init__(self, ip, port=4370):
        self.ip = ip
        self.port = port
        self.conn = None

    def connect(self):
        zk = ZK(self.ip, port=self.port, timeout=5)
        try:
            self.conn = zk.connect()
            return True, "Dispositivo conectado correctamente ✅"
        except Exception as e:
            return False, f"Error al conectar: {e}"

    def disconnect(self):
        if self.conn:
            self.conn.disconnect()
            self.conn = None
            return True, "Dispositivo desconectado 🔌"
        return False, "No hay conexión activa"
    
    def get_status(self):
        if not self.conn:
            return False, "No hay conexión activa"
        try:
            status = {
                "firmware_version": self.conn.get_firmware_version(),
                "serial_number": self.conn.get_serialnumber(),
                "device_name": self.conn.get_device_name() if hasattr(self.conn, "get_device_name") else "ZKTeco",
            }
            return True, status
        except Exception as e:
            return False, f"Error al obtener estado: {e}"

    def get_users(self):
        if not self.conn:
            return False, "No hay conexión activa"
        try:
            users = self.conn.get_users()
            return True, users
        except Exception as e:
            return False, f"Error al obtener usuarios: {e}"
        
    def get_attendance(self):
        if not self.conn:
            return False, "No hay conexión activa"
        try:
            logs = self.conn.get_attendance()
            return True, logs
        except Exception as e:
            return False, f"Error al obtener asistencias: {e}"
