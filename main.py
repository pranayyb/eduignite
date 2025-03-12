from quality.clarity import calculate_clarity
from quality.complexity import analyze_complexity
from quality.engagement import analyze_engagement
from quality.pacing import analyze_pacing

with open("sci_2.txt", "r", encoding="utf-8") as file:
    content = file.read()

clarity_result = calculate_clarity(content)
complexity_result = analyze_complexity(content)
engagement_result = analyze_engagement(content)
pacing_result = analyze_pacing(content, 1314)  

analysis_results = {
    "clr": clarity_result,
    "com": complexity_result,
    "eng": engagement_result,
    "pac": pacing_result,
}

import json

# print(json.dumps(analysis_results, indent=4))

with open("analysis_results.json", "w", encoding="utf-8") as result_file:
    json.dump(analysis_results, result_file, indent=4, ensure_ascii=False)
