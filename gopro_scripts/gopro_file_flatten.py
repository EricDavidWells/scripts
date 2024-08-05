import argparse
import os
import re
import shutil

def parse_arguments():
    # Create the parser
    parser = argparse.ArgumentParser(description="Process some directories.")

    # Add the arguments
    parser.add_argument(
        '--source-dir', 
        type=str, 
        help='The source directory'
    )
    
    parser.add_argument(
        '--output-dir', 
        type=str, 
        help='The output directory'
    )

    parser.add_argument(
        '--extra-regex',
        type=str,
        default=None,
        help='extra file match regex'
    )

    # Parse the arguments
    return parser.parse_args()

if __name__ == "__main__":
    # Parse the arguments
    args = parse_arguments()

    # Print the arguments (or do something with them)
    print(f"Source Directory: {args.source_dir}")
    print(f"Output Directory: {args.output_dir}")

    date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})')
    video_pattern = re.compile(r'\.mp4', re.IGNORECASE)
    if args.extra_regex:
        extra_pattern = re.compile(args.extra_regex)

    for root, subdirs, files in os.walk(args.source_dir):
        for file in files:

            file_path = os.path.join(root, file)
            if not video_pattern.search(file_path): continue

            date = date_pattern.search(root)
            if not date: continue

            if args.extra_regex:
                if not extra_pattern.search(file_path): continue

            out_file_path = os.path.join(args.output_dir, date[0] + "_" + file)

            print(f"copying {file_path} to {out_file_path}")
            shutil.copyfile(file_path, out_file_path)
