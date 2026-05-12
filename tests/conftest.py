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

    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"=== Inicio de Ejecución de Pruebas: {SESSION_TIMESTAMP} ===\n\n")


def pytest_runtest_logreport(report):
    """
    Registra de forma unificada y categorizada cada prueba ejecutada en la bitácora central.
    """
    if report.when == 'call' and LOG_FILE:
        categoria = "GENERAL"
        # Detección robusta compatible con separadores de Windows y POSIX
        node_id_lower = report.nodeid.lower()
        if "unit" in node_id_lower:
            categoria = "UNIT"
        elif "integration" in node_id_lower:
            categoria = "INTEGRATION"
        elif "system" in node_id_lower or "concurrency" in node_id_lower:
            categoria = "SYSTEM"

        hora = datetime.now().strftime('%H:%M:%S')
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{hora}] [{categoria}] {report.nodeid} -> {report.outcome.upper()}\n")


def pytest_sessionfinish(session, exitstatus):
    """
    Registra el fin de la sesión de pruebas.
    """
    if LOG_FILE:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"\n=== Fin de Ejecución con estado: {exitstatus} ===\n\n")
