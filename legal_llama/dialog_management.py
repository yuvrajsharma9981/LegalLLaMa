from legal_llama.bill_retrieval import BillRetriever
from legal_llama.summarizer import BillSummarizer


class DialogManager:
    """
    A class for managing conversation frames.
    """

    def __init__(self):
        """
        Initialize the DialogManager with predefined frames.
        """
        self.frames = {
            "bill_summarization": {
                "intent": "bill_summarization",
                "bill_query": None,
            },
            # Add more frames here as needed
        }
        self.current_frame = None

    def set_frame(self, intent, slot):
        """
        Set the current frame based on the recognized intent and provided slot value.

        Parameters:
            intent (str): The recognized intent.
            slot (str): The value of the slot provided by the user.
        """
        # Update this function in the future to check for intent.
        self.current_frame = self.frames.get(intent, {}).copy()
        if self.current_frame is not None:
            self.update_slot('bill_query', slot)
        else:
            print(f"Unrecognized intent: {intent}")

    def update_slot(self, slot_name, slot_value):
        """
        Update the value of a slot in the current frame.

        Parameters:
            slot_name (str): The name of the slot.
            slot_value (str): The new value of the slot.
        """
        if self.current_frame is not None and slot_name in self.current_frame:
            # If the current frame is set and the slot name exists in the frame, update the slot value
            self.current_frame[slot_name] = slot_value
        else:
            print(f"Cannot update slot '{slot_name}' - no current frame or slot does not exist")

    def generate_response(self):
        """
        Generate a response based on the current frame.

        Returns:
            str: The generated response.
        """
        # Check if a frame has been set
        if self.current_frame is None:
            print("No frame has been set")
            return None

        frame = self.current_frame
        if frame['intent'] == 'bill_summarization':
            # Extract the bill's text
            bill_retriever = BillRetriever()
            bill_text = bill_retriever.get_bill_by_query(frame['bill_query'])
            if bill_text is None:
                print("Unable to retrieve bill text")
                return None

            # Summarize the bill's text
            summarizer = BillSummarizer()
            summary = summarizer.summarize(bill_text)
            if summary is None:
                print("Unable to summarize bill text")
                return None

            return summary
        else:
            print(f"Unrecognized frame intent: {frame['intent']}")
            return None
