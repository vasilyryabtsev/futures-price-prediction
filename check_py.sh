#!/bin/bash

DIR=${1:-.}


for file in $(find "$DIR" -name "*.py"); do
    echo "Тестирование файла: $file"

    echo "pycodestyle:"
    python3 -m pycodestyle "$file"

    echo "flake8:"
    flake8 "$file" --max-line-length=120

    echo "pylint:"
    pylint "$file" --max-line-length=120 --disable="C0103,C0114,C0115"

    echo "-----------------------------------"
done