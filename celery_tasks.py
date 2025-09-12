from celery_run import celery_app

from asgiref.sync import async_to_sync

from hashlib import sha256

from user_agents import parse


@celery_app.task
def process_meta_collection(short: str, endpoint_type: str, request_data: dict):
    ip = request_data.get('ip_address', '')
    ua_string = request_data.get('user_agent', '')

    ua = parse(ua_string)
    hidden_ip = f'{".".join(ip.split(".")[:3])}.0' if ip else ''
    hashed_user = sha256(f"{hidden_ip}{ua_string}".encode()).hexdigest()[:16]

    metrics = {
        'short_code': short,
        'endpoint_type': endpoint_type,
        'hidden_ip': hidden_ip,
        'hashed_user': hashed_user,
        'browser': ua.browser.family if ua.browser else None,
        'browser_version': ua.browser.version_string if ua.browser else None,
        'os': ua.os.family if ua.os else None,
        'os_version': ua.os.version_string if ua.os else None,
        'device': ua.device.family if ua.device else None,
        'is_mobile': ua.is_mobile,
        'is_tablet': ua.is_tablet,
        'is_pc': ua.is_pc,
        'is_bot': ua.is_bot,
        'accept_language': request_data.get('accept_language', '')
    }

    async_to_sync(DBHelper.add_metric)(metrics)
    return {'status': 'success', 'short_code': short}

from server.db import DBHelper