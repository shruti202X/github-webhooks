# Dev Assessment - Webhook Receiver

Please use this repository for constructing the Flask webhook receiver.

*******************

## Setup

* Create a new virtual environment

```bash
pip install virtualenv
```

* Create the virtual env

```bash
virtualenv venv
```

* Activate the virtual env

```bash
source venv/bin/activate
```

* Install requirements

```bash
pip install -r requirements.txt
```

* Run the flask application (In production, please use Gunicorn)

```bash
python run.py
```

* The endpoint is at:

```bash
POST http://127.0.0.1:5000/webhook/receiver
```

You need to use this as the base and setup the flask app. Integrate this with MongoDB (commented at `app/extensions.py`)

*******************

# Install MongoDB:

## Official Website
https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/

## Import public key

```bash
curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg \
   --dearmor
```

## Create list file

```bash
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
```

## Reload package Database

```bash
sudo apt-get update
```

## Install mongoDB

```bash
sudo apt-get install -y mongodb-org
```

## Running MongoDB

```bash
sudo systemct start mongod
```

---

# Run MongoDB using Docker

## Pull MongoDB container and run it

```bash
docker --version
docker pull mongo
docker run -d -p 27017:27017 --name mongodb mongo
docker ps
docker exec -it mongodb mongosh
```

## Stop mongodb container

```bash
docker stop mongodb
```

## Restart mongodb container

```bash
docker start mongodb
```

---

# Testing MongoDB

```
use webhookDB

db.events.insertOne({
  "author": "Shruti",
  "action_type": "push",
  "from_branch": "",
  "to_branch": "main",
  "timestamp": new Date().toISOString()
})

db.events.find().pretty()

```