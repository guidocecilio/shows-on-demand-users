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