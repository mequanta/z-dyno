from qdb.server import QdbClientServer

class DynoQdbClientServer(QdbClientServer):
    def __init__(self, session_store):
        super(DynoQdbClientServer, self).init(session_store)
        self._server = None

    def address(self):
        raise NotImplementedError()

    def server_port(self):
        raise NotImplementedError()

    def start(self, *args, **kwargs):
        raise NotImplementedError()

    def stop(self, *args, **kwargs):
        raise NotImplementedError()