import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, set_seed

st.set_page_config(page_title="InkSpire - Story Generator", layout="centered")

# --- Load Model ---
@st.cache_resource
def load_generator():
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return pipeline('text-generation', model=model, tokenizer=tokenizer)

generator = load_generator()

# --- Styling ---
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: #39ff14;
        }
        .title-line {
            border-bottom: 2px solid #39ff14;
            width: 100%;
            margin: auto;
            margin-bottom: 20px;
        }
        .block-container {
            padding-top: 2rem;
        }
        div.stButton > button:first-child {
            background-color: #163216; /* very faint green */
            color: #39ff14;
            font-weight: bold;
            border: none;
            border-radius: 6px;
            padding: 0.5em 1em;
            transition: background-color 0.3s ease;
            min-width: 120px;
        }

        div.stButton > button:first-child:hover {
            background-color: #2ecc10;
            color: black;
        }

        div.stButton > button:first-child:active {
            background-color: #2ecc10 !important;
            color: black !important;
            box-shadow: none !important;
            outline: none !important;
            border: none !important;
            
        .small-warning {
            font-size: 0.85rem;
            color: #aaaaaa;
            margin-top: -10px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("""
    <h1 style='text-align: center; color: #39ff14;'>InkSpire</h1>
    <div class='title-line'></div>
    <p style='text-align: center;'>Craft AI-generated stories from just a prompt</p>
""", unsafe_allow_html=True)

# Initialize session state variables for story and prompt if not present
if "story_text" not in st.session_state:
    st.session_state.story_text = ""
if "prompt" not in st.session_state:
    st.session_state.prompt = ""
if "max_words" not in st.session_state:
    st.session_state.max_words = 150

# --- Input ---
example1 = "A time traveler visits ancient Egypt."
example2 = "A robot discovers human emotions."

st.markdown("<div style='width: 70%; margin: auto;'>", unsafe_allow_html=True)
prompt_input = st.text_area("Write a prompt:", height=100, placeholder="e.g. A lost explorer finds a hidden jungle city...", value=st.session_state.prompt)
st.caption(f"Examples: \"{example1}\" or \"{example2}\"")

max_words_input = st.number_input("Maximum number of words (approximate):", min_value=50, max_value=1000, value=st.session_state.max_words, step=50)

generate_btn = st.button("Generate Story")

st.markdown("</div>", unsafe_allow_html=True)

# --- Generate Story Function ---
def generate_story(prompt, max_words):
    set_seed(42)
    formatted_prompt = f"""
Write a fictional short story based on the idea below. The story should be vivid, adventurous, and set in a mysterious jungle. It should have a clear beginning, middle, and end, and include at least one named character.

Prompt: {prompt}

Story:"""

    max_new_tokens = int(max_words * 1.3)
    result = generator(
        formatted_prompt,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.8,
        top_k=40,
        top_p=0.92,
        repetition_penalty=1.4,
        no_repeat_ngram_size=3,
        eos_token_id=generator.tokenizer.eos_token_id,
        num_return_sequences=1
    )[0]['generated_text']

    story_start = result.find("Story:")
    story_text = result[story_start + len("Story:"):].strip() if story_start != -1 else result.strip()
    last_period = story_text.rfind('.')
    if last_period != -1:
        story_text = story_text[:last_period+1]
    return story_text

# --- Refine Story Function ---
def refine_story(existing_story, max_words):
    set_seed(42)
    refine_prompt = f"""
You are a professional fiction editor. Take the story below and rewrite it to improve clarity, pacing, and flow. Keep the core plot and characters the same, but enhance the writing with stronger descriptions, smoother transitions, and better narrative style.


Story:
{existing_story}

Refined Story:"""

    max_new_tokens = int(max_words * 1.3)
    result = generator(
        refine_prompt,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=0.7,
        top_k=30,
        top_p=0.9,
        repetition_penalty=1.3,
        no_repeat_ngram_size=3,
        eos_token_id=generator.tokenizer.eos_token_id,
        num_return_sequences=1
    )[0]['generated_text']

    refined_start = result.find("Refined Story:")
    refined_text = result[refined_start + len("Refined Story:"):].strip() if refined_start != -1 else result.strip()
    last_period = refined_text.rfind('.')
    if last_period != -1:
        refined_text = refined_text[:last_period+1]
    return refined_text

# --- Main Logic ---

if generate_btn:
    if prompt_input.strip() == "":
        st.warning("Please enter a prompt to generate a story.")
    else:
        with st.spinner("Generating your story..."):
            story = generate_story(prompt_input, max_words_input)
            st.session_state.story_text = story
            st.session_state.prompt = prompt_input
            st.session_state.max_words = max_words_input

if st.session_state.story_text:
    st.markdown(f"""
        <h3 style='color: #39ff14;'>Your Story</h3>
        <p><strong>Prompt:</strong> {st.session_state.prompt}</p>
        <div style="white-space: pre-wrap; background-color: #1a1a1a; color: #39ff14; padding: 15px; border-radius: 8px; font-size: 16px; min-height: 300px;">
            {st.session_state.story_text}
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    refine_btn = st.button("Refine Story", key="refine_btn")

    if "refine_done" not in st.session_state:
        st.session_state.refine_done = False


    if refine_btn:
        with st.spinner("Refining your story..."):
            refined = refine_story(st.session_state.story_text, st.session_state.max_words)
            st.session_state.story_text = refined
            st.session_state.refine_done = True  # Set the flag

    
    if st.session_state.refine_done:
        st.success("Story refined! Click below to refresh and view it.")
        if st.button("Refresh View", key="refresh_btn"):
            st.session_state.refine_done = False 
