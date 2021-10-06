import cefpyco
import socket

if __name__ == '__main__':
    with cefpyco.create_handle() as cef:
        cef.register("ccnx:/hcu/network")
        while True:
            info = cef.receive()

            if info.name == "ccnx:/hcu/network/index.html" and info.chunk_num == 0:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect(("cc", 80))
                    request_message = "GET /index.html\r\n\r\n"
                    sock.send(request_message.encode('utf-8'))

                    sequence = 0
                    while True:
                        response = sock.recv(1024)
                        print(response.decode('utf-8'))
                        if len(response) == 0:
                            break
                        cef.send_data("ccnx:/hcu/network/index.html", response.decode('utf-8'), sequence,
                                      cache_time=10000)
                        sequence += 1
