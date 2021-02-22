"""
copied from xdl repo
接口不好，这个文件后续需要配合 xdl-trace 进行重构....
"""

import numpy as np
import sys
import os
from xdl.python.proto import trace_pb2
import struct
import base64
from bmlx.utils import io_utils

SHARE_SLOTS = "shared_slots"
ITEM_SLOTS = "item_slots"


def trace2nptype(tp):
    if tp == trace_pb2.Int8:
        return np.int8
    elif tp == trace_pb2.Int16:
        return np.int16
    elif tp == trace_pb2.Int32:
        return np.int32
    elif tp == trace_pb2.Int64:
        return np.int64
    elif tp == trace_pb2.Float:
        return np.float32
    elif tp == trace_pb2.Double:
        return np.float64
    elif tp == trace_pb2.Bool:
        return np.bool
    elif tp == trace_pb2.Byte:
        return np.byte
    else:
        raise RuntimeError("unknown trace data type: {}".format(tp))


def getDct(infostr):
    dct = {}
    for iter_str in infostr.split("#"):
        if len(iter_str) == 0:
            continue
        fd_pos = iter_str.find(":")
        if fd_pos == -1:
            continue
        key = iter_str[:fd_pos]
        val = iter_str[fd_pos + 1 :]
        dct[key] = val
    return dct


def parse_column(key, col):
    val = np.frombuffer(col.data, dtype=trace2nptype(col.dtype)).reshape(
        col.shape
    )[0]
    if key == "sampleid":
        val = getDct("".join(chr(v) for v in val))
    else:
        val = list(val)
    return val


def parse_trace(trace_content, shared_slots, item_slots):
    content_len = len(trace_content)
    sz = struct.unpack("<I", trace_content[:4])[0]
    buf = trace_content[4 : 4 + sz]
    hdrs = trace_pb2.Header()
    hdrs.ParseFromString(buf)
    print("|".join(hdrs.key))

    print("shared slots: ", shared_slots)
    print("item slots: ", item_slots)

    readed = 4 + sz
    records = {}
    while readed < content_len:
        buf = trace_content[readed : readed + 4]
        if not buf:
            break
        readed += 4
        sz = struct.unpack("<I", buf)[0]
        buf = trace_content[readed : readed + sz]
        record = trace_pb2.Record()
        record.ParseFromString(buf)
        readed += sz
        item_records = {ITEM_SLOTS: {}}
        shared_records = {}
        dispatch_id = None
        vid = None
        for key, col in dict(zip(hdrs.key, record.column)).items():
            key = str(key)
            val = parse_column(key, col)
            if key == "sampleid":
                dispatch_id = str(val["dispatch_id"])
                vid = str(val["vid"])
            elif key == "y_pred":
                item_records["y_pred"] = val
            elif "#" in key:
                slot_list = key.split("#")
                slot_str = slot_list[0]
                slot = int(slot_str)

                if slot in shared_slots:
                    if slot_str not in shared_records:
                        shared_records[slot_str] = []
                    shared_records[slot_str].append(
                        {"emb_slot": slot_list[1], "pooling_weights": val}
                    )
                elif slot in item_slots:
                    if slot_str not in item_records[ITEM_SLOTS]:
                        item_records[ITEM_SLOTS][slot_str] = []

                    item_records[ITEM_SLOTS][slot_str].append(
                        {"emb_slot": slot_list[1], "pooling_weights": val}
                    )

        if dispatch_id not in records:
            records[dispatch_id] = {}
        if SHARE_SLOTS not in records[dispatch_id]:
            records[dispatch_id][SHARE_SLOTS] = shared_records
        records[dispatch_id][vid] = item_records
    return records


def parse_model_sample(sample_str):
    from xdl.python.proto.mlplat.feature.sample_pb2 import Sample
    import zlib

    buf = zlib.decompress(sample_str, zlib.MAX_WBITS | 16)
    buf_size = len(buf)

    readed = 0
    model_samples = []
    shared_slots = []
    item_slots = []
    while readed < buf_size:
        len_str = buf[readed : readed + 8]
        if not len_str:
            break
        record = Sample()
        lens = struct.unpack("<Q", len_str)[0]
        readed += 12
        record.ParseFromString(buf[readed : readed + lens])
        readed = readed + lens + 4
        user_info = record.user_debug_str
        user_info_dct = getDct(user_info)
        dispatch_id = str(user_info_dct["disp_id"])

        for sparse_fea in record.model_sample.shared_feature.sparse:
            shared_slots.append(sparse_fea.slot)
        for i in range(len(record.model_sample.item_feature)):
            for sparse_fea in record.model_sample.item_feature[i].sparse:
                item_slots.append(sparse_fea.slot)

        model_samples.append((dispatch_id, record.model_sample))

    return model_samples, list(set(shared_slots)), list(set(item_slots))


def gen_model_sample_and_scores(ori_model_samples, trace_records):
    from xdl.python.proto.mlplat.feature.score_pb2 import SampleScore
    model_samples_list = []
    scores_list = []

    for (dispatch_id, sample) in ori_model_samples:
        if dispatch_id not in trace_records:
            print("dispatch_id %s not found in trace info." % dispatch_id)
            continue
        trace_record = trace_records[dispatch_id]

        # shared feature
        single_shared = trace_record[SHARE_SLOTS]
        trace_shared_slots = single_shared.keys()
        shared_slots = []
        for sparse in sample.shared_feature.sparse:
            slot = str(sparse.slot)

            if slot not in single_shared:
                continue
            shared_slots.append(slot)

            single_slot = single_shared[slot]
            for info in single_slot:
                emb = sparse.embedding.add()
                emb.emb_slot = int(info["emb_slot"])
                for weight in info["pooling_weights"]:
                    emb.pooling_weight.append(weight)

        if len(shared_slots) < len(trace_shared_slots):
            print(
                "dispatch_id ",
                dispatch_id,
                " shared slots: ",
                list(set(trace_shared_slots).difference(set(shared_slots))),
                "not found in model sample.",
            )

        # iterator feature and score
        sample_score = SampleScore()
        for item in sample.item_feature:
            vid = str(item.item_id)
            if vid not in trace_record:
                print(
                    "vid %s not found in trace info, dispatch id %s."
                    % (vid, dispatch_id)
                )
                continue

            item_score = trace_record[vid]["y_pred"]
            score = sample_score.score.add()
            score.item_id = item.item_id
            for s in item_score:
                score.value.append(s)

            single_record = trace_record[vid][ITEM_SLOTS]
            trace_iterator_slots = single_record.keys()
            iterator_slots = []
            for sparse in item.sparse:
                slot = str(sparse.slot)
                if slot not in single_record:
                    continue
                iterator_slots.append(slot)
                single_slot = single_record[slot]
                for info in single_slot:
                    emb = sparse.embedding.add()
                    emb.emb_slot = int(info["emb_slot"])
                    for weight in info["pooling_weights"]:
                        emb.pooling_weight.append(weight)
            if len(iterator_slots) < len(trace_iterator_slots):
                print(
                    "dispatch_id ",
                    dispatch_id,
                    " vid: ",
                    vid,
                    " slots: ",
                    list(
                        set(trace_iterator_slots).difference(
                            set(iterator_slots)
                        )
                    ),
                    "not found in model sample.",
                )

        model_samples_list.append(
            base64.b64encode(sample.SerializeToString()).decode()
        )
        scores_list.append(
            base64.b64encode(sample_score.SerializeToString()).decode()
        )

    return "\n".join(model_samples_list), "\n".join(scores_list)


def convert_model_sample_and_scores(trace_content, sample_str):
    ori_model_samples, shared_slots, item_slots = parse_model_sample(sample_str)
    trace_records = parse_trace(trace_content, shared_slots, item_slots)
    return gen_model_sample_and_scores(ori_model_samples, trace_records)


PREDICT_TRACE_FILE = "predict.trace"


def convert_validate_samples(input_dict, output_dir):
    assert len(input_dict["validate_samples"]) == 1
    assert len(input_dict["validate_origin_samples"]) == 1
    assert len(input_dict["validate_predict_result"]) == 1

    validate_samples_path = input_dict["validate_samples"][0].meta.uri
    validate_origin_samples_path = input_dict["validate_origin_samples"][
        0
    ].meta.uri
    validate_predict_result_path = os.path.join(
        input_dict["validate_predict_result"][0].meta.uri,
        PREDICT_TRACE_FILE + ".0.1",
    )  # 注意这个的 trace 文件的名称, 在 xdl-predict 里面指定了 trace file name

    if not io_utils.exists(validate_samples_path):
        raise RuntimeError(
            "Invalid validate sample path: %s" % validate_samples_path
        )

    if not io_utils.exists(validate_origin_samples_path):
        raise RuntimeError(
            "Invalid origin validate sample path: %s"
            % validate_origin_samples_path
        )

    if not io_utils.exists(validate_predict_result_path):
        raise RuntimeError(
            "Invalid predict result path: %s" % validate_predict_result_path
        )
    # 将 sample(model sample) 和 predict trace 匹配，得到 sample 和 score的内容
    (model_samples_str, sample_scores_str,) = convert_model_sample_and_scores(
        io_utils.read_file_string(validate_predict_result_path),
        io_utils.read_file_string(validate_samples_path),
    )
    io_utils.write_string_file(
        os.path.join(output_dir, "original_samples"),
        io_utils.read_file_string(validate_origin_samples_path),
    )
    io_utils.write_string_file(
        os.path.join(output_dir, "model_samples"), model_samples_str.encode(),
    )
    io_utils.write_string_file(
        os.path.join(output_dir, "sample_scores"), sample_scores_str.encode(),
    )
