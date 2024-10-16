#!/bin/bash -x

pip3 install openai-whisper
# conda install ffmpeg

wget https://upload.wikimedia.org/wikipedia/commons/7/75/Winston_Churchill_-_Be_Ye_Men_of_Valour.ogg
whisper Winston_Churchill_-_Be_Ye_Men_of_Valour.ogg --model medium

wget https://upload.wikimedia.org/wikipedia/commons/1/1a/Lenin_-_What_Is_Soviet_Power.ogg
whisper Lenin_-_What_Is_Soviet_Power.ogg --language Russian --task translate --model medium
