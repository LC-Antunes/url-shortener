import hashlib, base64
from urllib.parse import urlsplit

# the in-memory dictionary of stored links and the length of the short link code
urldb = dict()
N = 7
# First work on making the endpoint for the url

def normalize_url(raw_url):
    #probably put this in a try catch so that errors dont just break the code.
    common_ports = [80, 443]
    strip_url = raw_url.strip()
    url_obj = urlsplit(strip_url)
    parsed_scheme = url_obj.scheme
    parsed_hostname = url_obj.hostname
    parsed_port = url_obj.port
    if parsed_port is None:
        parsed_port = ""
    elif parsed_scheme == "https" and parsed_port == 443:
        parsed_port = ""
    elif parsed_scheme == "http" and parsed_port == 80:
        parsed_port = ""
    else:
        parsed_port = ":" + str(parsed_port)
    parsed_path = url_obj.path
    parsed_query = url_obj.query
    if parsed_query is not None:
        parsed_query = "?" + parsed_query
    else:
        parsed_query = ""
    parsed_frag = url_obj.fragment
    if parsed_frag is not None:
        parsed_frag = "#" + parsed_frag
    else:
        parsed_frag = ""
    
    # print(parsed_scheme + "://" + parsed_hostname + str(parsed_port) + parsed_path + parsed_query + parsed_frag)
    normal_url = parsed_scheme + "://" + parsed_hostname + parsed_port + parsed_path + "?" + parsed_query + "#" + parsed_frag
    return normal_url
    # pass

def url_to_hash_to_code(clean_url, counter):
    encoded_text = clean_url.encode("utf-8")
    if counter != 0:
        encoded_text += bytes(counter)
    encoded_hash = hashlib.sha256(encoded_text).digest()
    base64_bytes = base64.urlsafe_b64encode(encoded_hash)
    coded_string = base64_bytes.decode("utf-8")
    return coded_string[0:N] # return first N characters
    # pass

def add_pair_to_database(proced_url, code):
    counter = 1
    current_code = code
    while current_code in urldb:
        current_code = url_to_hash_to_code(proced_url, counter)
        counter += 1
    urldb[current_code] = proced_url
    # pass

# Master function that adds everything toegether
def link_to_short(url):
    # Add to dict when done
    # first normalize the url
    processed_url = normalize_url(url)
    # next convert the url to a short code (this may be a dedup, so only show the keyvalue pair when its successful)
    short_code = url_to_hash_to_code(processed_url, 0)
    # add link and code to dict via while loop counter

    pass

