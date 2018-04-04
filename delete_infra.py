import json
import os

infra_config = json.load(open("config/infra_config.json"))
private_networks = infra_config["private_networks"].keys()
public_networks = infra_config["public_networks"].keys()

#DELETE ALL THE CONTAINERS
os.system("docker rm $(docker ps -a -q) --force")

#DELETE PRIVATE NETWORKS
for p in private_networks:
    os.system("docker network rm {0}".format(p))

#DELETE PUBLIC NETWORKS
for p in public_networks:
    os.system("docker network rm {0}".format(p))
