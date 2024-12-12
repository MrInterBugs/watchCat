# watch cat

Tired of checking if your docker containers are up to date manually? Watch cat checks all specified containers periodically for updates from the registry and notifies you.


## futures

 - Allows you to specify which containers should be monitored
 - Specify who to contact when updates are available via groups
 - Specify check cycle
 - Run at specified time

| Message Service  | Status |
|------------------|--------|
| discord          | ✅     |
| email            | ✅     |

## quick start

 1. Download the Docker-Compose file & and **change the timezone to suit you**:

    ```bash
    wget https://raw.githubusercontent.com/Salero-tech/watchCat/main/docker-compose.yml
    ```

    Optionally set the value of the environment variable `RUN_ON_STARTUP` to true to enable run on startup. 

 2. Create config folder & download config file [example config](examples/config.yml):

    ```bash
    mkdir config && cd config && wget https://raw.githubusercontent.com/Salero-tech/watchCat/main/src/config/config.yml
    ```

 3. Edit the config file for your preferred update cycle;
    - **every** specifies the interval of days.
    - **time** is the time of day the update check runs.

    ```yml
    interval:
        every: 1 # Every day: 1, every two days: 2, etc
        time: "02:30" # Run at 2:30 in the morning
    ```

 4. To setup your notification:
    - [Organize notifications in groups](docs/group.md)
    - [Discord](docs/discord.md)
    - [Mail](docs/mail.md)

 5. Add container to be monitored (if no group is specified the container is added to group "default"; [more details](docs/group.md)): <br>
    docker-compose [examples](examples/docker-compose.yml):

    ```yml
    labels:
        - "watchCat=True"
        - "watchCat.group=default"
    ```

    CLI:

    ```bash
    docker run -l watchCat=True hello-world:latest
    ```

 6. Start the container:

    ```bash
    docker-compose up -d
    ```

# Contribution 

If you want to contribute or need help feel free to open a issue/pull request.