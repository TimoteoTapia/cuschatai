# gradio.py
import gradio as gr
from model import main

# Initialize the model and the environment by calling the main function
query_engine = main()  # This will set up everything you need


# Function that processes user queries
def chatbot(query):
    # Use the query_engine to get the response for the query
    response = query_engine.query(
        query
    )  # Assuming query_engine has a method `.query()`
    return response


# Create the Gradio interface
iface = gr.Interface(
    fn=chatbot,  # Function to be executed when the query is received
    inputs=gr.Textbox(label="Ask me anything"),  # Textbox for the user's question
    outputs=gr.Textbox(label="Response"),  # Textbox for the response
    live=True,  # If you want it to be live (real-time)
)

# Launch the interface
iface.launch()

# Run the Gradio interface
