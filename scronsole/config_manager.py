import json


class ServerConfig(object):
    def __init__(self, data=None):
        self.data = data or {}

    @property
    def host(self):
        return self.data.get("host", None)

    @host.setter
    def host(self, value):
        self.data["host"] = value

    @property
    def user(self):
        return self.data.get("user", "")

    @user.setter
    def user(self, value):
        self.data["user"] = value

    @property
    def password(self):
        return self.data.get("password", "")

    @password.setter
    def password(self, value):
        self.data["password"] = value

    @property
    def ptr(self):
        return self.data.get("ptr", False) is True

    @ptr.setter
    def ptr(self, value):
        self.data["ptr"] = value

    @property
    def secure(self):
        return self.data.get("secure", False)

    @secure.setter
    def secure(self, value):
        self.data["secure"] = value


class ConfigManager(object):
    def __init__(self):
        self.config = {}
        try:
            with open('scronsole.json') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.save()

    def get_servers(self):
        return [ServerConfig(s) for s in self.config.get("servers", [])]

    def add_server(self, server: ServerConfig):
        servers = self.config.get("servers", [])
        servers.append(server.data)
        self.config['servers'] = servers
        self.save()

    def save(self):
        with open('scronsole.json', "w") as f:
            json.dump(self.config, fp=f, indent=2)
