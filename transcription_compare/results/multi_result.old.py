
class MultiResult:

    def __init__(self, output_results: dict):
        self.output_results = output_results

    def to_json(self):
        json_list = []
        count = 0
        output_identifier_list = []
        for (output_identifier, result) in self.output_results.items():
            current_alignment_result = result.alignment_result
            output_identifier_list.append(output_identifier)
            print(current_alignment_result)
            if count == 0:
                for aligned_token in current_alignment_result:
                    json_list.append(aligned_token.to_json())
                print('json_list', json_list)
                # print('count', count)
                new_list = json_list[0]['out']
                count += 1
            else:
                print('count2', count)
                i = 0  # number of reference
                len_name = len(output_identifier_list)
                # print('len_name', len_name)
                for aligned_token in current_alignment_result:
                    local_list = {}
                    current_output = aligned_token.to_json()
                    name_count = 0
                    print('current_output', current_output)
                    # print('json_list[i][', json_list[i]['ref'])
                    if current_output['ref'] == json_list[i]['ref']:
                        print('lalla')
                        print(json_list[i])
                        local_list[output_identifier_list[name_count]] = (json_list[i]['out'])
                        print('local_list', local_list)
                        local_list[output_identifier_list[len_name-i-1]] = (current_output['out'])
                        # local_list.append(current_output['out'])
                        json_list[i]['out'] = local_list
                        print('local_list', local_list)
                        print('json_list', json_list)
                        i += 1
                    else:
                        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print('json_list', json_list)
        return json_list

    def to_html(self):
        message = """<html>
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
              <tr>"""
        all_rows = []
        output_identifier_count = 0
        count = 0
        # print('self.output_results.items()',self.output_results.items())
        for (output_identifier, result) in self.output_results.items():
            message += """<th>Reference</th>
                                   <th>{}</th>
                                <th>distance</th>
                                <th>substitution</th>
                                <th>insertion</th>
                                <th>deletion</th>""".format(output_identifier)
            current_alignment_result = result.alignment_result
            print('current_alignment_result',current_alignment_result)
            print('all_rows2', all_rows)
            if count == 0:
                tmp_rows = []
                for aligned_token in current_alignment_result:
                    current_row = aligned_token.to_html_multi_list()
                    all_rows.append(current_row)
                    # print('current_row',current_row)
                count += 1

                # print('all_rows1', all_rows)
                len_of_list = len(all_rows)  # 多少行
            else:
                tmp_rows = []
                # print('all_rows2', all_rows)
                for index, aligned_token in enumerate(current_alignment_result):
                    # print('current_row2', current_row)
                    current_row = aligned_token.to_html_multi_list()
                    all_rows[index].extend(current_row)
        print('all_rows3', all_rows) # return will have same len of the al result

        all_substitution = 0
        all_insertion = 0
        all_deletion = 0
        all_distance = 0
        output_identifier_count += 1
        for current_list in all_rows:
            # print(current_list,current_list)
            # print(current_list[0])
            message += '\n<tr>\n<td>' + str(current_list[0]) + '</td>'
            x = 1
            while x < len(current_list)-1:
                message += '\n<td>' + str(current_list[x]) + '</td>'
                x += 1
            # print(current_list[0][len(current_list)])
            # print(current_list[0][-1])
            message += '\n<td>' + str(current_list[-1]) + '</td>\n</tr>'

            message += '\n</body>\n</html>'
            print(message)
        return message





