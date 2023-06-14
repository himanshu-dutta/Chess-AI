import json
import argparse
from pathlib import Path


labels = ["corner", "p", "r", "n", "b", "q", "k", "P", "R", "N", "B", "Q", "K"]
labels_dict = {n: i for i, n in enumerate(labels)}
label_count = len(labels)


def generate_YOLOv5_annotation(metadata: dict, img_width: float, img_height: float):
    """
    Generates the `.txt` file for a given image. Each row of the file has the following format:
    `class_id` `center_x` `center_y` `width` `height`

    More on YOLOv5 format: https://roboflow.com/formats/yolov5-pytorch-txt
    """
    annot = ""
    for bbox in metadata["bounding_boxes"]:
        label = labels_dict[bbox["type"]]
        bbox_width = float(bbox["width"])
        bbox_height = float(bbox["height"])
        bbox_center_x = (float(bbox["left"]) + bbox_width / 2) / img_width
        bbox_center_y = (float(bbox["top"]) + bbox_height / 2) / img_height
        bbox_width /= img_width
        bbox_height /= img_height
        annot += f"\n{label} {bbox_center_x} {bbox_center_y} {bbox_width} {bbox_height}"

    return annot[1:]


def generate_data_yaml(labels):
    out = f"nc: {len(labels)}\nnames: {labels}"
    return out


def main(args: argparse.Namespace):
    src_dir = Path(args.src).absolute()
    width = args.width
    height = args.height
    assert src_dir.exists(), f"Source directory doesn't exist: {str(src_dir)}"

    files = [fl.name.split(".")[0] for fl in list(src_dir.rglob("*.json"))]

    for fl_name in files:
        img_fl_name = src_dir / (fl_name + ".png")
        md_fl_name = src_dir / (fl_name + ".json")

        assert img_fl_name.exists(), f"Image file doesn't exist: {str(img_fl_name)}"
        assert md_fl_name.exists(), f"Image file doesn't exist: {str(md_fl_name)}"

        with open(str(md_fl_name)) as md_fp:
            src_md = json.load(md_fp)

        yolo_annot = generate_YOLOv5_annotation(src_md, width, height)
        yolo_annot_fl_name = src_dir / (fl_name + ".txt")
        with open(str(yolo_annot_fl_name), "w+") as md_fp:  # writing annotations
            md_fp.write(yolo_annot)

    labels_fl_name = src_dir / ("data.yaml")
    with open(str(labels_fl_name), "w+") as fp:
        fp.write(generate_data_yaml(labels))


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Chess Detection: Data Processing")
    parser.add_argument(
        "-s",
        "--src",
        type=str,
        required=True,
        help="Source directory with the images (.png) and metadata (.json) files.",
    )
    parser.add_argument("--height", type=int, help="Image height", default=640)
    parser.add_argument("--width", type=int, help="Image width", default=640)
    print(parser.parse_args())
    main(parser.parse_args())
