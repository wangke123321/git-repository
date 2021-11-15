import configparser


class FileConfig:
    def config(self, file_name, section, option):
        cf = configparser.ConfigParser()
        cf.read(file_name, encoding='utf-8')
        return cf.get(section, option)


if __name__ == '__main__':
    l1 = FileConfig().config('../class_config', 'MODE', 't1_step')
    l2 = FileConfig().config('../class_config', 'MODE', 't2_step')
    l3 = FileConfig().config('../class_config', 'MODE', 'step2_url')
    l4 = FileConfig().config('../class_config', 'MODE', 'step3_url')
    print(l1, l2, l3, l4)
