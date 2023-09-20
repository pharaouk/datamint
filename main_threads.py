
from datasets import load_dataset
import json
import jsonlines
from utils import openai_call
from concurrent.futures import ThreadPoolExecutor
from datasets import load_dataset
import json
import jsonlines
from utils import openai_call
import time

def cot_agent(input, output):
    for _ in range(3):  
        try:
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
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(2)  
    return None  

def main():
    with ThreadPoolExecutor(max_workers=5) as executor:
        with jsonlines.open('dfsample1.jsonl') as reader:
            with jsonlines.open('dfsample1_cot.jsonl', mode='a') as writer:
                futures = []
                for obj in reader:
                    instruction = obj['instruction']
                    inputObj = obj['input']
                    output = obj['output']
                    if inputObj is not None or "":
                        instruction += f"\n{inputObj}"
                        print(instruction)
                    future = executor.submit(cot_agent, instruction, output)
                    futures.append((future, obj))
                
                for future, obj in futures:
                    cot = future.result()  
                    if cot is not None: 
                        obj['thoughts'] = cot
                        writer.write(obj)

    print("Finished")



if __name__ == '__main__':
    main()
