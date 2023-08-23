from datetime import date
from pathlib import Path

from botocore.exceptions import ClientError
import click
import boto3
from gcloud import storage

from ..config import get_feed, load_config
from ..constants import KEY_TEMPLATE

def format_gcs_key(feed_key, file_name):
    feed = get_feed(feed_key)
    return KEY_TEMPLATE.format(
        provider=feed['provider'],
        source=feed['source'],
        feed=feed['feed'],
        export_date=date.today().strftime('%Y-%m-%d'),
        file=file_name
    )

def get_client(config):
    client = boto3.client(
        "s3",
        region_name="auto",
        endpoint_url="https://storage.googleapis.com",
        aws_access_key_id=config['upload-agent']['access-key'],
        aws_secret_access_key=config['upload-agent']['access-secret'],
    )
    return client

def upload(feed_key: str, path: str) -> None:
    path = Path(path)
    key = format_gcs_key(feed_key, path.name)
    
    config = load_config()   

    bucket_name = config['upload-agent']['raw-bucket']
    click.echo(f'Uploading {str(path.absolute())} to gcs://{bucket_name}/{key}')
    gcs = get_client(config)
    gcs.upload_file(str(path.absolute()), bucket_name, key)
    