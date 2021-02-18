from configparser import ConfigParser
import os

def main():

    xyz = SetConfig()
    xyz.read()

    # abc = SetConfig.read()

    print("HelloWorld")

class SetConfig():

    def read(self):


        # BASE_DIR = os.getcwd()

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        CONFIG_PATH = os.path.join(BASE_DIR,'config.ini')

        print("hell")

        config = ConfigParser()

        config.read(CONFIG_PATH)



        self.designer_name = config.get('fontinfo', 'designer_name')
        self.designer_url = config.get('fontinfo', 'designer_url')

        self.manufacturer = config.get('fontinfo', 'manufacturer')
        self.manufacturer_url = config.get('fontinfo', 'manufacturer_url')

        self.license = config.get('fontinfo', 'license')

        self.license_url = config.get('fontinfo', 'license_url')

        self.vendor_id = config.get('fontinfo', 'vendor_id')
        self.trademark = config.get('fontinfo', 'trademark')
        self.copyright = config.get('fontinfo', 'copyright')

        print("hello")

if __name__ == '__main__':
    main()
