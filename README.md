test

![badge](https://github.com/bunchofstring/dcs/actions/workflows/python-app.yml/badge.svg)

The following command is useful to disconnect all containers from the default network
'''
for i in ` docker network inspect -f '{{range .Containers}}{{.Name}} {{end}}' dap_experiment_default`; do docker network disconnect -f dap_experiment_default $i; done;
'''

Stop all containers
'''
docker stop $(docker container list -q)
'''

Clean up "orphans"
docker-compose down --remove-orphans
