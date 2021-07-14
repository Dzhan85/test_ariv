# test_ariv
task


## How to use

* You shouldn't have to clone the GitHub repo. You should use it as a base image for other images, using this in your `Dockerfile`:

```Dockerfile
FROM tiangolo/uwsgi-nginx:python3.8

# Your Dockerfile code...
```

* But, if you need Python 2.7 that line would have to be `FROM tiangolo/uwsgi-nginx:python2.7`.

* By default it will try to find a uWSGI config file in `/app/uwsgi.ini`.

* That `uwsgi.ini` file will make it try to run a Python file in `/app/main.py`.


## Advanced usage

###  app directory

If you need to use a directory for your app different than `/app`, you can override the uWSGI config file path with an environment variable `UWSGI_INI`, and put your custom `uwsgi.ini` file there.

For example, if you needed to have your application directory in `/application` instead of `/app`, your `Dockerfile` would look like:

```Dockerfile

ENV UWSGI_INI /application/uwsgi.ini

COPY ./application /application
WORKDIR /appapplication
```

And your `uwsgi.ini` file in `./application/uwsgi.ini` would contain:

```ini
[uwsgi]
wsgi-file=/application/main.py
```


### Custom uWSGI process number

the image starts with 2 uWSGI processes running. When the server is experiencing a high load, it creates up to 16 uWSGI processes to handle it on demand.

If you need to configure these numbers you can use environment variables.

The starting number of uWSGI processes is controlled by the variable `UWSGI_CHEAPER`, by default set to `2`.

The maximum number of uWSGI processes is controlled by the variable `UWSGI_PROCESSES`, by default set to `16`.

 `UWSGI_CHEAPER` must be lower than `UWSGI_PROCESSES`.


```Dockerfile

ENV UWSGI_CHEAPER 4
ENV UWSGI_PROCESSES 64

COPY ./app /app
```

### Custom max upload size

In this image, Nginx is configured to allow unlimited upload file sizes. This is done because by default a simple Python server would allow that, so that's the simplest behavior a developer would expect.

If you need to restrict the maximum upload size in Nginx, you can add an environment variable `NGINX_MAX_UPLOAD` and assign a value corresponding to the [standard Nginx config `client_max_body_size`](http://nginx.org/en/docs/http/ngx_http_core_module.html#client_max_body_size).

For example, if you wanted to set the maximum upload file size to 1 MB (the default in a normal Nginx installation), you would need to set the `NGINX_MAX_UPLOAD` environment variable to the value `1m`. Then the image would take care of adding the corresponding configuration file (this is done by the `entrypoint.sh`).

So, your `Dockerfile` would look something like:

```Dockerfile
FROM tiangolo/uwsgi-nginx:python3.8

ENV NGINX_MAX_UPLOAD 1m

COPY ./app /app
```

### Custom listen port

By default, the container made from this image will listen on port 80.

To change this behavior, set the `LISTEN_PORT` environment variable.

You might also need to create the respective `EXPOSE` Docker instruction.

You can do that in your `Dockerfile`, it would look something like:

```Dockerfile

ENV LISTEN_PORT 8080

EXPOSE 8080

COPY ./app /app
```

### Custom `/app/prestart.sh`

If you need to run anything before starting the app, you can add a file `prestart.sh` to the directory `/app`. The image will automatically detect and run it before starting everything.

For example, if you want to add database migrations that are run on startup (e.g. with Alembic, or Django migrations), before starting the app, you could create a `./app/prestart.sh` file in your code directory (that will be copied by your `Dockerfile`) with:

```bash
#! /usr/bin/env bash

# Let the DB start
sleep 10;
# Run migrations
alembic upgrade head
```

and it would wait 10 seconds to give the database some time to start and then run that `alembic` command (you could update that to run Django migrations or any other tool you need).

If you need to run a Python script before starting the app, you could make the `/app/prestart.sh` file run your Python script, with something like:

```bash
#! /usr/bin/env bash

# Run custom Python script before starting
python /app/my_custom_prestart_script.py
```

**Note**: The image uses `.` to run the script (as in `. /app/prestart.sh`), so for example, environment variables would persist. If you don't understand the previous sentence, you probably don't need it.

### Custom Nginx processes number

By default, Nginx will start one "worker process".

If you want to set a different number of Nginx worker processes you can use the environment variable `NGINX_WORKER_PROCESSES`.

You can use a specific single number, e.g.:

```Dockerfile
ENV NGINX_WORKER_PROCESSES 2
```

or you can set it to the keyword `auto` and it will try to autodetect the number of CPUs available and use that for the number of workers.

For example, using `auto`, your Dockerfile could look like:

```Dockerfile
FROM tiangolo/uwsgi-nginx:python3.8

ENV NGINX_WORKER_PROCESSES auto

COPY ./app /app
```

### Custom Nginx maximum connections per worker

By default, Nginx will start with a maximum limit of 1024 connections per worker.

If you want to set a different number you can use the environment variable `NGINX_WORKER_CONNECTIONS`, e.g:

```Dockerfile
ENV NGINX_WORKER_CONNECTIONS 2048
```

It cannot exceed the current limit on the maximum number of open files. See how to configure it in the next section.

### Custom Nginx maximum open files

The number connections per Nginx worker cannot exceed the limit on the maximum number of open files.

You can change the limit of open files with the environment variable `NGINX_WORKER_OPEN_FILES`, e.g.:

```Dockerfile
ENV NGINX_WORKER_OPEN_FILES 2048
```

### Customizing Nginx additional configurations

If you need to configure Nginx further, you can add `*.conf` files to `/etc/nginx/conf.d/` in your `Dockerfile`.

Just have in mind that the default configurations are created during startup in a file at `/etc/nginx/conf.d/nginx.conf` and `/etc/nginx/conf.d/upload.conf`. So you shouldn't overwrite them. You should name your `*.conf` file with something different than `nginx.conf` or `upload.conf`, for example: `custom.conf`.

**Note**: if you are customizing Nginx, maybe copying configurations from a blog or a StackOverflow answer, have in mind that you probably need to use the [configurations specific to uWSGI](http://nginx.org/en/docs/http/ngx_http_uwsgi_module.html), instead of those for other modules, like for example, `ngx_http_fastcgi_module`.

### Overriding Nginx configuration completely

If you need to configure Nginx even further, completely overriding the defaults, you can add a custom Nginx configuration to `/app/nginx.conf`.

It will be copied to `/etc/nginx/nginx.conf` and used instead of the generated one.

Have in mind that, in that case, this image won't generate any of the Nginx configurations, it will only copy and use your configuration file.

That means that all the environment variables described above that are specific to Nginx won't be used.

It also means that it won't use additional configurations from files in `/etc/nginx/conf.d/*.conf`, unless you explicitly have a section in your custom file `/app/nginx.conf` with:

```conf
include /etc/nginx/conf.d/*.conf;
```

If you want to add a custom `/app/nginx.conf` file but don't know where to start from, you can use [the `nginx.conf` used for the tests]
