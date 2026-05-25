import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ApiService:
    BASE_URL = "http://127.0.0.1:8000/api"

    def _construir_url(self, tabla, valor_id=None):
        recurso = tabla.strip('/')
        if valor_id:
            return f"{self.BASE_URL}/{recurso}/{str(valor_id).strip('/')}"
        return f"{self.BASE_URL}/{recurso}/"

    def listar(self, tabla, esquema=None, limite=None):
        url = self._construir_url(tabla)
        params = {k: v for k, v in {"limite": limite, "esquema": esquema}.items() if v}
        try:
            r = requests.get(url, params=params, timeout=5)
            if r.status_code == 204:
                return []
            r.raise_for_status()
            datos = r.json()
            return datos if isinstance(datos, list) else datos.get("datos", [])
        except Exception as e:
            logger.error(f"Error al listar {tabla}: {e}")
            return []

    def get(self, tabla, valor_id):
        if not valor_id:
            return None
        url = self._construir_url(tabla, valor_id)
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                return r.json()
            return None
        except Exception as e:
            logger.error(f"Error en GET {tabla}/{valor_id}: {e}")
            return None

    def crear(self, tabla, datos, esquema=None):
        url = self._construir_url(tabla)
        try:
            r = requests.post(url, json=datos, timeout=5)
            respuesta = r.json() if r.status_code in (200, 201) else {"mensaje": r.text}
            return r.status_code in (200, 201), respuesta.get("mensaje", "Registro creado.")
        except Exception as e:
            return False, f"Error de conexión: {str(e)}"

    def actualizar(self, tabla, clave_nombre, valor_id, datos, **kwargs):
        url = self._construir_url(tabla, valor_id)
        try:
            r = requests.put(url, json=datos, timeout=5)
            if r.status_code == 200:
                return True, r.json().get("mensaje", "Actualización exitosa.")
            msg = r.json().get("detail", "Error al actualizar") if r.status_code != 500 else "Error interno"
            return False, msg
        except Exception as e:
            return False, str(e)

    def eliminar(self, recurso, nombre_clave, valor_id):
        url = self._construir_url(recurso, valor_id)
        try:
            r = requests.delete(url, timeout=5)
            return r.status_code in (200, 204), "Eliminado correctamente."
        except Exception as e:
            return False, str(e)

    def eliminar_compuesto(self, tabla, id_1, id_2, esquema=None):
        url = f"{self.BASE_URL}/{tabla.strip('/')}/{id_1}/{id_2}"
        try:
            r = requests.delete(url, timeout=5)
            return r.status_code in (200, 204), "Vínculo eliminado."
        except Exception as e:
            return False, str(e)

    def actualizar_compuesto(self, tabla, id_1, id_2, datos, esquema=None):
        url = f"{self.BASE_URL}/{tabla.strip('/')}/{id_1}/{id_2}"
        try:
            r = requests.put(url, json=datos, timeout=5)
            return r.status_code == 200, r.json().get("mensaje", "Vínculo actualizado.")
        except Exception as e:
            return False, str(e)