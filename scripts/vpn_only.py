"""VPN-only model downloads.

When this is on (the default), model downloads go through the VPN-only port of the Mac's VPN relay
(127.0.0.1:18887 -> gluetun on Phoenix -> Proton VPN). That port never falls back to the home connection,
so a download can't leak onto it. If the VPN drops, downloads pause, wait for it to come back, then resume
where they left off (Hugging Face and curl both resume partial files).

Settings (environment variables, all optional):
  MODEL_DOWNLOADS_VPN_ONLY=0                 turn VPN-only off for a run (downloads use the normal connection)
  MODEL_DOWNLOADS_VPN_MAX_WAIT_HOURS=24      give up if the VPN stays down this long (default 24)
  MODEL_DOWNLOADS_VPN_RECHECK=60             seconds between "is the VPN back?" checks (default 60)
  MODEL_DOWNLOADS_VPN_PROXY=127.0.0.1:18887  VPN-only relay port (testing only)
"""
from __future__ import annotations

import json
import os
import time
import urllib.request
from typing import Callable, TypeVar

T = TypeVar("T")

PROXY = os.environ.get("MODEL_DOWNLOADS_VPN_PROXY", "127.0.0.1:18887")
ENABLED = os.environ.get("MODEL_DOWNLOADS_VPN_ONLY", "1").strip().lower() not in {"0", "false", "no", "off"}
RECHECK = max(5, int(os.environ.get("MODEL_DOWNLOADS_VPN_RECHECK", "60")))
MAX_WAIT_S = float(os.environ.get("MODEL_DOWNLOADS_VPN_MAX_WAIT_HOURS", "24")) * 3600
_NO_PROXY = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def _status() -> dict:
    try:
        with _NO_PROXY.open(f"http://{PROXY}/__status", timeout=5) as r:
            return json.loads(r.read().decode())
    except Exception as exc:  # noqa: BLE001
        return {"mode": "unreachable", "last_error": f"VPN relay not answering: {exc}"}


def vpn_up() -> bool:
    s = _status()
    return s.get("mode") == "vpn" and not s.get("consecutive_fails")


def wait_for_vpn() -> None:
    """Block until the VPN is up. Exits after MAX_WAIT_S."""
    start = time.time()
    announced = False
    while not vpn_up():
        s = _status()
        waited = time.time() - start
        if waited > MAX_WAIT_S:
            raise SystemExit(f"VPN-only downloads: the VPN has been down for {waited / 3600:.1f} h, giving up. "
                             "Run again once it's back, or set MODEL_DOWNLOADS_VPN_ONLY=0 to download without it.")
        if not announced:
            print(f"VPN-only downloads: PAUSED, the VPN is down ({s.get('last_error') or s.get('mode')}). "
                  f"Checking every {RECHECK}s; nothing will download over the home connection.", flush=True)
            announced = True
        time.sleep(RECHECK)
    if announced:
        print(f"VPN-only downloads: VPN is back after {int(time.time() - start)}s, resuming.", flush=True)


def enable() -> None:
    """Route this process (and anything it starts, e.g. curl) through the VPN-only port. Waits if the VPN is down."""
    if not ENABLED:
        print("VPN-only downloads: OFF (MODEL_DOWNLOADS_VPN_ONLY=0), using the normal connection.", flush=True)
        return
    url = f"http://{PROXY}"
    for key in ("HTTPS_PROXY", "HTTP_PROXY", "https_proxy", "http_proxy"):
        os.environ[key] = url
    os.environ.pop("ALL_PROXY", None)
    os.environ.pop("all_proxy", None)
    os.environ["NO_PROXY"] = os.environ["no_proxy"] = "localhost,127.0.0.1,::1"
    print(f"VPN-only downloads: ON (via {url}; pauses if the VPN drops).", flush=True)
    wait_for_vpn()


def run(fn: Callable[[], T], what: str = "download") -> T:
    """Run fn; if it fails because the VPN dropped, wait for the VPN and try again (fn must resume safely).
    Failures while the VPN is healthy are real errors and are raised unchanged."""
    if not ENABLED:
        return fn()
    while True:
        try:
            return fn()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as exc:  # noqa: BLE001
            time.sleep(20)  # give the relay's health check time to notice a drop
            if vpn_up():
                raise
            print(f"VPN-only downloads: {what} interrupted ({type(exc).__name__}); VPN is down, pausing.", flush=True)
            wait_for_vpn()
            print(f"VPN-only downloads: retrying {what} (resumes partial files).", flush=True)
