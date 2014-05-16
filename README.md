carteblanche-django-starter
===============================

CarteBlanche Django Starter App

Installation
------------

#install system programs
sudo su
apt-get -y install python-pip python2.7-dev git nodejs npm libpq-dev python-dev redis-server
pip install virtualenvwrapper 
#link node if needed
ln -s /usr/bin/nodejs /usr/bin/node
npm install -g bower
npm install --save bower-requirejs
#add variables to environment
sh -c "echo 'export WORKON_HOME=$HOME/.virtualenvs' >> ~/.bashrc"
sh -c "echo 'export PROJECT_HOME=$HOME/directory-you-do-development-in' >> ~/.bashrc"
sh -c "echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc"
sh -c "echo 'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc"
sh -c "echo 'export NODE_PATH=$HOME/local/lib/node_modules' >> ~/.bashrc"
exit
#reload
bash --login
#setup virtualenv
mkvirtualenv indiepen
git clone f4c89463a2b7744be2da647275818ab8be385fe9:@github.com:neuman/indiepen.git
pip install -r indiepen/requirements.txt
bower install indiepen
#start the server
sudo gunicorn indiepen.wsgi:application --bind 0.0.0.0:80
#start the celery daemon
python manage.py celery worker --loglevel=info
