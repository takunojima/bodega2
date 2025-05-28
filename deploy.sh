#!/bin/bash

# エラー時に停止
set -e

echo "Starting deployment process..."

# アプリケーションディレクトリの作成
echo "Creating application directory..."
sudo mkdir -p /var/www/bodegashift
cd /var/www/bodegashift

# 必要なパッケージのインストール
echo "Installing system dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-venv

# Python仮想環境の作成
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 必要なPythonパッケージのインストール
echo "Installing Python packages..."
pip install flask flask-sqlalchemy flask-login python-dotenv gunicorn

# アプリケーションコードのコピー
echo "Copying application code..."
sudo cp -r /path/to/your/application/* /var/www/bodegashift/
sudo chown -R www-data:www-data /var/www/bodegashift

# .envファイルの作成
echo "Creating .env file..."
sudo tee .env > /dev/null << 'EOF'
SECRET_KEY=your-secret-key-change-this
DATABASE_URL=sqlite:///app.db
LINE_CHANNEL_ID=your-line-channel-id
LINE_CHANNEL_SECRET=your-line-channel-secret
SERVER_NAME=bodegashift.com
PREFERRED_URL_SCHEME=http
LINE_CALLBACK_URL=http://bodegashift.com/auth/line/callback
FLASK_ENV=production
EOF

# systemdサービスファイルの作成
echo "Creating systemd service..."
sudo tee /etc/systemd/system/bodegashift.service > /dev/null << 'EOF'
[Unit]
Description=Bodega Shift Management Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/bodegashift
Environment="PATH=/var/www/bodegashift/venv/bin"
ExecStart=/var/www/bodegashift/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 run:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# データベースの初期化
echo "Initializing database..."
flask db upgrade

# サービスの有効化と起動
echo "Starting application service..."
sudo systemctl enable bodegashift
sudo systemctl start bodegashift

echo "Deployment completed successfully!" 