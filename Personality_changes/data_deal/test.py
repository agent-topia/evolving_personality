import json

mbti_dic = [
    "INTP", "INTJ", "INFP", "INFJ",
    "ISTP", "ISTJ", "ISFP", "ISFJ",
    "ENFP", "ENFJ", "ENTP", "ENTJ",
    "ESFP", "ESFJ", "ESTP", "ESTJ",
]

func_dic = [
    "Fi", "Fe", "Ti", "Te",
    "Si", "Se", "Ni", "Ne",
]

model_list = ["OPENAI", "LLAMA", "QWEN"]

save_msg = {
    "OPENAI" : {
        "INTP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "INTJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "INFP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "INFJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ISTP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ISTJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ISFP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ISFJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ENFP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ENFJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ENTP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ENTJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ESFP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ESFJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ESTP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ESTJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
    },
    "LLAMA" : {
        "INTP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "INTJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "INFP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "INFJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ISTP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ISTJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ISFP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ISFJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ENFP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ENFJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ENTP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ENTJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ESFP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ESFJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ESTP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ESTJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
    },
    "QWEN" : {
        "INTP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "INTJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "INFP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "INFJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ISTP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ISTJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ISFP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ISFJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ENFP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ENFJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ENTP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ENTJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ESFP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ESFJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ESTP" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
        "ESTJ" : {"Fi" : [], "Fe" : [], "Ti" : [], "Te" : [], "Si" : [], "Se" : [], "Ni" : [], "Ne" : [],},
    }
}
with open("data_weight.json", "r") as file:
    all_data = json.load(file)

for data in all_data:
    two_weight = data[2].split("\n")
    dic_weight = {}
    for weight in two_weight:
        key = weight[:11]
        func_weight = weight[14:]
        dic_weight[key] = eval(func_weight)
    mbti = mbti_dic[int((data[1]-1)/4)]
    func = func_dic[int((data[0] -3)/15)]
    model = model_list[(data[1] + 2)%4]
    save_msg[model][mbti][func].append(dic_weight)

with open("weight_change.json", "a") as file:
    file.write(json.dumps(save_msg, indent=4))
# print(save_msg)
