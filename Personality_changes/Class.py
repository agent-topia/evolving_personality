import random
from data.mbti_initial_weight import *
from llm_link import *
from prompt import *
from util import *

class Agent:
    def __init__(self, mbti):
        self.mbti            = mbti
        self.name            = ALL_MBTI[mbti][0]
        self.sex             = ALL_MBTI[mbti][1]
        self.age             = ALL_MBTI[mbti][2]
        self.weight          = {}
        self.change_history  = {'Ti' : 0, 'Fi' : 0, 'Te' : 0, 'Fe' : 0, 'Ni' : 0, 'Si' : 0, 'Ne' : 0, 'Se' : 0}
        self.history         = []
        self.model           = ''

    # Single problem processing
    def get_one_problem(self, scene : str, problem : str):
        main_func = mbti_to_function[self.mbti]['main']
        aux_func = mbti_to_function[self.mbti]['aux']
        sys_prompt, content = get_prompt(scene, problem, self.name, main_func, aux_func)
        rsp = get_rsp(content, self.model, sys_prompt, self.history)
        dict_rsp = extract_dict_content(rsp)
        if dict_rsp is None:
            while dict_rsp is None:
                rsp = get_rsp(content, self.model, sys_prompt, self.history)
                dict_rsp = extract_dict_content(rsp)
                print('format error. retry\n')


        if 'function' not in dict_rsp:
            while'function' not in dict_rsp :
                rsp = get_rsp(content, self.model, sys_prompt, self.history)
                dict_rsp = extract_dict_content(rsp)
                if dict_rsp is None:
                    while dict_rsp is None:
                        rsp = get_rsp(content, self.model, sys_prompt, self.history)
                        dict_rsp = extract_dict_content(rsp)

        content = "Scene:" + scene + "\n" + content
        self.history.append({"role": "user", "content": content})
        self.history.append({"role": "assistant", "content": rsp})
        self.main_func = dict_rsp['function']
        change_func = dict_rsp['function']
        self.change_history[change_func] += change_weight
        change_log = self.status_check(change_func)
        return dict_rsp, change_log

    # Weight status detection
    def status_check(self, change_func: str):
        main_func = mbti_to_function[self.mbti]['main']
        assist_func = mbti_to_function[self.mbti]['aux']
        main_base_weight = self.weight[main_func]
        main_temp_weight = self.weight[main_func] + self.change_history[main_func]
        assist_base_weight = self.weight[assist_func]
        assist_temp_weight = self.weight[assist_func] + self.change_history[assist_func]
        change_log = ""

        # Dominant auxiliary replacement detection
        if change_func == assist_func:
            if main_base_weight <= assist_temp_weight:
                change_log = self.reflection1()

        # Lead high-weight detection
        elif change_func == main_func:
            if main_temp_weight >= 0.5:
                self.norm_weight()

        elif change_func != main_func and change_func != assist_func:
            change_temp_weight = self.weight[change_func] + self.change_history[change_func]

            # Only lead the change detection
            if main_func == change_list[change_func]:
                if change_temp_weight >= main_base_weight:
                    change_log = self.reflection2()

            # Only for auxiliary replacement detection
            elif assist_func == change_list[change_func]:
                if change_temp_weight >= assist_base_weight:
                    change_log = self.reflection3()

            # Personality reorganization test
            else:
                if change_temp_weight >= main_base_weight:
                    change_log = self.reflection4(change_func)

        return change_log


    # Main and auxiliary replacement
    def reflection1(self):
        main_func = mbti_to_function[self.mbti]['main']
        aux_func = mbti_to_function[self.mbti]['aux']
        miss_func = ','.join(ALL_FUNCTION_cle - {main_func, aux_func})
        base_weight_prompt = ""
        temp_weight_prompt = ""
        history_prompt = ""
        change_log = ""
        temp_weight = {}

        for func in ALL_FUNCTION_cle:
            temp_weight[func] = self.change_history[func] + self.weight[func]
            base_weight_prompt += func + ":" + str(self.weight[func]) + '\n'
            temp_weight_prompt += func + ":" + str(temp_weight[func]) + '\n'

        for history in self.history:
            if history['role'] == 'assistant':
                rsp = extract_dict_content(history['content'])
                history_prompt += "**Function used:" + rsp['function'] + "\nRespond" + rsp['treatment'] + "\n"
            else:
                history_prompt += history['content'] + "\n"

        prompt1 = "\n**Based on Jungian eight-function theory, analyze the following**    \n-In Jungian theory, there are eight cognitive functions: Se, Si, Ne, Ni, Te, Ti, Fe, Fi \n-Each personality type assigns varying weights to these functions, e.g.: Ti: 0.46, Ne: 0.05, Si: 0.05, Fe: 0.05, Te: 0.05, Ni: 0.05, Se: 0.24, Fi: 0.05 \n-Every personality has a dominant and an auxiliary function. Shifts in the weights of these cognitive functions may result in changes to the dominant and auxiliary roles. A change in the dominant function can significantly alter the weights of related cognitive functions."
        prompt2 = "\n\n**Analysis Task**\n-You are given a person’s psychological type profile, including dominant and auxiliary types.\n-The person has recently used '" + aux_func + "' frequently, affecting its weight.\n-**Based on their past responses to events, decide whether the order of types should change (i.e., whether the dominant and auxiliary types should be swapped)\n-If a change occurs, provide the updated weights of the affected types."
        prompt3 = "\n\n##Basic Information##\nName:" + self.name + "\nGender:" + self.sex + "\nAge:" + self.age
        prompt4 = "\n\n##Psychological Type Characteristics##\nDominant function:" + main_func + "\nAuxiliary function:" + aux_func + "\nGenerally differentiated/undifferentiated function:" + miss_func
        prompt5 = "\n\n##Pre-change cognitive function weights##\n" + base_weight_prompt
        prompt6 = "\n\n##History##\n" + history_prompt
        prompt7 = "\n\n##Post-change cognitive function weights##\n" + temp_weight_prompt

        sys_prompt = prompt1 + prompt2 + prompt3 + prompt4 + prompt5 + prompt6 + prompt7
        content = get_ref_content1(main_func, aux_func)

        rsp = get_rsp(content, self.model, sys_prompt, [])
        rsp = extract_dict_content(rsp)
        if rsp is None:
            while rsp is None:
                print('\nformat error, retry\n')
                rsp = get_rsp(content, self.model, sys_prompt, [])
                rsp = extract_dict_content(rsp)

        if rsp['judgment'] == 'yes':
            print("Combined with historical conversation, due to the frequent use of " + aux_func + ", it was decided to swap the dominant and auxiliary.")
            change_log += '\nfunc change : main swap aux  \nmain_func : ' + main_func + '->' + aux_func + '\n'
            if float(rsp['aux_weight']) > 0.3 :
                rsp['aux_weight'] = '0.3'
            if float(rsp['aux_weight']) < 0.07 :
                rsp['aux_weight'] = '0.07'
            if float(rsp['main_weight']) > 1 :
                rsp['main_weight'] = '1'
            if float(rsp['main_weight']) < 0.31 :
                rsp['main_weight'] = '0.31'
            self.weight[aux_func] = float(rsp['main_weight'])
            self.weight[main_func] = float(rsp['aux_weight'])

            change_log += 'mbti change : ' + self.mbti + '->' + function_to_mbti[aux_func + main_func] + '\nreason: ' + rsp['reason'] + '\n\n'
            self.mbti = function_to_mbti[aux_func + main_func]
            self.norm_weight2()
        elif rsp['judgment'] == 'no':
            change_log += "no change" + '\nreason: ' + rsp['reason'] + '\n\n'
            for func in self.change_history:
                self.change_history[func] *= 0.2

        return change_log


    # Only the dominant function changes
    def reflection2(self):
        main_func = mbti_to_function[self.mbti]['main']
        aux_func = mbti_to_function[self.mbti]['aux']
        miss_func = ','.join(ALL_FUNCTION_cle - {main_func, aux_func})
        base_weight_prompt = ""
        temp_weight_prompt = ""
        history_prompt = ""
        change_log = ""
        temp_weight = {}
        change_func = change_list[main_func]

        for func in ALL_FUNCTION_cle:
            temp_weight[func] = self.change_history[func] + self.weight[func]
            base_weight_prompt += func + ":" + str(self.weight[func]) + '\n'
            temp_weight_prompt += func + ":" + str(temp_weight[func]) + '\n'

        for history in self.history:
            if history['role'] == 'assistant':
                rsp = extract_dict_content(history['content'])
                history_prompt += "**Function used:" + rsp['function'] + "\nRespond" + rsp['treatment'] + "\n"
            else:
                history_prompt += history['content'] + "\n"

        prompt1 = "\n**Based on Jungian eight-function theory, analyze the following**    \n-In Jungian theory, there are eight cognitive functions: Se, Si, Ne, Ni, Te, Ti, Fe, Fi \n-Each personality type assigns varying weights to these functions, e.g.: Ti: 0.46, Ne: 0.05, Si: 0.05, Fe: 0.05, Te: 0.05, Ni: 0.05, Se: 0.24, Fi: 0.05 \n-Every personality has a dominant and an auxiliary function. Shifts in the weights of these cognitive functions may result in changes to the dominant and auxiliary roles. A change in the dominant function can significantly alter the weights of related cognitive functions.\n-When the dominant or auxiliary function changes, the weight of the original function decreases significantly."
        prompt2 = "\n\n**Analysis Task**\n-You are given a person’s psychological type profile, including dominant and auxiliary types.\n-The person has recently used '" + change_func + "' frequently, affecting its weight.\n-**Based on their past responses to events, decide whether the order of types should change (i.e.,  whether the dominant function changes to '" + change_func + "')\n-If a change occurs, provide the updated weights of the affected types."
        prompt3 = "\n\n##Basic Information##\nName:" + self.name + "\nGender:" + self.sex + "\nAge:" + self.age
        prompt4 = "\n\n##Psychological Type Characteristics##\nDominant function:" + main_func + "\nAuxiliary function:" + aux_func + "\nGenerally differentiated/undifferentiated function:" + miss_func
        prompt5 = "\n\n##Pre-change cognitive function weights##\n" + base_weight_prompt
        prompt6 = "\n\n##History##\n" + history_prompt
        prompt7 = "\n\n##Post-change cognitive function weights##\n" + temp_weight_prompt

        sys_prompt = prompt1 + prompt2 + prompt3 + prompt4 + prompt5 + prompt6 + prompt7
        content = ref_content2

        rsp = get_rsp(content, self.model, sys_prompt, [])
        rsp = extract_dict_content(rsp)

        if rsp['judgment'] == 'yes':
            print("Combined with historical conversation, due to the frequent use of " + change_func + ", it was decided to promote it to the dominant type.")
            change_log += '\nfunc change : main change  \nmain_func : ' + main_func + '->' + change_func + '\n'

            if float(rsp['ori_main_weight']) > 0.3 :
                rsp['ori_main_weight'] = '0.3'
            if float(rsp['main_weight']) > 1 :
                rsp['main_weight'] = '1'
            if float(rsp['main_weight']) < 0.31:
                rsp['main_weight'] = '0.31'

            self.weight[main_func] = float(rsp['ori_main_weight'])
            self.weight[change_func] = float(rsp['main_weight'])

            change_log += 'mbti change : ' + self.mbti + '->' + function_to_mbti[change_func + aux_func] + '\nreason: ' + rsp['reason'] + '\n\n'
            self.mbti = function_to_mbti[change_func + aux_func]
            self.norm_weight2()
        elif rsp['judgment'] == 'no':
            change_log += "no change" + '\nreason: ' + rsp['reason'] + '\n\n'
            for func in self.change_history:
                self.change_history[func] *= 0.2
        return change_log


    # Only auxiliary functions change
    def reflection3(self):
        main_func = mbti_to_function[self.mbti]['main']
        aux_func = mbti_to_function[self.mbti]['aux']
        miss_func = ','.join(ALL_FUNCTION_cle - {main_func, aux_func})
        base_weight_prompt = ""
        temp_weight_prompt = ""
        history_prompt = ""
        change_log = ""
        temp_weight = {}
        change_func = change_list[aux_func]

        for func in ALL_FUNCTION_cle:
            temp_weight[func] = self.change_history[func] + self.weight[func]
            base_weight_prompt += func + ":" + str(self.weight[func]) + '\n'
            temp_weight_prompt += func + ":" + str(temp_weight[func]) + '\n'

        for history in self.history:
            if history['role'] == 'assistant':
                rsp = extract_dict_content(history['content'])
                history_prompt += "**Function used:" + rsp['function'] + "\nRespond" + rsp['treatment'] + "\n"
            else:
                history_prompt += history['content'] + "\n"

        prompt1 = "\n**Based on Jungian eight-function theory, analyze the following**    \n-In Jungian theory, there are eight cognitive functions: Se, Si, Ne, Ni, Te, Ti, Fe, Fi \n-Each personality type assigns varying weights to these functions, e.g.: Ti: 0.46, Ne: 0.05, Si: 0.05, Fe: 0.05, Te: 0.05, Ni: 0.05, Se: 0.24, Fi: 0.05 \n-Every personality has a dominant and an auxiliary function. Shifts in the weights of these cognitive functions may result in changes to the dominant and auxiliary roles. A change in the dominant function can significantly alter the weights of related cognitive functions.\n-When the dominant or auxiliary function changes, the weight of the original function decreases significantly."
        prompt2 = "\n\n**Analysis Task**\n-You are given a person’s psychological type profile, including dominant and auxiliary types.\n-The person has recently used '" + change_func + "' frequently, affecting its weight.\n-**Based on their past responses to events, decide whether the order of types should change (i.e.,  whether the auxiliary function changes to '" + change_func + "')\n-If a change occurs, provide the updated weights of the affected types."
        prompt3 = "\n\n##Basic Information##\nName:" + self.name + "\nGender:" + self.sex + "\nAge:" + self.age
        prompt4 = "\n\n##Psychological Type Characteristics##\nDominant function:" + main_func + "\nAuxiliary function:" + aux_func + "\nGenerally differentiated/undifferentiated function:" + miss_func
        prompt5 = "\n\n##Pre-change cognitive function weights##\n" + base_weight_prompt
        prompt6 = "\n\n##History##\n" + history_prompt
        prompt7 = "\n\n##Post-change cognitive function weights##\n" + temp_weight_prompt

        sys_prompt = prompt1 + prompt2 + prompt3 + prompt4 + prompt5 + prompt6 + prompt7
        content = ref_content3
        rsp = get_rsp(content, self.model, sys_prompt, [])
        rsp = extract_dict_content(rsp)
        if rsp is None:
            while rsp is None:
                rsp = get_rsp(content, self.model, sys_prompt, [])
                rsp = extract_dict_content(rsp)

        if rsp['judgment'] == 'yes':
            print("Combined with historical conversation, due to the frequent use of " + change_func + ", it was decided to promote it to the auxiliary type.")
            change_log = '\nfunc change : aux change  \naux_func : ' + aux_func + '->' + change_func + '\n'
            if float(rsp['ori_aux_weight']) > 0.06 :
                rsp['ori_aux_weight'] = '0.06'
            if float(rsp['aux_weight']) > 0.3 :
                rsp['aux_weight'] = '0.3'
            if float(rsp['aux_weight']) < 0.07 :
                rsp['aux_weight'] = '0.07'
            self.weight[aux_func] = float(rsp['ori_aux_weight'])
            self.weight[change_func] = float(rsp['aux_weight'])

            change_log += 'mbti change : ' + self.mbti + '->' + function_to_mbti[main_func + change_func] + '\nreason: ' + rsp['reason'] + '\n\n'
            self.mbti = function_to_mbti[main_func + change_func]
            self.norm_weight2()
        elif rsp['judgment'] == 'no':
            change_log += "no change" + '\nreason: ' + rsp['reason'] + '\n\n'
            for func in self.change_history:
                self.change_history[func] *= 0.2

        return change_log


    # Both the dominant and auxiliary functions have changed
    def reflection4(self, change_func: str):
        main_func = mbti_to_function[self.mbti]['main']
        aux_func = mbti_to_function[self.mbti]['aux']
        miss_func = ','.join(ALL_FUNCTION_cle - {main_func, aux_func})
        base_weight_prompt = ""
        temp_weight_prompt = ""
        history_prompt = ""
        change_log = ""
        temp_weight = {}
        aux_choices = main_to_aux[change_func]

        for func in ALL_FUNCTION_cle:
            temp_weight[func] = self.change_history[func] + self.weight[func]
            base_weight_prompt += func + ":" + str(self.weight[func]) + '\n'
            temp_weight_prompt += func + ":" + str(temp_weight[func]) + '\n'

        for history in self.history:
            if history['role'] == 'assistant':
                rsp = extract_dict_content(history['content'])
                history_prompt += "**Function used:" + rsp['function'] + "\nRespond" + rsp['treatment'] + "\n"
            else:
                history_prompt += history['content'] + "\n"

        prompt1 = "\n##Based on Jungian eight-function theory, analyze the following##    \n-In Jungian theory, there are eight cognitive functions: Se, Si, Ne, Ni, Te, Ti, Fe, Fi \n-Each personality type assigns varying weights to these functions, e.g.: Ti: 0.46, Ne: 0.05, Si: 0.05, Fe: 0.05, Te: 0.05, Ni: 0.05, Se: 0.24, Fi: 0.05 \n-Every personality has a dominant and an auxiliary function. Shifts in the weights of these cognitive functions may result in changes to the dominant and auxiliary roles. A change in the dominant function can significantly alter the weights of related cognitive functions.\n-When the dominant or auxiliary function changes, the weight of the original function decreases significantly."
        prompt2 = "\n\n**Analysis Task**\n-You are given a person’s psychological type profile, including dominant and auxiliary types.\n-The person has recently used '" + change_func + "' frequently, affecting its weight.\n-**Based on their past responses to events, decide whether the order of types should change (i.e.,  whether the dominant function changes to '" + change_func + "', and the auxiliary function changes to '" + aux_choices[0] + "' or '" + aux_choices[1] + "')\n-If a change occurs, provide the updated weights of the affected types."

        prompt3 = "\n\n##Basic Information##\nName:" + self.name + "\nGender:" + self.sex + "\nAge:" + self.age
        prompt4 = "\n\n##Psychological Type Characteristics##\nDominant function:" + main_func + "\nAuxiliary function:" + aux_func + "\nGenerally differentiated/undifferentiated function:" + miss_func
        prompt5 = "\n\n##Pre-change cognitive function weights##\n" + base_weight_prompt
        prompt6 = "\n\n##History##\n" + history_prompt
        prompt7 = "\n\n##Post-change cognitive function weights##\n" + temp_weight_prompt

        sys_prompt = prompt1 + prompt2 + prompt3 + prompt4 + prompt5 + prompt6 + prompt7
        content = "##Final output in JSON format, following the example. Do not include any additional content##\n{\n   \"judgment\" : \"yes\", ///only \"yes\" or \"no\" (in lowercase), indicating whether a change occurred.Use historical information as the basis for judgment; if a psychological function is used frequently, it may change.\n    \"reason\" : \"xxxxx\" //explanation for this judgment\n   \"main_weight\" : \"0.35\", //weight of the dominant function, between 0.31-1.00. omit if no change\n  \"aux_func\" : \"" + \
                  aux_choices[0] + "\", //One of '" + aux_choices[0] + "' and '" + aux_choices[1] + "'\n    \"aux_weight\" : \"0.18\", //weight of the auxiliary function, between 0.06-0.30. omit if no change\n  \"ori_main_weight\" : \"0.05\", //Weight of the original dominant function after decrease, between 0-0.30. omit if no change\n  \"ori_aux_weight\" : \"0.03\", //Weight of the original auxiliary function after decrease, between 0-0.06. omit if no change"

        rsp = get_rsp(content, self.model, sys_prompt, [])
        print(rsp + '\n')
        rsp = extract_dict_content(rsp)

        if rsp['judgment'] == 'yes':
            print("Combined with historical conversation, due to the frequent use of " + change_func + ", it was decided to reconstruct the basic personality.")
            new_aux_func = rsp['aux_func']
            if (new_aux_func != aux_choices[1]) and (new_aux_func != aux_choices[0]):
                new_aux_func = random.choice(aux_choices)
            change_log += '\nfunc change : main and aux change  \n' + 'main_func : ' + main_func + '->' + change_func + '\n' + 'aux_func : ' + aux_func + '->' + \
                          new_aux_func + '\n'

            if float(rsp['ori_main_weight']) > 0.30 :
                rsp['ori_main_weight'] = '0.30'
            if float(rsp['ori_aux_weight']) > 0.06 :
                rsp['ori_aux_weight'] = '0.06'
            if float(rsp['main_weight']) > 1 :
                rsp['main_weight'] = '1'
            if float(rsp['main_weight']) < 0.31:
                rsp['main_weight'] = '0.31'
            if float(rsp['aux_weight']) > 0.3 :
                rsp['aux_weight'] = '0.3'
            if float(rsp['aux_weight']) < 0.07 :
                rsp['aux_weight'] = '0.07'
            self.weight[main_func] = float(rsp['ori_main_weight'])
            self.weight[aux_func] = float(rsp['ori_aux_weight'])
            self.weight[change_func] = float(rsp['main_weight'])
            self.weight[new_aux_func] = float(rsp['aux_weight'])

            change_log += 'mbti change : ' + self.mbti + '->' + function_to_mbti[change_func + new_aux_func] + '\nreason: ' + rsp['reason'] + '\n\n'
            self.mbti = function_to_mbti[change_func + new_aux_func]
            self.norm_weight2()
        elif rsp['judgment'] == 'no':
            change_log += "no change" + '\nreason: ' + rsp['reason'] + '\n\n'
            for func in self.change_history:
                self.change_history[func] *= 0.2
        return change_log

    # Normalization function
    def norm_weight(self):
        sum_weight = 0
        result_weight = {}
        for func in ALL_FUNCTION_cle:
            sum_weight += self.weight[func] + self.change_history[func]
        for func2 in self.weight:
            new_weight = (self.weight[func2] + self.change_history[func2]) / sum_weight
            result_weight[func2] = float("%.2f" %new_weight)

        self.weight = result_weight
        self.change_history = {'Ti' : 0, 'Fi' : 0, 'Te' : 0, 'Fe' : 0, 'Ni' : 0, 'Si' : 0, 'Ne' : 0, 'Se' : 0}
        self.history = []

    # Normalization function
    def norm_weight2(self):
        sum_weight = 0
        result_weight = {}
        for func in ALL_FUNCTION_cle:
            sum_weight += self.weight[func]
        for func2 in self.weight:
            new_weight = self.weight[func2] / sum_weight
            result_weight[func2] = float("%.2f" %new_weight)

        self.weight = result_weight
        self.change_history = {'Ti' : 0, 'Fi' : 0, 'Te' : 0, 'Fe' : 0, 'Ni' : 0, 'Si' : 0, 'Ne' : 0, 'Se' : 0}
        self.history = []

