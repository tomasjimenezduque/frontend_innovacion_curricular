class IApiService:
    def listar(self, *args, **kwargs):
        raise NotImplementedError

    def obtener(self, *args, **kwargs):
        raise NotImplementedError

    def crear(self, *args, **kwargs):
        raise NotImplementedError

    def actualizar(self, *args, **kwargs):
        raise NotImplementedError

    def eliminar(self, *args, **kwargs):
        raise NotImplementedError
