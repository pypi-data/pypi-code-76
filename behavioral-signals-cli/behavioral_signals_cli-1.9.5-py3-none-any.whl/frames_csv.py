"""
Script that converts the frame json results of the Behavioral Signals API to a csv.

Copyright Behavioral Signals Technologies
"""
import json
import argparse
import csv

parse_config = {
    "speakers": ["0", "1"],
    "behaviors": ["emotion", "strength", "positivity", "speaking_rate", "engagement", "politeness"]
}


def process_speaker(speaker_dict, behaviors=["emotion"]):
    """Parse a speaker dictionary inside a frame and return only a set of
        behaviors. By default if the speaker dictionary is not None then the
        particular time interval is labeled as speech. Note that for now, only
        the behaviors being dicitonaries with the format of
        {uptonow":, "framelevel":} are considered valid.
    Args:
        speaker_dict (dict): A dictionary of speaker entries from the
            frame["speakers"] entry.
        behaviors (list): A list of behaviors included in the output

    Returns:
        (list): A list of labels for each behavior starting with "speech".

    Example:
        speaker_dict = {
            "emotion": {
                "uptonow": null,
                "framelevel": 4.0
            },
            "success": null,
            language": {
                "uptonow": 1.0,
                "framelevel": 1.0
            },
        }
        behaviors = ["emotion"]
        will return ["speech", 4.0]
    """
    return ["speech"] + [speaker_dict[behavior]["framelevel"]
                         for behavior in behaviors], str(speaker_dict["id"])


def process_frames(frames):
    """Process a series of frames and returns them in a list of lists.

    Args:
        frames (list): A list of frames from "frames" entry.
        parse_config (dict): A dictionary containing the identifications of
            each speaker and the behaviors that are to be included in the csv.

    Returns:
        (list): A list of lists. The first sublist is a header containing the
        names of the behaviors used and each subsequent sublist corresponds to
        a particular time interval specified by the first two elements and
        contains the predictions over the specified behaviors for both speaker.
    """

    behaviors = parse_config["behaviors"]
    speakers = parse_config["speakers"]
    rows = []
    for frame in frames:
        start = frame["st"]
        end = frame["et"]

        speaker_row = {
            sp: ["silence"] + [None for _ in behaviors]
            for sp in speakers
        }

        speakers_dict = frame.get("speakers", None)
        if speakers_dict:
            for speaker_dict in speakers_dict:
                values, speaker_id = process_speaker(speaker_dict,
                                                     behaviors)
                speaker_row[speaker_id] = values

        row = [start, end]
        for sp in speakers:
            row += speaker_row[sp]
        rows.append(row)

    header = ["start", "end"]
    for speaker in speakers:
        for behavior in ["speech"] + behaviors:
            header.append(behavior + "_{}".format(speaker))
    return [header] + rows


def frames_to_csv(input_json):
    if isinstance(input_json, dict):
        frames = input_json["frames"]
    else:
        with open(input_json, "r") as fp:
            data = json.load(fp)
        frames = data["frames"]

    rows = process_frames(frames=frames)
    return rows


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", required=True,
                        help="Path to input frame json file")
    parser.add_argument("-o", "--output", required=True,
                        help="Path to output csv file")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    rows = frames_to_csv(input_json=args.input)

    with open(args.output, "w") as fp:
        csv_writer = csv.writer(fp, delimiter=",")
        for row in rows:
            csv_writer.writerow(row)
