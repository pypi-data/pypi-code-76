class Student:
	def __init__(self,name):
		self.name = name
		self.exp = 0
		self.lesson = 0 

		#self.AddEXP(10)

	def Hello(self):
		print('สวัสดีจ้าา ผมชื่อ{}'.format(self.name)) 

	def Coding(self):
		print('{}:กำลังเขียนโปรแกรม..' .format(self.name))
		self.exp += 5
		self.lesson += 1 

	def ShowEXP(self):
		print('-{} มีประสบการณ์ {} EXP' .format(self.name,self.exp))
		print('- เรียนไป {} ครั้งแล้ว' .format(self.lesson))
	
	def AddEXP(self, score):
		self.exp += score
		self.lesson += 1 


		
		
class SpecialStudent(Student):    # สืบทอด class 

	def __init__(self,name,father):
		super().__init__(name)
		self.father = father 
		mafia = ['Bill Gates','Thomas Edison']
		if father in mafia:
			self.exp += 100

	def AddEXP(self,score):      #overwrite class
		self.exp += (score*3)
		self.lesson +=1 
	def AskEXP(self,score=10):
		print('ครูขอคะแนน {} EXP' .format(score))
		self.AddEXP(score)
		


print(_name_) 

if __name__ == '__main__':

	print('=======2021,1 Jan======')
	student0 = SpecialStudent('Mark Zuckerberg','Bill Gates')
	student0.AskEXP()
	student0.ShowEXP()


	student1 = Student('Albert')
	print(student1.name)
	student1.Hello()
	print('----------------------------') 
	student2 = Student('Steve')
	print(student2.name)
	student2.Hello()
	print('==========2021,2 Jan ====')
	print('----------Too : ใครอยากเรียนโค้ดดิ้ง? --- (10 exp)----')
	student1.AddEXP(10)

	print('ตอนี้ exp ของแต่ละคนได้เท่าไหรกันแล้ว') 
	print(student1.name,student1.exp)
	print(student2.name,student2.exp)

	print('===== 4 Jan ======') 

	for i in range(5):
		student2.Coding()

	student1.ShowEXP()
	student2.ShowEXP()