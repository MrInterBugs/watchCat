from discord_webhook import DiscordWebhook, DiscordEmbed
from dockerInteract.watchContainer import WatchContainer
import logging

class DiscordNotify:
    configMap: dict = {}
    containerList: list[WatchContainer] = []

    def __init__(self, config: dict) -> None:
        try:
            for groupName in config:
                if 'discord' not in config[groupName].keys():
                    logging.warning(f"Group '{groupName}' does not have a 'discord' configuration.")
                    continue
                self.configMap[groupName] = config[groupName]["discord"]
            if not self.configMap:
                logging.warning("No groups with 'discord' configuration found.")
        except Exception as e:
            logging.error(f"Error initializing DiscordNotify: {e}")

    def addContainer(self, container: WatchContainer):
        try:
            if not self.configMap:
                logging.warning("No Discord configurations available. Cannot add container.")
                return

            self.containerList.append(container)
            logging.debug(f"Container '{container.name}' added to the list.")
        except Exception as e:
            logging.error(f"Error adding container: {e}")

    def send(self):
        try:
            if not self.configMap:
                logging.warning("No Discord configurations available. Skipping send operation.")
                return

            if not self.containerList:
                logging.debug("No containers to send updates for. Skipping send operation.")
                return

            for group in self.configMap:
                groupHasContainer = False
                webhook_url = self.configMap[group].get("url")

                if not webhook_url:
                    logging.error(f"No webhook URL configured for group '{group}'.")
                    continue

                webhook = DiscordWebhook(url=webhook_url, content=self.configMap[group].get("onUpdate", ""))
                embed = DiscordEmbed(title='Update available!', color='03b2f8')

                for container in self.containerList:
                    if group in container.groups:
                        try:
                            embed.add_embed_field(name='Name:', value=container.name, inline=False)
                            embed.add_embed_field(name='ID:', value=container.idShort, inline=False)
                            embed.add_embed_field(name='Image:', value=container.imageName, inline=False)
                            groupHasContainer = True
                        except Exception as e:
                            logging.error(f"Error adding container fields to embed: {e}")

                if groupHasContainer:
                    try:
                        webhook.add_embed(embed)
                        response = webhook.execute()
                        if response.status_code == 200:
                            logging.debug(f"Successfully sent update for group '{group}'.")
                        else:
                            logging.error(f"Failed to send update for group '{group}'. HTTP Status: {response.status_code}")
                    except Exception as e:
                        logging.error(f"Error sending webhook for group '{group}': {e}")
                else:
                    logging.debug(f"No containers found for group '{group}'. Skipping webhook send.")
        except Exception as e:
            logging.error(f"Error in send method: {e}")
