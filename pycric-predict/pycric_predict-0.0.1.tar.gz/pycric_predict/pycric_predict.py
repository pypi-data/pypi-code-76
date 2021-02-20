import random
class cric_predict:
	def __init__(self, position, is_caption, caption_is_batsman, team, cchances, fchances):
		self.position = position
		self.caption = is_caption
		self.team = team


		self.verify = caption_is_batsman
		# percentage of century
		self.percentage = int(cchances * 100)
		# percentage of fifty
		self.fpercentage = int(fchances * 100)
		# list which stores century chances
		self.chances = []
		# list which stores fifty chances
		self.fchances = []
		# self.fchances = fhances
 
	@property 
	def run(self):
		self.remaining = 100 - self.percentage
		self.fremaining = 100 - self.fpercentage
		self.trial = []
		self.ftrial = []
		# determining chances for yes or no in century and fifty
		for t in range(self.percentage):
			self.trial.append(True)
		for ft in range(self.fpercentage):
			self.ftrial.append(True)
		for j in range(self.remaining):
			self.trial.append(False)
		for fj in range(self.fremaining):
			self.ftrial.append(False)
		self.fverify = []
		self.verify = []
		while True:
			l = random.randint(0, (len(self.trial) - 1))
			fl = random.randint(0, (len(self.ftrial) - 1))
			if l not in self.verify:

				self.verify.append(l)

				self.chances.append(self.trial[l])
				if len(self.chances) ==100:
					
					break
			elif l in self.verify:
				pass
			if fl not in self.fverify:

				self.fverify.append(fl)

				self.fchances.append(self.ftrial[fl])
				if len(self.fchances) ==100:
					
					break
			elif fl in self.fverify:
				pass
	@run.setter
	def run():
		pass
	def calculate_runs(self):
		if "reland" in self.team or "fghanistan" in self.team or "imbabwe" in self.team or "merica" in self.team:
			pass
		else:
			
			if self.caption == False:
				if self.position == 1 or self.position == 2 or self.position == 3:
					self.main1 = random.randint(0, 20)
					self.main2 = random.randint(120, 200)
					self.main3 = random.randint(120, self.main2)
					self.raw_runs = random.randint(self.main1, self.main3)
					if self.raw_runs >=100 and self.raw_runs<150:
						self.decider = random.choice(self.chances)
						if self.decider == False:
							self.to_decide1 = random.randint(20, 47)

							self.to_decide2 = random.randint(47, 89)
							self.raw_runs = random.randint(self.to_decide1, self.to_decide2)
						elif self.decider == True:
							self.raw_runs -= random.randint(1, 7)
					elif self.raw_runs>=150:
						self.decider3 = random.choice(self.chances)
						if self.decider3 == False:
							self.raw_runs-=random.randint(20, 55)
						elif self.decider3 == True:
							self.raw_runs-=random.randint(24, 35)
					elif self.raw_runs >= 50 and self.raw_runs<100:
						self.decider2 = random.choice(self.fchances)
						if self.decider2 == False:
							self.to_decide3 = random.randint(10, 30)
							self.to_decide4 = random.randint(30, 60)
							self.raw_runs = random.randint(self.to_decide3, self.to_decide4)
						elif self.decider2 == True:
							self.raw_runs+=random.randint(1, 10)
					self.raw_runs = self.raw_runs - random.randint(12, 17)
					if self.raw_runs<0:
						self.raw_runs = random.randint(1, 11 )

					return self.raw_runs
				elif self.position == 4 or self.position == 5 or self.position == 6:
					self.main1 = random.randint(1, 20)
					self.main2 = random.randint(120, 190)
					self.main3 = random.randint(120, self.main2)
					self.raw_runs = random.randint(self.main1, self.main3)
					if self.raw_runs >=100 and self.raw_runs<150:
						self.decider = random.choice(self.chances)
						if self.decider == False:
							self.to_decide1 = random.randint(10, 37)

							self.to_decide2 = random.randint(37, 79)
							self.raw_runs = random.randint(self.to_decide1, self.to_decide2)
						elif self.decider == True:
							self.raw_runs -= random.randint(11, 27)
					elif self.raw_runs>=150:
						self.decider3 = random.choice(self.chances)
						if self.decider3 == False:
							self.raw_runs-=random.randint(20, 47)
						elif self.decider3 == True:
							pass
					elif self.raw_runs >= 50 and self.raw_runs<100:
						self.decider2 = random.choice(self.fchances)
						if self.decider2 == False:
							self.to_decide3 = random.randint(10, 30)
							self.to_decide4 = random.randint(30, 50)
							self.raw_runs = random.randint(self.to_decide3, self.to_decide4)
						elif self.decider2 == True:
							self.raw_runs+=random.randint(8, 18)
					self.raw_runs = self.raw_runs - random.randint(3, 9)
					if self.raw_runs <0:
						self.raw_runs = 0
					return self.raw_runs
				elif self.position == 7 or self.position == 8:
					self.main1 = random.randint(0, 20)
					self.main2 = random.randint(70, 103)
					
					self.raw_runs = random.randint(self.main1, self.main2)
					if random.randint(1, 4) == 1:
						self.raw_runs-=random.randint(10, 20)
						if self.raw_runs<0:
							self.raw_runs = 0
					if random.randint(1, 7) == 4:
						self.raw_runs = random.randint(1, 8)

					if self.raw_runs >=100:
						self.decider = random.choice(self.chances)
						if self.decider == False:
							self.to_decide1 = random.randint(10, 37)

							self.to_decide2 = random.randint(37, 59)
							self.raw_runs = random.randint(self.to_decide1, self.to_decide2)
						elif self.decider == True:
							self.raw_runs -= random.randint(11, 27)
					elif self.raw_runs >= 50 and self.raw_runs<100:
						self.decider2 = random.choice(self.fchances)
						if self.decider2 == False:
							self.to_decide3 = random.randint(10, 20)
							self.to_decide4 = random.randint(20, 32)
							self.raw_runs = random.randint(self.to_decide3, self.to_decide4)
						elif self.decider2 == True:
							self.raw_runs-=random.randint(1, 8)
					
					if self.raw_runs<=40:
						self.raw_runs-=random.randint(10, 20)
					if self.raw_runs<0:
						self.raw_runs = 0
					return self.raw_runs
				elif self.position == 9 or self.position == 10 or self.position == 11:
					self.main1 = random.randint(1, 5)

					self.main2 = random.randint(5, 40)
					self.raw_runs = random.randint(self.main1, self.main2)
					self.circumstances = random.randint(1, 500)
				
					if random.randint(1, 3) == 1:
						self.raw_runs-=random.randint(10, 20)
						if self.raw_runs<0:
							self.raw_runs == 0
					if random.randint(1, 5) == 4:
						self.raw_runs = random.randint(0, 4)					
					if self.circumstances == random.randint(1, 500):
						self.raw_runs = random.randint(50, 120)
					elif self.raw_runs <0:
						self.raw_runs = 0
					return self.raw_runs
				else:
					exit("Position error: Position given is out of range.")

			elif self.caption == True:
				if self.verify == False:
					pass
				elif self.verify == True:
					self.main1 = random.randint(0, 20)
					self.main2 = random.randint(120, 200)
					self.main3 = random.randint(120, self.main2)
					self.raw_runs = random.randint(self.main1, self.main3)
					if self.raw_runs >=100 and self.raw_runs<150:
						self.decider = random.choice(self.chances)
						if self.decider == False:
							self.to_decide1 = random.randint(20, 57)

							self.to_decide2 = random.randint(57, 102)
							self.raw_runs = random.randint(self.to_decide1, self.to_decide2)
						elif self.decider == True:
							self.raw_runs -= random.randint(2, 6)
					elif self.raw_runs>=150:
						self.decider3 = random.choice(self.chances)
						if self.decider3 == False:
							self.raw_runs-=random.randint(20, 55)
						elif self.decider3 == True:
							self.raw_runs-=random.randint(24, 35)
					elif self.raw_runs >= 50 and self.raw_runs<100:
						self.decider2 = random.choice(self.fchances)
						if self.decider2 == False:
							self.to_decide3 = random.randint(10, 30)
							self.to_decide4 = random.randint(30, 78)
							self.raw_runs = random.randint(self.to_decide3, self.to_decide4)
						elif self.decider2 == True:

							self.raw_runs+=random.randint(10, 20)
					self.raw_runs =self.raw_runs - random.randint(1, 8)
					if self.raw_runs <0:
						self.raw_runs = 0
						return self.raw_runs
					else:
						return self.raw_runs

