# news-image-20-nov

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/heruruben-hub/news-image-20-nov/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/heruruben-hub/news-image-20-nov/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

One picture of one day: the world news of Friday 20 November 2026, drawn
pixel by pixel by a single Python program.

`main.py` (Python 3, standard library only, no network) draws a newspaper-style
front page on a 1024×1024 canvas and writes it as a PNG to
`/output/entry.png`. It uses no clock and no randomness, so every run produces
exactly the same bytes.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Without `MAKEFUN_OUTPUT_DIR` the image is written to `/output/entry.png`.

## The six stories on the page

1. **Diplomacy — US / Iran.** Trump says he is in "no rush" on an Iran
   decision and will look at it next year, Axios reports; no decision before
   2027 is expected.
2. **Weather — India.** Cyclone Akvan bears down on Odisha; landfall due
   around noon, with nearly 300,000 people moved to shelters as winds near
   110 kmph.
3. **Markets — Tech.** Anthropic shares jump on their debut, closing 17%
   higher on their first day of trading on Nasdaq.
4. **Space — Japan.** Engine trouble forces Hayabusa2 to drop its asteroid
   landing; no more asteroid landing.
5. **Europe — Ukraine.** European leaders say they are ready for talks with
   Russia on ending the war in Ukraine.
6. **Culture — Gaming.** GTA 6 sales pass $1.8 billion, already topping
   The Odyssey's global box-office run.

## How it is drawn

The program embeds its own 5×7 bitmap font as data and renders every letter,
icon and panel from primitives (rectangles, discs, lines, triangles) into an
RGB framebuffer, then encodes the PNG itself with `zlib` and `struct`. Nothing
is copied from a ready-made image.

## Sources

Each story was checked against reporting published on 20 November 2026:
Reuters and Axios for Trump's "no rush" remark on Iran; the IMD via The
Hindu for Cyclone Akvan's landfall and evacuations in Odisha; The Hindu for
Anthropic's 17% first-day share rise on Nasdaq; Space.com for Hayabusa2
dropping its asteroid landing; the BBC for Europe's readiness for talks with
Russia; and Mezha for GTA 6 sales passing $1.8 billion.

Verified locally: two consecutive runs of `main.py` produce byte-identical
PNG files (same SHA-256), 20,861 bytes, 1024×1024 — well inside the
competition's 1 MiB and 1024×1024 limits.

SHA-256 of `entry.png`:
`e5c8324339401718ba0555743c35998c4b5480bc3ffba9931d60927d6f26b71a`

---

Entered on [make.fun](https://make.fun/?ref=kh6903y0&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
