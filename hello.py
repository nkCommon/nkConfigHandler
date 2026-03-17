from confighandler.src.configuration import Configuration





config = Configuration(
    appname="indkomstopslag",
    debugging=True,
    ini_file="./database.ini",
)


my_map = config.indkomsttype_map
for key, value in my_map.items():
    print(f"{key}: {value}")
    

print(type(config.indkomsttype_map))