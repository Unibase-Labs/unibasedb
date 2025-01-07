import click

from unibasedb.db.base import Unibase
from unibasedb import __version__


@click.group()
@click.version_option(__version__, '-v', '--version', prog_name='unibasedb')
@click.help_option('-h', '--help')
def unibase():
    pass


@unibase.command(help='Locally serve a unibaseDB db')
@click.option(
    '--db',
    '--app',
    type=str,
    required=True,
    help='Unibase to serve, in the format "<module>:<attribute>"',
)
@click.option(
    '--port',
    '-p',
    type=str,
    default='8081',
    help='Port to use to access the Unibase. It can be a single one or a list corresponding to the protocols',
    required=False,
    show_default=True,
)
@click.option(
    '--protocol',
    '--protocols',
    type=str,
    default='grpc',
    help='Protocol to use to communicate with the Unibase. It can be a single one or a list of multiple protocols to use. Options are grpc, http and websocket',
    required=False,
    show_default=True,
)
@click.option(
    '--replicas',
    '-r',
    type=int,
    default=1,
    help='Number of replicas to use for the serving Unibase',
    required=False,
    show_default=True,
)
@click.option(
    '--shards',
    '-s',
    type=int,
    default=1,
    help='Number of shards to use for the served Unibase',
    required=False,
    show_default=True,
)
@click.option(
    '--workspace',
    '-w',
    type=str,
    default='.',
    help='Workspace for the Unibase to persist its data',
    required=False,
    show_default=True,
)
def serve(db, port, protocol, replicas, shards, workspace):
    import importlib
    definition_file, _, obj_name = db.partition(":")
    port = port.split(',')
    if len(port) == 1:
        port = int(port[0])
    else:
        port = [int(p) for p in port]
    protocol = protocol.split(',')
    if definition_file.endswith('.py'):
        definition_file = definition_file[:-3]
    module = importlib.import_module(definition_file)
    db = getattr(module, obj_name)
    service = db.serve(protocol=protocol,
                       port=port,
                       shards=shards,
                       replicas=replicas,
                       workspace=workspace)
    with service:
        service.block()


if __name__ == '__main__':
    unibase()
