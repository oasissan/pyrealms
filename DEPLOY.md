# Deploying to Oracle Cloud "Always Free"

This gets PyRealms running on a real, always-on VM at no cost,
with `git push` to `main` auto-deploying via GitHub Actions.

**I can't do the account/VM creation for you** — it requires your identity,
a payment card (for verification only; Always Free resources aren't
charged), phone verification, and accepting Oracle's ToS. Steps 1–5 below
are manual. Everything after that (the server setup, the deploy pipeline)
is scripted and ready in this repo.

⚠️ **Security note:** the code grader (`app/grading.py`) runs submitted
Python via `subprocess` with only a timeout + memory cap — not a real
sandbox. That's fine on your laptop; it's a real risk once the URL is
public. Step 8 sets up HTTP Basic Auth to close that off — don't skip it.

## 1. Create an Oracle Cloud account

Go to [cloud.oracle.com](https://cloud.oracle.com) → **Start for free**.
Verify email and phone, add a card for identity verification. Pick your
home region (can't be changed later for Always Free resources).

## 2. Create the VM instance

Compute → Instances → **Create Instance**.
- **Image**: Canonical Ubuntu 22.04 (change the default if needed)
- **Shape**: click "Change shape" → Ampere → `VM.Standard.A1.Flex`, 1 OCPU /
  6 GB memory (Always Free eligible), or the free `VM.Standard.E2.1.Micro`
  if A1 capacity isn't available in your region
- **SSH keys**: let Oracle generate a key pair and download the private key
  (or paste your own public key)

Create it, wait for it to reach "Running", and note its **public IP**.

## 3. Open the firewall for the app port

Networking → Virtual Cloud Networks → your VCN → the subnet's **Security
List** → Add Ingress Rule:
- Source CIDR: `0.0.0.0/0`
- Destination port: `8000`
- Protocol: TCP

## 4. Push this repo to GitHub (if you haven't already)

```bash
gh repo create pyrealms --source=. --public --push
```

## 5. SSH in and run the bootstrap script

```bash
chmod 400 /path/to/downloaded-key.pem
ssh -i /path/to/downloaded-key.pem ubuntu@<vm-public-ip>
curl -fsSL https://raw.githubusercontent.com/oasissan/pyrealms/main/deploy/setup-vm.sh \
  | bash -s -- https://github.com/oasissan/pyrealms.git
```

This installs Python, clones the repo to `/opt/pyrealms`,
creates a venv, and starts it as a systemd service (`pyrealms`)
bound to `0.0.0.0:8000`.

## 6. Verify it's up

Visit `http://<vm-public-ip>:8000` — you should see the World Map.

## 7. Wire up auto-deploy from GitHub Actions

In your GitHub repo → Settings → Secrets and variables → Actions, add:
- `VM_HOST` — the VM's public IP
- `VM_USER` — `ubuntu`
- `VM_SSH_KEY` — the *private* key contents (the `.pem` file, whole thing)

[.github/workflows/deploy.yml](.github/workflows/deploy.yml) now runs the
build-verification suite on every push to `main`, then SSHes in and runs
[deploy/redeploy.sh](deploy/redeploy.sh) (`git reset --hard origin/main` +
reinstall + restart the service) if it passes.

## 8. Turn on Basic Auth (do this before sharing the URL)

```bash
ssh -i /path/to/key.pem ubuntu@<vm-public-ip>
nano /opt/pyrealms/.env
```

Uncomment and set:
```
APP_USERNAME=yourname
APP_PASSWORD=something-only-you-know
```

Then:
```bash
sudo systemctl restart pyrealms
```

Every route now requires that Basic Auth credential.

## Rolling back / redeploying manually

```bash
ssh -i /path/to/key.pem ubuntu@<vm-public-ip>
bash /opt/pyrealms/deploy/redeploy.sh
```

## Resetting progress

The SQLite file lives at `/opt/pyrealms/app.db` on the VM. Stop
the service, delete it, and restart to reseed from scratch:

```bash
sudo systemctl stop pyrealms
rm /opt/pyrealms/app.db
sudo systemctl start pyrealms
```
