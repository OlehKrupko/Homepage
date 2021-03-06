cd ~/Projects/Homepage/

# install Xcode with command line tools OR only tools with command:
xcode-select --install
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install python3
### PyCharm install:
# Django
# beautifulsoup4
# collective.soupstrainer
# feedparser
# lxml
# requests

# not sure if works:
sudo python3 -m pip install django~=2.0.2 beautifulsoup4 collective.soupstrainer feedparser lxml requests

python3 ~/Projects/Homepage/manage.py makemigrations
python3 ~/Projects/Homepage/manage.py migrate
python3 ~/Projects/Homepage/manage.py createsuperuser

sudo systemctl stop homepage.server.service; cd /home/pi/Projects/Homepage; git pull; sudo systemctl start homepage.server.service
