## Overview

This is a dashboard to display all the movies uploaded by the user

## System  Pre-requisites

### Written for MacOS

#### Required packages

Following are the dependencies required to be installed on your system for the project to work

* A Good IDE (PyCharm/IntelliJ is recommended)
* Python
* Virtual Environment
* Mongo (4.4)
* redis

Before proceeding, make sure Homebrew is installed on your system. If it's not installed, you can install it by running the following command in your Terminal:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" 
```
Following these instructions will set up MongoDB 4.4 and Redis as services on your MacOS system. They will start automatically at login, ensuring they are available for your projects.
`brew tap mongodb/brew`
`brew install mongodb-community@4.4`
`brew services start mongodb/brew/mongodb-community@4.4`
`brew install redis`
`brew services start redis`

Create `moviesDB` Database by running `mongod`. 



## Getting started for Ubuntu and macOS

Clone the project into your development directory. Import the project using PyCharm.
Once the project is imported create a new Python SDK using virtual environment using:

`python -m venv ./venv`

Next, activate the venv for your project:

`source .venv/bin/activate`

Now, you should see `(.venv)` at the start of your prompt.
Now you can install all the dependencies by typing the following.

`pip install -r requirements.txt`


A utility named `run.py` is provided in the project. It has commands as follows:

* `python run.py`: This will run the server on port 5000 with dev environment.
* `python celery_worker.py`: This will run the consumer listing job with dev environment.
