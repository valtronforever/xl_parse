# xl_parse
Parse xlsx file with specific data format to json

## Instalation
Open project directory and prepare python virtual env
```
# Ubuntu Linux
sudo apt install python3-venv
python3 -m venv .venv
source .venv/bin/activate

# MacOS
pip install virtualenv
virtualenv .venv
source .venv/bin/activate
```

Install project dependencies:
```
pip install -r requirements.txt
```

## Using
Activate virtual environment (if is not active already):
```
source .venv/bin/activate
```

Run python script with file for parsing as param:
```
python parse.py input.xlsx
```
Result json will be saved to `output.json` file.
Run `python parse.py --help` for additional usage info.

## Run from docker
```
sudo docker run -it --rm --name xl_parse -v "$PWD":/app ghcr.io/valtronforever/xl_parse:latest input.xlsx
```
