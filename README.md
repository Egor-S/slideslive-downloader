# SlidesLive downloader

Simple scripts to download recorded fragments and concatenate them.
Supports JSON format and edited timeline (removed fragments).

## How to

1. Open slides page with browser developer tools
2. Save content from `https://studio.slideslive.com/api/web_recorder/v3/token_uploads/*****/share?share_token=*****` as `share.json`
3. Run `python fetch_data.py --input shares.json --output data/` to download fragments
4. Run `python cut_video.py --data data/upload-***** --view speaker --output speaker.mp4` to cut and concatenate speaker fragments with ffmpeg (with audio)
5. Run `python cut_video.py --data data/upload-***** --view slides --output slides.mp4` to cut and concatenate slides fragments with ffmpeg (no audio)
