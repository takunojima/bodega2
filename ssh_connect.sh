#!/bin/bash

# エラー時に停止
set -e

# デフォルト値の設定
SERVER_IP="your-server-ip"
SSH_USER="your-username"
SSH_KEY_PATH="$HOME/.ssh/id_rsa"
SSH_PORT=22

# ヘルプメッセージの表示関数
show_help() {
    echo "Usage: $0 [options]"
    echo "Options:"
    echo "  -i, --ip IP_ADDRESS    Server IP address"
    echo "  -u, --user USERNAME    SSH username"
    echo "  -k, --key KEY_PATH     Path to SSH private key"
    echo "  -p, --port PORT        SSH port (default: 22)"
    echo "  -h, --help            Show this help message"
    exit 1
}

# コマンドライン引数の解析
while [[ $# -gt 0 ]]; do
    case $1 in
        -i|--ip)
            SERVER_IP="$2"
            shift 2
            ;;
        -u|--user)
            SSH_USER="$2"
            shift 2
            ;;
        -k|--key)
            SSH_KEY_PATH="$2"
            shift 2
            ;;
        -p|--port)
            SSH_PORT="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            ;;
    esac
done

# 必要な値が設定されているか確認
if [[ "$SERVER_IP" == "your-server-ip" ]] || [[ "$SSH_USER" == "your-username" ]]; then
    echo "Error: Server IP and SSH username must be specified"
    show_help
fi

# SSH鍵の存在確認
if [[ ! -f "$SSH_KEY_PATH" ]]; then
    echo "Error: SSH key not found at $SSH_KEY_PATH"
    exit 1
fi

# SSH接続の試行
echo "Connecting to $SSH_USER@$SERVER_IP..."
ssh -i "$SSH_KEY_PATH" -p "$SSH_PORT" "$SSH_USER@$SERVER_IP" 