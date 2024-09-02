#!/bin/bash
# put inside /etc/cron.hourly/ and restart cron with /etc/init.d/cron restart
apt-get -y dist-upgrade
apt-get update
#apt -y autoremove
