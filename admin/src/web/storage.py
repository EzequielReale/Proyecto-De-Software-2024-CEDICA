from minio import Minio


class Storage:
    def __init__(self, app=None):
        self._client = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Inicializa la conexión con el servidor de almacenamiento y lo adjunta al contexto de la aplicación"""
        minio_server = app.config.get("MINIO_SERVER")
        minio_access_key = app.config.get("MINIO_ACCESS_KEY")
        minio_secret_key = app.config.get("MINIO_SECRET_KEY")
        minio_secure = app.config.get("MINIO_SECURE", True)

        self._client = Minio(
            minio_server,
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=minio_secure
        )

        app.storage = self

        return app

    @property
    def client(self):
        """Devuelve el cliente de MinIO"""
        return self._client
    
    @client.setter
    def client(self, client):
        """Establece el cliente de MinIO"""
        self._client = client


storage = Storage()