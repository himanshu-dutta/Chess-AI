"""
Dataset source: https://osf.io/xf3ka
"""


import numpy as np

import os
import json
import shutil
import argparse
from pathlib import Path


def find_camera_position(metadata: dict):
    """
    We can think of the camera position as making an angle with x-axis [Only x
    and y coordinate needed here as z coordinate should be positive since the
    camera must be above the board].

    If the angle is in range: 135 deg to 225 deg, we can say that the camera is
    on left. If the angle is in ranges: O deg to 45 deg or 315 deg to 360 deg,
    we can say that the camera is on right.

    This function classifies the camera position in accordance to the FEN
    convention of rank 8, file 8 starting from the top-left corner. It can
    classify the camera position as: - left - right - top - bottom - unknown

    finding the angle:
    - https://stackoverflow.com/a/64409300
    - https://math.stackexchange.com/a/879474
    """

    def in_range(x: float, min: float, max: float):
        # checks inclusion of x in half open interval [min, max)
        return x >= min and x < max

    camera_specs = metadata.get("camera")
    if not camera_specs:
        return "unknown"

    location = camera_specs.get("location")
    if not location:
        return "unknown"

    x, y, _ = location

    camera_vec = [x, y]
    x_axis_vec = [1, 0]

    angle = np.rad2deg(
        np.arctan2(camera_vec[1], camera_vec[0])
        - np.arctan2(x_axis_vec[1], x_axis_vec[0])
    )
    if angle < 0:
        angle = 360 + angle

    # putting top and bottom up first so that corner cases match to them, rather
    # than left and right
    if in_range(angle, 46, 136):
        return "top"
    elif in_range(angle, 226, 316):
        return "bottom"
    elif in_range(angle, 0, 46) or in_range(angle, 315, 360):
        return "right"
    elif in_range(angle, 136, 226):
        return "left"
    return "unknown"


def generate_metadata(src_md):
    dest_md = {}
    dest_md["fen"] = src_md["fen"]
    dest_md["camera_position"] = find_camera_position(src_md)

    dest_md["bounding_boxes"] = list()

    for corner in src_md["corners"]:
        bbox = {
            "type": "corner",
            "left": max(corner[0] - 10, 0),
            "top": max(corner[1] - 10, 0),
            "width": 20,
            "height": 20,
        }
        dest_md["bounding_boxes"].append(bbox)

    for piece in src_md["pieces"]:
        bbox = {
            "type": piece["piece"],
            "position": piece["square"],
            "left": piece["box"][0],
            "top": piece["box"][1],
            "width": piece["box"][2],
            "height": piece["box"][3],
        }
        dest_md["bounding_boxes"].append(bbox)

    return dest_md


def main(args: argparse.Namespace):
    src_dir = Path(args.src).absolute()
    assert src_dir.exists(), f"Source directory doesn't exist: {str(src_dir)}"

    dest_dir = Path(args.dest).absolute()
    if not dest_dir.exists():
        os.mkdir(str(dest_dir))

    summarize = args.summary
    summary = {
        "num_files": 0,
        "count_camera_position": {
            "top": 0,
            "bottom": 0,
            "right": 0,
            "left": 0,
            "unknown": 0,
        },
    }

    files = [fl.name.split(".")[0] for fl in list(src_dir.rglob("*.json"))]
    summary["num_files"] = len(files)

    for fl_name in files:
        img_fl_name = src_dir / (fl_name + ".png")
        md_fl_name = src_dir / (fl_name + ".json")

        assert img_fl_name.exists(), f"Image file doesn't exist: {str(img_fl_name)}"
        assert md_fl_name.exists(), f"Image file doesn't exist: {str(md_fl_name)}"

        with open(str(md_fl_name)) as md_fp:
            src_md = json.load(md_fp)

        dest_md = generate_metadata(src_md)
        dest_md_fl_name = dest_dir / (fl_name + ".json")
        with open(str(dest_md_fl_name), "w+") as md_fp:  # writing metadata
            json.dump(dest_md, md_fp)
        shutil.copy(str(img_fl_name), dest_dir)  # copying image

        summary["count_camera_position"][dest_md["camera_position"]] += 1

    if summarize:
        print(summary)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Chess Detection: Data Processing")
    parser.add_argument(
        "-s",
        "--src",
        type=str,
        required=True,
        help="Source directory with the images (.png) and metadata (.json) files.",
    )

    parser.add_argument(
        "-d",
        "--dest",
        type=str,
        required=True,
        help="Destination directory to output the files.",
    )

    parser.add_argument(
        "-b",
        "--summary",
        type=bool,
        default=True,
        help="Summarized information about the data.",
    )

    print(parser.parse_args())
    main(parser.parse_args())
