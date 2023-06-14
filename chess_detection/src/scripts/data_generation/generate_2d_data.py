from src import board as b
from pathlib import Path
import random
import argparse
import os

from PIL import ImageGrab
from string import Template
import json
import time


black_positions = [
    b.Pieces.ROOK | b.Colors.BLACK,
    b.Pieces.KNIGHT | b.Colors.BLACK,
    b.Pieces.BISHOP | b.Colors.BLACK,
    b.Pieces.QUEEN | b.Colors.BLACK,
    b.Pieces.KING | b.Colors.BLACK,
    b.Pieces.BISHOP | b.Colors.BLACK,
    b.Pieces.KNIGHT | b.Colors.BLACK,
    b.Pieces.ROOK | b.Colors.BLACK,
    b.Pieces.PAWN | b.Colors.BLACK,
    b.Pieces.PAWN | b.Colors.BLACK,
    b.Pieces.PAWN | b.Colors.BLACK,
    b.Pieces.PAWN | b.Colors.BLACK,
    b.Pieces.PAWN | b.Colors.BLACK,
    b.Pieces.PAWN | b.Colors.BLACK,
    b.Pieces.PAWN | b.Colors.BLACK,
    b.Pieces.PAWN | b.Colors.BLACK,
]

white_positions = [
    b.Pieces.ROOK | b.Colors.WHITE,
    b.Pieces.KNIGHT | b.Colors.WHITE,
    b.Pieces.BISHOP | b.Colors.WHITE,
    b.Pieces.QUEEN | b.Colors.WHITE,
    b.Pieces.KING | b.Colors.WHITE,
    b.Pieces.BISHOP | b.Colors.WHITE,
    b.Pieces.KNIGHT | b.Colors.WHITE,
    b.Pieces.ROOK | b.Colors.WHITE,
    b.Pieces.PAWN | b.Colors.WHITE,
    b.Pieces.PAWN | b.Colors.WHITE,
    b.Pieces.PAWN | b.Colors.WHITE,
    b.Pieces.PAWN | b.Colors.WHITE,
    b.Pieces.PAWN | b.Colors.WHITE,
    b.Pieces.PAWN | b.Colors.WHITE,
    b.Pieces.PAWN | b.Colors.WHITE,
    b.Pieces.PAWN | b.Colors.WHITE,
]
board_positions_flat = black_positions + [b.Pieces.BLANK] * 32 + white_positions
html_template_path = str(
    Path("./src/scripts/data_generation/web/chess_board_template.html").absolute()
)
html_doc_path = str(
    Path("./src/scripts/data_generation/web/chess_board.html").absolute()
)


def generate_random_board() -> b.Board:
    board_positions = board_positions_flat
    random.shuffle(board_positions)
    board_positions = [
        board_positions[i : i + 8] for i in range(0, len(board_positions), 8)
    ]
    board = b.Board(board_positions, b.Colors.BLACK)
    return board


def generate_piece_bounding_boxes_from_board(board: b.Board, width: int, height: int):
    sq_width = width // 8
    sq_height = height // 8

    bboxes = []

    for rank_idx in range(len(board.piece_placements)):
        for file_idx in range(len(board.piece_placements[0])):
            if board.piece_placements[rank_idx][file_idx] == b.Pieces.BLANK:
                continue
            left = file_idx * sq_width
            top = rank_idx * sq_height
            piece_type = b.Board.encode_fen_square(
                board.piece_placements[rank_idx][file_idx]
            )
            bbox = {
                "type": piece_type,
                "top": top,
                "left": left,
                "width": sq_width,
                "height": sq_height,
            }
            bboxes.append(bbox)

    return bboxes


def generate_corner_bounding_boxes(width: int, height: int):
    bboxes = [
        {
            "type": "corner",
            "left": 0,
            "top": 0,
            "width": 20,
            "height": 20,
        },
        {
            "type": "corner",
            "left": width - 20,
            "top": 0,
            "width": 20,
            "height": 20,
        },
        {
            "type": "corner",
            "left": 0,
            "top": height - 20,
            "width": 20,
            "height": 20,
        },
        {
            "type": "corner",
            "left": width - 20,
            "top": height - 20,
            "width": 20,
            "height": 20,
        },
    ]
    return bboxes


def generate_metadata(board: b.Board, width: int, height: int):
    md = {
        "fen": board.fen(),
        "bounding_boxes": generate_piece_bounding_boxes_from_board(board, width, height)
        + generate_corner_bounding_boxes(width, height),
    }
    return md


def main(args: argparse.Namespace):
    dest_dir = Path(args.dest).absolute()
    if not dest_dir.exists():
        os.mkdir(str(dest_dir))

    num_samples = args.num_samples
    idx_width = len(str(num_samples - 1))

    width = args.width
    height = args.height
    left = args.screen_left
    top = args.screen_top

    with open(html_template_path, "r") as fl:
        html_template = fl.read()

    screen_bbox = [left, top, left + width, top + height]

    for idx in range(num_samples):
        fl_name = str(idx).zfill(idx_width)
        print("Processing file: ", fl_name)
        board = generate_random_board()
        mdata = generate_metadata(board, width, height)

        html_doc = Template(html_template).substitute(
            fen=f'"{board.fen()}"', width=width, height=height
        )
        with open(html_doc_path, "t+w") as fp:
            fp.write(html_doc)
        time.sleep(0.5)
        img = ImageGrab.grab(screen_bbox)

        img_path = dest_dir / (fl_name + ".png")
        mdata_path = dest_dir / (fl_name + ".json")

        img.save(str(img_path), "PNG")
        with open(mdata_path, "w+") as fp:
            json.dump(mdata, fp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Generate 2D image dataset")
    parser.add_argument(
        "-n",
        "--num_samples",
        type=int,
        required=True,
        help="Number of samples to generate",
    )
    parser.add_argument("--height", type=int, help="Image height", default=640)
    parser.add_argument("--width", type=int, help="Image width", default=640)
    parser.add_argument(
        "-sl", "--screen_left", type=int, required=True, help="Left offset for screen"
    )
    parser.add_argument(
        "-st", "--screen_top", type=int, required=True, help="Top offset for screen"
    )
    parser.add_argument(
        "-d",
        "--dest",
        type=str,
        required=True,
        help="Destination folder to add generated images and annotations.",
    )

    print("Waiting for 5 seconds before initiating data generation...", flush=True)
    time.sleep(5)
    main(parser.parse_args())
