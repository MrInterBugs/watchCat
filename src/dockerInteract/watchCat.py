import docker
from dockerInteract.watchContainer import WatchContainer
import logging

APPLICATION_NAME = "watchCat"


class WatchCat:
    client: docker.DockerClient
    monitoredContainers: list[WatchContainer]

    def __init__(self) -> None:
        self.client = docker.DockerClient(base_url="unix://var/run/docker.sock")
        self.monitoredContainers = []

    def getMonitoredContainers(self) -> None:
        self.monitoredContainers.clear()
        allContainers = self.client.containers.list()

        for container in allContainers:
            labels = container.labels
            if labels.get(APPLICATION_NAME) == "True":
                self.monitoredContainers.append(WatchContainer(container, self.client))

    def getContainersWithUpdates(self) -> list[WatchContainer]:
        return [
            container
            for container in self.monitoredContainers
            if container.isUpdateAvailable()
        ]
