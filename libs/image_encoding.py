from PIL import Image
from numpy import array
from libs.static_files_loader import load_config_file
from libs.file_tools import data_dimension_rounding

# path to the image to embed data to
EMBEDDING_IMAGE = Image.open(load_config_file()["embedding_image"]).convert("RGBA")


def data_encoding(data: bytes) -> Image:
    # find a good size for data
    size = data_dimension_rounding(len(data))
    # resize image, then conver to array for faster operation
    img_buffer = array(EMBEDDING_IMAGE.resize((size, size)))
    # mark the size of data
    data = len(data).to_bytes(4, byteorder="little") + data
    # write to each pixel's alpha channel
    # may be try to use the slice in the future
    index = 0
    for y in range(size):
        for x in range(size):
            if index >= len(data):
                break
            # write to alpha channel
            img_buffer[y, x, 3] = data[index]
            index += 1
    img_buffer = Image.fromarray(img_buffer)
    return img_buffer


def data_decoding(img_buffer: Image) -> bytes:
    img_buffer = array(img_buffer)
    # get alpha channel
    alpha_channel = img_buffer[..., 3].flatten().tolist()
    # get data size
    size = int.from_bytes(alpha_channel[:4], byteorder="little")
    # get data
    alpha_channel = alpha_channel[4 : 4 + size]
    return bytes(alpha_channel)
