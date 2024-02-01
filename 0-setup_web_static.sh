#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static
sudo apt-get -y update && sudo apt-get -y upgrade
# Check if Nginx is installed, if not proceed to install
if ! command -v nginx &> /dev/null; then
    sudo apt-get -y install nginx
fi
sudo ufw allow 'nginx HTTP'
sudo service nginx start
# Create directories if they dont exist, -p ensures
# parent dirs are created as well
if [ ! -d "/data/web_static/releases/test/" ]; then
    sudo mkdir -p /data/web_static/releases/test/
fi
if [ ! -d "/data/web_static/shared/" ]; then
    sudo mkdir -p /data/web_static/shared/
fi
# Fake HTML file created
string="
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"
echo "$string" | sudo tee /data/web_static/releases/test/index.html
# Remove symbolic link if exists (-f) before creating a new one
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
# Configure Nginx to serve alias content
if ! sudo grep -q "alias /data/web_static/current/;" /etc/nginx/sites-enabled/default; then
    sudo sed -i "\#server_name _;#a \\
        location /hbnb_static { \\
            alias /data/web_static/current/; \\
        } \\
        "  /etc/nginx/sites-enabled/default
fi
sudo chown -R ubuntu:ubuntu /data/
sudo service nginx reload
