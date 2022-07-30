import configparser


class ConfigReader:
    def __init__(self):
        self.cfg_file = "./env.info.cfg"

    def get_value(self, section, option):
        cp = configparser.ConfigParser()
        cp.read(self.cfg_file, encoding='utf-8')
        return cp.get(section, option)

    def write_value(self, section, option, value):
        cp = configparser.ConfigParser()
        cp.read(self.cfg_file, encoding='utf-8')
        cp.set(section, option, value)
        cp.write(open(self.cfg_file, "w"))

