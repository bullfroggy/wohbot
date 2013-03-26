class Player:
	settings = {
				"sid": "",

			}

	def __init__(self, settings):
		self.settings.update(settings)

	def get_url(self, url):
		if self.settings["urls"][url]:
			return self.settings["urls"][url]
		else:
			return False