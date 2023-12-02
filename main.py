from requests.exceptions import RequestException
from urllib.parse import urlparse, parse_qs
from typer import Typer, Option, run, Exit
from assets.downloader import Downloader
from rich.progress import track
from typing import Optional
from munch import munchify
from loguru import logger
import requests
import yaml
import sys
debug = False
trace = False

app = Typer(no_args_is_help=True, add_completion=False)
with open('config.yaml') as stream:
  try:
    yamlfile=yaml.safe_load(stream)
  except yaml.YAMLError as exc:
    print(exc)
loadedyaml = munchify(yamlfile)
Youtube = Downloader(host=f'{loadedyaml.host}', port=loadedyaml.port)
@app.command()
def audio(
  urls:Optional[list[str]] = Option(None, '-l', '--link', help='Url to youtube video/playlist'),
  server:Optional[bool] = Option(False, '-s', '--server', help='Send a web request to pre-configured url using urls as request'),
  trace:Optional[bool] = Option(False, '-t', '--trace', is_flag=True, help='Enable trace-level debugging.'),
  debug:Optional[bool] = Option(False, '-d', '--debug', is_flag=True, help='Enables debug')
):
  logger.remove()
  if debug:
    logger.add(sys.stderr, level='DEBUG')
  elif trace:
    logger.add(sys.stderr, level='TRACE')
  else:
    logger.add(sys.stderr, level='INFO')
    pass
  try:
    r = requests.get(f'http://{Youtube.host}:{Youtube.port}/ping')
    r = munchify(r.json())
    logger.info(r)
    print(r.ping)
  except RequestException as e:
    print('Failed to connect to webserver run in debug to see more info')
    logger.info("Try making sure the webserver is up and your calling the right host and port!")
    logger.info(f"current host:{Youtube.host} port:{Youtube.port}")
    logger.debug(e)
    sys.exit()
  
  url=[]
  playlist_id = ''
  for x in urls:
    parsed_url=urlparse(x)

    query_params = parse_qs(parsed_url.query)
    video_id = query_params.get('v')
    playlist_id = query_params.get('list')
  if not playlist_id == None:
    url.append(playlist_id)
  else:
    url.append(video_id)
  
  logger.debug(f'Urls: {url}')
  logger.debug(f'Full Urls: {urls}')
  if not server:
    logger.debug(f'Downloading: {urls}')
    Youtube.download(urls=urls)
  else:
    url = url[0]
    logger.debug(f'http://{Youtube.host}:{Youtube.port}/download/{url[0]}')
    response = requests.get(f'http://{Youtube.host}:{Youtube.port}/download/{url[0]}')
    if response.status_code == 200:
      print(response.json())
    else:
      print(f'Failure: {response.status_code}')
    pass



if __name__ == "__main__":
  app()
  