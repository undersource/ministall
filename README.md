# MiniStall
Shop of virtual goods with cryptocurrency payment system of Monero.

## Features
* Works without javascript
* Cryptocurrency payment system of Monero
* REST API
* Custom captcha
* Can work in Tor/I2P
* Have categories
* Have search

## Dependencies
* Python
* Postgresql
* Nginx
* Systemd
* Monero-wallet-rpc

# Configuration
Site config `config.py`:
```
SECRET_KEY = '000000000000000000000000000000000000000000000000000000000000000000'
DB_NAME = 'ministall'
DB_USER = 'ministall'
DB_PASS = 'ministall'
DB_HOST = '127.0.0.1'
DB_PORT = 5432
MONERO_RPC_USER = 'ministall'
MONERO_RPC_PASS = 'ministall'
MONERO_RPC_ENDPOINT = 'http://127.0.0.1:28080/json_rpc'
```

# Installing
Working directory is in `/var/www/MiniStall`

## Setup and run Postgresql
```
su - postgres -c 'initdb -D /var/lib/postgres/data'
systemctl enable --now postgresql
echo -e "CREATE DATABASE ministall;\nCREATE USER ministall WITH ENCRYPTED PASSWORD 'ministall';\nGRANT ALL PRIVILEGES ON DATABASE ministall TO ministall;" | su - postgres -c 'psql'
```

## Setup Django
```
python -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
./manage.py makemigrations
./manage.py migrate
./manage.py collectstatic
./manage.py createsuperuser
```

## Setup services
```
cp contrib/systemd/MiniStall.service /etc/systemd/system/MiniStall.service
cp contrib/nginx/nginx.conf /etc/nginx/nginx.conf
```

# Setup monero
```
mkdir /var/www/MiniStall/wallets
monero-wallet-cli --generate-new-wallet /var/www/MiniStall/wallets/MiniStall
monero-wallet-rpc --wallet-file /var/www/MiniStall/wallets/MiniStall --password ministall --daemon-address example.com --rpc-bind-port 28080 --rpc-login ministall:ministall
```

# Start
```
systemctl enable --now MiniStall nginx
```