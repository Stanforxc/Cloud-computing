def read_in_chunks(_file, chunk_size):

    while True:
        chunk_data = _file.read(chunk_size)

        # if not chunk_data:
        #     break
        yield chunk_data





if __name__ == "__main__":
    pass
