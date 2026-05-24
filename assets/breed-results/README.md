# Breed Result Assets

This directory is reserved for real breed-specific DBTI result images.

Only add images here after they are generated in the accepted low-poly DBTI style:

- one redrawn dog breed per image
- same scene, props, composition, and humor as the base result image
- no pasted sticker overlays
- square image, compressed for web loading
- target size: under 2 MB per image

Expected layout:

```text
assets/breed-results/<breed-key>/<result-file>.jpg
```

Example:

```text
assets/breed-results/golden-retriever/yes-or-no.jpg
```

After adding generated source images, run:

```bash
python3 tools/ingest_breed_results.py --source <source-dir> --update-index
```

