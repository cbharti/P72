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

### Option A: Hugging Face (no API key, true AI motion)

Uses the [Wan 2.2 first/last frame](https://huggingface.co/spaces/multimodalart/wan-2-2-first-last-frame) Space to interpolate between two keyframes:

```bash
python3 generate_video.py --backend hf
```

Requires `village_scene.png` and `village_scene_end.png` (included in the repo).

### Option B: Replicate text-to-video

```bash
export REPLICATE_API_TOKEN="r8_..."
python3 generate_video.py --backend replicate
```

### Option C: ffmpeg fallback (no API key, no AI motion)

```bash
python3 generate_video.py --from-image village_scene.png
```

Output is saved to `output/village_walk.mp4`.

### Options

| Flag | Description |
|------|-------------|
| `--backend {hf,replicate,ffmpeg}` | Generation backend (default: `replicate`) |
| `--model MODEL` | Replicate model (default: `wan-video/wan-2.5-t2v-fast`) |
| `--duration SEC` | Clip length in seconds (default: 5) |
| `--output PATH` | Output file path (default: `output/village_walk.mp4`) |
| `--start-image PATH` | Start frame for `--backend hf` |
| `--end-image PATH` | End frame for `--backend hf` |
| `--from-image PATH` | Shorthand for `--backend ffmpeg` |

### Model choices

| Model | Trade-off |
|-------|-----------|
| `wan-video/wan-2.5-t2v-fast` | Fastest, cheapest (default) |
| `minimax/hailuo-2.3` | Better realism and motion |
| `runwayml/gen-4.5` | Highest quality, higher cost |

## Prompt

The default prompt describes a man walking through a golden-hour European village with a gentle tracking camera shot. Edit `PROMPT` in `generate_video.py` to customize the scene.
