# Utility to compare output transcript to reference

Uses [Ukkonen algorithm](https://www.sciencedirect.com/science/article/pii/S0019995885800462) to efficiently compute Leneshtein distance and character error rate (CER).

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
  -e, --error_type [CER|WER]
  -j, --output_format [JSON|TABLE]
  --help                          Show this message and exit.
```

## Acknowledgements

Contributed by [VoiceGain](https://www.voicegain.ai).

VoiceGain provides Deep-Neural-Network-based Speech-to-Text (ASR) both in Cloud and On-Prem.
Acessible via Web API or MRCP interface.


## License

[MIT © VoiceGain](./LICENSE)
