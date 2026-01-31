#!/usr/bin/env bash

input_file="output.txt"
current_section=""
auto_counter=0

pad() {
  printf "%03d" "$1"
}

sanitize() {
  echo "$1" | sed 's/[\/:*?"<>|]//g'
}

while IFS= read -r line; do

  # Section line
  if [[ "$line" =~ ^Section\ ([0-9]+):\ (.*)$ ]]; then
    sec_num=$(pad "${BASH_REMATCH[1]}")
    sec_name=$(sanitize "${BASH_REMATCH[2]}")
    current_section="Section_${sec_num} - ${sec_name}"
    mkdir -p "$current_section"
    auto_counter=0
    continue
  fi

  # Numbered lectures
  if [[ "$line" =~ ^[[:space:]]*([0-9]+)\.\ (.*)$ ]]; then
    num=$(pad "${BASH_REMATCH[1]}")
    title=$(sanitize "${BASH_REMATCH[2]}")
    touch "$current_section/${num} - ${title}.md"
    auto_counter=${BASH_REMATCH[1]}
    continue
  fi

  # Coding Exercise Quiz Assignment without leading number
  if [[ "$line" =~ ^[[:space:]]*(Coding\ Exercise|Quiz|Assignment)[[:space:]]*([0-9]*):?[[:space:]]*(.*)$ ]]; then
    auto_counter=$((auto_counter + 1))
    num=$(pad "$auto_counter")
    title=$(sanitize "${BASH_REMATCH[1]} ${BASH_REMATCH[2]} ${BASH_REMATCH[3]}")
    title=$(echo "$title" | sed 's/  */ /g')
    touch "$current_section/${num} - ${title}.md"
    continue
  fi

done < "$input_file"

echo "Course folder tree created successfully"
