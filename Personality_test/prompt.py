import json
from data.mbti_initial_weight import WEIGHT, ALL_FUNCTION


def get_psyc_prompt(name : str, mbti: str, dimension:str, degree):

    main_func = WEIGHT[mbti]['main_function'] #主导人格
    assist_func = WEIGHT[mbti]['assist_function'] #辅助人格

    main_func_weight = WEIGHT[mbti][main_func]
    assist_func_weight = WEIGHT[mbti][assist_func]
      
    main_description, main_degree = degree_judgment(main_func, main_func_weight, 'HIGH')
    assist_description, assist_degree = degree_judgment(assist_func, assist_func_weight, degree)

    work_logic = get_work_logic(mbti, dimension, main_description, assist_description, degree)

    prompt1 = "\n##" + name + " Psychological Type Processing Mechanism##\n" + \
        work_logic + '\n'

    return prompt1



def get_work_logic(mbti : str, dimension, main_description, assist_description, degree):

    with open('data/mbti_prompt.json', encoding='UTF-8') as file:
        data = json.load(file)

    if degree == 'HIGH':
        level = 'conflict'
    elif degree == 'MID':
        level = 'balance'
    elif degree == 'LOW':
        level = 'imbalance'
    if mbti in ['INTP', 'ISTP', 'INFP', 'ISFP', 'ENTJ', 'ESTJ', 'ENFJ', 'ESFJ']:
        if dimension == 'I/E':
            get_mechanism = main_description
        elif dimension == 'N/S':
            get_mechanism = assist_description
        elif dimension == 'T/F':
            get_mechanism = main_description
        elif dimension == 'J/P':
            get_mechanism = data['MBTI'][mbti][level]
    else:
        if dimension == 'I/E':
            get_mechanism = main_description
        elif dimension == 'N/S':
            get_mechanism = main_description
        elif dimension == 'T/F':
            get_mechanism = assist_description
        elif dimension == 'J/P':
            get_mechanism = data['MBTI'][mbti][level]
    return get_mechanism




def degree_judgment(func, weight, degree):

    with open('data/mbti_prompt.json', encoding='UTF-8') as file:
        data = json.load(file)

    message = data['FUNCTION'][func][degree]
    return message, degree



def get_question_prompt(name : str, question):

    prompt1 = "\nNow, please strictly follow the information above, especially the content in ##" + name + " Psychological Type ## and answer the multiple-choice questions carefully as " + \
    name + ". Provide the reasoning behind your choice and which mode you chose, keeping your answer to 50 words or less. The question is as follows:"

    prompt2 = "\nQuestion:" + question['question'] + "\nOption " + question['answerOptions'][0]['type'] + ":" + \
              question['answerOptions'][0]['answer'] + "\nOption " + question['answerOptions'][1]['type'] + ":" + \
              question['answerOptions'][1]['answer']
    
    prompt3 = """\n\nYou must return your response in the following structure only(output with English),with absolutely no content beyond the specified example structure:\n{\n"answer" : "A", // only the single letter of the option\n"reason" : ""// reason for choosing the option\n}"""

    question_prompt = prompt1 + prompt2 + prompt3
    # print(question_prompt)
    return question_prompt


def get_question_dimension(question):
    prompt1 = "##Player##\nNow you need to accurately identify the dimension (I/E, N/S, T/F, J/P) to which the question belongs based on the user's question and answer options.\n\n## Dimension Definition##\n1. I/E (Introversion/Extroversion)\n- Core: Energy Direction and Focus\n- Key Characteristics: The question addresses social preferences (solitude vs. group), energy sources (internal reflection vs. external interaction), and expression style (introversion vs. extroversion).\n- Example: 'How do you recharge after social activities?' → I/E\n2. N/S (Intuition/Sensing)\n- Core: Information Acquisition Style\n- Key Characteristics: The question focuses on information processing details (concrete facts vs. abstract concepts), time focus (present reality vs. future possibilities), and description style (actual experience vs. theoretical association). - Example: 'How do you understand the meaning of this metaphor?' → N/S\n3. T/F (Thinking/Feeling)\n- Core: Decision-making Logic\n- Key Characteristics: The question involves decision-making criteria (objective logic vs. subjective emotion), value orientation (fairness vs. interpersonal relationships), and conflict resolution (reasoning vs. emphasizing harmony).\n- Example: 'Do you rely more on logic or empathy when making decisions?' → T/F\n4. J/P (Judgment/Perception)\n- Core: Attitude toward the External World\n- Key Characteristics: The question addresses behavioral patterns (planning vs. flexibility), organizational style (structured vs. spontaneous), and goal-oriented approach (results-oriented vs. process-oriented). \n- Example: 'Do you make a detailed itinerary before traveling?' → J/P\n\n## Analysis Process##\nPlease reason strictly according to the steps: \n1. Understand the Essence of the Question\n- Extract keywords and behavioral scenarios from the question (e.g., 'going out,' 'making decisions,' 'social interaction'). \n2. Compare Answer Options\n- Analyze the cognitive preferences implied by each option (e.g., 'Planning' → Structured; 'Going Directly' → Spontaneous). \n3. Match Dimensions\n- Compare the question characteristics with the dimension definitions: \n- If it involves 'Energy Source/Social Orientation' → I/E\n- If it involves 'Information Processing Style' → N/S\n- If it involves 'Decision-Making Logic' → T/F\n- If it involves 'Planning/Flexibility' → J/P\n4. Eliminate Distractions\n- Ensure there is no confusion between dimensions (e.g., planning belongs to J/P, not T/F). \n\n## Example Analysis##\nQuestion: What do you do when you have to go out all day? \nOption A: Plan what you will do and when\nOption B: Just go\nReasoning Process: \n1. Question Essence: Behavior patterns when out (planning vs. improvisation). \n2. Option Comparison: \n- A emphasizes structure (planning time/items) → Judging (J) \n- B emphasizes flexibility (unplanned action) → Perceiving (P) \n3. Dimension Match: The difference in behavior patterns directly corresponds to the J/P dimension (Judging vs. Perceiving). \n4. Interference Elimination: No social/decision-making/information processing elements, excluding I/E/T/F/N/S. \nOutput: \n{'dimension': 'J/P', 'reason': 'This question reflects attitudes toward the outside world (J/P dimension) by comparing planning and flexibility.'} \n\n Provide the reasoning behind your choice and which mode you chose, keeping your answer to 50 words or less.. The question is as follows:\n"

    prompt2 = "\nQuestion:" + question['question'] + "\nOption " + question['answerOptions'][0]['type'] + ":" + \
              question['answerOptions'][0]['answer'] + "\nOption " + question['answerOptions'][1]['type'] + ":" + \
              question['answerOptions'][1]['answer']
    prompt3 = "\n\nResponse output format (strictly defined, JSON only): \n{\n'dimension': 'J/P', //option letters only\n'reason': 'xxxxx' //Reason. This question reflects attitudes toward the outside world (J/P dimension) by comparing planning and flexibility. \n}\n"
    
    if question['answerOptions'][0]['score'] in "I/E":
        dimension = "I/E"
    elif question['answerOptions'][0]['score'] in "N/S":
        dimension = "N/S"
    elif question['answerOptions'][0]['score'] in "T/F":
        dimension = "T/F"
    elif question['answerOptions'][0]['score'] in "J/P":
        dimension = "J/P"
    return prompt1 + prompt2 + prompt3, dimension
 
def get_info_prompt(name : str):

    prompt1 = "**Based on Jung's personality theory, role-play as " + name + " with the personality described below to solve the presented problem.**\n\n##Basic Information##\nName:" + name

    prompt2 = "\n"

    with open('data/character.json', encoding='UTF-8') as file:
        all_character = json.load(file)
    
    for i in all_character:
        if i['name'] == name:
            character_info = i

    
    prompt2 = "\ngender:" + character_info['gender'] + "\n" + "age:" + character_info['age'] + "\n"

    info_prompt = prompt1 + prompt2

    return info_prompt