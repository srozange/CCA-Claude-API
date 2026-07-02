#!/usr/bin/env python3
from anthropic import Anthropic
from statistics import mean
import json, re, ast

def validate_json(text):
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0

def validate_python(text):
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0

def validate_regex(text):
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, system=None, temperature=1.0, stop_sequences=[]):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature
    }
    if system:
        params["system"] = system
    if stop_sequences:
        params["stop_sequences"] = stop_sequences
    
    response = client.messages.create(**params)
    return response.content[0].text

def generate_dataset():
    prompt = """
Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects, each representing task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
  {
    "task": "Description of task",
    "format": "The task format : python, json or regex"
    "solution_criteria": "Solution criteria for the task. Example : Must include runtime, memory size, timeout and basic structure for AWS Lambda configuration."
  },
  ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
* Focus on tasks that do not require writing much code
* Respond only with Python, JSON, or a plain Regex
* Do not add any comments or commentary or explanation

Please generate 3 objects.
"""

    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```json")
    text = chat(messages, stop_sequences=["```"])
    return json.loads(text)

def run_prompt(test_case):
    """Merges the prompt and test case input, then returns the result"""
    prompt = f"""
Please solve the following task with output format as { test_case["format"] }:

{test_case["task"]}
"""
    
    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```code")
    output = chat(messages, stop_sequences=["```"])
    return output

def grade_by_model(test_case, output):
    eval_prompt = """
    You are an expert code reviewer. Evaluate this AI-generated solution.
    
    Task: {task}
    Output: {output}
    Solution criteria : {solution_criteria}
    
    Provide your evaluation as a structured JSON object with:
    - "strengths": An array of 1-3 key strengths
    - "weaknesses": An array of 1-3 key areas for improvement  
    - "reasoning": A concise explanation of your assessment
    - "score": A number between 1-10
    """.format(task=test_case['task'], output=output, solution_criteria=test_case['solution_criteria'])

    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")
    
    eval_text = chat(messages, stop_sequences=["```"])
    return json.loads(eval_text)

def grade_syntax(response, test_case):
    format = test_case["format"]
    if format == "json":
        return validate_json(response)
    elif format == "python":
        return validate_python(response)
    else:
        return validate_regex(response)

def run_test_case(test_case):
    """Calls run_prompt, then grades the result"""
    output = run_prompt(test_case)
    model_grade = grade_by_model(test_case, output)
    model_score = model_grade["score"]
    syntax_score = grade_syntax(output, test_case)
    print(f"output : { output } - format : { test_case["format"] } - syntax score : { syntax_score }")
    score = (model_score + syntax_score) / 2

    return {
        "output": output,
        "test_case": test_case,
        "score": score
    }

def run_eval(dataset):
    results = []
    
    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)
    
    average_score = mean([result["score"] for result in results])
    print(f"Average score: {average_score}")
    
    return results

client = Anthropic()
model = "claude-haiku-4-5"

print("Choisissez une démo :")
print("  1. generate data set")
print("  2. evaluation")
choice = input("Votre choix (1/2/3) : ").strip()

if choice == "1":
    dataset = generate_dataset()
    print(dataset)
    with open('dataset.json', 'w') as f:
        json.dump(dataset, f, indent=2)

if choice == "2":
    with open("dataset.json", "r") as f:
        dataset = json.load(f)

    results = run_eval(dataset)
    print(json.dumps(results, indent=2))