# Welcome to the UMDearborn Web Tech AI Virtual Assistant! 🚀🤖

Hi there! 👋 We're thrilled to have you on board. This Virtual Assistant provides insightful feedback for your Web Tech assignments.

## Documentation 📚

- **User Interface**: 
  - Chainlit: [Chainlit Documentation](https://docs.chainlit.io) 

- **LLM Agent Framework**: 
  - Langchain: [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction) 

- **NLP Tool**: 
  - OpenAI API: [OpenAI API Documentation](https://platform.openai.com/docs/overview) 

## Operating System 💻

- **Ubuntu 22.04.3 LTS**: 
  - (GNU/Linux 5.15.133.1-microsoft-standard-WSL2 x86_64): [Ubuntu Install](https://ubuntu.com/download/desktop) 😊

- **Windows**: 
  - WSL 2: [WSL 2 Installation](https://ubuntu.com/wsl) 😊

## Requirements 🔗

### Ubuntu Packages 
To utilize this project, ensure the installation of the following packages:

#### Dependencies:

- `sudo apt install php==2:8.1+92ubuntu1 php-cli==2:8.1+92ubuntu1 php-fpm=2:8.1+92ubuntu1 php-json=2:8.1+92ubuntu1 php-common==2:92ubuntu1 php-mysql=2:8.1+92ubuntu1 php-zip=2:8.1+92ubuntu1 php-gd=2:8.1+92ubuntu1 php-mbstring=2:8.1+92ubuntu1 php-curl=2:8.1+92ubuntu1 php-xml=2:8.1+92ubuntu1 php-pear=1:1.10.12+submodules+notgz+20210212-1ubuntu3 php-bcmath=2:8.1+92ubuntu1 php-json=2:8.1+92ubuntu1`

- `sudo apt install php-codesniffer=3.6.2-1`

#### Optional:
- For Ubuntu users: `sudo python3 install.py`

#### Manual Installation:
1. Install listed ubuntu dependencies
2. In the root directory: `pip3 install -r requirements.txt`
3. Create a finetuned GPT 3.5-Turbo OpenAI model trained on the dataset in the Datasets folder for 16 epochs

## OpenAI API Key Setup 🔑

1. Create a `.env` file in the root directory of `src`.
2. Add `OPENAI_API_KEY="INSERT API KEY HERE"`.
3. Add `FINETUNED_FEEDBACK_MODEL="YOUR FINETUNED MODEL FOR WEB TECH FEEDBACK"`.

## Finetune Dataset Preparation 🔑

Prepare your finetuning data with this tool: [OpenAIFineTuningDataSoftware](https://github.com/BinaryBills/OpenAIFineTuningDataSoftware)

## Build Project

To build the project, execute: `chainlit run main.py`
