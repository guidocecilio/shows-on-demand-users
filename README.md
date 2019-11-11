# Shows on-demand Auth & Users service

Notice that this is a Microservice that is part of the [Shows on Demand](https://github.com/guidocecilio/shows-on-demand-main) service and it in an early stage

This service is intended to be used with the [Shows on Demand](https://github.com/guidocecilio/shows-on-demand-main) service.

## Installation

### From sources

Clone the Project
```bash
$ git clone https://github.com/guidocecilio/shows-on-demand-users.git
```

Run the app using docker-compose
```bash
$ docker-compose up --build
```

## Initializing the Database and seeding the data
```bash
$ docker exec -it admin-service bash
```
```bash
$ python manage.py initialize_db
```

## Troubleshooting

### Initializing the database
If there are no migrations at the moment you could use the followig Flask command
```bash
$ flask init db stamp head
```

## Contributions, Bug Reports, Feature Requests
This is an POC project. However, it will be soon an Open Source project and we would be happy to see contributors who report bugs and file feature requests submitting pull requests as well.
Ideas are welcome and they can be added as feature here https://github.com/guidocecilio/shows-on-demand-admin/issues. Notice, that as this is a work on progress features will be adding as ticket to https://github.com/guidocecilio/shows-on-demand-admin/issues with the label _enhancement_.
Please report issues here https://github.com/guidocecilio/shows-on-demand-admin/issues. It is also recommended to go through the [high level design document](https://github.com/guidocecilio/shows-on-demand-main/blob/master/docs/hld.md) while the Developer Handbook still a work on progress in order to get a basic understanding of the ecosystem.
