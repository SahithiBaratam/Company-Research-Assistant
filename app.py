import streamlit as st
from dotenv import load_dotenv

from agent import CompanyResearchAgent

load_dotenv()

st.set_page_config(
    page_title="Company Research Assistant - Account Plan Generator",
    layout="wide",
)

if "agent" not in st.session_state:
    st.session_state.agent = CompanyResearchAgent()

agent = st.session_state.agent

st.title("🤖 Company Research Assistant (Account Plan Generator)")
st.write(
    "Use this assistant to research a company through conversation and generate a structured account plan."
)

with st.sidebar:
    st.header("📋 Account Plan")

    if agent.account_plan_markdown:
        st.markdown(agent.account_plan_markdown)
    else:
        st.info(
            "No account plan yet.\n\n"
            "1. Start chatting in the main window.\n"
            "2. When ready, click **Generate / Update Account Plan**."
        )

    if st.button("Generate / Update Account Plan", use_container_width=True):
        with st.spinner("Generating account plan using the conversation so far..."):
            plan = agent.generate_account_plan()
        st.success("Account plan generated/updated!")
        st.markdown(plan)

    st.markdown("---")
    st.subheader("🌐 Live Web Research (DuckDuckGo)")

    company_for_web = st.text_input(
        "Company name for web research",
        placeholder="e.g., Salesforce, TCS, Microsoft",
    )
    extra_kw = st.text_input(
        "Extra keywords (optional)",
        placeholder="e.g., cloud, AI, recent news",
    )

    if st.button("Run DuckDuckGo Research", use_container_width=True):
        if not company_for_web.strip():
            st.warning("Enter a company name first.")
        else:
            with st.spinner("Fetching web results and summarizing with AI..."):
                summary = agent.research_company_with_ddg(
                    company_name=company_for_web.strip(),
                    keywords=extra_kw.strip(),
                )
            st.success("Web research summary added to conversation context.")
            st.markdown(summary)

    st.markdown("---")
    st.subheader("✏️ Edit specific section")

    if agent.account_plan_markdown:
        section = st.selectbox(
            "Select a section to refine",
            [
                "Account Overview",
                "Key Stakeholders & Org Map",
                "Business Objectives & Initiatives",
                "Current State & Existing Solutions",
                "Pain Points & Challenges",
                "Opportunity Summary",
                "Recommended Strategy & Tactics",
                "Action Plan & Next Steps",
            ],
        )
        edit_instruction = st.text_area(
            "Describe what to change in this section "
            "(e.g., 'add CFO as key stakeholder', 'emphasize cloud migration')."
        )

        if st.button("Apply Section Update", use_container_width=True, key="edit_section"):
            if not edit_instruction.strip():
                st.warning("Please enter update instructions first.")
            else:
                with st.spinner("Updating selected section with generative AI..."):
                    plan = agent.update_account_plan(
                        section_name=section,
                        user_instruction=edit_instruction,
                    )
                st.success("Section updated!")
                st.markdown(plan)
    else:
        st.caption("Generate a plan before editing individual sections.")

    st.markdown("---")
    st.subheader("💾 Export")
    if agent.account_plan_markdown:
        st.download_button(
            label="Download Account Plan (Markdown)",
            data=agent.account_plan_markdown,
            file_name="account_plan.md",
            mime="text/markdown",
            use_container_width=True,
        )
    else:
        st.caption("Generate a plan to enable export.")

st.markdown("### 💬 Conversation")

for msg in agent.chat_history[1:]:
    if msg["role"] not in ["user", "assistant"]:
        continue

    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about a company, paste info, or request next steps...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = agent.chat(user_input)
        st.markdown(response)
