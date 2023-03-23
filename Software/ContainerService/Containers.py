from python_on_whales import DockerClient

class Containers:
	def __init__(self):
		self.docker = DockerClient(compose_files=["./ContainerService/docker-compose.yml"])

	def startContainers(self):
		self.docker.compose.up(detach=True)
		while True:
			if "Waiting for connection" in self.docker.compose.logs(tail=1,no_log_prefix=True):
				print("Servers started")
				break
			else:
				continue

	def stopContainers(self):
		self.docker.compose.stop()

	def rmContainers(self):
		self.docker.compose.down()

	def status(self):
		for container in self.docker.compose.ps():
			print(container.name, container.state.status)

