#pyoopbyikanit95.py

class Vehicle:
    '''
    --------------------
        
    Test Documentation
        
    นี่คือทดสอบเขียน Python OOP (Object-Oriented Programming)
        
    --------------------
    '''
    #def __init__(self,price,budget):
    def __init__(self,price=15000,budget=100000):
    #ตั้งค่า Default ของค่า Price และ Budget เพื่อ Run Module ไม่ให้เกิด Error ในกรณีไม่ได้ใส่ค่า
        self.captain = 'Captain A'
        self.sub_name = 'The Avenger I'
        self.price = price # Milion
        self.km = 0
        self.budget = budget
        self.totalcost = 0

    def Engineering(self):
        print('We are Department of Engineering')

    def CalCommission(self):
        ''' นี่คือฟังก์ชั่นว่า คุณได้ค่าคอมมิชชั่นกี่บาท '''
        pc = 10 # 10%
        percent = self.price * (pc/100)
        print('Captain A! You got: {} Million Baht'.format(percent))
                
    def GoTo(self,enemypoint,distance):
        #print('Let\'s go to {} Distance: {} KM'.format(enemypoint,distance))
        # Or #
        print(f"Let's go to {enemypoint} Distance: {distance} KM")
        self.km = self.km + distance # Or # self.km += distance
        self.Fuel()
                
    def Fuel(self):
        diesel_cost = 20 # 20 Baht/Litre
        cal_fuel_cost = self.km * diesel_cost
        print('Current Fuel Cost: {:,d} Baht'.format(cal_fuel_cost))
        # :,d = จำนวนเต็ม (d = decimal integer)
        # :,.0f = ไม่ใส่จุดทศนิยม (f = float)
        # :,.2f = ใส่จุดทศนิยม 2 ตำแหน่ง
        self.totalcost += cal_fuel_cost

    #def BudgetRemaining(self):
    #   remaining = self.budget - self.totalcost
    #   print('Budget Remaining: {:,.2f} Baht'.format(remaining))
    # Or #
    @property
    def BudgetRemaining(self):
        remaining = self.budget - self.totalcost
        print('Budget Remaining: {:,.2f} Baht'.format(remaining))
        return remaining
    # @property คู่กับ return #
    # เป็นการเปลี่ยนจาก "ผลลัพธ์ (Result)" ให้กลายเป็น "ค่า (Value)" เพื่อจะนำไปคำนวณกับอย่างอื่นต่อไป

class ElectricVehicle(Vehicle): # เป็นการสืบทอด (inherit) จาก Class Vehicle เพื่อประหยัด Coding ไม่ต้องเขียนใหม่หลายบรรทัด
    #def __init__(self,price,budget):
    def __init__(self,price=10000,budget=400000):
    #ตั้งค่า Default ของค่า Price และ Budget เพื่อ Run Module ไม่ให้เกิด Error ในกรณีไม่ได้ใส่ค่า
        self.sub_name = 'The Avenger II'
        self.battery_distance = 100000
        # Vehicle can go out 100000 KM / 100 Percent
        super().__init__(price,budget)
        # super เป็น Function ในการสั่งให้สืบทอด Class
        # เพื่อให้ Copy ทุก Function จากข้างบนมาใส่ใน Class นี้
        # หรือทุก Function ข้างบนถูกเรียกใช้งานด้วย

    def Battery(self):
        allbattery = 100
        print('KM:',self.km)
        calculate = (self.km / self.battery_distance) * 100
        print('Take Battery: {}%'.format(calculate))
        print('We have Battery Remaining: {}%'.format(allbattery-calculate))

    #def CalBattery(self):
    #    print(self.km)

    def Fuel(self):
        electricity_cost = 5 # 5 Baht/kilowatt-hour (kWh)
        cal_fuel_cost = self.km * electricity_cost
        print('Current Electric Power Cost: {:,d} Baht'.format(cal_fuel_cost))
        self.totalcost += cal_fuel_cost

'''
Tesla = ElectricVehicle(40000,2000000)
print(Tesla.captain)
print(Tesla.budget)
Tesla.GoTo('Japan',10000)
print(Tesla.BudgetRemaining)
#Tesla.CalBattery()
Tesla.Battery()

print('------------------')

AvengerB = Vehicle(40000,2000000)
print(AvengerB.captain)
print(AvengerB.budget)
AvengerB.GoTo('Japan',10000)
print(AvengerB.BudgetRemaining)
'''

if __name__ == '__main__':
# เป็น Function ป้องกันเมื่อ Import Function (ElectricVehicle,Vehicle) นี้ไปใช้ใน File อื่น
# จะ Run ก็เมื่อไฟล์นี้เป็นไฟล์ Main หรือหมายถึงถ้าไม่ใช่ไฟล์ Main จะไม่ Run Function ด้านล่างนี้ได้
    Tesla = ElectricVehicle(40000,2000000)
    print(Tesla.captain)
    print(Tesla.budget)
    Tesla.GoTo('Japan',10000)
    print(Tesla.BudgetRemaining)
    #Tesla.CalBattery()
    Tesla.Battery()

    print('------------------')

    AvengerB = Vehicle(40000,2000000)
    print(AvengerB.captain)
    print(AvengerB.budget)
    AvengerB.GoTo('Japan',10000)
    print(AvengerB.BudgetRemaining)


'''
print('-- AvengerA --')
AvengerA = Vehicle(64365)
print(AvengerA.captain)
print(AvengerA.sub_name)
AvengerA.CalCommission()
print(AvengerA.kilo)
AvengerA.GoTo('China',7000)
print('Current Distance:', AvengerA.kilo)
AvengerA.Fuel()
#AvengerA.BudgetRemaining()
# Or # สำหรับการใช้ Property เพื่อ Return ค่า
current_budget = AvengerA.BudgetRemaining
print('20 % Reserve Paying:', current_budget * 0.2)

print('------------------')
print('-- AvengerB --')
AvengerB = Vehicle(70000)
print('Before...')
print(AvengerB.captain)
print('After...')
AvengerB.captain = 'Captain B'
print(AvengerB.captain)
'''
