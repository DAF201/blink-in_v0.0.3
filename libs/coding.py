# convert from C++ to python with GPT since ctypes does not like my c++ dll
class Data:
    # Character encoding and decoding maps
    byte2char_map = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+-"

    @staticmethod
    def byte2char(c):
        return Data.byte2char_map[c]

    @staticmethod
    def char2byte(c):
        if c == "+":
            return 62
        if c == "-":
            return 63
        if "0" <= c <= "9":
            return ord(c) - ord("0")
        if "A" <= c <= "Z":
            return ord(c) - ord("A") + 10
        if "a" <= c <= "z":
            return ord(c) - ord("a") + 36
        return -1  # Invalid character

    @staticmethod
    def encode(data):
        # Convert input bytes to a string of encoded characters
        result = []
        padded_data = bytearray(data)  # Use bytearray for input data

        # Handle padding to make the length a multiple of 3 (needed for base64-like encoding)
        while len(padded_data) % 3 != 0:
            padded_data.append(0)  # Add padding byte (0) if necessary

        for i in range(0, len(padded_data), 3):
            # Break 3 bytes into 4 characters
            result.append(Data.byte2char((padded_data[i] & 0b11111100) >> 2))
            result.append(
                Data.byte2char(
                    ((padded_data[i] & 0b00000011) << 4)
                    | ((padded_data[i + 1] & 0b11110000) >> 4)
                )
            )
            result.append(
                Data.byte2char(
                    ((padded_data[i + 1] & 0b00001111) << 2)
                    | ((padded_data[i + 2] & 0b11000000) >> 6)
                )
            )
            result.append(Data.byte2char(padded_data[i + 2] & 0b00111111))

        return "".join(result)

    @staticmethod
    def decode(data):
        # Decode string of encoded characters into bytes
        decoded_data = bytearray()

        for i in range(0, len(data), 4):
            # Each group of 4 characters corresponds to 3 bytes
            b0 = Data.char2byte(data[i])
            b1 = Data.char2byte(data[i + 1])
            b2 = Data.char2byte(data[i + 2])
            b3 = Data.char2byte(data[i + 3])

            # Rebuild the original 3 bytes from 4 encoded characters
            decoded_data.append((b0 << 2) | ((b1 & 0b00110000) >> 4))
            decoded_data.append(((b1 & 0b00001111) << 4) | ((b2 & 0b00111100) >> 2))
            decoded_data.append(((b2 & 0b00000011) << 6) | b3)

        return decoded_data
