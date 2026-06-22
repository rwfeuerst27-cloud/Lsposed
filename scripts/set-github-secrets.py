#!/usr/bin/env python3
"""
Set GitHub Actions secrets for the LSPosed signing keystore.
Requires a GitHub PAT with repo scope (or Actions write permission).

Usage:
    python3 scripts/set-github-secrets.py --token ghp_xxxx
    python3 scripts/set-github-secrets.py  # prompts for token
"""

import argparse
import base64
import getpass
import json
import sys
from pathlib import Path

import requests
from nacl import encoding, public

REPO_OWNER = "rwfeuerst27-cloud"
REPO_NAME  = "Lsposed"
REPO       = f"{REPO_OWNER}/{REPO_NAME}"
API        = "https://api.github.com"

KEYSTORE_B64_FILE = Path(__file__).parent.parent / "lsposed-release.jks.b64"

SECRETS = {
    "KEYSTORE_BASE64":    lambda: KEYSTORE_B64_FILE.read_text().strip(),
    "KEYSTORE_PASSWORD":  lambda: "lsposed123",
    "KEY_ALIAS":          lambda: "lsposed",
    "KEY_PASSWORD":       lambda: "lsposed123",
}


def encrypt_secret(public_key_b64: str, secret_value: str) -> str:
    pub = public.PublicKey(public_key_b64.encode(), encoding.Base64Encoder)
    sealed = public.SealedBox(pub).encrypt(secret_value.encode())
    return base64.b64encode(sealed).decode()


def get_public_key(session: requests.Session) -> tuple[str, str]:
    r = session.get(f"{API}/repos/{REPO}/actions/secrets/public-key")
    r.raise_for_status()
    data = r.json()
    return data["key_id"], data["key"]


def set_secret(session: requests.Session, key_id: str, pub_key: str,
               name: str, value: str) -> None:
    encrypted = encrypt_secret(pub_key, value)
    r = session.put(
        f"{API}/repos/{REPO}/actions/secrets/{name}",
        json={"encrypted_value": encrypted, "key_id": key_id},
    )
    if r.status_code in (201, 204):
        print(f"  ✓ {name}")
    else:
        print(f"  ✗ {name}: {r.status_code} {r.text}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Set LSPosed GitHub Actions secrets")
    parser.add_argument("--token", help="GitHub PAT with repo/actions:write scope")
    args = parser.parse_args()

    token = args.token or getpass.getpass("GitHub PAT: ")

    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })

    # Verify token works
    r = session.get(f"{API}/repos/{REPO}")
    if r.status_code == 401:
        print("Error: invalid token")
        sys.exit(1)
    r.raise_for_status()
    print(f"Authenticated. Setting secrets on {REPO} ...\n")

    key_id, pub_key = get_public_key(session)
    for name, value_fn in SECRETS.items():
        set_secret(session, key_id, pub_key, name, value_fn())

    print(f"\nDone. Trigger a release build with:\n  git tag v1.0.0 && git push origin v1.0.0")


if __name__ == "__main__":
    main()
