#!/usr/bin/env bash
# Sets up your web servers for the deployment of web_static.
if ! dpkg -l | grep -q "nginx";then
    sudo apt-get -y update
    sudo apt-get install -y nginx
fi
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
sudo touch /data/web_static/releases/test/index.html
echo -e '<h1>Hello world!</h1>' | sudo tee /data/web_static/releases/test/index.html > /dev/null
sudo ln -sf /data/web_static/releases/test /data/web_static/current
sudo chown -R "ubuntu":"ubuntu" /data/
sudo sed -i 's#^}$#\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n&#' /etc/nginx/sites-enabled/default
sudo service nginx restart
