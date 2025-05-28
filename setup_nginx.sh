#!/bin/bash

# エラー時に停止
set -e

echo "Nginx setup script starting..."

# Nginxのインストール
echo "Installing Nginx..."
sudo apt update
sudo apt install -y nginx

# Nginxの設定ファイル作成
echo "Creating Nginx configuration..."
sudo tee /etc/nginx/sites-available/bodegashift.com > /dev/null << 'EOF'
server {
    listen 80;
    listen [::]:80;
    
    server_name bodegashift.com www.bodegashift.com;
    
    access_log /var/log/nginx/bodegashift.access.log;
    error_log /var/log/nginx/bodegashift.error.log;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /static {
        alias /var/www/bodegashift/app/static;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location = /favicon.ico {
        alias /var/www/bodegashift/app/static/favicon.ico;
        access_log off;
        log_not_found off;
    }

    location = /robots.txt {
        alias /var/www/bodegashift/app/static/robots.txt;
        access_log off;
        log_not_found off;
    }

    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
}
EOF

# シンボリックリンクの作成
echo "Creating symbolic link..."
sudo ln -sf /etc/nginx/sites-available/bodegashift.com /etc/nginx/sites-enabled/

# デフォルト設定の無効化
echo "Removing default configuration..."
sudo rm -f /etc/nginx/sites-enabled/default

# ディレクトリ構造の作成
echo "Creating directory structure..."
sudo mkdir -p /var/www/bodegashift/app/static
sudo chown -R www-data:www-data /var/www/bodegashift

# Nginxの設定テスト
echo "Testing Nginx configuration..."
sudo nginx -t

# Nginxの再起動
echo "Restarting Nginx..."
sudo systemctl restart nginx

# ファイアウォールの設定
echo "Configuring firewall..."
sudo ufw allow 80
sudo ufw allow 'Nginx HTTP'

echo "Nginx setup completed successfully!" 