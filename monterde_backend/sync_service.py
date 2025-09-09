# monterde_backend/sync_service.py
import threading
import time
import logging
import socket
from apartments.sync import run_full_sync

logger = logging.getLogger(__name__)


def internet_available(host="8.8.8.8", port=53, timeout=3):
    """
    Check internet connection by trying to connect to a DNS server.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except OSError:
        return False


def background_sync_loop(interval=60):
    """
    Background loop that runs sync every <interval> seconds if internet is available.
    """
    while True:
        if internet_available():
            print("🌐 Internet detected, running sync...")
            try:
                run_full_sync()
            except Exception as e:
                print(f"❌ Sync failed: {e}")
        else:
            print("⚠️ No internet, will retry later...")
        time.sleep(interval)


def sync_loop():
    from apartments.sync import run_full_sync  # <-- Import inside the loop
    while True:
        try:
            run_full_sync()
        except Exception as e:
            logger.error(f"Sync failed: {e}")
        time.sleep(30)


def start_background_sync():
    """
    Start background sync in a separate thread.
    Call this once when Django starts.
    """
    thread = threading.Thread(target=background_sync_loop, daemon=True)
    thread.start()
    logger.info("Background sync started")
    print("🚀 Background sync service started")
