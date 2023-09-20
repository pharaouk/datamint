
from datasets import load_dataset
import json
import jsonlines
from utils import openai_call

def cot_agent(input, output):
    prompt = f"""
    Given the following Instruction and Output, I want you to come up with a cohesive, comprehensive, consice well-packed, logical and correct reasoning chain of thought that you would go through to generate the correct output/answer. Please make sure to write it within a string with all the new lines. The chain of thought should be the numbered logical step by step thinking/thoughts/reasoning to arrive at the output:


    Instruction:
    "{input}"


    CHAIN OF THOUGHT: <>


    Output: 
    "{output}"

    CHAIN OF THOUGHT:     
    """
    response = openai_call(prompt, model="gpt-4-0314", max_tokens=500)
    return response



def main():
    with jsonlines.open('dfsample2.jsonl') as reader:

        with jsonlines.open('dfsample2_cot.jsonl', mode='w') as writer:

            for obj in reader:
                instruction = obj['instruction']
                inputObj = obj['input']
                output = obj['output']
                if inputObj is not None or "":
                    instruction += f"\n{inputObj}"
                    print(instruction)
                cot = cot_agent(instruction, output)

                obj['thoughts'] = cot

                writer.write(obj)

    print("Finished")


if __name__ == '__main__':
    main()
