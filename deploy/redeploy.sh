#!/usr/bin/env bash
# Run on the VM (invoked over SSH by .github/workflows/deploy.yml) to pull
# the latest main and restart the service. Assumes setup-vm.sh already ran.
set -euo pipefail

APP_DIR="/opt/pyrealms"
cd "$APP_DIR"

git fetch origin main
git reset --hard origin/main
.venv/bin/pip install -r requirements.txt
sudo systemctl restart pyrealms
sudo systemctl --no-pager status pyrealms
