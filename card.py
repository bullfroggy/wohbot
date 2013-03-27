
class Card:
	properties = {
		"global_id": "",
		#"unique_id": "",
		"rarity": "",
		"max_level": 99,
		"level": 1,
		"ability_level": 1,
		"atk_pwr": None,
		"def_pwr": None,
		"pwr_req": None,
		"silver": 0,
	}

	def __init__(self, unique_id, properties):
		self.unique_id = unique_id
		self.properties.update(properties)

	def __eq__(self, other):
		return self.get_unique_id()==other.get_unique_id()

	def __hash__(self):
		return hash(('unique_id', self.get_unique_id()))

	def set_global_id(self, global_id):
		self.global_id = global_id

	def get_global_id(self):
		return self.properties["global_id"]

	def set_unique_id(self, unique_id):
		self.unique_id = unique_id

	def get_unique_id(self):
		return self.unique_id

	def get_rarity(self):
		return self.rarity

	def set_rarity(self, rarity):
		self.rarity = rarity

	def get_max_level(self):
		return int(self.get_max_level)

	def set_max_level(self, max_level):
		self.max_level = max_level

	def set_level(self, level):
		self.level = level

	def get_level(self):
		return int(self.level)

	def set_ability_level(self, ability_level):
		self.ability_level = ability_level

	def get_ability_level(self):
		return int(self.ability_level)

	def set_atk_pwr(self, atk_pwr):
		self.atk_pwr = atk_pwr

	def get_atk_pwt(self):
		return int(self.atk_pwr)

	def set_def_pwr(self, def_pwr):
		self.def_pwr = def_pwr

	def get_def_pwr(self):
		return int(self.def_pwr)

	def set_pwr_req(self, pwr_req):
		self.pwr_req = pwr_req

	def get_pwr_req(self):
		return int(self.pwr_req)

	def set_silver(self, silver):
		self.silver = silver

	def get_silver(self):
		return int(self.silver)
