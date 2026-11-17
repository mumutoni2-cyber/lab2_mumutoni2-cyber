#!/bin/bash
# Archives grades.csv with a timestamp, resets the workspace, and logs the action.

ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"
ORIGINAL="grades.csv"

[ -d "$ARCHIVE_DIR" ] || mkdir -p "$ARCHIVE_DIR"

if [ ! -f "$ORIGINAL" ]; then
    echo "Error: $ORIGINAL not found in $(pwd)." >&2
    exit 1
fi

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
NEW_NAME="grades_${TIMESTAMP}.csv"

mv "$ORIGINAL" "$ARCHIVE_DIR/$NEW_NAME" || exit 1
touch "$ORIGINAL"

echo "[$TIMESTAMP] original: $ORIGINAL | archived as: $ARCHIVE_DIR/$NEW_NAME" >> "$LOG_FILE"
echo "Archived $ORIGINAL -> $ARCHIVE_DIR/$NEW_NAME"
