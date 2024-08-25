#!/bin/bash

# Do we want to ingest the videos into our vault?
DOWNLOAD_VIDEOS=false

# Ensure we're running in the directory where this script is located
cd "/Users/pedram/Library/Mobile Documents/iCloud~md~obsidian/Documents/Pedsidian/Content Farm/YouTube"

# Set the playlist URL
playlist_url="https://www.youtube.com/playlist?list=PLubfvXZfGDEs-TGK8wkNmLpLXWY6WcZb5"

# Specify the Table of Contents file
toc_file="📇 YouTube Index.md"

# Initialize TOC file only if it doesn't exist
if [ ! -f "$toc_file" ]; then
    echo "# Table of Contents" > "$toc_file"
    echo "Created Table of Contents file."
fi

# Initialize an array to keep track of processed videos
processed_videos=()

# Fetch playlist data using yt-dlp and parse it with jq
entries=$(yt-dlp -J --flat-playlist "$playlist_url" | jq -r '.entries[] | "\(.id) \(.title)"')

# Count total videos
total=$(echo "$entries" | wc -l | awk '{print $1}')
echo "Total videos in playlist: $total"

# Counter for progress
count=0

# Process each video in the playlist
echo "$entries" | while IFS=' ' read -r id title; do
    # Skip "deleted video" entries
    title_lower=$(echo "$title" | tr '[:upper:]' '[:lower:]')

    if [[ "$title_lower" == "deleted video" || -z "$id" ]]; then
        echo "Skipping deleted video or invalid entry."
        continue
    fi

    # Increment counter
    ((count++))

    # Clean title to remove any non-alphanumeric characters except spaces,
    # replace multiple spaces with a single space, and trim trailing spaces
    clean_title=$(echo "$title" | sed 's/[^a-zA-Z0-9 ]//g' | sed 's/  */ /g' | sed 's/[[:space:]]*$//')

    # Construct the video URL
    video_url="https://www.youtube.com/watch?v=$id"

    # Log processing
    echo "Processing ($count/$total): $title"

    markdown_file="${clean_title}.md"

    # Check for the existence of the video file using the cleaned title
    if [ "$DOWNLOAD_VIDEOS" = true ]; then
        video_file="./Videos/${clean_title}.mp4"
        if [[ -f "$video_file" ]]; then
            echo "Video already downloaded: $title"
        else
            echo "Downloading video: $title"
            yt-dlp -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' -o "$video_file" "$video_url"
            # Add the video file to the list of processed videos
            processed_videos+=("$video_file")
        fi
    fi

    # Create markdown file if it doesn't exist
    if [[ ! -f "$markdown_file" ]]; then
        echo "Creating markdown file: $markdown_file"
        echo "[YouTube Link]($video_url)" >> "$markdown_file"
        echo "- [ ] Watched" >> "$markdown_file"
    fi

    # Add the title to the ToC if not already present
    if ! grep -Fq -- "- [[$clean_title]]" "$toc_file"; then
        echo "- [[$clean_title]]" >> "$toc_file"
        echo "Added '$clean_title' to Table of Contents."
    fi

    # Skip processing if #no-transcript tag exists
    if grep -q "^#no-transcript" "$markdown_file"; then
        echo "No transcript available, skipping further processing for $title."
        continue
    fi

    # Generate transcript if missing
    if ! grep -q "^# Summary" "$markdown_file"; then
        echo "Checking for available transcript for $title..."
        transcript_available=$(yt --transcript "$video_url" 2>/dev/null)

        if [[ $transcript_available == *"Transcript not available"* ]]; then
            echo "No transcript available for $title."
            echo "#no-transcript" >> "$markdown_file"
            continue
        else
            echo "Transcript available from YouTube."
            transcript=$(echo "$transcript_available" | fabric --pattern ped_sitrep)
            echo "Transcript summarized."
            echo -e "\n# Summary\n$transcript" >> "$markdown_file"
        fi
    fi

    echo "Processed $count of $total videos."
done

echo "Download complete. Markdown files generated."

# Log the list of new video files processed
if [ ${#processed_videos[@]} -gt 0 ]; then
    echo "Processed new video files in this run:"
    for video in "${processed_videos[@]}"; do
        echo "$video"
    done
else
    echo "No new video files were processed in this run."
fi
