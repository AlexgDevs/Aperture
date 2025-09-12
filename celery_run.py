from os import getenv

from celery import Celery

from dotenv import load_dotenv


load_dotenv()

celery_app = Celery(
    'metadata_collector',
    broker=getenv('REDIS_URL'),
    backend=getenv('REDIS_BACKEND_URL'),
    include=['celery_tasks']
)

celery_app.conf.update(
    task_serializer="json", 
    result_serializer="json",  
    timezone="UTC",              
    enable_utc=True,      
)

