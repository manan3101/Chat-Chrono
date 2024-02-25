# Chat Chrono

Chat Chrono is a Python-based project utilizing modules such as Streamlit and Twilio. It offers two main features: WhatsApp chat scheduling and chat analysis.

## Benefits of Chat Chrono:

1. **Efficient Communication:** Schedule messages in advance, ensuring timely communication without the need for constant manual intervention.

2. **Insightful Analysis:** Gain insights into chat patterns and interactions through the chat analysis feature, allowing users to better understand communication dynamics.

3. **User-Friendly Interface:** The project provides a streamlined interface through Streamlit, making it easy for users to navigate and utilize its functionalities.

## Setup and Installation:

1. Clone the repository:
   ```bash
   git clone https://github.com/manan3101/Chat-Chrono.git
2. Install necessary packages and modules:
   ```bash
   pip install "module_name"
4. Run the application:
   ```bash
   streamlit run app.py

# Chat Scheduler

To use the chat scheduler feature:

1. **Login to Twilio** and register your WhatsApp number.
2. **Obtain** your Account SID, Authentication Token, and Message Service SID, and update them in the `helper.py` file.
3. Once configured, users can **schedule messages** by providing the receiver's number, message content, date, and time.

# Chat Analyzer

To utilize the chat analysis feature:

1. **Import** a group chat `.txt` file from WhatsApp and upload it to the analyzer.
2. **Select** the person's name from the chat.
3. Click **"Start"** to initiate the analysis process and obtain necessary details.

# Project Structure

- **app.py:** Contains the main frontend components of the application.
- **helper.py:** Includes functions for different analysis and scheduling operations.
- **processor.py:** Contains functions to preprocess the `.txt` file of the chat for analysis.

`Check the output folder to get a glimpse of the project.`
