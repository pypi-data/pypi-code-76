from selenium import webdriver
import time
from PIL import Image, ImageDraw
from io import BytesIO

class Gochujang:
    def __init__(self):
        self.gochujangs = []
        self.window_size = [1200,1900]
        self.xpath_to_element_to_capture = "/html"
        self.path_to_save = "c:/"
        self.webdriver = None
        
    def add_ganjang(self, Ganjang):
        self.gochujangs.append(Ganjang)

    def set_window_size(self, width, height):
        self.window_size[0]=width
        self.window_size[1]=height

    def set_xpath_to_element_to_capture(self, xpath):
        self.xpath_to_element_to_capture = xpath

    def set_path_to_save(self, path_to_save):
        self.path_to_save = path_to_save

    def set_webdriver(self, webdriver):
        self.webdriver = webdriver
        
    def capture_screens(self):
        if self.gochujangs:
            for ganjang in self.gochujangs:
                self.screenshot(ganjang.STAGING_URL, f'{ganjang.BASE_NAME}_screen_staging.png')
                self.screenshot(ganjang.PRODUCTION_URL, f'{ganjang.BASE_NAME}_screen_production.png')

                Bibigo.analyze(self.path_to_save, ganjang.BASE_NAME)
        
    def screenshot(self, url, file_name):
        driver = webdriver.Firefox(executable_path=self.webdriver)
        
        driver.get(url)

        driver.set_window_size(self.window_size[0],self.window_size[1])
        driver.get(url)
        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight)")
        driver.implicitly_wait(2)
        time.sleep(2)

        element = driver.find_element_by_xpath(self.xpath_to_element_to_capture)
        location = element.location
        size = element.size
        png = driver.get_screenshot_as_png() 
       
        im = Image.open(BytesIO(png)) 

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        im = im.crop((left, top, right, bottom)) 
        im.save(f'{self.path_to_save}{file_name}')
        
        driver.close()
        driver.quit()



class Bibigo:    
    @staticmethod
    def analyze(path,base_name):
        screenshot_staging = Image.open(f"{path}{base_name}_screen_staging.png")
        screenshot_production = Image.open(f"{path}{base_name}_screen_production.png")
        columns = 60
        rows = 80
        screen_width, screen_height = screenshot_staging.size
        
        block_width = ((screen_width - 1) // columns) + 1 
        block_height = ((screen_height - 1) // rows) + 1

        for y in range(0, screen_height, block_height+1):
            for x in range(0, screen_width, block_width+1):
                region_staging = Bibigo.process_region(screenshot_staging, x, y, block_width, block_height)
                region_production = Bibigo.process_region(screenshot_production, x, y, block_width, block_height)

                if region_staging is not None and region_production is not None and region_production != region_staging:
                    draw = ImageDraw.Draw(screenshot_staging)
                    draw.rectangle((x, y, x+block_width, y+block_height), outline = "red")

        screenshot_staging.save(f"{path}{base_name}_result.png")
    
    @staticmethod
    def process_region(image, x, y, width, height):
        region_total = 0
        factor = 100

        for coordinateY in range(y, y+height):
            for coordinateX in range(x, x+width):
                try:
                    pixel = image.getpixel((coordinateX, coordinateY))
                    region_total += sum(pixel)/4
                except:
                    return None

        return region_total/factor
