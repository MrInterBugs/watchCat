from dockerInteract.watchCat import WatchCat
from dockerInteract.watchContainer import WatchContainer
from notify.notify import Notify
import schedule
import time
import yaml
import os
import logging

CONFIG_FILE_PATH = '/usr/src/config/config.yml'

class Main:
    def __init__(self) -> None:
        self.loadConfigFile()

        # Set up schedule for running periodically
        schedule.every(self.configInterval["every"]).day.at(self.configInterval["time"]).do(self.run)
    
    def loop(self):
        while True:
            schedule.run_pending()
            # Sleep until next job
            time.sleep(schedule.idle_seconds())
            # Reload config
            self.loadConfigFile()

    def loadConfigFile(self):
        # Check if config file exists
        if not os.path.exists(CONFIG_FILE_PATH):
            logging.error("Config file not found at %s", CONFIG_FILE_PATH)
            exit(1)

        # Load YAML config
        with open(CONFIG_FILE_PATH, 'r') as file:
            self.config = yaml.safe_load(file)
        logging.info("Configuration file loaded successfully.")

    def run(self):
        logging.info("Starting scan now.")
        # Version check of containers
        cat = WatchCat()
        cat.getMonitoredContainers()
        updatableList: list[WatchContainer] = cat.getContainersWithUpdates()

        # All containers up to date?
        if len(updatableList) == 0:
            logging.info("No containers to update.")
            return

        logging.info("Sending notifications.")
        # Notify for updates
        notify = Notify(self.configNotify)
        notify.sendNotifications(updatableList)

    # Data
    @property
    def configNotify(self):
        return self.config["notification"]

    @property
    def configInterval(self):
        return self.config["interval"]


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    main = Main()

    # Check if RUN_ON_STARTUP environment variable is set to "true"
    if os.getenv("RUN_ON_STARTUP", "false").lower() == "true":
        main.run()

    main.loop()
