#!/bin/bash
# put inside /etc/cron.hourly/ and restart cron with /etc/init.d/cron restart
# edit cd path

#cp -a c9/ /var/www 
cd /var/www/
if $(ps aux | grep -q "server.js") ; then
  echo "found js" ;
else
  sudo -u www-data -s node server.js -p 8081 -a c9:agurk666&
fi
if $(ps aux | grep -q "backendserver.py") ; then
  echo "found py" ;
else
  cd /var/www/rockefellerthrust/
  sudo -u www-data -s .venv/bin/python /var/www/*/backendserver.py&
  #/var/www/*/backendserver.py
  chown www-data:www-data /var/www/*/uploads/*
  chmod gu+wr /var/www/*/uploads/*
fi

apt-get -y dist-upgrade
apt-get update
#apt -y autoremove