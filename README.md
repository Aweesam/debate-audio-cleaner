# debate-audio-cleaner


## Docker usage

Build the image:

```bash
docker build -t debate-audio-cleaner .
```

Run the cleaner on a YouTube video:

```bash
docker run --rm -v "$(pwd)/output:/app/output" debate-audio-cleaner \
  python src/clean_debate_audio.py "https://youtu.be/VIDEO_ID" --gpu
```

The default command displays CLI help:

```bash
docker run --rm debate-audio-cleaner
```
