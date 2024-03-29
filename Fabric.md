## Obsidian + Fabric = 💕

Fabric pairs well with Obsidian.md:

[GitHub - danielmiessler/fabric: fabric is an open-source framework for augmenting humans using AI. It provides a modular framework for solving specific problems using a crowdsourced set of AI prompts that can be used anywhere.](https://github.com/danielmiessler/fabric/)

## Configuration
You can find API keys and other environment variables in `~/.config/fabric/.env`

## Tooling

This tooling comes bundled with Fabric

- `save [--tag TAG] [--nofabric] <stub>`
    - A "tee-like" utility for pipelining saved content with the option to generate Obsidian front matter, use --nofabric to suppress default tags. This tool is configured to write outputs to Pedsidian/Fabric/CLI.
- `ts <audio_file>`
    - Transcribe a local audio file.
    - We can also use Whisper: `whisper transcribe <audio_file>`
- `yt --transcript https://www.youtube....`
    - Pull the transcript from a given YouTube, requires API key setup.

Other third party tooling I've installed and if of relevant value:

- `yt-dlp <url>` retrieve video content from various sources, which can then be piped through transcription. there's a **TON** of command line options for this utility.
    - `yt-download <url>` alias that enforces .mp4 output.
- `pdftotext <file> - | clean ` feed PDF content into the pipeline.

## Obsidian Integration
I define new patterns within Obsidian as, for example, `Fabric/Patterns/PATTERN_NAME/system.md`. Then run `fabric-update` to sync new patterns as CLI commands. Then you can start chaining commands together to get content out of, processed, and back into Obsidian. Some examples:

```
# Pull content via Chrome, multiplex it out through various prompts in parallel, save those results back into Obsidian with a tag and display the MD to screen via 'glow'.
cf https://towardsdatascience.com/visualize-your-rag-data-evaluate-your-retrieval-augmented-generation-system-with-ragas-fc2486308557 | fms | save visualize-your-rag | glow
```

## Custom Commands
Some commands via @pedramamini. We can chain these things together to create complex pipelines:

- `clean` remove non UTF8 characters from input stream.
- `chrome-fetch <url>` retrieve content via Chrome/Selenium. I've contributed [this](https://gist.github.com/pedramamini/e1f7f9dc6013734fca44961cca4e7890) to [Fabric](https://github.com/danielmiessler/fabric/issues/289).
- `compress-video <video>` compress large videos down for local storage.
- `fabric-multiplex` feeds stdin into multiple patterns and collects all their outputs in parallel, [this](https://gist.github.com/pedramamini/db892ddeed5179a58309b7345970a864) is also contributed to [Fabric](https://github.com/danielmiessler/fabric/issues/290).
- `fabric-patterns` list all fabric patterns, newest first.
- `fabric-pattern $PATTERN` show the system.md prompt for the given pattern.
- `fabric-update` updates `~/Utils/Fabric` repo, pulls down latest patterns into `/Users/pedram/.config/fabric/patterns`, symlinks all Pedsidian patterns as well.
- `md-filter $SECTION` pipe Markdown through this utility to extract specific headings.
- `md-speak-by-section` pipe Markdown through this utility to speak the output section-by-section.
- `speak` alias to `say -r 195` for local speaking of content.

```
alias c='pbcopy'
alias clean='iconv -f utf-8 -t utf-8//IGNORE'
alias gollama='OLLAMA_ORIGINS=app://obsidian.md* open -a Ollama.app'
alias ollama-update="for model in \$(ollama list | awk '{print \$1}' | tail -n +2); do ollama pull \$model; done"
alias p='pbpaste'
alias play='afplay -q 1'
alias speak='say -r 195'

yt-download ()
{
    if [[ $# -ne 1 ]]; then
        echo "Usage: yt-download <video-url>"
        return 1
    fi

    yt-dlp -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' $1
}

compress-video ()
{
    if [[ $# -ne 1 ]]; then
        echo "Usage: compress_video <video_name>"
        return 1
    fi

    input_file="$1"
    output_file="${input_file%.mov}_compressed.mov"

    ffmpeg -i "$input_file" -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 128k "$output_file"

    if [[ $? -eq 0 ]]; then
        mv "$output_file" "$input_file"
        echo "Compression successful. Compressed file replaced the original."
    else
        echo "Error: Compression failed."
    fi
}

pf ()
{
    local temp_file=$(mktemp)
    curl "$1" -so "$temp_file"
    pdftotext "$temp_file" - | clean
    rm -f "$temp_file"
}

cf ()
{
    chrome-fetch "$1" --headless --referrer --adblock --bypass --human --echourl --stats
}

md-filter ()
{
  keyword=$(echo "$1" | awk '{print tolower($0)}')
  awk -v keyword="$keyword" '
    BEGIN { RS=""; FS="\n"; IGNORECASE=1; found=0 }
    {
      if (found) {
        if ($1 ~ "^#+") exit
        else print
      }
      else {
        for (i=1; i<=NF; i++) {
          if ($i ~ "^#+" && tolower($i) ~ keyword) {
            found=1
            print $i
          }
        }
      }
    }
  '
}

# pedram added, update fabric and link all Obsidian patterns into the environment.
function fabric-update ()
{
    cd /Users/pedram/Utils/Fabric/patterns
    git pull
    pipx upgrade fabric
    fabric --update

    # XXX - for some reason the second time this routine runs it will switch symlinks to directories. so we are simply
    # blowing them all away for now.
    rm -rf /Users/pedram/.config/fabric/patterns/ped_*

    for ped_pattern in /Users/pedram/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Pedsidian/Fabric/Patterns/ped_*
    do
        filename=$(basename "$ped_pattern")
        if [ ! -e "/Users/pedram/.config/fabric/patterns/$filename" ]
        then
            echo "linking $filename"
            ln -s "$ped_pattern" /Users/pedram/.config/fabric/patterns/$filename
        fi
    done

    echo "done. refresh other shells via:"
    echo "source ~/.zshrc"

    # refresh current shell.
    source ~/.zshrc
}

# pedram added, list fabric patterns, newest first.
function fabric-patterns ()
{
    echo ">>>>> Ped Patterns"
    ls -1 /Users/pedram/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Pedsidian/Fabric/Patterns
    echo
    echo ">>>>> Default Patterns"
    ls -lt /Users/pedram/Utils/Fabric/patterns | awk '{print $9}' | xargs -I {} stat -f "%Sm %N" -t "%Y-%m-%d" /Users/pedram/Utils/Fabric/patterns/{} | xargs -n 2 sh -c 'echo "$0 $(basename "$1")"'
}

# pedram added, view pattern details via glow.
function fabric-pattern ()
{
    pattern=$1
    if [ ! -e /Users/pedram/.config/fabric/patterns/$pattern ]
    then
        echo "invalid pattern: $pattern"
        return
    fi

    glow /Users/pedram/.config/fabric/patterns/$pattern/system.md
}

# fabric multiplex shortcuts.
alias fmh='echo "fm{a,s,sn,c,p} a=analyze s=summarize sn=summarize-newsletter c=critique p=paper"'
alias fms='fabric-multiplex summarize ped_summarize ped_summarize_twitter ped_summarize_linkedin extract_wisdom label_and_rate rate_value'
alias fmsn='fabric-multiplex summarize_newsletter ped_summarize extract_wisdom analyze_prose_pinker find_logical_fallacies extract_sponsors'
alias fmc='fabric-multiplex analyze_claims analyze_prose_pinker find_logical_fallacies label_and_rate rate_value'
alias fmp='fabric-multiplex summarize analyze_paper analyze_claims analyze_tech_impact find_logical_fallacies'
alias fma='fabric-multiplex cat summarize extract_wisdom analyze_claims'

# pedram fabric aliases
for d in /Users/pedram/.config/fabric/patterns/ped_*
do
    pattern=$(basename $d)
    alias $pattern="fabric --pattern $pattern"
    alias ${pattern}_local="fabric --pattern $pattern --model gemma:7b"
    alias ${pattern}_claude="fabric --pattern $pattern --model claude-3-haiku-20240307"
done
```
