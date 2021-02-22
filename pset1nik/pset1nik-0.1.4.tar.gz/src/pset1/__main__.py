from .hash_str import get_user_id
import pyarrow.parquet as pq
from .io import atomic_write
from .canvas import get_course_id, get_quiz_id, get_assignment_id, quiz_submission, get_excel_user_ids


def main(user_id_func=True, atomic_write_func=True, parquet_func=True, canvas_func=True):
    """
    :param user_id_func: If user id function needs to execute
    :param atomic_write_func: If atomic write function needs to execute
    :param parquet_func: If parquet function needs to execute
    :param canvas_func: If canvas function needs to execute
    :return: hashed user id, parquet file output and canvas submission
    """
    if user_id_func:
        for user in ["gorlins", "nikhar1210"]:
            print("Id for {}: {}".format(user, get_user_id(user)))

    if atomic_write_func:
        data_source_df = get_excel_user_ids()
        with atomic_write(filepath='data/hashed.parquet', mode='w', as_file=False) as f:
            data_source_df.to_parquet(f)

    if parquet_func:
        data_source_pq = pq.ParquetDataset('data/hashed.parquet').read_pandas().to_pandas()
        print(data_source_pq.index)

    if canvas_func:
        with quiz_submission(course_id=get_course_id(), quiz_id=get_quiz_id(), assignment_id=get_assignment_id()) as q:
            print(q)


    # TODO: read in, save as new parquet file, read back just id column, print


if __name__ == "__main__":

    main()
