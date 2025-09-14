import asyncio
import os
import streamlit as st
from main_agent import MainAgent, load_data, display_energy_providers_carousel

def main():
    st.set_page_config(page_title="Energy Assistant", page_icon=":zap:")
    st.header(":battery: Your Intelligent Energy Analysis Platform")
    st.write("Upload data, ask questions, find news or check live energy prices.")

    # --- Sidebar: Live Prices ---
    with st.sidebar:
        st.header("⚡ Live Energy Prices")
        if st.button("🔄 Load Live Prices"):
            from tools.live_price_tool import get_live_energy_data
            try:
                st.session_state.energy_data = get_live_energy_data()
                st.success("✅ Prices loaded!")
            except Exception as e:
                st.error(f"❌ Failed: {e}")

        if st.session_state.get("energy_data"):
            display_energy_providers_carousel(st.session_state.energy_data)

    # --- Session state init ---
    st.session_state.setdefault("conversation_history", [])
    st.session_state.setdefault("chat_messages", [])

    # --- Setup agent ---
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    if not mistral_api_key:
        st.error("Missing MISTRAL_API_KEY env variable")
        return
    agent = MainAgent(mistral_api_key)

    # --- Upload data ---
    df = None
    uploaded = st.file_uploader("Upload your dataset", type=["csv", "xlsx"])

    if uploaded:
        # Reset state if a new file is uploaded
        if "last_uploaded" not in st.session_state or st.session_state.last_uploaded != uploaded.name:
            st.session_state.chat_messages = []
            st.session_state.conversation_history = []
            st.session_state.last_uploaded = uploaded.name

        df = load_data(uploaded)
        if df is not None:
            st.subheader("📂 Data Preview")
            st.dataframe(df.head(8))
            st.caption(f"{df.shape[0]} rows × {df.shape[1]} columns")


    # --- Show chat ---
    st.subheader("💬 Chat")
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            for code in msg.get("code_blocks", []):
                st.code(code, language="python")
            for fig in msg.get("figures", []):
                st.pyplot(fig)

    # --- Input ---
    query = st.chat_input("Ask something about your data , energy prices , or news...")
    if query:
        st.session_state.chat_messages.append({"role": "user", "content": query})

        with st.spinner("Analyzing..."):
            result = asyncio.run(agent.analyze_query(query, df, st.session_state.conversation_history))

        if result["type"] == "tool_with_response":
            figures, code_blocks = [], []
            for tool_result in result["tool_results"]:
                figures.extend(tool_result.get("figures", []))
                if tool_result.get("type") == "analysis":
                    code_blocks.append(tool_result.get("code", ""))
                if tool_result.get("type") == "forecast":
                    fig = tool_result.get("result", {}).get("figure")
                    if fig: figures.append(fig)

            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": result["llm_response"],
                "figures": figures,
                "code_blocks": code_blocks
            })
        else:
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": result["response"]
            })

        st.session_state.conversation_history = result["conversation_history"]
        st.rerun()

if __name__ == "__main__":
    main()
