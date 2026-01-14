import json
import re

def extract_dict_content(message):
    json_pattern = re.compile(r'```json\n([\s\S]*?)\n```', re.DOTALL)
    match = json_pattern.search(message)

    if match:
        try:
            json_str = match.group(1).strip('```').strip()
            data = eval(json_str)
            return data
        except json.JSONDecodeError:
            # 如果 JSON 解析失败，返回 None
            return None

    # 检测纯字典格式
    dict_pattern = re.compile(r'\{[\s\S]*?}')
    match = dict_pattern.search(message)

    if match:
        try:
            # 去除首尾的换行符
            dict_str = match.group(0).strip()
            data = eval(dict_str)
            return data
        except Exception as e:
            # 如果解析失败，返回 None
            print(f"Failed to parse dictionary: {e}")
            return None

    # 如果两种格式都未匹配到，返回 None
    return None