# Deobfuscate Android App

LLM tool to find any potential security vulnerabilities in android apps and deobfuscate android app code. Supports Ollama local models, and Public APIs for Google's Gemini Model, Anthropic's Model and OpenAI's Model.

Android apps generally use Proguard for obfuscating the app and reversing app can be hard with meaning less variable and function names. LLMs seems to do a good job in understanding the context of the code and renaming variables, functions, adding comments etc (to certain extent but embrace the unpredictibility of it too).

## Description

Input - Takes decompiled code directory as an input.

Output -

1) a JSON file will be created with name "vuln_report", listing security risk and its impact in the provided output directory.

2) Deobfuscates each file for easier readability and save it in package directory structure for manual reviews. Also, labels any security issues seen in the generated code with #SECURITY-ISSUE. (Only when save_code parameter is set to True, read below in run the script section)

## Installation

### 1. Clone the repo

git clone [https://github.com/In3tinct/Deobfuscate-android-app.git](https://github.com/In3tinct/Deobfuscate-android-app.git)

### 2. Install dependencies 

pip3 install -r requirements.txt

### 3. Decompile APK

Get the APK of the intended app. And You can use jadx [https://github.com/skylot/jadx](https://github.com/skylot/jadx) to decompile.
It will create a "resources" and "sources" directory. "Sources" directory is where the decompiled .java files sit.

`jadx androidapp.apk`

### 4. Run the script 

**a. Using Google/Anthropic/OpenAI LLM Models.**

`EXPORT API_KEY= "Your API Key"`

You can get the API key for Google [gemini](https://ai.google.dev/), OpenAI [chatgpt](https://platform.openai.com/settings/organization/api-keys), Anthropic [claude](https://console.anthropic.com/settings/keys)

To Run script, 

Gemini - `python3 androidmeda.py --llm_provider google --llm_model gemini-1.5-flash -output_dir /tmp/ver/ -source_dir "input_dir1/ input_dir2/"`

ChatGPT - `python3 androidmeda.py --llm_provider openai --llm_model gpt-4.1 -output_dir /tmp/ver/ -source_dir "input_dir1/ input_dir2/"`

**OR**

**b. Using Ollama open source models to run locally.**

Follow steps here to download and run the model locally [github.com/ollama/ollama](https://github.com/ollama/ollama) 

To Run script, 

`python3 androidmeda.py --llm_provider ollama --llm_model llama3.2 -output_dir /tmp/ver/ -source_dir "input_dir1/ input_dir2/"`

**Parameters -** 

*-llm_provider* is the LLM provider of the model. e.g. google, anthropic, openaI, ollama 

*-llm_model* is the LLM model to use, Gemini, Claude, ChatGPT are supported. You can get the model variants from here. 

[google](https://ai.google.dev/gemini-api/docs/models/gemini#model-variations)

[openai](https://docs.anthropic.com/en/docs/about-claude/models/overview#model-names)

[anthropic](https://platform.openai.com/docs/models/)

*-output_dir* is the output directory you want to save generated files.

*-source_dir* is the source directory for the decompiled code. You can send more than one directory separated by space as above.

*-save_code* (optional) Default is false. if set as True, it will deobfuscate the code and save in the output directory provided, otherwise only vuln_report file will be generated.

**Important - Don't send the entire package at once which would contain libraries etc. Otherwise It may take forever to scan. Send the specific directories as input which contains app specific code. For example - if package directory looks like com/google/android/yourapp, send com/google/android/yourapp/receivers/**

## Demo

Decompiled code (Obfuscated)

![Screenshot 2024-12-06 at 10 01 19 AM](https://github.com/user-attachments/assets/37cd1454-6187-4027-8b34-1546fc9921b9)

Decompiled code (After processing with LLM)

![Screenshot 2024-12-06 at 9 59 14 AM](https://github.com/user-attachments/assets/a9c8d34d-3a24-4f64-819a-b908a8dc815f)

Security Issues identified by LLM

![Screenshot 2024-12-06 at 10 20 46 AM](https://github.com/user-attachments/assets/bba67dd9-69e8-4323-b696-203a232a33cd)

## Citation
Please cite, If you use this software in your Research papers, articles etc.

```
@software{Agrawal_Deobfuscate-android-app_Android_app_2024,
author = {Agrawal, Vaibhav},
month = nov,
title = {{Deobfuscate-android-app: Android app Vulnerability Scanner and Deobfuscator using LLM}},
url = {https://github.com/In3tinct/deobfuscate-android-app},
version = {1.0.0},
year = {2024}
}
```

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
