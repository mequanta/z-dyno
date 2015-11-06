from qdb.server import QdbClientServer

class DynoQdbClientServer(QdbClientServer):
    def __init__(self):
        super(DynoQdbClientServer, self).__init__(None)
        self._server = None

    def address(self):
        raise NotImplementedError()

    def server_port(self):
        raise NotImplementedError()

    def start(self, *args, **kwargs):
        raise NotImplementedError()

    def stop(self, *args, **kwargs):
        raise NotImplementedError()