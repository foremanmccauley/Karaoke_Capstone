import requests
from django import template
import json
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET
from .util import update_or_create_user_tokens, is_spotify_authenticated, get_user_tokens
from requests import Request, post

register = template.Library()

@register.simple_tag
def get_search(request, search_input, limit=5, market="US"):
  # can't have pesky spaces in your urls!
  search_input = search_input.replace(' ', '%20')

  code = request.GET.get("code")
  error = request.GET.get("error")

  response = post('https://accounts.spotify.com/api/token', data={
      'grant_type': 'client_credentials',
      'client_id': CLIENT_ID,
      'client_secret': CLIENT_SECRET
  }).json()

  access_token = response.get('access_token')
  expires_in = response.get('expires_in')
  error = response.get('error')

  if not request.session.exists(request.session.session_key):
      request.session.create()

  update_or_create_user_tokens(
      request.session.session_key, access_token, expires_in)

  # SETTINGS 
  endpoint_url = "https://api.spotify.com/v1/search?"
  search_type = 'track'

  # PERFORM THE QUERY
  # search_input given by user in frontend
  query = f'{endpoint_url}q={search_input}&type={search_type}&market={market}&limit={limit}'

  response = requests.get(query, 
                headers={"Content-Type":"application/json", 
                          "Authorization":f"Bearer {access_token}"})
  json_response = response.json()

  st = ""

  for i,j in enumerate(json_response['tracks']['items']):
    st += f"{i+1}) \"{j['name']}\" by {j['artists'][0]['name']}<br/>"

  return mark_safe(st)