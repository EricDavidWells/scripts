import argparse
import os
import re
import shutil
import subprocess

def parse_arguments():
    # Create the parser
    parser = argparse.ArgumentParser(description="Process some directories.")

    # Add the arguments
    parser.add_argument(
        '--source-dir', 
        type=str, 
        help='The source directory'
    )
    parser.add_argument('--rewrite-existing', action='store_true')

    # Parse the arguments
    return parser.parse_args()

if __name__ == "__main__":
    # Parse the arguments
    args = parse_arguments()

    # Print the arguments (or do something with them)
    print(f"Source Directory: {args.source_dir}")

    video_pattern = re.compile(r'\.mp4', re.IGNORECASE)

    for root, subdirs, files in os.walk(args.source_dir):
        for file in files:

            file_path = os.path.join(root, file)
            if not video_pattern.search(file_path): continue

            file_root, file_ext = os.path.splitext(file_path)
            output_path = os.path.join(root, f"{file_root}.mov")
            if os.path.exists(output_path) and not args.rewrite_existing: continue

            

            subprocess.call([f"ffmpeg -i {file_path} -c:v mpeg4 -q:v 1 -c:a pcm_s16le {output_path} {'-y' if args.rewrite_existing else ''}"], shell=True)
