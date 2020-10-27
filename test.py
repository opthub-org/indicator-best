import json
import sys

import docker


client = docker.from_env()
c = client.containers.run(
    image='best-fitness',
    command=['vv'],
    stdin_open=True,
    detach=True,
)
s = c.attach_socket(params={'stdin': 1, 'stream': 1, 'stdout': 1, 'stderr': 1})
x = input() + '\n'
print(x)
xs = input() + '\n'
print(xs)
s._sock.sendall((x + xs).encode('utf-8'))
c.wait()
stdout = c.logs(stdout=True, stderr=False).decode('utf-8')
c.remove()
print(stdout)
