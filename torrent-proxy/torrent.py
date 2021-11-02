from qbittorent import Client

class Torrent(object):

    def parse_file(self, torrent_file):

        with open(torrent_file, 'rb') as f:
            result = self.parse(f.read())

        return result

    def parse(self, bencode_bytes):

        result = []
        while bencode_bytes:

            if bencode_bytes[0] == 'i':
                v, bencode_bytes = self.parse_number(bencode_bytes)

            elif bencode_bytes[0] == 'l':
                v, bencode_bytes = self.parse_list(bencode_bytes)

            elif bencode_bytes[0] == 'd':
                v, bencode_bytes = self.parse_dict(bencode_bytes)

            elif bencode_bytes[0] == 'e':
                return result, bencode_bytes[1:]

            else:
                v, bencode_bytes = self.parse_string(bencode_bytes)

            result.append(v)

        return result

    @staticmethod
    def parse_number(bencode_bytes):
        index = bencode_bytes.find('e')
        value = int(bencode_bytes[1:index])

        return value, bencode_bytes[index + 1:]

    @staticmethod
    def parse_string(bencode_bytes):
        index = bencode_bytes.find(':')
        last_index = index + int(bencode_bytes[:index]) + 1
        value = bencode_bytes[index + 1:last_index]

        return value, bencode_bytes[last_index:]

    def parse_list(self, bencode_bytes):
        return self.parse(bencode_bytes[1:])

    def parse_dict(self, bencode_bytes):
        list_value, bencode_bytes = self.parse(bencode_bytes[1:])
        value = {}
        for i in range(0, len(list_value), 2):
            value[list_value[i]] = list_value[i + 1]

        return value, bencode_bytes


if __name__ == '__main__':
    pass
