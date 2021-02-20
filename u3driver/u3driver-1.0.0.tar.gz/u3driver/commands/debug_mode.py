from u3driver.commands.base_command import BaseCommand
import time
import json

class DebugMode(BaseCommand):

    def __init__(self, socket,request_separator,request_end,file_path = None):
        super().__init__(socket,request_separator,request_end)
        self.file_path = file_path
    
    def execute(self):
        screen = self.send_data(self.create_command('getScreen'))
        print(screen)
        screen = json.loads(screen)
        screen = {"width":int(screen["width"]), "height":int(screen['height'])}

        response = self.send_data(self.create_command('debugMode', '0'))
        if response == "Open Debug Mode" or response == "Debug Already Opened":
            ##结束行有17行
            end_str = """\texcept Exception as e:\n\t\tprint(f'{e}')\n\t\traise e\n\nif __name__ == '__main__':\n\tparser = argparse.ArgumentParser()\n\tparser.add_argument('-s', help="device serial")\n\tparser.add_argument('-i', help="ip address")\n\tparser.add_argument('-port', help="ip address")\n\targs = parser.parse_args()\n\tdevice_s = args.s\n\tip = args.i\n\tport = int(args.port)\n\tudriver = AltrunUnityDriver(device_s,"", ip, TCP_PORT=port,timeout=60, log_flag=True)\n\tAutoRun(udriver)\n\tudriver.stop()"""
            tap_count = 0
            if self.file_path != None:
                data_str = ''
                data_str += 'from u3driver import AltrunUnityDriver\n'
                data_str += 'from u3driver import By\n'
                data_str += 'import time\n'
                data_str += 'import argparse\n\n'
                data_str += 'def AutoRun(udriver):\n'
                tap_count += 1
                data_str += '\t' * tap_count + 'try:\n'
                tap_count += 1
                
                if self.file_path != None:
                        with open(file=self.file_path, mode='w+', encoding='utf-8') as f:
                            f.write(data_str)
            start_position = None
            end_position = None
            while True:
                data = self.recvall()
                data_str = ''
                if data == "Close Debug Mode":
                    
#                     tap_count -= 1
#                     data_str += '\t' * tap_count + 'except Exception as e:\n'
#                     tap_count += 1
#                     data_str += '\t' * tap_count + 'print(f"{e}")\n'
#                     data_str += '\t' * tap_count + 'raise e\n\n'
#                     tap_count -= 1

#                     data_str += """
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-s', help="device serial")
#     parser.add_argument('-i', help="ip address")
#     parser.add_argument('-port', help="ip address")
#     args = parser.parse_args()
#     device_s = args.s
#     ip = args.i
#     port = args.port
#     udriver = AltrunUnityDriver(device_s,"", ip, TCP_PORT=port,timeout=60, log_flag=True)
#     AutoRun(udriver)
#     udriver.stop()
# """
#                     if self.file_path != None:
#                         with open(file=self.file_path, mode='a+', encoding='utf-8') as f:
#                             f.write(data_str)
                    return data
                json_data = json.loads(data)
                time = 2
                if "time" in json_data:
                    time = float(json_data['time'])
                if "start position" in json_data:
                    start_position = tuple(eval(json_data['start position']))
                elif "end position" in json_data:
                    end_position = tuple(eval(json_data['end position']))
                    if start_position != None and end_position != None:
                        data_str += '\t' * tap_count + f'time.sleep({time})\n'
                        data_str += '\t' * tap_count + 'udriver.drag_object("'+json_data['name'].replace("/","//")+f'",{start_position[0] / screen["width"]},{start_position[1] / screen["height"]},{end_position[0] / screen["width"]},{end_position[1] / screen["height"]})\n'
                        start_position = None
                        end_position = None
                elif "value" in json_data:
                    data_str += '\t' * tap_count + f'time.sleep({time})\n'
                    data_str += '\t' * tap_count + 'udriver.find_object(By.PATH,"'+json_data['name'].replace("/","//")+'")'
                    data_str += '.set_text("' + json_data['value'] + '")\n'
                elif "name" in json_data:
                    data_str += '\t' * tap_count + f'time.sleep({time})\n'
                    data_str += '\t' * tap_count + 'udriver.find_object(By.PATH,"'+json_data['name'].replace("/","//")+'")'
                    data_str += '.tap()\n'
                if self.file_path != None:
                        all_str = '' 
                        with open(file=self.file_path, mode='r+', encoding='utf-8') as f:
                            all_str = f.read()

                        all_str = all_str.replace(end_str,"")
                        all_str += data_str
                        all_str += end_str

                        with open(file=self.file_path, mode='w+', encoding='utf-8') as f:
                            
                            f.write(all_str)
                
        return response
