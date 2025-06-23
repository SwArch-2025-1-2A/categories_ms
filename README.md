## Table of contents

- [Categories Microservice](#categories-microservice)
  - [Table of contents](#table-of-contents)
  - [Environment variables](#environment-variables)
    - [Generating a working `.env` file](#generating-a-working-env-file)  
  - [Building the project](#building-the-project)
    - [Building with docker](#building-with-docker)
    - [Partially clean enviroment](#partially-clean-enviroment)
    - [Fully clean environment](#fully-clean-environment)
  - [Running the project](#running-the-project)
    - [Using Docker to run](#using-docker-to-run)
      - [Running without rebuilding](#running-without-rebuilding)
      - [Running while rebuilding images](#running-while-rebuilding-images)

---

## Environment variables

Many configurations can be set configuring a `.env` file. If you want
to see and example about it, please go to [this file](./.env.example).

> [!NOTE]
> Once you have [created](#generating-a-working-env-file) your `.env`
> file, you can run any docker command for
> [building](#building-with-docker) or [running](#using-docker-to-run)
> the project without having to do any extra work.

### Generating a working `.env` file

To generate a file based on a working template run this command:

```sh
cp .env.example .env
```

## Building the project

The recommended way to build the project is to use Docker
[(click here)](#building-with-docker), as it ensures that the build environment
is consistent and eliminates any potential issues with dependencies on your
local machine. 

### Building with docker

> [!IMPORTANT]
> Make sure your `.dockerignore` file is set up correctly to exclude any
> unnecessary files. Like so:

```sh
cat .gitignore .prodignore > .dockerignore
```

> [!TIP]
> You can modify the behavior of the software system like
> ports, hostnames and more by using a `.env` file. Please refer to
> [this section](#environment-variables) for more information.

To build the whole project using Docker, you can use the provided
[docker-compose.yml](./docker-compose.yml). This will take care of everything related
to the building and running processes, including each needed service to run the
project locally. You can start from a
[partially](#partially-clean-enviroment) clean environment or from a
[clean environmentment](#fully-clean-environment).

### Partially clean enviroment

> [!TIP]
> If you want to have a _almost_ clean build you need to stop
> and remove containers, networks by running:

```sh
docker compose down --remove-orphans
```

### Fully clean environment

> [!WARNING]
> The following command gives you a clean slate to start from, but it
> remove the volumes too. So any data that you may have, it will be
> removed as well.

```sh
docker compose down --remove-orphans --volumes
```

## Running the project

### Using Docker to run

> [!TIP]
> You can modify the behavior of the software system like
> ports, hostnames and more by using a `.env` file. Please refer to
> [this section](#environment-variables) for more information.

We personally recommend [this option](#running-while-rebuilding-images).

#### Running without rebuilding

It doesn't contemplate the current state of your files but the most recent built
images. Make sure it is in the correct [`mode`](#modes)

```sh
docker compose up
```

#### Running while rebuilding images

This will allow you to start from the current version of your repository.
This means that if you modified any file included in Docker, a new image will be
built in the [default mode](#building-modes-in-docker) and run after the
building process has been completed

```sh
docker compose up --build
```
