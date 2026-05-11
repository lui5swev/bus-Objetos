import os
from datetime import datetime


LOG_FILE = None
SESSION_TIMESTAMP = None
ROOT_DIR = None


def pytest_configure(config):
    global SESSION_TIMESTAMP, ROOT_DIR, LOG_FILE
    SESSION_TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')
    ROOT_DIR = str(config.rootdir)

    log_dir = os.path.join(ROOT_DIR, 'tests', 'logs')
    os.makedirs(log_dir, exist_ok=True)

    LOG_FILE = os.path.join(log_dir, "test_runs.log")

    with open(LOG_FILE, 'a') as f:
        f.write(f"=== Test run started at {SESSION_TIMESTAMP} ===\n\n")


def pytest_runtest_logreport(report):
    """
    Log individual test results to the session log file.
    """
    if report.when == 'call' and LOG_FILE:
        with open(LOG_FILE, 'a') as f:
            f.write(f"{report.nodeid}: {report.outcome.upper()}\n")


def pytest_sessionfinish(session, exitstatus):
    """
    Log end of session.
    """
    if LOG_FILE:
        with open(LOG_FILE, 'a') as f:
            f.write(f"\n=== Test run finished with status {exitstatus} ===\n\n")
