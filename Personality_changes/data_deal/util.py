change_weight = 0.08
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

x_posts = {
    'Fi' : 1, 'Fe' : 2, 'Ti' : 3, 'Te' : 4,
    'Si' : 5, 'Se' : 6, 'Ni' : 7, 'Ne' : 8,
}

y_posts = {
    "INTP" : 1, "INTJ" : 2, "INFP" : 3, "INFJ" : 4, "ISTP" : 5,
    "ISTJ" : 6, "ISFP" : 7, "ISFJ" : 8, "ENFP" : 9, "ENFJ" : 10,
    "ENTP" : 11, "ENTJ" : 12, "ESFP" : 13, "ESFJ" : 14, "ESTP" : 15, "ESTJ" : 16
}

bias = {'OPENAI' : -2, 'QWEN' : 0, 'LLAMA' : -1}
