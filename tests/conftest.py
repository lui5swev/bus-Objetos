import os
from datetime import datetime

# Store log file paths per test module
LOG_FILES = {}
SESSION_TIMESTAMP = None
ROOT_DIR = None

def pytest_configure(config):
    global SESSION_TIMESTAMP, ROOT_DIR
    SESSION_TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')
    ROOT_DIR = str(config.rootdir)

def get_log_file_for_nodeid(nodeid):
    """
    Extracts the test filename from the nodeid and returns its specific log file path.
    """
    # nodeid usually looks like 'tests/unit/test_list.py::TestClass::test_method'
    # or just 'test_list.py::TestClass::test_method' depending on where pytest is run from.
    parts = nodeid.split('::')
    file_path = parts[0]
    file_name = os.path.basename(file_path).replace('.py', '')
    
    if file_name not in LOG_FILES:
        # Assuming we always want logs in 'tests/logs/' relative to the rootdir
        log_dir = os.path.join(ROOT_DIR, 'tests', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"{file_name}_{SESSION_TIMESTAMP}.log")
        LOG_FILES[file_name] = log_file
        
        with open(log_file, 'a') as f:
            f.write(f"=== Test run for {file_name} started at {SESSION_TIMESTAMP} ===\n\n")
            
    return LOG_FILES[file_name]

def pytest_runtest_logreport(report):
    """
    Log individual test results to the module-specific log file.
    """
    if report.when == 'call' and ROOT_DIR:
        log_file = get_log_file_for_nodeid(report.nodeid)
        with open(log_file, 'a') as f:
            f.write(f"{report.nodeid}: {report.outcome.upper()}\n")

def pytest_sessionfinish(session, exitstatus):
    """
    Log end of session for all created log files.
    """
    for file_name, log_file in LOG_FILES.items():
        with open(log_file, 'a') as f:
            f.write(f"\n=== Test run finished with status {exitstatus} ===\n")
