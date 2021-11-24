from mesa import Agent

class cargador(Agent):

	def __init__(self, unique_id, pos, base, model):
		super().__init__(unique_id, model)
		self.direction = 4
		self.pos = pos
		self.unique_id = unique_id
		self.tieneCaja = False
		self.miCaja = None
		self.directions = []
		self.base = base

	def hayCajaObs(self, i):
		for j in self.model.grid.get_cell_list_contents(i):
			if(isinstance(j, caja) and i != self.base and not isinstance(j, cargador)):
				print("si hubo obsss en pos")
				print(i)
				return True
		print("no hubo obsss")
		return False

	def moveRandom(self):
		possible_steps = self.model.grid.get_neighborhood(
			self.pos,
			moore=False, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
			include_center=False)

		self.direction = self.random.choice(possible_steps) 
		print(self.direction)

		self.model.grid.move_agent(self, self.direction)

	def moveConCaja(self):
		possible_steps = self.model.grid.get_neighborhood(
			self.pos,
			moore=False, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
			include_center=True)

		#Calclular menor x y y
		distToX = abs(self.pos[0] - self.base[0])
		distToY = abs(self.pos[1] - self.base[1])

		#Si los dos son cero significa que ya esta en la posición de la caja
		if(distToY == 0 and distToX  == 0):
			self.miCaja = None
			self.tieneCaja = False

		#Avanzar para asercarse a la base tomando la mejor direccion
		else:
			self.directions.append((0,0))
			self.directions.append((0,0))
			self.directions.append((0,0))
			self.directions.append((0,0))

			if(distToY >= distToX): #(2,9) - (0,4) 
				if(self.pos[1] - self.base[1] > 0):
					self.directions[0] = (self.pos[0], self.pos[1] - 1)
					self.directions[3] = (self.pos[0], self.pos[1] + 1)
				else: 
					self.directions[0] = (self.pos[0], self.pos[1] + 1)
					self.directions[3] = (self.pos[0], self.pos[1] - 1)

				if(self.pos[0] - self.base[0] > 0):
					self.directions[1] = (self.pos[0] - 1, self.pos[1])
					self.directions[2] = (self.pos[0] + 1, self.pos[1])
				else:
					self.directions[1] = (self.pos[0] + 1, self.pos[1])
					self.directions[2] = (self.pos[0] - 1, self.pos[1])

			elif(distToX > distToY):

				if(self.pos[0] - self.base[0] > 0):
					self.directions[0] = (self.pos[0] - 1, self.pos[1])
					self.directions[3] = (self.pos[0] + 1, self.pos[1])
				else:
					self.directions[0] = (self.pos[0] + 1, self.pos[1])
					self.directions[3] = (self.pos[0] - 1, self.pos[1])

				if(self.pos[1] - self.base[1] > 0):
					self.directions[1] = (self.pos[0], self.pos[1] - 1)
					self.directions[2] = (self.pos[0], self.pos[1] + 1)
				else: 
					self.directions[1] = (self.pos[0], self.pos[1] + 1)
					self.directions[2] = (self.pos[0], self.pos[1] - 1)

			for i in self.directions:
				if(not self.hayCajaObs(i) and i in possible_steps):
					print(i)
					self.model.grid.move_agent(self, i)
					self.miCaja.model.grid.move_agent(self.miCaja, i)
					break

		self.directions = []


	def hayCaja(self, i):
		for j in self.model.grid.get_cell_list_contents(i):
			if(isinstance(j, caja)):
				self.miCaja = j
				self.tieneCaja = True
				return True
		return False
		
	def step(self):
		if(self.tieneCaja == False):
			if(self.hayCaja(self.pos)):
				self.moveConCaja()
				if(self.pos == self.base):
					self.miCaja = None
					self.tieneCaja = False
					self.moveRandom()
			else:
				self.moveRandom()
		else:
			self.moveConCaja()

class caja(Agent):

	def __init__(self, pos, model):
		super().__init__(pos, model)
		self.pos = pos

	def step(self):
		pass