from dockerInteract.watchContainer import WatchContainer
from notify.discord import DiscordNotify
from notify.mail import MailNotify
import logging
from typing import List, Dict


class Notify:
    discord: DiscordNotify
    mail: MailNotify

    def __init__(self, config: Dict) -> None:
        try:
            self.setupGroups(config)
        except Exception as e:
            logging.error(f"Error setting up notification groups: {e}")

    def setupGroups(self, config: Dict) -> None:
        self.discord = DiscordNotify(config)
        self.mail = MailNotify(config)

    def sendNotifications(self, containers: List[WatchContainer]) -> None:
        if not containers:
            logging.info("No containers to notify.")
            return

        for container in containers:
            try:
                self.discord.addContainer(container)
                self.mail.addContainer(container)
            except Exception as e:
                logging.error(
                    f"Error adding container '{container.name}' to notifications: {e}"
                )

        try:
            self.discord.send()
            self.mail.send()
        except Exception as e:
            logging.error(f"Error sending notifications: {e}")
