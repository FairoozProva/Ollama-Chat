import json
import requests
import streamlit as st

BASE_URL = "http://localhost:11434"
CHAT_URL = f"{BASE_URL}/api/chat"
TAGS_URL = f"{BASE_URL}/api/tags"

st.set_page_config(page_title="Local LLM Chat", page_icon="🤖")
st.title("🤖 Local LLM Chat (Ollama)")


def get_models():
    try:
        r = requests.get(TAGS_URL, timeout=5)
        r.raise_for_status()
        return [m["name"] for m in r.json()["models"]]
    except Exception:
        return []


if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Settings")

    models = get_models()
    if models:
        model = st.selectbox("Model", models)
    else:
        st.warning("No models found. Is Ollama running?")
        model = st.text_input("Model name", value="llama3.2")

    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)

    if st.button("🔄 Reset conversation"):
        st.session_state.messages = []
        st.rerun()

    chat_text = "\n\n".join(
        f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages
    )
    st.download_button(
        "💾 Download chat",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain",
        disabled=not st.session_state.messages,
    )

    st.header("Conversation history")
    user_msgs = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
    if user_msgs:
        for i, q in enumerate(user_msgs, 1):
            st.write(f"{i}. {q[:50]}{'...' if len(q) > 50 else ''}")
    else:
        st.caption("No messages yet.")

# ---------------- Chat area ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        answer = ""
        payload = {
            "model": model,
            "messages": st.session_state.messages,
            "stream": True,
            "options": {"temperature": temperature},
        }
        try:
            with requests.post(CHAT_URL, json=payload, stream=True, timeout=300) as r:
                r.raise_for_status()
                for line in r.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        answer += chunk.get("message", {}).get("content", "")
                        placeholder.markdown(answer + "▌")
            placeholder.markdown(answer)
        except requests.exceptions.ConnectionError:
            answer = "⚠️ Cannot reach Ollama. Is it running?"
            placeholder.markdown(answer)
        except Exception as e:
            answer = f"⚠️ Error: {e}"
            placeholder.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()