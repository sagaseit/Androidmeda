import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from absl import app,flags
from typing import Sequence
import os
import traceback
import sys
import json
import threading
import asyncio
from collections import defaultdict
from google.api_core.exceptions import ResourceExhausted

_LLM_MODEL = flags.DEFINE_string(
    'llm_model', None, 'LLM Model to use')
_OUTPUT_DIR = flags.DEFINE_string(
    'output_dir', None, 'the output directory to save the report and source code (if flag provided)')
_SOURCE_DIR = flags.DEFINE_spaceseplist('source_dir', [], 'List of Directory of the Source code')
_SAVE_CODE = flags.DEFINE_boolean(
    'save_code', False, 'If provided we will save the deobfuscated code')
_THREAD_SIZE = flags.DEFINE_integer(
    'thread_size',1, 'No. of threads to use for concurrent requests to Gemini')

async def send_code_to_gemini(client,files_data):
    
    retry_delay = 2  # Initial retry delay in seconds
    max_retries = 5  # Maximum number of retries

    for attempt in range(max_retries):
        try:
            response_template =  await client.generate_content_async([files_data,],
            safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
            )
            return response_template.text
        except ResourceExhausted as e:
            print(f"Rate limit error: {e}")
            print(f"Retrying in {retry_delay} seconds (attempt {attempt + 1}/{max_retries})...")
            await asyncio.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
        except Exception as e:
            print(f"Gemini API Error: {e}")
            traceback.print_exc()
            sys.exit()

output_data_lock = threading.Lock()
output_data = defaultdict(list)

def process_response(response_text,file_path,output_dir):
    with output_data_lock:
        #Removing JSON block from LLM response to process
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        data = json.loads(response_text)

        # 1. Read the code between Java code block
        java_code = data['Code']
            
        #Saves Deobfuscated Source code, if flag is provided
        if (_SAVE_CODE.value):
            create_unobfuscated_code_files(output_dir,file_path,java_code)

        # 2. Read the Security Vulnerabilities section
        vulnerabilities = data['Vulnerabilities']
        
        #Only process files where vulns have been identified
        if len(vulnerabilities) > 0:
            output_data[file_path].extend(vulnerabilities)

def create_unobfuscated_code_files(code_output_directory, file_path, java_code):
    
    # Extract directory path from file path
    directory = os.path.join(code_output_directory,os.path.dirname(file_path))
    # Create directories recursively, if they don't exist
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    # Create the file
    full_file_path = os.path.join(code_output_directory, file_path)
    with open(full_file_path, 'a+',encoding="utf-8") as output_file:
        output_file.write(java_code)

    print(f"Created file: {full_file_path}")

def find_java_files(directory):
    """
    Recursively searches for Java files within the specified directory.

    Args:
        directory: The directory to start the search from.

    Returns:
        A list of paths to all found Java files.
    """
    java_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root,file))

    return java_files

def read_file_content(file_path):
    """Reads the content of a file."""
    with open(file_path, 'r',encoding="utf-8") as file:
      content = file.read()+"\n\n"
    return content

async def process_code_files(semaphore, file_path):
    
    async with semaphore:
        try:
            client = genai.GenerativeModel(_LLM_MODEL.value,
                                           system_instruction=prompt)
            print(f"Processing file {file_path} with Semaphore : {semaphore._value}")
            
            #Read the decompiled code file
            content = read_file_content(file_path)

            #Send Input to Gemini
            response =  await send_code_to_gemini(client,content)

            # Process the response as needed and create a vuln file
            print(response)
            process_response(response,file_path,_OUTPUT_DIR.value)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            traceback.print_exc()
        finally:
            print(f"File processing completed {file_path}.")

def write_vuln_output(output_vuln_dir):
    output_json = {}
    
    for file_name, vulnerabilities in output_data.items():
        output_json[file_name] = vulnerabilities
    
    with open(output_vuln_dir, "w+", encoding="utf-8") as output_file:
        json.dump(output_json, output_file, indent=4)
    

async def main(argv: Sequence[str]) -> None:
    flags.FLAGS(argv)
    if _LLM_MODEL.value is None or _OUTPUT_DIR.value is None or  len(_SOURCE_DIR.value) == 0:
        raise app.UsageError(
            f'Usage: {argv[0]} -llm_model=<LLM Model to use> -output_dir=<output directory> -source_dir=<source directory>'
        )
    if os.environ['API_KEY'] is None:
        raise app.UsageError(f'Usage: Set api_key in the environ variable')

    genai.configure(api_key=os.environ['API_KEY'])

    semaphore = asyncio.Semaphore(_THREAD_SIZE.value)
    
    global prompt

    #Find all java files within given directories, comma separated directories are accepted.
    code_files = []
    for source_dirs in _SOURCE_DIR.value:
        code_files = code_files + find_java_files(source_dirs)
        print(code_files)

    #Read the prompt
    with open("prompt.txt", 'r',encoding="utf-8") as file:
      prompt = file.read()

    tasks = []
    
    #Parallel processing of files with Gemini
    if (len(code_files) > 0):
        for file_path in code_files:
            task = asyncio.create_task(
            process_code_files(semaphore, file_path)
            )
            tasks.append(task)

        await asyncio.gather(*tasks)

        #Save the vulns
        if (len(output_data.items()) > 0):
            output_vuln_path = os.path.join(_OUTPUT_DIR.value,"vuln_report")
            write_vuln_output(output_vuln_path)
            print("Vulnerability report created at " + output_vuln_path)
        else:
            print("No Vulnerability found to report")
    else:
        print("No decompiled java files found")

if __name__ == '__main__':
    asyncio.run(main(sys.argv))
