def read_in_chunks(_file, chunk_size):

    while True:
        chunk_data = _file.read(chunk_size)

        # if not chunk_data:
        #     break
        yield chunk_data


def read_in_lines(_file):

    while True:
        line_data = _file.readline()

        # if not chunk_data:
        #     break
        yield line_data


if __name__ == "__main__":
    pass
