from dockerInteract.watchCat import WatchCat
from dockerInteract.watchContainer import WatchContainer
from notify.notify import Notify
import schedule
import time
import os
import logging
import fileSystem

class Main:
    config = {}
    def __init__(self) -> None:
        fileSystem.init()
        #loadconfig
        self.config = fileSystem.loadConfigFile()
        #set up scheduel for running periodically
        schedule.every(self.configInterval["every"]).day.at(self.configInterval["time"]).do(self.run)
    
    def loop (self):
        while True:
            #reload config
            self.config = fileSystem.loadConfigFile()
            schedule.run_pending()
            # Sleep until next job
            time.sleep(schedule.idle_seconds())
    
    def run (self):
        print("start scan now")
        #version check of containers
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
    verbose = os.getenv("VERBOSE", "false") == "true"
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    main = Main()

    # Check if RUN_ON_STARTUP environment variable is set to "true"
    if os.getenv("RUN_ON_STARTUP", "false").lower() == "true":
        main.run()

    main.loop()
