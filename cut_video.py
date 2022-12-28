import json
import argparse
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, required=True)
    parser.add_argument('--view', choices=['speaker', 'slides'], default='speaker')
    parser.add_argument('-o', '--output', type=Path, required=True)
    args = parser.parse_args()

    with (args.data / 'slrec.json').open('r') as f:
        slrec = json.load(f)
        files = {i['id']: i['file_name'] for i in slrec['files']}

    inputs = []
    filter_complex = []
    concat = []
    for i, clip in enumerate(slrec['timelines'][args.view]['video']):
        filename = files[clip['clip']['file_id']]
        inputs.append(filename)

        start = clip['clip']['in_cut_ms']
        end = start + clip['clip']['duration_ms']
        filter_complex.append(f"[{i}:v]trim=start={start}ms:end={end}ms,setpts=PTS-STARTPTS[v{i}]")
        concat.append(f"[v{i}]")
        if args.view == 'speaker':
            filter_complex.append(f"[{i}:a]atrim=start={start}ms:end={end}ms,asetpts=PTS-STARTPTS[a{i}]")
            concat.append(f"[a{i}]")

    streams = len(slrec['timelines'][args.view]['video'])
    concat = ''.join(concat)
    if args.view == 'speaker':
        filter_complex.append(f"{concat}concat=n={streams}:v=1:a=1[v][a]")
    else:
        filter_complex.append(f"{concat}concat=n={streams}:v=1[v]")
    filter_complex = ';'.join(filter_complex)

    cmd = ['ffmpeg']
    for i in inputs:
        cmd += ['-i', args.data / i]
    cmd += ['-filter_complex', filter_complex, '-map', '[v]']
    if args.view == 'speaker':
        cmd += ['-map', '[a]']
    cmd += ['-vsync', '2', '-y', args.output]
    subprocess.run(cmd)


if __name__ == '__main__':
    main()
