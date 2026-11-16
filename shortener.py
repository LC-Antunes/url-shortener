import hashlib, urllib
from urllib.parse import urlsplit

shorturl = dict()
# First work on making the endpoint for the url

def normalize_url(raw_url):
    common_ports = [80, 443, 21, 22]
    strip_url = raw_url.strip()
    url_obj = urlsplit(strip_url)
    parsed_scheme = url_obj.scheme
    parsed_hostname = url_obj.hostname
    parsed_port = url_obj.port
    parsed_path = url_obj.path
    parsed_query = url_obj.query
    parsed_frag = url_obj.fragment
    if parsed_port in common_ports:
        parsed_port = ""
    else:
        parsed_port = ":" + str(parsed_port)
    print(parsed_scheme + "://" + parsed_hostname + str(parsed_port) + parsed_path + parsed_query + parsed_frag)
    pass

normalize_url("hTTps://outloOk.LIVE.Com:8080/mailroomboXstuff/./b/../c/?highlight=params")

def link_to_short(url):
    # Add to dict when done
    # processed_url = 
    pass

def hash_to_code(hashed_url):

    pass