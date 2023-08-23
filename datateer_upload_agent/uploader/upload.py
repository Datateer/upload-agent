from datetime import date
from pathlib import Path

from botocore.exceptions import ClientError
import boto3
import click

from ..config import get_feed, load_config
from ..constants import KEY_TEMPLATE
from . import upload_s3
from . import upload_gcs

def format_s3_key(feed_key, file_name):
    feed = get_feed(feed_key)
    return KEY_TEMPLATE.format(
        provider=feed['provider'],
        source=feed['source'],
        feed=feed['feed'],
        export_date=date.today().strftime('%Y-%m-%d'),
        file=file_name
    )

def upload(feed_key: str, path: str) -> None:
    config = load_config() 
    if config['cloud-platform'] == 'gcs':
        upload_gcs.upload(feed_key, path)
    else:
        upload_s3.upload(feed_key, path)
    