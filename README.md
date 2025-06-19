# InkSpire – AI Story Generator

**InkSpire** is a lightweight AI-powered storytelling app built with [Streamlit](https://streamlit.io/) and [Hugging Face Transformers](https://huggingface.co/docs/transformers).  
Enter a prompt, and InkSpire will craft a vivid, imaginative short story using the TinyLlama language model.

---

## Features

- ✍️ Prompt-based story generation  
- 🪄 AI-powered story refinement  
- 🌑 Dark mode with neon styling  
- 🧠 Based on `TinyLlama-1.1B-Chat-v1.0`  
- 💡 Fully local and free to run  

---

## Project Structure

inkspire-story-generator/
- ├── app.py # Streamlit app
- ├── requirements.txt # Python dependencies
- └── README.md # This file

---

##  Installation

### 1. Clone the Repository

git clone https://github.com/your-username/inkspire-story-generator.git
cd inkspire-story-generator

### 2. (Optional) Create a Virtual Environment
python -m venv venv
source venv/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt
Run the App with: streamlit run app.py
Visit http://localhost:8501 in your browser to use the app.

---

## Model Information
This app uses the TinyLlama/TinyLlama-1.1B-Chat-v1.0 model via the Hugging Face transformers library.
The model (~2GB) is downloaded on first use. Please ensure you're connected to the internet.

---

## Example Prompts
"A robot discovers human emotions."

"A time traveler visits ancient Egypt."

"A child finds a portal to a secret world."

---

## Troubleshooting
- Model won’t load? Make sure you're online the first time you run the app.

- Slow performance? This model runs best with a GPU. CPU will work, just slower.

- Upgrade tools (if needed): pip install --upgrade pip setuptools

---

## Credits
- TinyLlama Model
- Streamlit
- Transformers by Hugging Face
