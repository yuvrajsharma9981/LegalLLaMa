from legal_llama.dialog_management import DialogManager
import streamlit as st


class ChatBotInterface:
    def __init__(self):
        """Initializes the chatbot interface, sets the page title, and initializes the DialogManager."""
        # Set up Streamlit page configuration
        st.set_page_config(page_title="Legal LLaMa 🦙")
        st.title("Legal LLaMa 🦙")

        # Define roles
        self.user = "user"
        self.llama = "Assistant"

        # Initialize the DialogManager for managing conversations
        self.dialog_manager = DialogManager()

        # Initialize chat history in the session state if it doesn't exist
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Start the conversation with a greeting message
        first_message = ("Hello there! I'm Legal LLaMa, your friendly guide to the complex world of U.S. legislation."
                         "\n\nThink of me as a law student who is always eager to learn and share knowledge. Right now,"
                         "my skills are a bit limited, but I can certainly help you understand the gist of the latest "
                         "bills proposed in the U.S. Congress. You just have to provide me with a topic - could be "
                         "climate change, prison reform, healthcare, you name it! I'll then fetch the latest related "
                         "bill and serve you up a digestible summary.\n\nRemember, being a law student (and a LLaMa, no"
                         "less!) is tough, so if I miss a step, bear with me. I promise to get better with every "
                         "interaction. So, what topic intrigues you today?")
        self.display_message(self.llama, first_message)

    @staticmethod
    def display_chat_history():
        """Displays the chat history stored in the session state."""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    @staticmethod
    def add_message_to_history(role, chat):
        """Adds a message to the chat history in the session state."""
        st.session_state.messages.append({"role": role, "content": chat})

    @staticmethod
    def display_message(role, text):
        """Displays a chat message in the chat interface."""
        st.chat_message(role).markdown(text)

    def handle_user_input(self, user_input):
        """Handles user input by recognizing the intent and updating the dialog frame."""
        # In future, use the IntentRecognizer to check for intent
        intent = "bill_summarization"

        # Update the dialog frame based on the recognized intent
        self.dialog_manager.set_frame(intent, user_input)

    def continue_conversation(self):
        """Continues the conversation by displaying chat history, handling user input, and generating responses."""
        # Display chat history
        self.display_chat_history()

        # Handle user input
        if prompt := st.chat_input("Ask your questions here!"):
            # Display user message
            self.display_message(self.user, prompt)

            # Add user message to chat history
            self.add_message_to_history(self.user, prompt)

            # Handle user input (recognize intent and update frame)
            self.handle_user_input(prompt)

            with st.spinner('Processing your request...'):
                # Generate response based on the current dialog frame
                response = self.dialog_manager.generate_response()

            # Display assistant response
            self.display_message(self.llama, response)

            # Add assistant response to chat history
            self.add_message_to_history(self.llama, response)
