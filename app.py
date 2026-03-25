import streamlit as st
import google.generativeai as genai
import json

st.set_page_config(page_title="AI Architecture Recommender", page_icon="🌩️", layout="wide")

st.title("🌩️ AI System Architecture Recommender")
st.write("Describe your project constraints, and the AI agent will recommend the best cloud architecture.")

# ==========================================
# SIDEBAR: Security & Config
# ==========================================
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Gemini API Key", type="password", help="Get this from Google AI Studio")
    if not api_key:
        st.warning("Please enter a Gemini API Key to use the recommender.")

# ==========================================
# MAIN UI: Hybrid Input Form
# ==========================================
with st.form("project_form"):
    st.subheader("Project Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Project Name", placeholder="e.g., Transport Tracker")
        ai_workload = st.selectbox("AI Workload Type", ["prediction", "nlp", "vision", "expert_system"])
        system_size = st.selectbox("System Size", ["small", "medium", "large"])
        scalability = st.selectbox("Scalability Need", ["low", "medium", "high"])
        
    with col2:
        real_time = st.selectbox("Real-Time Requirement", ["yes", "no"])
        budget = st.selectbox("Budget", ["low", "medium", "high"])
        cloud_expertise = st.selectbox("Team Cloud Expertise", ["low", "medium", "high"])
        data_sensitivity = st.selectbox("Data Sensitivity", ["low", "high"])
        
    deployment_pref = st.selectbox("Deployment Preference", ["public", "private", "hybrid", "community"])

    st.subheader("Additional Context (The Hybrid Magic)")
    extra_context = st.text_area(
        "Describe any specific architectural separations, data pipelines, or other needs:",
        placeholder="e.g., I need to pull live environmental factors like rain and visibility to feed a predictive ML model. The architecture needs to cleanly separate the data processing pipeline, the ML engine, and the controller..."
    )
    
    submitted = st.form_submit_button("Consult AI Architect")

# ==========================================
# AGENT LOGIC (Runs when button is clicked)
# ==========================================
if submitted:
    if not api_key:
        st.error("Please provide an API key in the sidebar first!")
    else:
        with st.spinner("Analyzing architecture constraints and calculating trade-offs..."):
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            project_data = {
                "name": name, "ai_workload": ai_workload, "system_size": system_size,
                "scalability": scalability, "real_time": real_time, "budget": budget,
                "cloud_expertise": cloud_expertise, "data_sensitivity": data_sensitivity,
                "deployment_preference": deployment_pref, "additional_context": extra_context
            }
            
            # UPGRADED PROMPT: Asking for specific arrays of benefits and tradeoffs
            prompt = f"""
            You are an expert AI System Architect. Evaluate these requirements and recommend the best technical architecture:
            {json.dumps(project_data, indent=2)}
            
            Select from these exact categories:
            - Architecture: monolithic, layered, microservices, event-driven, or serverless
            - Service Model: SaaS, PaaS, or IaaS
            - Deployment Model: Public, Private, Hybrid, or Community
            
            You MUST respond ONLY in valid JSON with exactly the following keys:
            - "architecture" (string)
            - "service_model" (string)
            - "deployment_model" (string)
            - "why_this" (string: A detailed paragraph explaining why this exact combination was chosen)
            - "benefits" (array of strings: 3-4 key advantages of this approach)
            - "tradeoffs" (array of strings: 2-3 potential drawbacks or challenges to watch out for)
            """
            
            try:
                response = model.generate_content(
                    prompt, 
                    generation_config=genai.GenerationConfig(response_mime_type="application/json")
                )
                result = json.loads(response.text)
                
                st.success("✅ Architecture Blueprint Generated Successfully!")
                
                # DISPLAY UPGRADE: Better layout for the new data points
                st.markdown("---")
                st.markdown("### 📊 Architectural Blueprint")
                
                # Top level metrics
                m1, m2, m3 = st.columns(3)
                m1.metric("Architecture Style", result.get('architecture', 'N/A').title())
                m2.metric("Service Model", result.get('service_model', 'N/A'))
                m3.metric("Deployment Model", result.get('deployment_model', 'N/A').title())
                
                st.markdown("### 🧠 Why This Architecture?")
                st.info(result.get('why_this', 'No explanation provided.'))
                
                st.markdown("---")
                
                # Side-by-side comparison for Benefits and Trade-offs
                b_col, t_col = st.columns(2)
                
                with b_col:
                    st.markdown("#### ✅ Key Benefits")
                    for benefit in result.get('benefits', []):
                        st.markdown(f"- {benefit}")
                        
                with t_col:
                    st.markdown("#### ⚠️ Trade-offs & Risks")
                    for tradeoff in result.get('tradeoffs', []):
                        st.markdown(f"- {tradeoff}")
                        
            except Exception as e:
                st.error(f"Error consulting the AI Agent. Ensure your API key is correct. Details: {e}")