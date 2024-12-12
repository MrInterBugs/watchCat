# Manage your notifications in groups

## create a group

Go to the `notification` section in your config.yml file.
```yml
notification:
    default:
        discord: # Rest of config
    backup:
        discord: # Rest of config
    testing:
        discord: # Rest of config
```
Add your group in the stile (default, backup, testing) shown above. **No spaces allowed!** [create notification for every group, see 4.](../README.md#quick-start)


## add a container to a group
Add the config below to your docker-compose.yml file you want to monitor. To add a container to multiple groups use a space.
```yml
labels:
    - "watchCat=True"
    - "watchCat.group=default backup"
```