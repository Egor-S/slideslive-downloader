import json
import time
import argparse
import urllib.parse
import urllib.request
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='share.json', type=Path)
    parser.add_argument('--output', default='data', type=Path)
    parser.add_argument('--delay', default=3, type=int)
    args = parser.parse_args()

    with args.input.open('r') as f:
        share = json.load(f)

    output_dir: Path = args.output / f"upload-{share['data']['upload']['id']}"
    output_dir.mkdir(exist_ok=True, parents=True)

    files = share['data']['upload']['files']
    for i, (key, url) in enumerate(files.items()):
        if key == "slrec-log":
            continue
        filename = urllib.parse.urlparse(url).path.rsplit('/', maxsplit=1)[-1]
        print(f"{i + 1}/{len(files)}: {filename}")
        with (output_dir / filename).open('wb') as f, urllib.request.urlopen(url) as remote:
            f.write(remote.read())
        time.sleep(args.delay)


if __name__ == '__main__':
    main()
