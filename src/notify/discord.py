from discord_webhook import DiscordWebhook, DiscordEmbed
from dockerInteract.watchContainer import WatchContainer

class DiscordNotify:
    configMap:map = {}
    containerList:list[str] = []

    def __init__(self, config:map) -> None:
        for groupName in config:
            if not ('discord' in config[groupName].keys()):
                return
            self.configMap[groupName] = config[groupName]["discord"]

    def addContainer (self, container:WatchContainer):
        # If no discord return
        if self.configMap == {}:
            return
        
        self.containerList.append(container)

    def send (self):
        # If no discord return
        if self.configMap == {}:
            return
        
        # If group setup for discord send message
        for group in self.configMap:
            groupHasContainer = False
            # Set webhook
            webhook = DiscordWebhook(url=self.configMap[group]["url"], content=self.configMap[group].get("onUpdate", ""))
            embed = DiscordEmbed(title=f'Updates available!', color='03b2f8')

            for container in self.containerList:
                # Check group
                if group in container.groups:
                    embed.add_embed_field(name='Name:', value=container.name)
                    embed.add_embed_field(name='ID:', value=container.idShort)
                    embed.add_embed_field(name='Image:', value=container.imageName)
                    
                    groupHasContainer = True

            if groupHasContainer:
                # Send msg
                webhook.add_embed(embed)
                response = webhook.execute()