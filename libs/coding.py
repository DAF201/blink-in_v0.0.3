class Data:
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
        result = []
        padded_data = bytearray(data)  # Convert input data to mutable bytearray
        padding_count = (3 - (len(padded_data) % 3)) % 3  # Calculate padding needed

        # Store the padding count in the first character
        result.append(Data.byte2char(padding_count))

        # Add padding bytes (0s) if needed
        for _ in range(padding_count):
            padded_data.append(0)

        for i in range(0, len(padded_data), 3):
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

        return "".join(result)  # Return encoded string

    @staticmethod
    def decode(data):
        decoded_data = bytearray()

        # Read padding count from the first character
        padding_count = Data.char2byte(data[0])
        data = data[1:]  # Remove padding byte from encoded data

        for i in range(0, len(data), 4):
            b0 = Data.char2byte(data[i])
            b1 = Data.char2byte(data[i + 1])
            b2 = Data.char2byte(data[i + 2])
            b3 = Data.char2byte(data[i + 3])

            decoded_data.append((b0 << 2) | ((b1 & 0b00110000) >> 4))
            decoded_data.append(((b1 & 0b00001111) << 4) | ((b2 & 0b00111100) >> 2))
            decoded_data.append(((b2 & 0b00000011) << 6) | b3)

        return decoded_data[:-padding_count] if padding_count > 0 else decoded_data
