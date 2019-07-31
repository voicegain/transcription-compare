from ..utils.html_color import create_bg_color


class MultiResult:
    def __init__(self, output_results: dict):
        """
        :param output_results: dict from identifier(str) to Result
        """
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

        self.multi_alignment_result = MultiAlignmentResult(alignment_results)

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
              </tr>
            <tbody>
               """
        for identifier in self.identifiers:
            body += """<tr><td>{}</td></tr>""".format(identifier)
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
    def __init__(self, alignment_results):
        """
        :param alignment_results: List[AlignmentResult]
        """
        if len(alignment_results) <= 1:
            raise ValueError("length of alignment_results should be >= 2")
        print('len(alignment_results)', len(alignment_results))
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
        print('alignment_tokens_list', alignment_tokens_list)
        for i in range(alignment_result_size):
            tmp_aligned_token_list = []
            for alignment_tokens in alignment_tokens_list:
                tmp_aligned_token_list.append(alignment_tokens[i])
            self.multi_alignment_tokens.append(MultiAlignedToken(tmp_aligned_token_list))

    def to_html(self):
        """
        include header and call to_html of all items in self.multi_alignment_tokens
        Return table2
            <table>
                  <tr>
            <th>Reference</th>
                    <th>output</th>
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
        body = """<table>\n<tr>\n<th>Reference</th>
                   <th>output</th>
                <th>distance</th>
                <th>substitution</th>
                <th>insertion</th>
                <th>deletion</th></tr><tbody>"""
        # create header
        for t in self.multi_alignment_tokens:
            body += t.to_html()
        # something else
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
    def __init__(self, aligned_token_list):
        self.aligned_token_list = aligned_token_list
        self.reference = None
        self.output = []
        self.distance = []
        self.substitution = []
        self.insertion = []
        self.deletion = []
        for aligned_token in self.aligned_token_list:
            distance, substitution, insertion, deletion = \
                aligned_token.calculate_three_kinds_of_distance()
            if self.reference is None:
                self.reference = aligned_token.reference
                self.output.append(aligned_token.outputs)
                self.distance.append(distance)
                self.substitution.append(substitution)
                self.insertion.append(insertion)
                self.deletion.append(deletion)
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
                    # print('!!!!self.output', self.output)
        print('lalalalal   self.output',self.output)

    def to_html(self):
        """
        one row
        Example output string:
          <tr>
            <td rowspan="3">ref</td>
            <td>output</td>
            <td>distance</td>
            <td>sub</td>
            <td>ins</td>
            <td>de</td>
          </tr>
          <tr>
            <td>output</td>
            <td>distance</td>
            <td>sub</td>
            <td>ins</td>
            <td>de</td>
          </tr>
          <tr>
            <td>output</td>
            <td>distance</td>
            <td>sub</td>
            <td>ins</td>
            <td>de</td>
          </tr>
        :return:
        """
        message = '\n<tr>\n<td rowspan="{}">'.format(len(self.output)) + self.reference + '</td>'
        for i in range(len(self.output)):
            if i != 0:
                message += '\n<tr>'
            message += '\n<td {}>'.format(
                create_bg_color(self.substitution[i], self.insertion[i], self.deletion[i])
            ) + " ".join(self.output[i]) + '</td>'

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

