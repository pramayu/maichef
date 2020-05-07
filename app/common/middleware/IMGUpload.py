import os
import cloudinary
import cloudinary.uploader
import base64


cloudinary.config(
	cloud_name = os.getenv("CLOUDINARY_NAME"),
	api_key = os.getenv("CLOUDINARY_APIQ"),
	api_secret = os.getenv("CLOUDINARY_APIS")
)

class IMGUploadChef():

	def __init__(self, code64, dimens):
		self.code64 = code64
		self.dimens = dimens

	def code64_decode(self):
		image = base64.b64decode(self.code64)
		return image

	def upload(self):
		image = self.code64_decode()
		res = cloudinary.uploader.upload(image, eager = [
			{ "width": self.dimens, "height": self.dimens, "crop": "fill" }
		])
		return res
