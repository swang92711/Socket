from CookieJar import CookieJar
import socket


class ServerMessage:
	"""this is a model that parsing received message from HTTP server"""

	def __init__(self, mySocket):
		self.version = ""
		self.headers = {}
		self.body = ""
		self.status_code = None
		self.status = ""
		self.cookieJar = CookieJar()

		file = mySocket.makefile("rb")

		self.readHeader(file)
		bodyLength = int(self.getHeader("content-length"))
		self.readBody(file, bodyLength)
		file.close()

	def readHeader(self, file):
		# read the first line to get status info
		statusLine = file.readline().decode("utf-8")

		version, status_code, status = statusLine.split()
		self.version = version
		self.status_code = status_code
		self.status = status

		#start reading 2nd line of header
		key = ""

		while(1):
			line = file.readline().decode("utf-8")

			if ":" not in line:
				break

			#remove leading space
			sLine = line.strip()

			#TODO: may be uselss
			if line[0] is " ":
				self.addHeader(key.lower(), sLine)
				continue

			key, value = sLine.split(":", 1)
			self.addHeader(key.lower(), value)

	def addHeader(self, key, value):

		if key == "set-cookie":
			self.cookieJar.add_cookie_from_string(value)

		#TODO: maybe useless
		if key in self.headers.keys():
			self.headers[key] = self.header[key] +", " + value
		else:
			self.headers[key] = value

	def readBody(self, file, fileLength):
		body = ""
		#TODO: may be useless as well
		while fileLength > 0:
			data = file.read(fileLength).decode("utf-8")
			fileLength -= len(data)
			body += data
		self.body = body

	def getHeader(self, key):
		return self.headers[key]







