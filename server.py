import json
import os

from twisted.internet import endpoints, reactor
from twisted.web import resource, server


def file_does_not_exist(file_name):
    return not os.path.isfile(file_name)


class LogStreamer(resource.Resource):
    isLeaf = True

    file_name = 'test.jsonl'
    offset_diff = 10

    def calculate_next_offset(self, current_offset, total_size):
        next_offset = current_offset + self.offset_diff
        if next_offset < total_size:
            return next_offset
        else:
            return total_size

    def render_POST(self, request):
        request.setHeader('content-type', 'application/json')

        if file_does_not_exist(self.file_name):
            return json.dumps(
                {
                    'ok': False,
                    'reason': 'could not open the file {}'.format(
                        self.file_name
                    )
                }
            )

        with open('test.jsonl') as f:
            file_data = f.readlines()
            total_size = len(file_data)

            request_data = json.loads(request.content.read())
            offset = request_data.get('offset')

            if offset not in xrange(total_size):
                return json.dumps(
                    {
                        'ok': False,
                        'reason': 'offset should be from 0 to {}'.format(
                            total_size)
                    }
                )
            next_offset = self.calculate_next_offset(offset, total_size)
            messages = []
            for i in xrange(offset, next_offset):
                line = file_data[i]
                messages.append(json.loads(line))

            result = {
                'ok': True,
                'next_offset': next_offset,
                'messages': messages,
                'total_size': total_size
            }
            return json.dumps(result)


root = resource.Resource()
root.putChild('read_log', LogStreamer())
site = server.Site(root)
endpoint = endpoints.TCP4ServerEndpoint(reactor, 8000)
endpoint.listen(site)
reactor.run()
