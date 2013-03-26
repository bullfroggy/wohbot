
class Card:
	properties = {
		"global_id": "",
		"unique_id": "",
		"rarity": "",
		"max_level": 99,
		"level": 1,
		"ability_level": 1,
		"atk_power": None,
		"def_power": None,
		"pwr_req": None,
	}

	def __init__(self, properties):
		self.properties.update(properties)

	def set_global_id(self, global_id):
		self.global_id = global_id

	def get_global_id(self):
		return self.global_id
