import socket


class OfflineRouter:
    """
    A database router that directs database operations to the 'offline' database
    when the application is running on a machine with hostname 'DESKTOP-12345'.
    """

    def db_for_read(self, model, **hints):
        return self.get_db()

    def db_for_write(self, model, **hints):
        return self.get_db()

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True

    def get_db(self):
        try:
            # Try connecting to MySQL (default database)
            socket.create_connection(("127.0.0.1", 3306), timeout=1)
            return 'online'
        except OSError:
            # If connection fails, use 'offline' database
            return 'default'
