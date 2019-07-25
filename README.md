# Utility to compare output transcript to reference

Uses [Ukkonen algorithm](https://www.sciencedirect.com/science/article/pii/S0019995885800462) to efficiently compute [Leveshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) and character error rate (CER).

Additionally it can output alignment information.

## Usage

```
Usage: transcribe-compare [OPTIONS]

  Transcription compare tool provided by VoiceGain

Options:
  -r, --reference TEXT            source string
  -o, --output TEXT               target string
  -R, --reference_file FILENAME   source file path
  -O, --output_file FILENAME      target file path
  -a, --alignment                 Do you want to see the alignment result?
                                  True/False
  -e, --error_type [CER|WER]
  -j, --output_format [JSON|TABLE]
  -l, --to_lower                  Do you want to lower all the words?
                                  True/False
  -p, --remove_punctuation        Do you want to remove all the punctuation?
                                  True/False
  -P, --to_save_plot              Do you want to see the windows? True/False
  -s, --to_edit_step INTEGER      Please enter the step
  -w, --to_edit_width INTEGER     Please enter the width
  --help                          Show this message and exit.
  ```

## Dependencies

+ click
+ inflect
+ re

# Sample Commands

```
python transcribe-compare -R sample_data/The_Princess_and_the_Pea-reference.txt -O sample_data/The_Princess_and_the_Pea-output-1.txt -e CER
```

## Acknowledgements

Contributed by [VoiceGain](https://www.voicegain.ai).

VoiceGain provides Deep-Neural-Network-based Speech-to-Text (ASR) both in Cloud and On-Prem.
Acessible via Web API or MRCP interface.


## License

[MIT © VoiceGain](./LICENSE)
