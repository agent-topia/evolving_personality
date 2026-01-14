import json
from data.mbti_initial_weight import ALL_FUNCTION_cle

test_prompt = """
##Compensation Mechanism##
1. When the dominant and auxiliary functions cannot effectively cope with the current situation, you will differentiate a new psychological function from the unconscious to compensate.
2.The differentiation process is based on task requirements: analyze the core demands of the situation, match the most appropriate Jungian psychological function, and refer to the following function descriptions:
 -Ti: Internal logic analysis, theoretical system construction, pursuit of accuracy, principle-driven; typical matching situations: issues requiring deep reasoning, system deconstruction, or principle exploration.
 -Te: External organization optimization, efficiency-driven decision-making, practical result-oriented, structured execution; typical matching situations: tasks requiring efficient management, problem-solving, or resource allocation.
 -Fi: Personal value system maintenance, moral emotional judgment, pursuit of inner authenticity, self-harmony; typical matching situations: issues involving ethical choices, personal beliefs, or emotional introspection.
 -Fe: Group emotional coordination, social norm adaptation, response to others’ needs, promotion of harmony; typical matching situations: situations requiring interpersonal relationship management, emotional support, or social interaction.
 -Ni: Deep pattern insight, foresight of future trends, abstract integration, symbolic understanding; typical matching situations: issues requiring development prediction, interpretation of complex meanings, or long-term planning.
 -Ne: Exploration of multiple possibilities, generation of creative ideas, conceptual connection, challenge to the status quo; typical matching situations: situations requiring innovative brainstorming, multi-perspective exploration, or opportunity discovery.
 -Si: Specific memory recall, focus on detailed facts, reliance on traditional methods, stability maintenance; typical matching situations: tasks based on historical data, sensory details, or customary execution.
 -Se: Focus on immediate sensory experience, real-time action response, adaptation to physical reality, environmental interaction; typical matching situations: tasks requiring quick responses, sensory inputs, or real-world operations.

##Following the steps##
1.Task Demand Analysis:
 -Analyze the core tasks and requirements of the current scenario.
 -Identify which specific psychological functions are needed to handle this task effectively (based on Jungian theory, explain why).
2.Current Function Evaluation:
 -Assess whether your dominant function and auxiliary function can meet the task requirements.
 -Conclusion: If insufficient, state "Current psychological type cannot effectively cope, triggering the compensation mechanism."
3.Compensatory Function Identification:
 -If the current functions are insufficient, choose the most appropriate psychological function from your undeveloped functions to compensate.
 
"""

Compensation_prompt = """
##Rules##
You now need to precisely match Jung’s eight psychological functions based on the user’s question. You must follow these steps:
1.Understand the essence of the question: Identify which main area the question involves:
    -Thinking: If the question requires logical analysis, decision-making, system building, organizational management, or fact-based reasoning (e.g., math problems, process optimization).
    -Feeling: If the question involves values, relationships, moral judgment, or harmony (e.g., team conflict, ethical dilemmas).
    -Sensing: If the question requires attention to facts, details, sensory experience, practical experience, immediate operation, or real-time action (e.g., emergency handling, data collection).
    -Intuition: If the question requires insight into patterns, abstract ideas, future trends, possibilities, or innovation (e.g., strategic planning, idea generation).
2.Determine the orientation of the question: Decide whether it is more focused on internal processes or external interaction:
    -Introversion (I): If the question involves self-reflection, independent thinking, deep analysis, theoretical depth, independent decision-making, or internal consistency.
    -Extraversion (E): If the question involves group interaction, environmental adaptation, practical action, communication, external organization, or reliance on external standards.
3.Match the cognitive function: Based on the essence and orientation, choose the corresponding psychological type:
 a.If the essence is Thinking:
    -Introversion (I) → Ti (Introverted Thinking): Focused on internal logical frameworks and analysis.
    -Extraversion (E) → Te (Extraverted Thinking): Focused on external organization and efficiency.
 b.If the essence is Feeling:
    -Introversion (I) → Fi (Introverted Feeling): Focused on personal values and morality.
    -Extraversion (E) → Fe (Extraverted Feeling): Focused on group harmony and social norms.
 c.If the essence is Sensing:
    -Introversion (I) → Si (Introverted Sensing): Focused on past experiences and detailed memory.
    -Extraversion (E) → Se (Extraverted Sensing): Focused on real-time sensory experience and immediate action.
 d.If the essence is Intuition:
    -Introversion (I) → Ni (Introverted Intuition): Focused on future insights and deep patterns.
    -Extraversion (E) → Ne (Extraverted Intuition): Focused on multiple possibilities and external connections.
"""

Output_prompt = """
##Output JSON format data in English strictly following the example below, prohibited to output any content other than the examples provided##
Example(Output strictly in JSON format):
{
    "function" : "xx" ,//One of Ti,Te,Fi,Fe,Ni,Ne,Si,Se
    "treatment" : "xxxxx" , //Response to the question
    "reason" : "xxxxx"  //Why choose the function (e.g., "Emphasize internal logic due to the problem")
}

"""

ref_content2 = """
##Final output in JSON format, following the example. Do not include any additional content##
{
    "judgment" : "yes", //only "yes" or "no" (in lowercase), indicating whether a change occurred.Use historical information as the basis for judgment; if a psychological function is used frequently, it may change.
    "reason" : "xxxxx" //explanation for this judgment
    "main_weight" : "0.35", //weight of the new dominant function after change,must between 0.31-1.00. omit if no change
    "ori_main_weight" : "0.15", //Weight of the original dominant function after decrease, must between 0-0.30. omit if no change
}
"""

ref_content3 = """
##Final output in JSON format, following the example. Do not include any additional content##
{
    "judgment" : "yes", //only "yes" or "no" (in lowercase), indicating whether a change occurred.Use historical information as the basis for judgment; if a psychological function is used frequently, it may change.
    "reason" : "xxxxx" //explanation for this judgment
    "aux_weight" : "0.18", //weight of the new auxiliary function after change,must between 0.06-0.30. omit if no change
    "ori_aux_weight" : "0.05", //Weight of the original auxiliary function after decrease,must between 0-0.06. omit if no change
}
"""

def get_ref_content1(main : str, aux : str):
    pre = "##Final output in JSON format, following the example. Do not include any additional content##\n"
    judgment = "    \"judgment\" : \"yes\", //only \"yes\" or \"no\" (in lowercase), indicating whether the change occurred(reference psychological functions used in History).Use historical information as the basis for judgment; if a psychological function is used frequently, it may change.\n"
    main_weight = "     \"main_weight\" : \"0.40\", //weight of the new dominant function '" + aux + "' after change, *must between 0.31-1.00. omit if no change\n"
    aux_weight = "      \"aux_weight\" : \"0.18\", //weight of the new auxiliary function '" + main + "' after change, *must between 0.06-0.30. omit if no change\n"
    reason = "      \"reason\" : \"xxxxx\" //explanation for this judgment"
    ref_content1 = pre + "{" + judgment + reason + main_weight + aux_weight + "}"
    return ref_content1


def get_psyc_prompt(name, main_func, aux_func):
    miss_func = ','.join(ALL_FUNCTION_cle - {main_func, aux_func})

    psyc_prompt = "##Psychological Type Characteristics of " + name + "##\n**Current Personality Configuration**\n-1. Dominant Function:" \
              + main_func + ",highly differentiation, high weight" + "\n-2. Auxiliary Function:" + aux_func + ",general differentiation, medium weight" + "\n-3. Undifferentiated Function Pool: " + miss_func + ", in an unconscious state, with extremely low or zero weight\n"

    return psyc_prompt


def get_info_prompt(name : str):

    prompt1 = "**Based on Jungian cognitive functions theory, role-play as the personality described below " + name + \
             " to solve a series of problems in specific scenarios**\n\n##Basic Information##\nName:" + name

    prompt2 = "\n"

    with open('data/character.json', encoding='UTF-8') as file:
        all_character = json.load(file)
    character_info = all_character[name]

    for key in character_info:
        prompt2 += key + ":" + character_info[key] + "\n"

    info_prompt = prompt1 + prompt2 + "\n"

    return info_prompt


def get_prompt(scene : str, problem : str, name : str, main_func : str, aux_func : str):

    scene_prompt = '##Scene##\n' + scene
    user_prompt = 'Problem ' + ' : ' + problem

    sys_prompt = get_info_prompt(name) + test_prompt + get_psyc_prompt(name, main_func, aux_func) + Output_prompt + scene_prompt


    return sys_prompt, user_prompt


