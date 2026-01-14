import json
import re
from data.mbti_initial_weight import WEIGHT

change_weight = 0.06
change_list = {
    'Ti' : 'Fi', 'Fi' : 'Ti',
    'Te' : 'Fe', 'Fe' : 'Te',
    'Ni' : 'Si', 'Si' : 'Ni',
    'Ne' : 'Se', 'Se' : 'Ne',
}

mbti_to_function = {
    "INTP" : {"main" : "Ti", "aux" : "Ne"}, "ISTP" : {"main" : "Ti", "aux" : "Se"}, "ENFP" : {"main" : "Ne", "aux" : "Fi"}, "ESFP" : {"main" : "Se", "aux" : "Fi"},
    "INTJ" : {"main" : "Ni", "aux" : "Te"}, "ISTJ" : {"main" : "Si", "aux" : "Te"}, "ENFJ" : {"main" : "Fe", "aux" : "Ni"}, "ESFJ" : {"main" : "Fe", "aux" : "Si"},
    "INFP" : {"main" : "Fi", "aux" : "Ne"}, "ISFP" : {"main" : "Fi", "aux" : "Se"}, "ENTP" : {"main" : "Ne", "aux" : "Ti"}, "ESTP" : {"main" : "Se", "aux" : "Ti"},
    "INFJ" : {"main" : "Ni", "aux" : "Fe"}, "ISFJ" : {"main" : "Si", "aux" : "Fe"}, "ENTJ" : {"main" : "Te", "aux" : "Ni"}, "ESTJ" : {"main" : "Te", "aux" : "Si"},
}

function_to_mbti = {
    "TiNe" : "INTP", "NiTe" : "INTJ", "FiNe" : "INFP", "NiFe" : "INFJ",
    "TiSe" : "ISTP", "SiTe" : "ISTJ", "FiSe" : "ISFP", "SiFe" : "ISFJ",
    "NeFi" : "ENFP", "FeNi" : "ENFJ", "NeTi" : "ENTP", "TeNi" : "ENTJ",
    "SeFi" : "ESFP", "FeSi" : "ESFJ", "SeTi" : "ESTP", "TeSi" : "ESTJ"
}

main_to_aux = {
    'Ti' : ['Ne', 'Se'], 'Te' : ['Ni', 'Si'], 'Ni' : ['Te', 'Fe'], 'Ne' : ['Fi', 'Ti'],
    'Fi' : ['Ne', 'Se'], 'Fe' : ['Ni', 'Si'], 'Si' : ['Fe', 'Te'], 'Se' : ['Fi', 'Ti'],
}

# 初始化权重
def initialize_weights(personality_type : str):
    weights = WEIGHT[personality_type]
    weight_sum = sum(weights.values())
    assert abs(weight_sum - 1) <= 0.00001
    return weights

# 将AI回复转化为字典变量
def extract_dict_content(message):
    json_pattern = re.compile(r'```json\n([\s\S]*?)\n```', re.DOTALL)
    match = json_pattern.search(message)

    if match:
        try:
            json_str = match.group(1).strip('```').strip()
            data = json.loads(json_str)
            return data
        except json.JSONDecodeError:
            return None

    # 检测纯字典格式
    dict_pattern = re.compile(r'\{[\s\S]*?}')
    match = dict_pattern.search(message)

    if match:
        try:
            dict_str = match.group(0).strip()
            data = eval(dict_str)
            return data
        except Exception as e:
            print(f"Failed to parse dictionary: {e}")
            return None

    return None