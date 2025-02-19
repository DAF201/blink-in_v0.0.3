from PIL import Image
from numpy import array
from libs.static_files_loader import load_config_file
from libs.file_tools import data_dimension_rounding

EMBEDDING_IMAGE = Image.open(load_config_file()["embedding_image"]).convert("RGBA")


def data_encoding(data: bytes) -> Image:
    size = data_dimension_rounding(len(data))
    img_buffer = array(EMBEDDING_IMAGE.resize((size, size)))
    data = len(data).to_bytes(4, byteorder="little") + data
    index = 0
    for y in range(size):
        for x in range(size):
            if index >= len(data):
                break
            img_buffer[y, x, 3] = data[index]
            index += 1
    img_buffer = Image.fromarray(img_buffer)
    return img_buffer


def data_decoding(img_buffer: Image) -> bytes:
    img_buffer = array(img_buffer)
    alpha_channel = img_buffer[..., 3].flatten().tolist()
    size = int.from_bytes(alpha_channel[:4], byteorder="little")
    alpha_channel = (alpha_channel[4 : 4 + size])
    return bytes(alpha_channel)
