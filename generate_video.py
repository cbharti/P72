#!/usr/bin/env python3
"""Generate an AI video of a man walking through a village."""

import argparse
import os
import shutil
import subprocess
import sys
import urllib.request

import replicate

MODEL = "wan-video/wan-2.5-t2v-fast"
HF_SPACE = "multimodalart/wan-2-2-first-last-frame"
OUTPUT_PATH = "output/village_walk.mp4"

PROMPT = (
    "A man in simple clothes walks slowly down a cobblestone path "
    "through a peaceful European village at golden hour. Stone cottages "
    "with flower boxes line the narrow street. Warm sunlight, gentle "
    "camera tracking shot following from behind, cinematic realism, "
    "natural walking motion."
)


def download_video(url: str, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    urllib.request.urlretrieve(url, path)


def create_video_from_image(image_path: str, output_path: str, duration: int = 5) -> None:
    """Create a short cinematic clip from a still image using ffmpeg."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    vf = (
        f"scale=1920:1080:force_original_aspect_ratio=increase,"
        f"crop=1920:1080,"
        f"zoompan=z='min(zoom+0.0008,1.15)':x='iw/2-(iw/zoom/2)+on*0.3':"
        f"y='ih/2-(ih/zoom/2)':d={duration * 25}:s=1920x1080:fps=25"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-loop", "1", "-i", image_path,
            "-vf", vf, "-t", str(duration),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            output_path,
        ],
        check=True,
        capture_output=True,
    )


def generate_with_huggingface(
    start_image: str, end_image: str, output_path: str, duration: float
) -> None:
    """Generate video by interpolating between start/end frames via HF Space."""
    from gradio_client import Client, handle_file

    print(f"Connecting to {HF_SPACE}...")
    client = Client(HF_SPACE)
    print("Generating AI video (this may take several minutes)...")
    result = client.predict(
        start_image_pil=handle_file(start_image),
        end_image_pil=handle_file(end_image),
        prompt=PROMPT,
        duration_seconds=duration,
        api_name="/generate_video",
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    shutil.copy(result[0], output_path)
    print(f"Saved to {output_path}")


def generate_with_replicate(model: str, output_path: str, duration: int) -> None:
    if not os.environ.get("REPLICATE_API_TOKEN"):
        print("Error: REPLICATE_API_TOKEN environment variable is not set.", file=sys.stderr)
        print("Get a token at https://replicate.com/account/api-tokens", file=sys.stderr)
        print("Or use --backend hf with start/end images.", file=sys.stderr)
        sys.exit(1)

    print(f"Generating video with model: {model}")
    print(f"Prompt: {PROMPT}")

    output = replicate.run(
        model,
        input={"prompt": PROMPT, "duration": duration, "size": "1280*720"},
    )

    video_url = output.url if hasattr(output, "url") else str(output)
    print(f"Downloading video from: {video_url}")
    download_video(video_url, output_path)
    print(f"Saved to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a village walk video")
    parser.add_argument(
        "--backend",
        choices=["replicate", "hf", "ffmpeg"],
        default="replicate",
        help="Generation backend (default: replicate)",
    )
    parser.add_argument("--model", default=MODEL, help="Replicate model identifier")
    parser.add_argument("--duration", type=float, default=5, help="Clip duration in seconds")
    parser.add_argument("--output", default=OUTPUT_PATH, help="Output MP4 path")
    parser.add_argument("--start-image", default="village_scene.png", help="Start frame (hf backend)")
    parser.add_argument("--end-image", default="village_scene_end.png", help="End frame (hf backend)")
    parser.add_argument(
        "--from-image",
        metavar="PATH",
        help="Create a cinematic clip from a still image via ffmpeg (sets --backend ffmpeg)",
    )
    args = parser.parse_args()

    if args.from_image:
        args.backend = "ffmpeg"
        args.start_image = args.from_image

    if args.backend == "ffmpeg":
        if not os.path.isfile(args.start_image):
            print(f"Error: image not found: {args.start_image}", file=sys.stderr)
            sys.exit(1)
        print(f"Creating video from image: {args.start_image}")
        create_video_from_image(args.start_image, args.output, int(args.duration))
        print(f"Saved to {args.output}")
    elif args.backend == "hf":
        for path in (args.start_image, args.end_image):
            if not os.path.isfile(path):
                print(f"Error: image not found: {path}", file=sys.stderr)
                sys.exit(1)
        generate_with_huggingface(args.start_image, args.end_image, args.output, args.duration)
    else:
        generate_with_replicate(args.model, args.output, int(args.duration))


if __name__ == "__main__":
    main()
