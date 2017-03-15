Python dating site grabber
==========================

## Project' structure ##
```
docs/
    mamba.ipynb         Ipython notebook with samples and tutorials

dating_grabber/
    __init__.py         Package file
    core.py             Implementation of dating site grabber
    models.py           DB schema definitions

tests/
    test_model.py       Tests of DB schema tables

main.py                 main script to run questionary grabber

LICENSE                 License file

README.md               this file with short description of project

requirements.txt        Requirements of libraries and packages

setup.py                Setup file for package installation
```

## Environment setup ##

Install virtualenv

```bash
sudo apt install python-pip
pip install virtualenvwrapper
```

Add next lines to ~/.bashrc (~/.profile)

```bash
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel

# load virtualenvwrapper for python (after custom PATHs)
venvwrap="virtualenvwrapper.sh"
/usr/bin/which $venvwrap
if [ $? -eq 0 ]; then
    venvwrap=`/usr/bin/which $venvwrap`
    source $venvwrap
fi
```

Run script

```bash
. ~/.local/bin/virtualenvwrapper.sh
```

Clone git repository

```bash
git clone https://github.com/onidzelskyi/dating_grabber.git
```

Create virtual environment

```bash
mkvirtualenv -p python3.5 dating_grabber
```

## Install dependencies ##

```bash
cd dating_grabber
pip install -r requirements.txt
```

## install the package locally (for use on our system) ##

```bash
pip install -e .
```

## Run tests ##

```bash
pytest tests
```

## Download firefox driver ##

```bash
http://selenium-python.readthedocs.io/installation.html#drivers
```

## Install firefox browser (ubuntu)##

```bash
sudo apt install firefox
```

## Add PATH environment for selenium firefox driver ##

```bash
export PATH=$PATH:`$(pwd)`
```

## Run questionary grabber ##

```bash
python main.py
```

## Check PEP008 code style ##

```bash
flake8  --max-line-length=120 .
```

## Migrate DB ##

```bash
migrate create migrations "migrations"
python migrations/manage.py version_control mysql+mysqlconnector://root:Pass1234@localhost/mamba?charset=utf8mb4 migrations

python migrations/manage.py db_version mysql+mysqlconnector://root:Pass1234@localhost/mamba?charset=utf8mb4 migrations

migrate manage manage.py --repository=migrations --url=mysql+mysqlconnector://root:Pass1234@localhost/mamba?charset=utf8mb4

python manage.py script "Add question likes"
python manage.py upgrade

python manage.py downgrade 0
```