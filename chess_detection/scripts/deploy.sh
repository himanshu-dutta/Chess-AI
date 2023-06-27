#!/bin/bash

MODEL="yolov5s/2D/416x416_Grayscaled_Augmented/best.torchscript.pt"
MODEL_NAME="yolov5s"

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )""/.." \
&& \
mkdir -p $BASEDIR"/model-store/" \
&& \
torch-model-archiver --model-name $MODEL_NAME --version 1.0 --serialized-file $BASEDIR"/models/$MODEL" --extra-files $BASEDIR"/extra_files/index_to_name.json",$BASEDIR"/src/object_detection.py",$BASEDIR"/src/utils.py",$BASEDIR"/src/config.py" --handler $BASEDIR"/src/handler.py" --export-path $BASEDIR"/model-store" -f \
&& \
torchserve --start --model-store $BASEDIR"/model-store" --models $MODEL_NAME="$MODEL_NAME.mar" --ts-config $BASEDIR"/torchserve.properties"

tail -f > /dev/null