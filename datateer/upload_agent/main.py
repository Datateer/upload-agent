import click

# import datateer.upload_agent.config as config
from .config import load_config, save_config, save_feed, DEFAULT_PATH as default_config_path
config = load_config()

@click.group()
def cli():
    pass
    

@cli.command()
# @click.argument("name")
def upload():
    pass


@cli.group(name='config')
def config_group():
    pass


def show_upload_agent_config(ctx, param, value):
    if value:
        print(param, value)
        ctx.exit()

@config_group.command()
@click.option('-s', '--show', is_flag=True, is_eager=True, callback=show_upload_agent_config, expose_value=False, default=False, help="Shows the configuration instead of updating it")
@click.option('-c', '--client-code', prompt=True, default=lambda: config.get('client-code'), help="Your three-character code from Datateer")
@click.option('-b', '--raw-bucket', prompt='Raw bucket name', default=lambda: config.get('upload-agent', {}).get('raw-bucket'), help='The name of your data lake\'s raw bucket')
@click.option('-k', '--access-key', prompt=True, default=lambda: config.get('upload-agent', {}).get('access-key'), help='The AWS access key of your upload agent')
@click.option('-a', '--access-secret', prompt=True, default=lambda: config.get('upload-agent', {}).get('access-secret'), help='The AWS secret key of your upload agent')
def upload_agent(access_key, access_secret, client_code, raw_bucket):
    config = load_config()
    config['client-code'] = client_code
    config['upload-agent'] = {
        'raw-bucket': raw_bucket,
        'access-key': access_key,
        'access-secret': access_secret
    }
    config = save_config(config)
    click.echo(f'Saved configuration to {default_config_path}')


def show_feed_config(ctx, param, value):
    if value:
        print(param, value)
        ctx.exit()

@config_group.command()
@click.option('-s', '--show', is_flag=True, is_eager=True, callback=show_feed_config, expose_value=False, default=False, help="Shows the configuration instead of updating it")
@click.option('-p', '--provider', prompt=True, default=lambda: config.get('client-code'), help="A provider is an organization that provides a data feed. If this is an internal data feed, leave blank to use your client code")
@click.option('-d', '--source', prompt=True, help="A provider can own one or more systems or applications that are a source of data")
@click.option('-f', '--feed', prompt=True, help='A data source can provide one or more feeds')
@click.option('-k', '--feed-key', default=None, help='Uniquely identifies this feed configuration. Leave blank to use the feed name as the key')
def feed(feed, feed_key, provider, source):
    if feed_key is None:
        feed_key = click.prompt('Feed key', default=feed, show_default=True)

    feed = {
        'provider': provider,
        'source': source,
        'feed': feed
    }
    save_feed(feed_key, feed)



@cli.command()
@click.argument('feed-key')
@click.argument('path')
def upload(feed_key, path):
    pass


