'''HTML tokenizer for the assignment.'''

class Tokenizer(object):

    def __init__(self):
        self.tokens = []
        self.current_token = ''
        self.in_tag = False
        self.in_start_tag = False
        self.in_attribute = False
        self.in_attribute_value = False

    def get_tokens_from(self, html):
        self._parse(html)
        return self.tokens

    def _parse(self, html):
        for char in html:

            if not self.in_tag:

                if '<' == char:
                    if self.current_token:
                        # Queue up the current text.
                        for line in self.current_token.splitlines():
                            self.tokens.extend(line.split())
                        # Enter tag state.
                        self.in_tag = True
                        self.in_start_tag = True
                        self.current_token = char

                else:
                    # Just keep building up current text.
                    self.current_token += char

            elif self.in_tag:

                if self.in_start_tag:

                    if ' ' == char:
                        self.tokens.append(self.current_token)
                        self.current_token = ''
                        self.in_start_tag = False
                        self.in_attribute = True
                    else:
                        self.current_token += char

                elif self.in_attribute:

                    if '"' == char:
                        self.current_token += char

                        if self.in_attribute_value:
                            self.tokens.append(self.current_token)
                            self.current_token = ''

                        self.in_attribute_value = not self.in_attribute_value

                    elif '>' == char and not self.in_attribute_value:
                        if self.current_token:
                            self.tokens.append(self.current_token)
                            self.current_token = ''

                        self.tokens.append('>')
                        self.in_tag = False
                        self.in_attribute = False
                        self.in_attribute_value = False

                    else:
                        self.current_token += char

                else:
                    pass

        if self.current_token:
            self.tokens.append(self.current_token)
            self.current_token = ''





def test():
    tokenizer = Tokenizer()

    html = '''
    bar<select attribute="value">foo</select>
    '''

    tokens = ['bar', '<select', 'attribute="value"', '>', 'foo', '</select>']
    result = tokenizer.get_tokens_from(html.strip())
    print(result)
    assert tokens == result

if __name__ == '__main__':
    test()