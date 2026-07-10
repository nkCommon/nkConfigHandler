from confighandler.src.configuration import Configuration





config = Configuration(
    appname="revenue",
    debugging=True,
    ini_file="./database.ini",
)


my_map = config.report_mails
for key, value in my_map.items():
    print(f"{key}: {value}")
    

print(type(config.report_mails))