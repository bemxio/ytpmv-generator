# ytpmv-generator
A script that takes notes from a MIDI file track, and fits them into a song using samples that are pitch-corrected and speed-shifted.

## Running
Make sure you're running Python 3.7+ before doing any steps.

1. Clone the repository into a directory of your choice.
2. Move to the directory with the files in a terminal.
3. Get the original song into the directory as `song.wav`, and the samples to be used in the YTPMV.
4. Get your MIDI file into the directory as `baseline.mid`, with a track that can be used as a baseline.
5. Edit the `samples` list in the `main.py` file, correcting the root notes & the path names.
6. Run the `main.py` file and wait for the `final.wav` file to generate!

## Contributing
As with all my projects, contributions are highly appreciated!