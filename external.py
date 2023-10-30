import configparser
import redis

# singleton design pattern for read only configuration data


class External():

    __instance = None

    def __init__(self):
        if External.__instance != None:
            raise Exception("App singleton exists!")
        else:
            External.__instance = self

            config = configparser.ConfigParser()
            config.read("config.cfg")

            self.dbconn = redis.Redis(
                host=config["Database"]["host"],
                port=config["Database"]["port"],
                password=config["Database"]["password"],
                decode_responses=True
            )

            self.api_key = config["API_KEY"]["api_key"]
