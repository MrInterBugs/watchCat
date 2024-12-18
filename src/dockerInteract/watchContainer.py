import docker
import logging


class WatchContainer:
    container: docker.models.containers.Container
    client: docker.DockerClient

    def __init__(self, container: docker.models.containers.Container, client: docker.DockerClient) -> None:
        self.container = container
        self.client = client

    @property
    def name(self) -> str:
        return self.container.name

    @property
    def groups(self) -> list[str]:
        labels = self.container.labels
        return labels.get("watchCat.group", "default").split(" ")

    @property
    def idShort(self) -> str:
        return self.container.short_id

    @property
    def imageName(self) -> str:
        img = self.container.image
        return img.tags[0] if img.tags else "unknown"

    def isUpdateAvailable(self) -> bool:
        img = self.container.image
        repo_digests = img.attrs.get("RepoDigests")

        if not repo_digests or not img.tags:
            logging.debug(f"No RepoDigests or tags for image {self.imageName}.")
            return False

        repo_id_local = repo_digests[0].split("@")[1]

        try:
            img_reg = self.client.images.get_registry_data(self.imageName)
            repo_id_remote = img_reg.id
        except docker.errors.APIError as e:
            logging.error(f"Failed to fetch registry data for image {self.imageName}: {e}")
            return False

        return repo_id_remote != repo_id_local

    def __str__(self) -> str:
        return f"{self.name}, {self.idShort}, {self.isUpdateAvailable()}"