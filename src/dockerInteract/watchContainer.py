import docker


class WatchContainer:
    container: docker.models.containers.Container
    client: docker.DockerClient

    def __init__(self, container: docker.models.containers.Container, client) -> None:
        self.container = container
        self.client = client

    @property
    def name(self):
        return self.container.name

    @property
    def groups(self):
        labels = self.container.labels
        # Check if any group specified if not return default
        if not "watchCat.group" in labels:
            return ["default"]

        # If specified return groups specified
        # Convert to list
        return self.container.labels["watchCat.group"].split(" ")

    @property
    def idShort(self):
        return self.container.short_id

    @property
    def imageName(self):
        img = self.container.image
        return img.tags[0]

    def isUpdateAvailable(self) -> bool:
        # Local image
        img = self.container.image
        try:
            repoIdLocal = img.attrs["RepoDigests"][0].split("@")[1]
        except:
            print(f"unable to find repository for: {self.imageName}")
            self.update = False
            return self.update

        # Remote image
        try:
            img_reg = self.client.images.get_registry_data(self.imageName)
            repo_id_remote = img_reg.id
        except Exception as e:
            # Handle exceptions when fetching remote data
            raise RuntimeError(
                f"Failed to fetch registry data for image {self.imageName}: {e}"
            )

        # Check if update is available
        self.update = repo_id_remote != repoIdLocal
        return self.update

    def toDict (self):
        dataDict = {}

        #adding all data to a dict
        dataDict["name"] = self.name
        dataDict["idShort"] = self.idShort
        dataDict["imageName"] = self.imageName
        dataDict["groups"] = self.groups

        return dataDict

    def __str__ (self):
        return f"{self.name}, {self.idShort}, {self.isUpdateAvilable()}"
