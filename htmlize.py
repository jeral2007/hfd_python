def print_float_table(table):
    html = ["<table>"]
    for row in table:
        html += ["<tr>"]
        for col in row:
            html += ["<td>{}</td>".format(col)]
        html += ["</tr>"]
    html += ["</table>"]
    return Html("".join(html))


class Html:
    def __init__(self, html):
        self.html = html

    def _repr_html_(self):
        return self.html
