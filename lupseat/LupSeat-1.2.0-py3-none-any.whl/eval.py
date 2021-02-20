def eval_chunk_size(rm):
    chunks = []
    chunk_size = 0
    for row in range(rm.max_row):
        for col in range(rm.max_col):
            if (rm.seats[row][col] == None or rm.seats[row][col].sid == -1) and chunk_size > 0:
                chunks.append(chunk_size)
                chunk_size = 0
            else:
                chunk_size += 1

        if chunk_size > 0:
            chunks.append(chunk_size)
            chunk_size = 0

    score = sum(chunks) / len(chunks)

    # Remove decimals past 2 sigfigs
    score *= 100
    score = round(score) / 100

    print(score)
