import json
from quality.clarity import calculate_clarity
from quality.complexity import analyze_complexity
from quality.engagement import analyze_engagement
from quality.pacing import analyze_pacing


def get_analysis(file_path, pacing_word_count):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    analysis_results = {
        "clr": calculate_clarity(content),
        "com": analyze_complexity(content),
        "eng": analyze_engagement(content),
        "pac": analyze_pacing(content, pacing_word_count),
    }

    result_file_path = "analysis_results.json"
    with open(result_file_path, "w", encoding="utf-8") as result_file:
        json.dump(analysis_results, result_file, indent=4, ensure_ascii=False)

    return analysis_results


results = get_analysis("sci_2.txt", 1314)
print(results)
