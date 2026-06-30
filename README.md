# P72 — AI Village Walk Video

Generate an AI video of a man walking through a European village using [Replicate](https://replicate.com)'s text-to-video API.

## Prerequisites

- Python 3.8+
- A [Replicate API token](https://replicate.com/account/api-tokens)

## Setup

```bash
pip install -r requirements.txt
export REPLICATE_API_TOKEN="r8_..."   # your token
```

You can also place the token in a `.env` file (gitignored):

```
REPLICATE_API_TOKEN=r8_...
```

## Generate the video

```bash
python3 generate_video.py
```

Output is saved to `output/village_walk.mp4`.

### Options

| Flag | Description |
|------|-------------|
| `--model MODEL` | Replicate model (default: `wan-video/wan-2.5-t2v-fast`) |
| `--duration SEC` | Clip length in seconds (default: 5) |
| `--output PATH` | Output file path (default: `output/village_walk.mp4`) |
| `--from-image PATH` | Create a cinematic clip from a still image using ffmpeg (no API key) |

### Model choices

| Model | Trade-off |
|-------|-----------|
| `wan-video/wan-2.5-t2v-fast` | Fastest, cheapest (default) |
| `minimax/hailuo-2.3` | Better realism and motion |
| `runwayml/gen-4.5` | Highest quality, higher cost |

## Fallback (no API key)

If you don't have a Replicate token, generate a still image and create a short cinematic clip:

```bash
python3 generate_video.py --from-image village_scene.png
```

This uses ffmpeg to apply a slow tracking zoom — not true AI video motion, but produces an MP4 without API access.

## Prompt

The default prompt describes a man walking through a golden-hour European village with a gentle tracking camera shot. Edit `PROMPT` in `generate_video.py` to customize the scene.
