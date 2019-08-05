#!/usr/bin/env python

import click
from transcription_compare.levenshtein_distance_calculator import UKKLevenshteinDistanceCalculator
from transcription_compare.tokenizer import CharacterTokenizer, WordTokenizer
from transcription_compare.local_optimizer.digit_util import update_alignment_result

@click.command()
@click.option('--reference', '-r', type=str, help='source string')
@click.option('--output', '-o',  type=str, help='target string')
@click.option('--reference_file', '-R', type=click.File('r'), help='source file path')
@click.option('--output_file', '-O', type=click.File('r'), help='target file path')
@click.option('--alignment', '-a', default=False, is_flag=True, help='Do you want to see the alignment result?')
@click.option('--error_type', '-e', default='CER', type=click.Choice(['CER', 'WER']))
@click.option('--output_format', '-j', default='TABLE', type=click.Choice(['JSON', 'TABLE']))
def main(reference, output, reference_file, output_file, alignment, error_type,output_format,digit):
    """
    Transcription compare tool provided by VoiceGain
    """
    if reference is not None:
        reference = reference
    elif reference_file is not None:
        # with open(reference_file, 'r') as file1:
        reference = reference_file.read()
    else:
        raise ValueError("One of --reference and --reference_file must be specified")

    if output is not None:
        output = output
    elif output_file is not None:
        # with open(output_file, 'r') as file2:
        output = output_file.read()
    else:
        raise ValueError("One of --output and --output_file must be specified")

    if error_type == "CER":

        calculator = UKKLevenshteinDistanceCalculator(
            tokenizer=CharacterTokenizer(),
            get_alignment_result=alignment
        )
    else:
        calculator = UKKLevenshteinDistanceCalculator(
            tokenizer=WordTokenizer(),
            get_alignment_result=alignment
        )

    if output_format == 'TABLE':
        alignment_result = calculator.get_distance(reference, output).alignment_result
        error_list =alignment_result.get_error_section_list()
        for e in error_list:
            print("+++++++++++++++")
            print(e.original_alignment_result)
            # updated_alignment_result = update_alignment_result(e.original_alignment_result)
            updated_alignment_result = update_alignment_result(e.original_alignment_result)
            e.set_correction(updated_alignment_result)

        alignment_result.apply_error_section_list(error_list)
        click.echo(alignment_result)

    if output_format == 'JSON':
        alignment_result = calculator.get_distance(reference, output).alignment_result
        error_list =alignment_result.get_error_section_list()
        for e in error_list:
            print("+++++++++++++++")
            print(e.original_alignment_result)
            # updated_alignment_result = update_alignment_result(e.original_alignment_result)
            updated_alignment_result = update_alignment_result(e.original_alignment_result)
            e.set_correction(updated_alignment_result)

        alignment_result.apply_error_section_list(error_list)
        distance = alignment_result.calculate_three_kinds_of_distance()[0]
        click.echo(alignment_result.to_json())




if __name__ == '__main__':
    main()
