import webvtt
import json


def extract_sentences_from_vtt(vtt_file):
    sentences = []
    total_duration = 0.0

    for caption in webvtt.read(vtt_file):
        start_time = parse_time(caption.start)
        end_time = parse_time(caption.end)
        duration = end_time - start_time

        sentences.append({"sentence": caption.text.strip(), "duration": duration})
        total_duration += duration

    result = {"sentences": sentences, "total_duration": total_duration}

    # Save as JSON file
    with open("output.json", "w", encoding="utf-8") as json_file:
        json.dump(result, json_file, indent=4, ensure_ascii=False)

    return result


def parse_time(time_str):
    """Converts VTT timestamp (hh:mm:ss.sss) to seconds."""
    h, m, s = map(float, time_str.replace(",", ".").split(":"))
    return h * 3600 + m * 60 + s


# Example usage
vtt_file_path = "sci_2.vtt"  # Replace with your VTT file path
json_output = extract_sentences_from_vtt(vtt_file_path)

# print(json.dumps(json_output, indent=4, ensure_ascii=False))
