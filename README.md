# Deobfuscate Android App

LLM tool to find any potential security vulnerabilities in android apps and deobfuscate android app code. Uses Google's Gemini public API. 

Android apps generally use Proguard for obfuscating the app and reversing app can be hard with meaning less variable and function names. LLMs seems to do a good job in understanding the context of the code and renaming variables, functions, adding comments etc (to certain extent but embrace the unpredictibility of it too).

## Description

Input - Takes decompiled code directory as an input.

Output -

1) a JSON file will be created with name "vuln_report", listing security risk and its impact in the provided output directory.

2) Deobfuscates each file for easier readability and save it in package directory structure for manual reviews. Also, labels any security issues seen in the generated code with #SECURITY-ISSUE. (Only when save_code parameter is set to True, read below in run the script section)

## Installation

### 1. Clone the repo

### 2. Install dependencies 

pip3 install -r requirements.txt

### 3. Decompile APK

Get the APK of the intended app. And You can use jadx [https://github.com/skylot/jadx](https://github.com/skylot/jadx) to decompile.
It will create a "resources" and "sources" directory. "Sources" directory is where the decompiled .java files sit.

`jadx androidapp.apk`

### 4. Run the script 

a. `EXPORT API_KEY= "Your Gemini API Key"`

You can get the API key from [ai.google.dev](https://ai.google.dev/)

b. `python3 script.py --llm_model gemini-1.5-flash -output_dir /tmp/ver/ -source_dir "input_dir1/ input_dir2/"`

where, 

-llm_model is the LLM model to use, Currently only Google's Gemini is supported. You can get the model variants from here. https://ai.google.dev/gemini-api/docs/models/gemini#model-variations

-output_dir is the output directory you want to save generated files.

-source_dir is the source directory for the decompiled code. You can send more than one directory separated by space as above.

-save_code (*optional*) Default is false. if set as True, it will deobfuscate the code and save in the output directory provided, otherwise only vuln_report file will be generated.

**Important - Don't send the entire package at once which would contain libraries etc. Otherwise It may take forever to scan. Send the specific directories as input which contains app specific code. For example - if package directory looks like com/google/android/yourapp, send com/google/android/yourapp/receivers/**

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
