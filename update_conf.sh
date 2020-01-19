#!/bin/bash
# update tracker nginx config file

c=$(ps -ef | grep "fdfs_trackerd" | grep -v "grep" | wc -l)
if [ $c -gt 0 ]; then
  #generate tracker_group[n].conf
  python /nginx_conf/update_conf.py

  rm -rf  /usr/local/nginx/conf/conf.d/*
  cp -f /nginx_conf/conf.d/tracker.conf /usr/local/nginx/conf/conf.d/

  #
  echo "restart nginx..."
  /usr/local/nginx/sbin/nginx -s reload
fi

