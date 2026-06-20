#!/usr/bin/env python3
import sqlite3
import shutil
import os
import time
from datetime import datetime
from typing import Tuple

def check_database(db_path: str = 'database.db') -> Tuple[str, str]:
    if not os.path.exists(db_path):
        return 'error', f'Archivo de BD no encontrado: {db_path}'
    try:
        start = time.time()
        conn = sqlite3.connect(db_path, timeout=5)
        conn.execute('SELECT 1')
        conn.close()
        elapsed_ms = (time.time() - start) * 1000
        if elapsed_ms > 500:
            return 'warning', f'BD lenta: {elapsed_ms:.1f}ms'
        return 'ok', f'BD accesible en {elapsed_ms:.1f}ms'
    except sqlite3.OperationalError as e:
        return 'error', f'Error: {e}'

def check_disk(path: str = '/') -> Tuple[str, str]:
    try:
        usage = shutil.disk_usage(path)
        used_pct = (usage.used / usage.total) * 100
        free_gb = usage.free / (1024**3)
        if used_pct >= 95:
            return 'error', f'Disco critico: {used_pct:.1f}% usado'
        if used_pct >= 80:
            return 'warning', f'Disco alto: {used_pct:.1f}% usado'
        return 'ok', f'Disco saludable: {used_pct:.1f}% usado'
    except Exception as e:
        return 'error', f'No se pudo verificar: {e}'

def check_backup(backup_dir: str = 'backups', max_age_hours: int = 25) -> Tuple[str, str]:
    if not os.path.isdir(backup_dir):
        return 'warning', f'Directorio backups no existe: {backup_dir}'
    backups = sorted([f for f in os.listdir(backup_dir) if f.endswith('.tar.gz')])
    if not backups:
        return 'error', 'No se encontraron backups'
    latest = backups[-1]
    latest_path = os.path.join(backup_dir, latest)
    age_hours = (time.time() - os.path.getmtime(latest_path)) / 3600
    if age_hours > max_age_hours:
        return 'warning', f'Backup antiguo: {age_hours:.1f}h'
    return 'ok', f'Backup reciente: {latest}'

def run_all_checks() -> dict:
    checks = {}
    checks['database'] = {'status': check_database()[0], 'message': check_database()[1]}
    checks['disk'] = {'status': check_disk()[0], 'message': check_disk()[1]}
    checks['backup'] = {'status': check_backup()[0], 'message': check_backup()[1]}

    all_statuses = [checks[k]['status'] for k in checks]
    if 'error' in all_statuses:
        overall = 'unhealthy'
    elif 'warning' in all_statuses:
        overall = 'degraded'
    else:
        overall = 'healthy'

    return {
        'status': overall,
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'version': '1.0.0',
        'checks': checks,
    }

if __name__ == '__main__':
    import json
    result = run_all_checks()
    print(json.dumps(result, indent=2))