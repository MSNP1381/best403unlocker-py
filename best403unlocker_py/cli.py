import click
from .main import read_config, scan_dns_servers, set_dns, sort_dict, write_dns_config

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        default()

@click.command()
@click.option('--url', default='developers.google.com', help='URL to use for DNS search')
def search_dns(url):
    dns_servers = read_config()
    results = scan_dns_servers(url, dns_servers)
    sorted_dns_servers = sort_dict(results)
    write_dns_config(sorted_dns_servers)
    for dns, time in results.items():
        print(f"{dns}: {time} seconds")
    return sorted_dns_servers

@click.command()
@click.argument('dns_servers', nargs=-1, required=True)
def set_custom_dns(dns_servers):
    if not dns_servers:
        print("Error: At least one DNS server must be provided.")
        return
    set_dns(dns_servers)

@click.command()
@click.option('--url', default='developers.google.com', help='URL to use for DNS search')
def default(url='developers.google.com'):
    sorted_dns_servers = search_dns.callback(url)
    set_dns(sorted_dns_servers[:2])
    print("DNS servers have been searched and set successfully.")

cli.add_command(search_dns)
cli.add_command(set_custom_dns)

if __name__ == "__main__":
    cli()
