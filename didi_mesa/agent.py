from mesa import Agent
import random

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
		self.cContent = {} #(2,1) obs
		self.toWhere = None

	def hayCajaObs(self, i):
		for j in self.model.grid.get_cell_list_contents(i):
			#and not isinstance(j, cargador)
			if(isinstance(j, caja) and i != self.base):
				return True
		return False

	def moveRandom(self):
		possible_steps = self.model.grid.get_neighborhood(
			self.pos,
			moore=False, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
			include_center=False)

		self.direction = self.random.choice(possible_steps) 

		for k in possible_steps:
			if(self.hayCajaObs(k)):
				self.cContent[k] = "obs"
				self.direction = k
			else:
				self.cContent[k] = "free"

		self.model.grid.move_agent(self, self.direction)

	def obsInMap(self):
		for key in self.cContent:
			if(self.cContent[key] == "obs"):
				return True
		return False

	def moveConCaja(self):
		possible_steps = self.model.grid.get_neighborhood(
			self.pos,
			moore=False, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
			include_center=False)

		self.cContent[self.base] = "free"

		if(self.toWhere == None):
			return

		#Añade las posiciones neighbors
		for k in possible_steps:
			if(self.hayCajaObs(k)):
				self.cContent[k] = "obs"
				if(self.tieneCaja == False):
					self.model.grid.move_agent(self, k)
					self.toWhere = self.base
					return
			else:
				self.cContent[k] = "free"

		#Calclular menor x y y
		distToX = abs(self.pos[0] - self.toWhere[0])
		distToY = abs(self.pos[1] - self.toWhere[1])

		#Si los dos son cero significa que ya esta en la posición de la caja
		if(distToY == 0 and distToX  == 0):
			if(self.pos == self.base):
				self.miCaja = None
				self.tieneCaja = False
				self.calcularCamino()

		#Avanzar para asercarse a la base tomando la mejor direccion
		else:
			self.directions.append((0,0))
			self.directions.append((0,0))
			self.directions.append((0,0))
			self.directions.append((0,0))

			if(distToY >= distToX): 
				if(self.pos[1] - self.toWhere[1] > 0):
					self.directions[0] = (self.pos[0], self.pos[1] - 1)
					self.directions[3] = (self.pos[0], self.pos[1] + 1)
				else: 
					self.directions[0] = (self.pos[0], self.pos[1] + 1)
					self.directions[3] = (self.pos[0], self.pos[1] - 1)

				if(self.pos[0] - self.toWhere[0] > 0):
					self.directions[1] = (self.pos[0] - 1, self.pos[1])
					self.directions[2] = (self.pos[0] + 1, self.pos[1])
				else:
					self.directions[1] = (self.pos[0] + 1, self.pos[1])
					self.directions[2] = (self.pos[0] - 1, self.pos[1])

			elif(distToX > distToY):

				if(self.pos[0] - self.toWhere[0] > 0):
					self.directions[0] = (self.pos[0] - 1, self.pos[1])
					self.directions[3] = (self.pos[0] + 1, self.pos[1])
				else:
					self.directions[0] = (self.pos[0] + 1, self.pos[1])
					self.directions[3] = (self.pos[0] - 1, self.pos[1])

				if(self.pos[1] - self.toWhere[1] > 0):
					self.directions[1] = (self.pos[0], self.pos[1] - 1)
					self.directions[2] = (self.pos[0], self.pos[1] + 1)
				else: 
					self.directions[1] = (self.pos[0], self.pos[1] + 1)
					self.directions[2] = (self.pos[0], self.pos[1] - 1)

			for i in self.directions:
				if(not self.hayCajaObs(i) and i in possible_steps):
					print("entro a mover agente")
					self.model.grid.move_agent(self, i)
					if(self.tieneCaja == True):
						print("entro a mover cajita")
						self.miCaja.model.grid.move_agent(self.miCaja, i)
					break

		self.directions = []


	def hayCaja(self, i):
		for j in self.model.grid.get_cell_list_contents(i):
			if(isinstance(j, caja) and i != self.base):
				return True
		return False

	def assignCaja(self, i):
		for j in self.model.grid.get_cell_list_contents(i):
			if(isinstance(j, caja) and self.miCaja != "base"):
				self.miCaja = j
				self.tieneCaja = True
				self.toWhere = self.base
				return True
			if(isinstance(j, caja)):
				self.calcularCamino()
		return False

	def calcularCamino(self):
		for key in self.cContent:
			if(self.cContent[key] == "obs" and key != self.base):
				self.toWhere = key
				return
			elif(key == self.base):
				self.toWhere = None
				return
		
	def step(self):
		print("toWhere")
		print(self.toWhere)

		if(self.tieneCaja == True and self.pos == self.base):
			self.tieneCaja = False
			self.miCaja = None
			self.calcularCamino()
			self.moveConCaja()

		elif(self.tieneCaja == True):
			self.toWhere = self.base
			self.moveConCaja()

		elif(self.hayCaja(self.pos) and self.tieneCaja == False):
			self.assignCaja(self.pos)
			self.moveConCaja()

		elif(self.toWhere == None):
			self.moveRandom()
			if(self.obsInMap()):
				self.calcularCamino()

		elif(self.tieneCaja == False and self.pos == self.toWhere):
			self.calcularCamino()
			self.moveConCaja()

		elif(self.tieneCaja == False):
			self.moveConCaja()

class caja(Agent):

	def __init__(self, pos, base, model):
		super().__init__(pos, model)
		self.pos = pos
		self.base = base
		self.cond = "floor"

	def step(self):
		if(self.pos == self.base):
			self.cond = "base"





