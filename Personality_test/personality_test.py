from llm_link import *
from prompt import *
from util import *
import random
import threading
from tqdm import tqdm
import argparse

def all_mbti_test(model, all_mbti, method, num, degree, num_mbti):
    load_dotenv('para.env')
    with open('data/character.json', encoding='UTF-8') as file1:
        all_character = json.load(file1)

    error_results = [] # A result that differs from the initial mbti
    results = [] # All results
    counts = {} # Count the correct number of each dimension
    

    def mbti_test(name, mbti, model, pbar, method, num_mbti):
        if method == 'judge':
            result, error_res = question_judge(name, mbti, model, pbar)
            results.extend(result)
            error_results.extend(error_res)
        elif method == 'test':
            count, result, error_res = personality_test(name, mbti, model, degree,num_mbti, pbar)
            results.append(result)
            counts[mbti] = count
            error_results.append(error_res)
        elif method == 'no_prompt':
            count, result, error_res = no_prompt_test(name, mbti, model, num_mbti, pbar)
            results.append(result)
            counts[mbti] = count
            # error_results.append(error_res)

    threads = []  # Used for storing thread objects
    progress_bars = [] # Used for the progress bar
    for i in range(len(all_mbti)):
        pbar = tqdm(total=int(num_mbti), desc=f"任务 {all_mbti[i]}", position=i)  
        progress_bars.append(pbar)

    for i in range(len(all_mbti)): 
        t = threading.Thread(target=mbti_test, args=(all_character[i]['name'], all_mbti[i], model, progress_bars[i], method, num_mbti))
        threads.append(t)  
    for t in threads:
        t.start()  # start progress
    for t in threads:
        t.join()  # wait for progress

    # write json
    if method == 'test':
        # all results in test method
        with open('result/exp1_' + model + '_' + method + '_' + str(num) + '.json', "w") as file2:
            json.dump(results, file2, ensure_ascii=False, indent=4)
        # The number of answers from different dimensions
        with open('result/exp1_' + model + '_' +  method + '_' + str(num) + '_score.json', "w") as file2:
            json.dump(counts, file2, ensure_ascii=False, indent=4)
        # with open('result/exp1_' + model + '_' +  method + '_' + str(num) + '_error.json', "w") as file2:
        #     json.dump(error_results, file2, ensure_ascii=False, indent=4)
    if method == 'judge':
        # all results in test method
        with open('result/exp1_' + model + '_' + method + '70.json', "w") as file2:
            json.dump(results, file2, ensure_ascii=False, indent=4)
        # with open('result/exp1_' + model + '_' +  method + '_error.json', "w") as file2:
        #     json.dump(error_results, file2, ensure_ascii=False, indent=4)
    if method == 'no_prompt':
        # all results in test method
        with open('result/exp1_' + model + '_' + method + '_' + str(num) + '.json', "w") as file2:
            json.dump(results, file2, ensure_ascii=False, indent=4)
        # The number of answers from different dimensions
        with open('result/exp1_' + model + '_' +  method + '_' + str(num) + '_score.json', "w") as file2:
            json.dump(counts, file2, ensure_ascii=False, indent=4)
        # with open('result/exp1_' + model + '_' +  method + '_error.json', "w") as file2:
        #     json.dump(error_results, file2, ensure_ascii=False, indent=4)

# It is used to make judgments on the dimensions of the problem
def question_judge(name: str, mbti: str, model : str, pbar):
    result = []
    error_res = []
    with open('data/mbti_70_en.json', encoding='UTF-8') as file:
        all_question = json.load(file)
    for question in all_question:
        # Construct prompt words
        question_prompt, dimension = get_question_dimension(question)
        # Select the api and model
        rsp = get_rsp(question_prompt, model)
        message = extract_dict_content(rsp)
        if message is None:
            while message is None:
                print('again\n')
                rsp = get_rsp(question_prompt, model)
                message = extract_dict_content(rsp)
        result.append({'Question' : question, 'Answers': message})
        if dimension != message['dimension']:
            error_res.append({'Question' : question, 'Answers': message})
        pbar.update(1) 
    return result, error_res

# The results of problems for different personalities
def personality_test(name: str, mbti: str, model : str, degree, num_mbti, pbar):
    with open(f'result/exp1_{model}_judge{num_mbti}.json', encoding='UTF-8') as file:
        all_question = json.load(file)

    all_score = []
    result = {mbti : []}
    error_res = {mbti : []}

    info_prompt = get_info_prompt(name) # Prompt words for basic personality information
  
    for QA in all_question:
        question = QA['Question']
        dimension = QA['Answers']['dimension']
        psyc_prompt = get_psyc_prompt(name, mbti, dimension, degree) # Prompt words for the three mechanisms of personality understanding problems
        question_prompt = get_question_prompt(name, question)  # Prompt words for question and answer formats
        prompt = info_prompt + psyc_prompt + question_prompt
        # print(prompt)

        rsp = get_rsp(prompt, model)  # Call the api interface
        message = extract_dict_content(rsp)  # Correct the format of the answers
        if message is None:
            while message is None:
                print('again\n')
                rsp = get_rsp(prompt, model)
                message = extract_dict_content(rsp)

        for ans in question['answerOptions']:
            if ans['type'] == message['answer']:
                score = ans['score']
                message['answer'] = score
        result[mbti].append({'Question' : question, 'Answers': message, 'Prompt': prompt})
        
        if message['answer'] not in mbti:
            error_res[mbti].append({'Question' : question, 'Answers': message, 'Prompt': prompt})

        all_score.append(score)
        pbar.update(1) 

    return number_count(all_score), result, error_res

# Run the MBTI test directly without any prompt words---no prompt
def no_prompt_test(name: str, mbti: str, model : str, num_mbti, pbar):
    with open(f'data/mbti_{num_mbti}_en.json', encoding='UTF-8') as file:
        all_question = json.load(file)

    all_score = []
    result = {mbti : []}
    error_res = {mbti : []}

    info_prompt = get_info_prompt(name)
    psyc_prompt = "##" + name + " Psychological Type ##\nYour MBTI personality type is " + mbti + "\n"
    
    for question in all_question:
        
        question_prompt = get_question_prompt(name, question)
        prompt = info_prompt + psyc_prompt + question_prompt
        # print(prompt)

        rsp = get_rsp(prompt, model)  # Call the api interface
        message = extract_dict_content(rsp)  # Correct the format of the answers
        if message is None:
            while message is None:
                print('again\n')
                rsp = get_rsp(prompt, model)
                message = extract_dict_content(rsp)

        for ans in question['answerOptions']:
            if ans['type'] == message['answer']:
                score = ans['score']
                message['answer'] = score
        result[mbti].append({'Question' : question, 'Answers': message, 'Prompt': prompt})
        
        if message['answer'] not in mbti:
            error_res[mbti].append({'Question' : question, 'Answers': message, 'Prompt': prompt})

        all_score.append(score)
        pbar.update(1)  # 更新进度条

    return number_count(all_score), result, error_res

# The counting function of the answer
def number_count(all_score):

    i_count = all_score.count("I")
    e_count = all_score.count("E")
    s_count = all_score.count("S")
    n_count = all_score.count("N")
    f_count = all_score.count("F")
    t_count = all_score.count("T")
    p_count = all_score.count("P")
    j_count = all_score.count("J")

    all_count = {
        "I": i_count,
        "E": e_count,
        "S": s_count,
        "N": n_count,
        "F": f_count,
        "T": t_count,
        "P": p_count,
        "J": j_count
    }

    return all_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--method', type=str, default = 'no_prompt') # no_prompt, test, judge
    parser.add_argument('--mbti_num', type=int, default= 16)
    parser.add_argument('--model', type=str, default= 'OPENAI')# QWEN, OPENAI, LLAMA
    parser.add_argument('--steps', type=int, default= 5)
    parser.add_argument('--test_num', type=int, default= 70)
    parser.add_argument('--degree', type=str, default= 'MID')
    args = parser.parse_args()

    if args.mbti_num == 16:
        all_mbti = list(WEIGHT.keys())
    elif args.mbti_num == 1:
        all_mbti = ['ENTJ']
    for i in range(args.steps):
        all_mbti_test(args.model, all_mbti, args.method, i, args.degree, str(args.test_num)) 
        print('-----------------------------------第'+ str(i) +'轮测试结束--------------------------------------------')


