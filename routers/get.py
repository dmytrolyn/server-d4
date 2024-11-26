from fastapi import APIRouter
from dotenv import load_dotenv
import requests
import datetime
import os

load_dotenv()

router = APIRouter()

BASE_URL = "https://vulners.com/api/v3/search/lucene/"
API_KEY = os.getenv("API_KEY")

def POST_REQUEST(url, payload):
 response = requests.post(url, json=payload)
 data = response.json()

 return data["data"]["search"]

@router.get('/')
def get_cve(key: str):
 payload = {
  "query": f"type:cve AND {key}",
  "size": 10,
  "sort": "published",
  "order": "desc",
  "apiKey": API_KEY
 }
  
 return POST_REQUEST(BASE_URL, payload)

@router.get('/all')
def get_all_cve():
 today = datetime.date.today()
 five_days_ago = today - datetime.timedelta(days=5)
 five_days_ago_str = five_days_ago.strftime("%Y-%m-%dT00:00:00")

 payload = {
    "query": f"type:cve AND published:[{five_days_ago_str} TO NOW]",
    "size": 40,
    "sort": "published",
    "order": "desc",
    "apiKey": API_KEY
 }
 cve_list = POST_REQUEST(BASE_URL, payload)
 filtered_cve_list = [cve for cve in cve_list if cve['_id'].startswith('CVE-')]

 return filtered_cve_list

@router.get('/new')
def get_new_cve():
 payload = {
    "query": "type:cve",
    "size": 10,
    "sort": "published",
    "order": "desc",
    "apiKey": API_KEY
 }

 return POST_REQUEST(BASE_URL, payload)

@router.get('/critical')
def get_critical_cve():
 payload = {
    "query": "type:cve AND (cvss.score:{9 TO *} OR cvss3.score:{9 TO *})",
    "size": 10,
    "sort": "published",
    "order": "desc",
    "apiKey": API_KEY
 }
 
 return POST_REQUEST(BASE_URL, payload)
