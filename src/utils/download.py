import requests
from pathlib import Path

def download_to_local(url:str, out_path:Path, parent_mkdir:bool=True):
    if parent_mkdir:
        out_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        res = requests.get(url)
        res.raise_for_status()
        # Write using binary mode to prevent \n conversions
        out_path.write_bytes(res.content)

        return True
    except requests.RequestException as e:
        print(f'Failed to download {url}: {e}')

        return False