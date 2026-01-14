import threading
import argparse
from Class import *

compensation_weight = 0.05
save_load = {'QWEN' : 'data/QWEN_result.txt', 'OPENAI' : 'data/OPENAI_result.txt', 'LLAMA' : 'data/LLAMA_result.txt'}
MBTI_LIST = ["INTP", "INTJ", "INFP", "INFJ", "ISTP", "ISTJ", "ISFP", "ISFJ", "ENFP", "ENFJ", "ENTP", "ENTJ", "ESFP", "ESFJ", "ESTP", "ESTJ"]


def one_func_test(mbti : str, function : str, model : str):
    agent = Agent(mbti)
    with open('data/weight.json', encoding='UTF-8') as file:
        all_weight = json.load(file)
    agent.weight = all_weight[mbti]
    agent.change_history = {'Ti' : 0, 'Fi' : 0, 'Te' : 0, 'Fe' : 0, 'Ni' : 0, 'Si' : 0, 'Ne' : 0, 'Se' : 0}
    agent.model = model
    weight_data = []

    with open('data/question_with_scene.json', encoding='UTF-8') as file:
        all_function_q = json.load(file)
    problems = all_function_q[function]

    all_score = []
    all_false_rsp = []
    all_log = []
    ture_count = 0
    turn_count = -1
    for sc_and_p in problems:
        scene = sc_and_p['scene']
        problems_in_sc = sc_and_p['problems']
        all_log.append('\nScene : ' + scene + '\n')
        turn_count += 1
        problem_count = 1

        for problem in problems_in_sc:
            rsp, change_log = agent.get_one_problem(scene, problem)
            weight = str(agent.weight)
            log = '\nProblem ' + str(problem_count) + ' : ' + problem + '\nRespond : ' + str(rsp) + '\nChoose function : ' + rsp['function'] + '\nbase_weight : ' + weight + '\ntemp_weight : ' + str(agent.change_history) + '\n' + change_log + "\n"

            print(log)
            for func in ALL_FUNCTION_cle:
                print(func + ":" + str(float(agent.weight[func]) + agent.change_history[func]) + "  ")
            print("\n\n")
            all_log.append(log)
            problem_count += 1
            all_score.append(rsp['function'])

            if rsp['function'] == function:
                ture_count += 1
            else:
                false_log = '\nScene : ' + scene + '\nProblem : ' + problem + '\nRespond : ' + str(rsp) + '\nChoose function : ' + rsp['function'] + '\nTrue function : ' + function + '\n'
                all_false_rsp.append(false_log)

    all_log += mbti + '|' + function + ' score:' + ','.join(all_score) + '\nTrue count: ' + str(ture_count) + '\n' + 'mbti change:' + mbti + '->' + agent.mbti + '\n\n'
    result = mbti + '|' + function + ' score:' + ','.join(all_score) + '\nTrue count: ' + str(ture_count) + '\n' + 'mbti change:' + mbti + '->' + agent.mbti + '\n\n'

    return all_log, all_false_rsp, result, weight_data

def one_mbti_test(mbti : str, model : str, scene : list):

    save_msg = '\nmbti:' + mbti + '\n'
    all_result = []
    all_weight_data = []

    for function in scene:
        all_log, all_false_rsp, result, weight_data = one_func_test(mbti, function, model)
        all_result.append(result)
        all_weight_data.append(weight_data)

        for log in all_log:
            save_msg += log
        for false_log in all_false_rsp:
            save_msg += false_log

    for r in all_result:
        save_msg += r + '\n'
    with open(save_load[model], 'a', encoding='UTF-8') as file:
        file.write(save_msg)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--method', type=str, default = 'all_scene') # all_scene / single_scene
    parser.add_argument('--scene', type=str, default = 'Se')
    parser.add_argument('--mbti', type=str, default= 'INTJ')
    parser.add_argument('--model', type=str, default= 'OPENAI')# QWEN, OPENAI, LLAMA
    args = parser.parse_args()
    if args.method == 'all_scene':
        scene = ["Fi", "Fe", "Ti", "Te", "Si", "Se", "Ni", "Ne"]
    elif args.method == 'single_scene':
        scene = [args.scene]
    one_mbti_test(args.mbti, args.model, scene)