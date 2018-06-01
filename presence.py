import asyncio
import json
import os
import struct
import sys
import time

class InvalidID(Exception):
    def __init__(self):
        super().__init__('Client ID is Invalid')


class InvalidPipe(Exception):
    def __init__(self):
        super().__init__('Pipe Not Found - Is Discord Running?')


class ServerError(Exception):
    def __init__(self, message):
        super().__init__(message.replace(']','').replace('[','').capitalize())


class DiscordError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__('Error Code: {0} Message: {1}'.format(code, message))


class ArgumentError(Exception):
    def __init__(self):
        super().__init__('Event function must have one argument.')


class EventNotFound(Exception):
    def __init__(self, event):
        super().__init__('No event with name {0} exists.'.format(event))

def remove_none(d: dict): # Made by https://github.com/LewdNeko ;^)
    for item in d.copy():
        if isinstance(d[item], dict):
            if len(d[item]):
                d[item] = remove_none(d[item])
            else:
                del d[item]
        elif d[item] is None:
            del d[item]
    return d


try: # Thanks, Rapptz :^)
    create_task = asyncio.ensure_future
except AttributeError:
    create_task = asyncio.async


class Presence:
    def __init__(self, client_id, pipe=0):
        client_id = str(client_id)
        if sys.platform == 'linux' or sys.platform == 'darwin':
            self.ipc_path = (
                os.environ.get(
                    'XDG_RUNTIME_DIR',
                    None) or os.environ.get(
                    'TMPDIR',
                    None) or os.environ.get(
                    'TMP',
                    None) or os.environ.get(
                    'TEMP',
                    None) or '/tmp') + '/discord-ipc-'+str(pipe)
            self.loop = asyncio.get_event_loop()
        elif sys.platform == 'win32':
            self.ipc_path = r'\\?\pipe\discord-ipc-'+str(pipe)
            self.loop = asyncio.ProactorEventLoop()
        self.sock_reader: asyncio.StreamReader = None
        self.sock_writer: asyncio.StreamWriter = None
        self.client_id = client_id

    @asyncio.coroutine
    def read_output(self):
        try:
            data = yield from self.sock_reader.read(1024)
        except BrokenPipeError:
            raise InvalidID
        code, length = struct.unpack('<ii', data[:8])
        payload = json.loads(data[8:].decode('utf-8'))
        if payload["evt"] == "ERROR":
            raise ServerError(payload["data"]["message"])
        return payload

    def send_data(self, op: int, payload: dict):
        payload = json.dumps(payload)
        self.sock_writer.write(
            struct.pack(
                '<ii',
                op,
                len(payload)) +
            payload.encode('utf-8'))

    @asyncio.coroutine
    def handshake(self):
        if sys.platform == 'linux' or sys.platform == 'darwin':
            self.sock_reader, self.sock_writer = yield from asyncio.open_unix_connection(self.ipc_path, loop=self.loop)
        elif sys.platform == 'win32' or sys.platform == 'win64':
            self.sock_reader = asyncio.StreamReader(loop=self.loop)
            reader_protocol = asyncio.StreamReaderProtocol(
                self.sock_reader, loop=self.loop)
            try:
                self.sock_writer, _ = yield from self.loop.create_pipe_connection(lambda: reader_protocol, self.ipc_path)
            except FileNotFoundError:
                raise InvalidPipe
        self.send_data(0, {'v': 1, 'client_id': self.client_id})
        data = yield from self.sock_reader.read(1024)
        code, length = struct.unpack('<ii', data[:8])

    def update(self,pid=os.getpid(),state=None,details=None,start=None,end=None,large_image=None,large_text=None,small_image=None,small_text=None,party_id=None,party_size=None,join=None,spectate=None,match=None,instance=True):
        current_time = time.time()
        payload = {
            "cmd": "SET_ACTIVITY",
            "args": {
                "pid": pid,
                "activity": {
                    "state": state,
                    "details": details,
                    "timestamps": {
                        "start": start,
                        "end": end
                    },
                    "assets": {
                        "large_image": large_image,
                        "large_text": large_text,
                        "small_image": small_image,
                        "small_text": small_text
                    },
                    "party": {
                        "id": party_id,
                        "size": party_size
                    },
                    "secrets": {
                        "join": join,
                        "spectate": spectate,
                        "match": match
                    },
                    "instance": instance,
                },
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        payload = remove_none(payload)

        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())

    def clear(self,pid=os.getpid()):
        current_time = time.time()
        payload = {
            "cmd": "SET_ACTIVITY",
            "args": {
                "pid": pid,
                "activity": None
            },
            "nonce": '{:.20f}'.format(current_time)
        }
        self.send_data(1, payload)
        return self.loop.run_until_complete(self.read_output())
    
    def connect(self):
        self.loop.run_until_complete(self.handshake())

    def close(self):
        self.send_data(2, {'v': 1, 'client_id': self.client_id})
        self.sock_writer.close()
        self.loop.close()