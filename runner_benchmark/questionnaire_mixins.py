import re


class QuestionnaireMixins:
    client = None
    csrf_token = None
    previous_url = None

    def get(self, url, allow_redirects=False):
        print('\nGET', url)

        response = self.client.get(allow_redirects=allow_redirects, url=url)

        if not response.content:
            raise Exception(f"No content in GET response for url: {url}")

        self.csrf_token = _extract_csrf_token(response.content.decode('utf8'))
        self.previous_url = url

        print('csrf_token', self.csrf_token)

        return response

    def post(self, url, data={}):

        data['csrf_token'] = self.csrf_token

        headers = {'Referer': self.base_url}

        print('POST Headers', headers)

        response = self.client.post(
            allow_redirects=False, headers=headers, data=data, url=url
        )
        return response


CSRF_REGEX = re.compile(
    r'<input id="csrf_token" name="csrf_token" type="hidden" value="(.+?)">'
)


def _extract_csrf_token(html):
    match = CSRF_REGEX.search(html)
    if match:
        return match.group(1)
