# Flex Browser - AI Powered Web Browser

Flex is a modern, frameless browser with a built-in Gemini AI assistant.

## How to Run
1. Install Python 3.10+
2. Install dependencies:
   `pip install -r requirements.txt`
3. Set your Google API Key:
   (Windows): `set GEMINI_API_KEY=your_key_here`
   (Mac/Linux): `export GEMINI_API_KEY=your_key_here`
4. Run the browser:
   `python main.py`

## Technical Write-Up

- AI Model used in the project: I went with Google Gemini 2.0 Flash, in which I integrated that into Google Search tool.

- Why I Used this Model?
  Google Gemini, especially 2.0 Flash version is fast, has low latency which is definitely needed for seamless real-time    browsing experience. Implementing the google search tool means that the AI can actually get new information or live  data from the web than relying on traning data. 

- AI Integration features
  The Flex is a AI-Native browser, it has a built-in sidebar in the browser itself. To easily access the AI assistant instead of jumping to other tabs, the assistant can summarize any task, handle research and answer your queries with live search.

- Architecture and Other Components I used:

For my frontend, I used Python (version 3.13), PyQt6, QtWebEngine - Qt6 is a popular framwork in Python for building cross-platform desktop applications. PyQt6 allows you to create a framless window, handles complex user interactions for instance, moving the title bar or managing multiple browser tabs. 
QtWebEngine is designed to handle heavy websites like Google maps, YouTube and ensures at most performance and efficiency. It is ensures Security that is, it provides isolated rendering processes to make sure the web content is separate from the application's logic.

One of the challenges I faced is the UI freezing while waiting for a network response, in this case, I designed a sidebar that can be opened when the user clicks on it on the top right corner, this AI communicates with Gemini 2.0 Flash API asynchronously. 
The browser displays real-time data by using the google-genai SDK it looks into web through the model to provide factual information.

Finally, I incorporated 'markdown' library that is used to convert the AI text formats such as the code, lists and blocks of code into HTML. Once it is converted the HTML is then added to QTextEdit widget in which I applied custom CSS to make sure the AI's response matches the browser's theme.
