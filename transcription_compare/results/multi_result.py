from transcription_compare.utils.html_color import create_bg_color
from transcription_compare.results.aligned_token_classifier import ErrorType
from transcription_compare.tokens import Token


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
        self.alignment_results = []

        for (identifier, result) in output_results.items():
            self.identifiers.append(identifier)
            self.distance.append(result.distance)
            self.error_rate.append(result.error_rate)
            self.is_final.append(result.is_final)
            self.substitution.append(result.substitution)
            self.insertion.append(result.insertion)
            self.deletion.append(result.deletion)
            self.alignment_results.append(result.alignment_result)

        self.multi_alignment_result = MultiAlignmentResult(self.alignment_results, self.calculator_local)
        self.total_rows = len(self.alignment_results[0])

    def result(self):
        return 'distance', self.distance, 'error_rate', self.error_rate, 'substitution', self.substitution,\
               'insertion', self.insertion, 'deletion', self.deletion, 'identifiers', self.identifiers

    def result_2(self):
        print(' self.multi_alignment_result', self.multi_alignment_result)
        for i in self.multi_alignment_result:
            print(i.__str__())
        return self.multi_alignment_result

    def __str__(self):
        return self.multi_alignment_result.__str__()



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
        [{"error_type": ["number", "double" ....]}]
        [{"ref": "abc", "out": [[],["abc"],[]], "error_type": self.error_type,
        "local_cer": self.local_cer, "distance": self.substitution, "ins": self.insertion,
        "del": self.deletion}]
        :return:
        {'distance': [2, 6], 'error_rate': [0.04081632653061224, 0.12244897959183673],
        'is_final': [True, True], 'substitution': [1, 2], 'insertion': [1, 3], 'deletion': [0, 1],
        'identifiers': ['scribble-2019-06-13-50.txt', '05152019-bi-51.txt'],
        'error_type_info': [{"error_type": "number" , "sum":['1', '1'], "percentage":['..', '..'],
         {"error_type": "double" , "sum":['2', '6'], "percentage":['..', '..'],
         {"error_type": "split" , "sum":['17', '12'] "percentage":['..', '..'],...}]

        'multi_alignment_result': [{"ref": "abc", "out": [[],["abc"],[]], "error_type": self.error_type,
        "local_cer": self.local_cer, "distance": self.substitution, "ins": self.insertion,
        "del": self.deletion]}
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
            'error_type_info': self.multi_alignment_result.to_json_error_type(self.total_rows),
            "multi_alignment_result": self.multi_alignment_result.to_json_alignment_result()
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

    def __str__(self):
        return self.to_pretty_str()

    def to_pretty_str(self):
        s = ""
        for aligned_token in self.multi_alignment_tokens:
            tokens = [str(aligned_token.reference)] + [str(aligned_token.output)]
            # print('to', tokens)
            s += ("\t".join(tokens) + "\n")
        return s
    # def __str__(self):
    #     return self.multi_alignment_tokens
    #     # r = ''
    #     # for i in self.multi_alignment_tokens:
    #     #     r += i[0]+ ' ' + i[1] + '\n'
    #     #     return r
    def __iter__(self):
        """
        for word in ..:
            pass
        :return:
        """
        return self.multi_alignment_tokens.__iter__()
    def __getitem__(self, item):
        """
        self[1:3]
        :param item:
        :return:
        """
        return self.multi_alignment_tokens[item]

    def all_error_type(self):
        """
        all_count_error_type is a list contain more than or equal to one dictionary.
        The dictionary is that all error types and their statistics.

        :return:[{'number': '1', 'double': '2', ...},{'number': '1', 'double': '6', ...}]
        """
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
        return all_count_error_type

        # print(all_count_error_type)
    def to_html_error_type(self, total_rows):
        all_count_error_type = self.all_error_type()
        body = ''
        for key in ErrorType:
            if key == ErrorType.NA:
                continue
            body += """<tr><td>{}</td>""".format(key.get_display_name())
            for j in range(len(all_count_error_type)):
                # print('all_count_error_type[j][key]', all_count_error_type[j][key])
                body += '\n<td>' + str(all_count_error_type[j][key]) + '</td>'
                body += '\n<td>' + str(round(100*all_count_error_type[j][key]/total_rows, 7)) + '</td>' #  /all rows
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

    def to_json_error_type(self, total_rows):
        """
        all_count_error_type is a list contain more than or equal to one dictionary.
        the output of all_count_error_type is
        [{'number': '1', 'double': '2', ...},{'number': '1', 'double': '6', ...}]


        'error_type_info': [{"error_type": "number" , "sum":['1', '1'], "percentage":['..', '..'],
         {"error_type": "double" , "sum":['2', '6'], "percentage":['..', '..'],
         {"error_type": "split" , "sum":['17', '12'] "percentage":['..', '..'],...}]
        """
        error_type = []

        all_count_error_type = self.all_error_type()
        # print('all_count_error_type', all_count_error_type)
        # print(len(all_count_error_type))

        for key in ErrorType:
            if key == ErrorType.NA:
                continue
            error_dict = {"error_type": "", "sum": [], "percentage": []}
            error_dict["error_type"] = key.get_display_name()
            # print('key', key.get_display_name())
            for j in range(len(all_count_error_type)):

                # print('j', j)
                # print('all_count_error_type[j][key]', all_count_error_type[j][key])
                # error_dict["sum"] += str(all_count_error_type[j][key])
                # error_dict["percentage"] += str(round(all_count_error_type[j][key]/total_rows, 7))
                error_dict["sum"].append(all_count_error_type[j][key])
                # print('error_dict["sum"]', error_dict["sum"])
                error_dict["percentage"].append(round(100*all_count_error_type[j][key] / total_rows, 7))

            error_type.append(error_dict)
        # print('error_type', error_type)
        return error_type

    def to_json_alignment_result(self):
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
        self.pre = []
        self.post = []
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

            if not isinstance(self.reference, Token):
                self.pre.append(None)
                self.post.append(None)
            else:
                self.pre.append(self.reference.prefix)
                self.post.append(self.reference.postfix)


        is_zero = True
        for i in self.distance:
            if i != 0:
                is_zero = False
                break
        if is_zero:
            self.output = [self.output[0]]
            self.distance = [self.distance[0]]
            self.substitution = [self.substitution[0]]
            self.insertion = [self.insertion[0]]
            self.deletion = [self.deletion[0]]
            self.local_cer = [self.local_cer[0]]
            self.error_type = [self.error_type[0]]

            if not isinstance(self.reference, Token):
                self.pre.append(None)
                self.post.append(None)
            else:
                self.pre = [self.reference.prefix]
                self.post = [self.reference.postfix]

    def __str__(self):
        return self.aligned_token_list
        # for i in self.aligned_token_list:
        #     print('aaaaaaaaaaaaaaa')
        #     print(i)
        # return i



    @ staticmethod
    def has_pre_post(pre, post):
        has_pre = False
        has_post = False
        for i in pre:
            if i is not None:
                has_pre = True
        for i in post:
            if i is not None:
                has_post = True
        # print('has_pre, has_post', has_pre, has_post)
        return has_pre, has_post

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

        has_pre, has_post = self.has_pre_post(self.pre, self.post)
        if has_pre:
            # print('has pre')
            ref = " ".join(self.pre[0]) + " " + self.reference
        else:
            ref = self.reference
        if has_post:
            # print('has post')
            ref += " " + " ".join(self.post[0])

        if (c % 2) == 0:

            message = '\n<tr bgcolor=#dddddd >\n<td rowspan="{}"  width="10%">'.format(len(self.output)) \
                      + str(c) + '</td>'
            message += '\n<td rowspan="{}">'.format(len(self.output)) + ref + '</td>'
        else:
            message = '\n<tr>\n<td rowspan="{}">'.format(len(self.output)) + str(c) + '</td>'
            message += '\n<td rowspan="{}">'.format(len(self.output)) + ref + '</td>'
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
        {"ref": "abc", "out": [[],["abc"],[]], "error_type": self.error_type,
        "local_cer": self.local_cer, "distance": self.substitution, "ins": self.insertion,
        "del": self.deletion,"sub" : self.substitution}
        :return:
        """
        out = {
            "ref": self.reference,

        }

        has_pre, has_post = self.has_pre_post(self.pre, self.post)
        if has_pre:
            out_pre = {"pre": [i for i in self.pre]}
            out.update(out_pre)

        if has_post:
            out_post = {"post": [i for i in self.post]}
            out.update(out_post)

        out_3 = {"out": self.output,
                    "error_type": [i.get_display_name() for i in self.error_type],
                    "local_cer": [i for i in self.local_cer],
                    "distance": [i for i in self.distance],
                    "ins": [i for i in self.insertion],
                    "del": [i for i in self.deletion],
                    "sub": [i for i in self.substitution]}
        out.update(out_3)
        return out



