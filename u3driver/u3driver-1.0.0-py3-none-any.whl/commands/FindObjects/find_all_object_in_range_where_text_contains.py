from u3driver.commands.command_returning_alt_elements import CommandReturningAltElements
import json
class FindAllObjectInRangeWhereTextContains(CommandReturningAltElements):
    def __init__(self, socket,request_separator,request_end,appium_driver,value,text):
        super(FindAllObjectInRangeWhereTextContains, self).__init__(socket,request_separator,request_end,appium_driver)
        self.value=value
        self.text = text

    
    def execute(self):
        data = self.send_data(self.create_command('findAllObjectInRangeWhereTextContains', self.value,self.text))
        return json.loads(data)['name']
    