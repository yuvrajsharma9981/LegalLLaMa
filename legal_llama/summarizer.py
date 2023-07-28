from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import streamlit as st


@st.cache_resource
def load_model():
    tokenizers = AutoTokenizer.from_pretrained("nsi319/legal-led-base-16384")
    model = AutoModelForSeq2SeqLM.from_pretrained("nsi319/legal-led-base-16384")
    return tokenizers, model


class BillSummarizer:
    def __init__(self):
        """
        Initialize a BillSummarizer, which uses the Hugging Face transformers library to summarize bills.
        """
        try:
            self.tokenizer, self.model = load_model()
        except Exception as e:
            print(f"Error initializing summarizer pipeline: {e}")

    def summarize(self, bill_text):
        """
        Summarize a bill's text using the summarization pipeline.

        Parameters:
            bill_text (str): The text of the bill to be summarized.

        Returns:
            str: The summarized text.
        """
        try:
            input_tokenized = self.tokenizer.encode(bill_text, return_tensors='pt',
                                                    padding="max_length",
                                                    pad_to_max_length=True,
                                                    max_length=6144,
                                                    truncation=True)

            summary_ids = self.model.generate(input_tokenized,
                                              num_beams=4,
                                              no_repeat_ngram_size=3,
                                              length_penalty=2,
                                              min_length=350,
                                              max_length=500)

            summary = [self.tokenizer.decode(g,
                                             skip_special_tokens=True,
                                             clean_up_tokenization_spaces=False)
                       for g in summary_ids][0]

            return summary
        except Exception as e:
            print(f"Error summarizing text: {e}")
            return "Sorry, I couldn't summarize this bill. Please try again."
