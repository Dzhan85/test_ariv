# test_ariv
task


## How to use

### 
* Clone your repository

### Build docker image and push to docker repository
* Go to directory `docker-image` and build docker images with using this in your `Dockerfile` and push it:

```Dockerfile


# Your Dockerfile code...

  docker build -t kurbik/web-app .
  
  docker image push kurbik/web-app 
  
```

* But, if you need Python 2.7 that line would have to be `FROM tiangolo/uwsgi-nginx:python2.7`.

* By default it will try to find a uWSGI config file in `/app/uwsgi.ini`.

* That `uwsgi.ini` file will make it try to run a Python file in `/app/main.py`.


## Deploy application to Kubernetes cluster

### Authorize to cluster in console line

```Dockerfile

oc login
az login
gcloud login


```

### Create namespace in cluster

```Dockerfile

kubectl create namespace backend

```


###  Deploy with helm

Tar  directory  `nginx` of repository and run command to deploy it to cluster


```Dockerfile

helm template nginx.tgz | kubectl create --namespace backend -f -

```


### Deploy with ansible 

```Dockerfile

ansible-playbook main.yml

```
### Deploy with terraform


