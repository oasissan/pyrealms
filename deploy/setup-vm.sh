#!/usr/bin/env bash
# One-time bootstrap for a fresh Oracle Cloud "Always Free" Ubuntu VM.
# Run this yourself over SSH after creating the instance:
#   ssh -i <your-key> ubuntu@<vm-public-ip>
#   curl -fsSL https://raw.githubusercontent.com/<you>/<repo>/main/deploy/setup-vm.sh | bash -s -- https://github.com/<you>/<repo>.git
set -euo pipefail

REPO_URL="${1:?Usage: setup-vm.sh <git-clone-url>}"
APP_DIR="/opt/pyrealms"
SERVICE_USER="$(whoami)"

sudo apt-get update -y
sudo apt-get install -y python3-venv python3-pip git

if [ -d "$APP_DIR/.git" ]; then
  git -C "$APP_DIR" pull
else
  sudo git clone "$REPO_URL" "$APP_DIR"
  sudo chown -R "$SERVICE_USER":"$SERVICE_USER" "$APP_DIR"
fi

cd "$APP_DIR"
python3 -m venv .venv
.venv/bin/pip install --upgrade pip -q
.venv/bin/pip install -r requirements.txt

if [ ! -f "$APP_DIR/.env" ]; then
  cat > "$APP_DIR/.env" <<'EOF'
# Uncomment and set to protect the public URL with HTTP Basic Auth.
# The grader executes submitted code unsandboxed — see README.
# APP_USERNAME=
# APP_PASSWORD=
EOF
  echo "Created $APP_DIR/.env — edit it to set APP_USERNAME/APP_PASSWORD, then restart the service."
fi

sudo tee /etc/systemd/system/pyrealms.service > /dev/null <<EOF
[Unit]
Description=PyRealms
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$APP_DIR
EnvironmentFile=-$APP_DIR/.env
ExecStart=$APP_DIR/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now pyrealms

echo "Done. Check status with: sudo systemctl status pyrealms"
echo "Remember to open TCP/8000 in the VCN's Security List (see DEPLOY.md)."
