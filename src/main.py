from dockerInteract.watchCat import WatchCat
from dockerInteract.watchContainer import WatchContainer
from notify.notify import Notify
import schedule
import time
import yaml
import os
import logging

CONFIG_FILE_PATH = "/usr/src/config/config.yml"


class Main:
    def __init__(self) -> None:
        self.loadConfigFile()
        schedule.every(self.configInterval["every"]).day.at(
            self.configInterval["time"]
        ).do(self.run)

    def loop(self) -> None:
        while True:
            schedule.run_pending()
            time.sleep(schedule.idle_seconds())
            self.loadConfigFile()

    def loadConfigFile(self) -> None:
        if not os.path.exists(CONFIG_FILE_PATH):
            logging.error("Config file not found at %s", CONFIG_FILE_PATH)
            exit(1)

        with open(CONFIG_FILE_PATH, "r") as file:
            self.config = yaml.safe_load(file)
        logging.info("Configuration file loaded successfully.")

    def run(self) -> None:
        logging.info("Starting scan now.")
        cat = WatchCat()
        cat.getMonitoredContainers()
        updatableList: list[WatchContainer] = cat.getContainersWithUpdates()

        if not updatableList:
            logging.info("No containers to update.")
            return

        logging.info("Sending notifications.")
        notify = Notify(self.configNotify)
        notify.sendNotifications(updatableList)

    @property
    def configNotify(self) -> dict:
        return self.config["notification"]

    @property
    def configInterval(self) -> dict:
        return self.config["interval"]


if __name__ == "__main__":
    verbose = os.getenv("VERBOSE", "false").lower() == "true"
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    main = Main()

    if os.getenv("RUN_ON_STARTUP", "false").lower() == "true":
        main.run()

    main.loop()
