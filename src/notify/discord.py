from discord_webhook import DiscordWebhook, DiscordEmbed
from dockerInteract.watchContainer import WatchContainer
import logging


class DiscordNotify:
    configMap: dict
    containerList: list[WatchContainer]

    def __init__(self, config: dict) -> None:
        self.configMap = {
            groupName: groupConfig["discord"]
            for groupName, groupConfig in config.items()
            if "discord" in groupConfig
        }
        if not self.configMap:
            logging.warning("No groups with 'discord' configuration found.")

    def addContainer(self, container: WatchContainer) -> None:
        if not self.configMap:
            logging.warning(
                "No Discord configurations available. Cannot add container."
            )
            return

        if any(c.idShort == container.idShort for c in self.containerList):
            logging.debug(
                f"Container '{container.name}' already in the list. Skipping."
            )
            return

        self.containerList.append(container)
        logging.debug(f"Container '{container.name}' added to the list.")

    def send(self) -> None:
        if not self.configMap:
            logging.warning(
                "No Discord configurations available. Skipping send operation."
            )
            return

        if not self.containerList:
            logging.debug("No containers to send updates for. Skipping send operation.")
            return

        for group, config in self.configMap.items():
            webhook_url = config.get("url")
            if not webhook_url:
                logging.error(f"No webhook URL configured for group '{group}'.")
                continue

            webhook = DiscordWebhook(
                url=webhook_url, content=config.get("onUpdate", "")
            )
            embed = DiscordEmbed(title="🚀 Update Available!", color="03b2f8")

            groupHasContainer = False
            for container in self.containerList:
                if group in container.groups:
                    embed.add_embed_field(
                        name="🛠 **Container Details**",
                        value=(
                            f"**Name:** `{container.name}`\n"
                            f"**ID:** `{container.idShort}`\n"
                            f"**Image:** `{container.imageName}`"
                        ),
                        inline=False,
                    )
                    groupHasContainer = True

            embed.set_footer(text="Powered by WatchCat 🐱")

            if groupHasContainer:
                try:
                    webhook.add_embed(embed)
                    response = webhook.execute()
                    if response.status_code == 200:
                        logging.debug(f"Successfully sent update for group '{group}'.")
                    else:
                        logging.error(
                            f"Failed to send update for group '{group}'. HTTP Status: {response.status_code}"
                        )
                except Exception as e:
                    logging.error(f"Error sending webhook for group '{group}': {e}")

        self.containerList.clear()
