import sys
import socket
from threading import Thread
import cefpyco


def hexdump(src, length=16):
    result = []

    for i in range(0, len(src), length):
        s = src[i:i + length]
        hexa = ' '.join(['{:02X}'.format(x) for x in s])
        text = ''.join([chr(x) if 32 <= x < 127 else '.' for x in s])
        result.append('{:04X}  {}{}  {}'.format(i, hexa, ((length - len(s)) * 3) * ' ', text))
    for s in result:
        print(s)


def received_from(connection):
    buffer = b''
    # connection.settimeout(2)

    try:
        recv_len = 1
        while recv_len:
            data = connection.recv(4096)
            buffer += data
            recv_len = len(data)
            if recv_len < 4096:
                break
    except:
        pass

    return buffer


def request_handler(buffer):
    return buffer


def response_handler(buffer):
    return buffer


def proxy_handler(cef, remote_host, remote_port):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    chunk_num = 0
    while True:
        remote_buffer = received_from(remote_socket)

        if len(remote_buffer):
            print('[<==] Received {} bytes from remote.'.format(len(remote_buffer)))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            cef.send_data("ccnx:/proxy/http/hcu/index.html", remote_buffer, chunk_num)
            chunk_num += 1

            print('[<==] Sent to client.')


# TODO interestのparser作成
def server_loop(remote_host, remote_port):
    with cefpyco.create_handle() as cef:
        cef.register("ccnx:/proxy")
        print('Prefix registration.')
        while True:
            info = cef.receive()
            print('Received Data {}'.format(info))
            if info.is_succeeded and info.is_interest \
                    and info.name == "ccnx:/proxy/http/hcu/index.html" and info.chunk_num == 0:
                proxy_thread = Thread(target=proxy_handler,
                                      args=[cef, remote_host, remote_port])
                proxy_thread.start()


def main():
    remote_host = '127.0.0.1'
    remote_port = 8000

    server_loop(remote_host, remote_port)


if __name__ == '__main__':
    main()
