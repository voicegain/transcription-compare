from transcription_compare.utils.html_color import create_bg_color
from transcription_compare.results.aligned_token_classifier import ErrorType


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
        self.total_rows = len(alignment_results[0])

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
        first table
        second table
        third table
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
        for index, identifier in enumerate(self.identifiers):
            body += """<tr><td>{}</td>""".format(identifier)
            body += '\n<td>' + str(self.distance[index]) + '</td>'
            body += '\n<td>' + str(self.error_rate[index]) + '</td>'
            body += '\n<td>' + str(self.substitution[index]) + '</td>'
            body += '\n<td>' + str(self.insertion[index]) + '</td>'
            body += '\n<td>' + str(self.deletion[index]) + '</td>\n</tr>'
        body += """</tbody>
                </table>
                """
        body += """<table>\n<tr>\n<th>error_type</th>"""
        for index, identifier in enumerate(self.identifiers):
            body += """ <th>{}</th>""".format(identifier)
            body += """<th>percentage</th>"""
        body += """</tr>"""
        body += self.multi_alignment_result.to_html_error_type(self.total_rows)
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
        self.size = len(alignment_results)
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

    def to_html_error_type(self, total_rows):
        # create header
        all_count_error_type = []
        for i in range(self.size):
            d = dict()
            for et in ErrorType:
                d[et] = 0
            all_count_error_type.append(d)
        for t in self.multi_alignment_tokens:
            error_type_list = t.error_type

            for (M, error_type) in enumerate(error_type_list):
                all_count_error_type[M][error_type] += 1

        # print(all_count_error_type)
        body = ''
        for key in ErrorType:
            if key == ErrorType.NA:
                continue
            body += """<tr><td>{}</td>""".format(key.get_display_name())
            for j in range(len(all_count_error_type)):
                # print('all_count_error_type[j][key]', all_count_error_type[j][key])
                body += '\n<td>' + str(all_count_error_type[j][key]) + '</td>'
                body += '\n<td>' + str(round(all_count_error_type[j][key]/total_rows, 7)) + '</td>' #  /all rows
        body += '\n</tr>'
        return body

    def to_html(self):
        """
        include header and call to_html of all items in self.multi_alignment_tokens
        Return table2
        <table>\n<tr>\n
           <th>error_type</th>
            <th>sum</th></tr><tbody>
                 \n</tbody>\n</table>


            <table>
                  <tr>
            <th>num</th>
            <th>Reference</th>
                    <th>output</th>
                    <th>error_type</th>
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
                   <th>error_type</th>
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
        self.aligned_token_list = aligned_token_list
        self.reference = None
        self.output = []
        self.distance = []
        self.substitution = []
        self.insertion = []
        self.deletion = []
        self.local_cer = []
        self.error_type = []
        for aligned_token in self.aligned_token_list:
            distance, substitution, insertion, deletion = \
                aligned_token.calculate_three_kinds_of_distance()
            local_cer = aligned_token.get_character_level_cer(calculator_local)

            if self.reference is None:
                self.reference = aligned_token.reference
            else:
                if self.reference != aligned_token.reference:
                    raise ValueError("Difference reference")
            self.output.append(aligned_token.outputs)
            self.distance.append(distance)
            self.substitution.append(substitution)
            self.insertion.append(insertion)
            self.deletion.append(deletion)
            self.local_cer.append(local_cer)
            self.error_type.append(aligned_token.classify())

    def to_html(self, c):
        """
        one row
        Example output string:
          <tr>
            <td rowspan="3">ref</td>
            <th>num</th>
            <td>output</td>
            <td>error_type</td>
            <td>local_cer</td>
            <td>distance</td>
            <td>sub</td>
            <td>ins</td>
            <td>de</td>
          </tr>
          <tr>
            <td>output</td>
            <td>error_type</td>
            <td>local_cer</td>
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

            message = '\n<tr bgcolor=#dddddd >\n<td rowspan="{}"  width="10%">'.format(len(self.output)) \
                      + str(c) + '</td>'
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
            message += '\n<td>' + str(self.error_type[i].get_display_name()) + '</td>'
            #  local_cer
            message += '\n<td>' + str(self.local_cer[i]) + '</td>'
            message += '\n<td>' + str(self.distance[i]) + '</td>'
            message += '\n<td>' + str(self.substitution[i]) + '</td>'
            message += '\n<td>' + str(self.insertion[i]) + '</td>'
            message += '\n<td>' + str(self.deletion[i]) + '</td>\n</tr>'

        return message

    def to_json(self):
        """
        {"ref": "abc", "out": [[],["abc"],[]], "error_type": self.error_type}
        :return:
        """
        return {
            "ref": self.reference,
            "out": self.output,
            "error_type": [i.get_display_name() for i in self.error_type]
        }

