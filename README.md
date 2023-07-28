# LegalLLaMa 🦙 (*WORK IN PROGRESS*)
LegalLLaMa: Your friendly neighborhood lawyer llama, turning legal jargon into a piece of cake!

Legal LLaMa is a chatbot developed to provide summaries of U.S. legislative bills based on user queries. It's built using the Hugging Face's Transformers library, and is hosted using Streamlit on Hugging Face Spaces.

You can interact with the live demo of Legal LLaMa on Hugging Face Spaces [here](https://huggingface.co/spaces/LLaMaWhisperer/legalLLaMa).

The chatbot uses a frame-based dialog management system to handle conversations, and leverages the ProPublica and Congress APIs to fetch information about legislative bills. The summaries of bills are generated using a state-of-the-art text summarization model.

## Features 🎁

- Frame-based dialog management
- Intent recognition and slot filling
- Real-time interaction with users
- Bill retrieval using ProPublica and Congress APIs
- Bill summarization using Transformer models

## Future Work 💡

Legal LLaMa is still a work in progress, and there are plans to make it even more useful and user-friendly. Here are some of the planned improvements:

- Enhance intent recognition and slot filling using Natural Language Understanding (NLU) models
- Expand the chatbot's capabilities to handle more tasks, such as providing summaries of recent bills by a particular congressman
- Train a custom summarization model specifically for legislative texts

## Getting Started 🚀

To get the project running on your local machine, follow these steps:

1. Clone the repository:
```commandline
git clone https://github.com/YuvrajSharma9981/LegalLLaMa.git
```
2. Install the required packages:
```commandline
pip install -r requirements.txt
```

3. Run the Streamlit app:
```commandline
streamlit run app.py
```

Please note that you will need to obtain API keys from ProPublica and Congress to access their APIs.

## Contributing 🤝

Contributions to improve Legal LLaMa are welcomed. Feel free to submit a pull request or create an issue for any bugs, feature requests, or questions about the project.

## License 📄

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.
