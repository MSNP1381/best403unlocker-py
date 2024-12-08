import datetime
import os
import platform
import click
import logging

import colorlog
from best403unlocker_py.main import read_config, scan_dns_servers, set_dns, sort_dict, write_dns_config
log_dir = os.path.expanduser("~/.unlock403/tmp/logs/")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = os.path.join(log_dir, f"logs{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

color_handler = colorlog.StreamHandler()
file_handler = logging.FileHandler(log_file)

color_handler.setFormatter(colorlog.ColoredFormatter(
	'%(log_color)s%(levelname)s:%(name)s:%(message)s'))
color_handler.setLevel(logging.ERROR)
file_handler.setLevel(logging.DEBUG)

logger =logging.getLogger(__name__)
logger.addHandler(color_handler)
logger.addHandler(file_handler)


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "--url", default="https://developers.google.com", help="URL to use for DNS search"
)
def cli(ctx, url):
    if ctx.invoked_subcommand is None:
        default()

@click.command()
@click.option(
    "--url", default="https://developers.google.com", help="URL to use for DNS search"
)
def search_dns(url):
    dns_servers = read_config()
    results,_ = scan_dns_servers(url, dns_servers)
    sorted_dns_servers = sort_dict(results)
    write_dns_config(sorted_dns_servers)
    for dns, time in sorted(results.items(), key=lambda x: x[1]):
        print(f"{dns}: {'didn\'t respond' if time == 1000 else round(time, 2)} seconds")
    # set_dns(dns_servers)
    os_type = platform.system().lower()
    results = {dns: time for dns, time in results.items() if time < 1000}
    dns_servers_filtered = sort_dict(results)
    if os_type == "windows":
        return dns_servers_filtered

    print("DNS servers have been searched and set successfully.")
    return dns_servers_filtered

@click.command()
@click.argument("dns_servers", nargs=-1, required=True)
def set_custom_dns(dns_servers):
    if not dns_servers:
        logger.debug("Error: At least one DNS server must be provided.")
        return
    set_dns(dns_servers)

@click.command()
@click.option(
    "--url", default="developers.google.com", help="URL to use for DNS search"
)
def default(url="developers.google.com"):
    sorted_dns_servers = search_dns.callback(url)
    set_dns(sorted_dns_servers[:2])
    logger.info("DNS servers have been searched and set successfully.")

cli.add_command(search_dns)
cli.add_command(set_custom_dns)

if __name__ == "__main__":
    cli()
