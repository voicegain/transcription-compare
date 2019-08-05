from ..utils.html_color import create_bg_color
# from transcription_compare.levenshtein_distance_calculator import UKKLevenshteinDistanceCalculator
# from transcription_compare.tokenizer import CharacterTokenizer


class MultiResult:
    def __init__(self, output_results: dict, calculator_local):
        """
        :param output_results: dict from identifier(str) to Result
        """
        self.calculator_local = calculator_local
        self.distance = []
        self.error_rate = []
        self.is_final = []
        self.substitution = []
        self.insertion = []
        self.deletion = []
        self.identifiers = []
        alignment_results = []

        for (identifier, result) in output_results.items():
            self.identifiers.append(identifier)
            self.distance.append(result.distance)
            self.error_rate.append(result.error_rate)
            self.is_final.append(result.is_final)
            self.substitution.append(result.substitution)
            self.insertion.append(result.insertion)
            self.deletion.append(result.deletion)
            alignment_results.append(result.alignment_result)

        self.multi_alignment_result = MultiAlignmentResult(alignment_results, self.calculator_local)

    def to_html(self):
        """
        very beginning table and call to_html of self.multi_alignment_result
        <html>
          <head>
            <style>
              table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
              }

              td, th {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
              }

            </style>
          </head>
          <body>

            <h2>transcription-compare Table</h2>
             <table>
              <tr>
                <th>output_name</th>
          </tr>
        <tbody>
          <tr>
            <td>1</td>
          </tr>
          <tr>
            <td>February</td>
          </tr>
            <tr>
            <td>33</td>
          </tr>
        </tbody>
        </table>
        :return:
        """
        # create table 1
        body = """<html>
            <head>
            <style>
            table {
              font-family: arial, sans-serif;
              border-collapse: collapse;
              width: 100%;
            }

            td, th {
              border: 1px solid #dddddd;
              text-align: left;
              padding: 8px;
            }

            </style>
            </head>
            <body>

            <h2>transcription-compare Table</h2>
                 <table>
                  <tr>
                    <th>output_name</th>
                    <th>distance</th>
                    <th>error_rate</th>
                    <th>substitution</th>
                    <th>insertion</th>
                    <th>deletion</th>
              </tr>
            <tbody>
               """
        # print('self.distance', self.distance)
        for index, identifier in enumerate(self.identifiers):
            # print('identifiers', identifier)
            body += """<tr><td>{}</td>""".format(identifier)
            body += '\n<td>' + str(self.distance[index]) + '</td>'
            body += '\n<td>' + str(self.error_rate[index]) + '</td>'
            body += '\n<td>' + str(self.substitution[index]) + '</td>'
            body += '\n<td>' + str(self.insertion[index]) + '</td>'
            body += '\n<td>' + str(self.deletion[index]) + '</td>\n</tr>'
        body += """</tbody>
                </table>
                """
        body += self.multi_alignment_result.to_html()
        body += '\n</body>\n</html>'
        return body

    def to_json(self):
        """
        self.distance = []
        self.error_rate = []
        self.is_final = []
        self.substitution = []
        self.insertion = []
        self.deletion = []
        self.identifiers = []
        [{"ref": "abc", "out": [[],["abc"],[]]}, {"ref": "efg", "out": [["hehe"],[],["cdff"]]}]
        :return:
        """
        identifiers = []
        for identifier in self.identifiers:
            identifiers.append(identifier)
        # print('identifiers', identifiers)
        return {
            "distance": self.distance,
            "error_rate": self.error_rate,
            "is_final": self.is_final,
            "substitution": self.substitution,
            "insertion": self.insertion,
            "deletion": self.deletion,
            "identifiers": identifiers,
            "multi_alignment_result": self.multi_alignment_result.to_json()
        }


class MultiAlignmentResult:
    def __init__(self, alignment_results, calculator_local):
        """
        :param alignment_results: List[AlignmentResult]
        """
        self.calculator_local = calculator_local
        if len(alignment_results) < 1:
            raise ValueError("length of alignment_results should be >= １")
        # print('len(alignment_results)', len(alignment_results))
        self.multi_alignment_tokens = []
        if None in alignment_results:
            # TODO: if one of the result does not have alignment_result, return
            return
        for i in range(len(alignment_results) - 1):
            if len(alignment_results[i]) != len(alignment_results[i+1]):
                raise ValueError("alignment_result have different length in results")

        alignment_result_size = len(alignment_results[0])
        alignment_tokens_list = [
            alignment_result.aligned_tokens_list for alignment_result in alignment_results
        ]
        # print('alignment_tokens_list', alignment_tokens_list)
        for i in range(alignment_result_size):
            tmp_aligned_token_list = []
            for alignment_tokens in alignment_tokens_list:
                tmp_aligned_token_list.append(alignment_tokens[i])
            self.multi_alignment_tokens.append(MultiAlignedToken(tmp_aligned_token_list, self.calculator_local))

    def to_html(self):
        """
        include header and call to_html of all items in self.multi_alignment_tokens
        Return table2
            <table>
                  <tr>
            <th>num</th>
            <th>Reference</th>
                    <th>output</th>
                    <th>local_cer</th>
                    <th>distance</th>
                    <th>substitution</th>
                    <th>insertion</th>
                    <th>deletion</th>
              </tr>
            <tbody>
            call
            </tbody>
            </table>
        :return:
        """
        body = """<table>\n<tr>\n<th>num</th>
        <th>Reference</th>
                   <th>output</th>
                   <th>local_cer</th>
                <th>distance</th>
                <th>sub</th>
                <th>ins</th>
                <th>del</th></tr><tbody>"""
        # create header
        for c, t in enumerate(self.multi_alignment_tokens):
            body += t.to_html(c)
        # something else
        # <p> annotation </p>
        body += '\n</tbody>\n</table>'
        return body

    def to_json(self):
        """
        put them together
        [{"ref": "abc", "out": [[],["abc"],[]]}, {"ref": "efg", "out": [["hehe"],[],["cdff"]]}]
        :return:
        """
        json_list = []

        for t in self.multi_alignment_tokens:
            json_list.append(t.to_json())
        return json_list


class MultiAlignedToken:
    def __init__(self, aligned_token_list, calculator_local):
        self.calculator_local = calculator_local
        self.aligned_token_list = aligned_token_list
        self.reference = None
        self.output = []
        self.distance = []
        self.substitution = []
        self.insertion = []
        self.deletion = []
        self.local_cer = []
        for aligned_token in self.aligned_token_list:
            distance, substitution, insertion, deletion = \
                aligned_token.calculate_three_kinds_of_distance()
            local_cer = aligned_token.get_character_level_result(self.calculator_local).distance
            if self.reference is None:
                self.reference = aligned_token.reference
                self.output.append(aligned_token.outputs)
                self.distance.append(distance)
                self.substitution.append(substitution)
                self.insertion.append(insertion)
                self.deletion.append(deletion)
                self.local_cer.append(local_cer)
                # print('self.reference is None',self.reference)
            else:
                if self.reference != aligned_token.reference:
                    raise ValueError("Difference reference")
                else:
                    # print('aligned_token.outputs', aligned_token.outputs)
                    self.distance.append(distance)
                    self.substitution.append(substitution)
                    self.insertion.append(insertion)
                    self.deletion.append(deletion)
                    self.output.append(aligned_token.outputs)
                    self.local_cer.append(local_cer)
                    # print('!!!!self.output', self.output)

    def to_html(self, c):
        """
        one row
        Example output string:
          <tr>
            <td rowspan="3">ref</td>
            <th>num</th>
            <td>output</td>
            <th>local_cer</th>
            <td>distance</td>
            <td>sub</td>
            <td>ins</td>
            <td>de</td>
          </tr>
          <tr>
            <td>output</td>
            <th>local_cer</th>
            <td>distance</td>
            <td>sub</td>
            <td>ins</td>
            <td>de</td>
          </tr>
          <tr>
            <td>output</td>
            <th>local_cer</th>
            <td>distance</td>
            <td>sub</td>
            <td>ins</td>
            <td>de</td>
          </tr>
        :return:
        """
        if (c % 2) == 0:

            message = '\n<tr bgcolor=#dddddd >\n<td rowspan="{}"  width="10%">'.format(len(self.output)) + str(c) + '</td>'
            message += '\n<td rowspan="{}">'.format(len(self.output)) + self.reference + '</td>'
        else:
            message = '\n<tr>\n<td rowspan="{}">'.format(len(self.output)) + str(c) + '</td>'
            message += '\n<td rowspan="{}">'.format(len(self.output)) + self.reference + '</td>'
        # message += '\n<td>' + str(c) + '</td>'
        for i in range(len(self.output)):
            if i != 0:
                if (c % 2) == 0:
                    message += '\n<tr bgcolor=#dddddd>'
                else:
                    message += '\n<tr>'
            message += '\n<td {}>'.format(
                create_bg_color(self.substitution[i], self.insertion[i], self.deletion[i])
            ) + " ".join(self.output[i]) + '</td>'
            #  local_cer
            message += '\n<td>' + str(self.local_cer[i]) + '</td>'
            message += '\n<td>' + str(self.distance[i]) + '</td>'
            message += '\n<td>' + str(self.substitution[i]) + '</td>'
            message += '\n<td>' + str(self.insertion[i]) + '</td>'
            message += '\n<td>' + str(self.deletion[i]) + '</td>\n</tr>'

        return message

    def to_json(self):
        """
        {"ref": "abc", "out": [[],["abc"],[]]}
        :return:
        """
        return {
            "ref": self.reference,
            "out": self.output
        }

