# Deobfuscate Android App

LLM tool to deobfuscate android app code and also find any potential vulnerabilities. Uses Google's Gemini public API.

## Description

Input - Takes decompiled code directory as an input.

Output -

1) a JSON file will be created with name "vuln_report", listing security risk and its impact.

2) Deobfuscates the files for easier readability and save it in package directory structure for manual reviews.

## Installation

### 1. Clone the repo

### 2. Install dependencies 

pip3 install -r requirements.txt

### 3. Decompile APK

You can use jadx https://github.com/skylot/jadx for that.
It will create a resources and sources directory. Sources directory is where the decompiled .java files sit.

jadx test.apk

### 4. Run the script 

a. EXPORT API_KEY= "Your Gemini API Key" 

You can get the API key from ai.google.dev

b. python3 script.py --llm_model gemini-1.5-flash -output_dir /tmp/ver/ -source_dir "input_dir1/ input_dir2/" -thread_size 10

where, 
-llm_model is the LLM model to use, Currently only Google's Gemini is supported.
-output is the output directory you want to save generated files.
-source_dir is the source directory for the decompiled code
-save_code (optional) set as True will deobfuscate the code and save in the output directory provided, otherwise only vuln_report file will be generated.
-thread (optional) for parallel execution of multiple files. Default 1.

**Important - Don't send the entire package at once which would contain libraries etc. Otherwise It may take forever to scan. Send the specific directories as input which contains app specific code.**

## Contributing

See [`CONTRIBUTING.md`](docs/CONTRIBUTING.md) for details.

## License

Apache 2.0; see [`LICENSE`](LICENSE) for details.

## Disclaimer

This project is not an official Google project. It is not supported by
Google and Google specifically disclaims all warranties as to its quality,
merchantability, or fitness for a particular purpose. 
This is an experimental project and the owner of this project shall not be held liable for any actions performed using this tool. It is the sole responsibility of the end-user.
Also, please review the TOS for Gemini API before using the tool. https://ai.google.dev/gemini-api/terms
