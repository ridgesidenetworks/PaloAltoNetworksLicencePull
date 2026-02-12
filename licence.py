import json
import os
import sys
import urllib.request
import urllib.parse


try:
    from config import api
except ImportError:
    api = None

def setup(): 	
    
# This section just registers the LicenceAPI key for future use, it should be a one of process and not repeated.
# however if a customer regenerates the key for any reason, they would need to rerun. 

    with open('config.py', 'w') as f:
        api_key = input("What is the licensing API key for your account: ").strip()
        key = "api = '%s'\n" % api_key
        f.write(key)
        
def serialretrieve(serial=None, out_dir="."):
    
# this section is to be able to retrieve the licence files for off line installations after the registration is 
# completed either via the API or the portal directly.
# the process generates the licence key files that can be imported. 
# always import the support key first or the base VM key.
    
    if not serial:
        serial = input("What is the Serial number of the license you wish to retrieve: ").strip()
    if not serial:
        print("Serial number is required.")
        sys.exit(1)

    if not api:
        print("API key not found. Run: python3 licence.py setup")
        sys.exit(1)

    data = urllib.parse.urlencode({"serialNumber": serial}).encode('ascii')

    url = "https://api.paloaltonetworks.com/api/license/activate"
    req = urllib.request.Request(url, data)
    req.add_header('apikey', api)

    try:
        with urllib.request.urlopen(req) as resp_str:
            for x in resp_str:
                resp = json.loads(x)
                count = len(resp)
                i = 0
                while i < count:
                    fname = serial + "-" + resp[i]['partidField'] + ".key"
                    out_path = os.path.join(out_dir, fname)
                    with open(out_path, "w") as f:
                        f.write(resp[i]['keyField'])
                    i += 1
    except urllib.error.HTTPError as e:
        print("HTTP error:", e)
        sys.exit(1)
    except urllib.error.URLError as e:
        print("Network error:", e)
        sys.exit(1)
    except (KeyError, json.JSONDecodeError) as e:
        print("Unexpected response:", e)
        sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 licence.py setup | serial [SERIAL] [OUT_DIR]")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "setup":
        setup()
    elif cmd == "serial":
        serial_arg = sys.argv[2] if len(sys.argv) > 2 else None
        out_dir_arg = sys.argv[3] if len(sys.argv) > 3 else "."
        serialretrieve(serial=serial_arg, out_dir=out_dir_arg)
    else:
        print("Usage: python3 licence.py setup | serial [SERIAL] [OUT_DIR]")
       
