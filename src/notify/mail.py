import smtplib
from dockerInteract.watchContainer import WatchContainer
from email.mime.text import MIMEText
import logging


class MailNotify:
    configMap: dict
    containerList: list[WatchContainer]

    def __init__(self, config: dict) -> None:
        self.configMap = {
            groupName: groupConfig["mail"]
            for groupName, groupConfig in config.items()
            if "mail" in groupConfig
        }
        if not self.configMap:
            logging.warning("No groups with 'mail' configuration found.")

    def addContainer(self, container: WatchContainer) -> None:
        if not self.configMap:
            logging.warning("No mail configurations available. Cannot add container.")
            return

        self.containerList.append(container)

    def generateHtml(self, htmlListItems: list[str]) -> str:
        return f"""
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    table {{
                        font-family: arial, sans-serif;
                        border-collapse: collapse;
                        width: 100%;
                    }}
                    td, th {{
                        border: 1px solid #dddddd;
                        text-align: left;
                        padding: 8px;
                    }}
                    tr:nth-child(even) {{
                        background-color: #dddddd;
                    }}
                </style>
            </head>
            <body>
                <h2>Available Updates:</h2>
                <table>
                    <tr>
                        <th>Name</th>
                        <th>ID</th>
                        <th>Image</th>
                    </tr>
                    {"".join(htmlListItems)}
                </table>
            </body>
            </html>
        """

    def send(self) -> None:
        if not self.configMap:
            logging.warning(
                "No mail configurations available. Skipping send operation."
            )
            return

        htmlListItems = []

        for group, config in self.configMap.items():
            groupHasContainer = False

            for container in self.containerList:
                if group in container.groups:
                    groupHasContainer = True
                    htmlListItems.append(
                        f"""
                        <tr>
                            <td>{container.name}</td>
                            <td>{container.idShort}</td>
                            <td>{container.imageName}</td>
                        </tr>
                        """
                    )

            if groupHasContainer:
                fromMail = f"Watch Cat <{config['from_mail']}>"
                toMail = config["to_mail"]

                html = self.generateHtml(htmlListItems)
                msg = MIMEText(html, "html")
                msg["From"] = fromMail
                msg["To"] = ", ".join(toMail)
                msg["Subject"] = "Docker Updates"

                try:
                    with smtplib.SMTP(config["host"], config["port"]) as smtpServer:
                        smtpServer.login(config["user"], config["passwd"])
                        smtpServer.sendmail(fromMail, toMail, msg.as_string())
                except smtplib.SMTPException as e:
                    logging.error(f"Error sending email for group '{group}': {e}")
