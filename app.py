import streamlit as st
import google.generativeai as genai
import json

# Set up the webpage tab title
st.set_page_config(page_title="AI Architecture Recommender", page_icon="🏗️")

st.title("🏗️ AI System Architecture Recommender")
st.write("Describe your project constraints, and the AI agent will recommend the best cloud architecture.")

# ==========================================
# SIDEBAR: Security & Config
# ==========================================
with st.sidebar:
    st.header("⚙️ Configuration")
    # Users paste their key here so it stays out of the code!
    api_key = st.text_input("Gemini API Key", type="password", help="Get this from Google AI Studio")
    if not api_key:
        st.warning("Please enter a Gemini API Key to use the recommender.")

# ==========================================
# MAIN UI: Hybrid Input Form
# ==========================================
with st.form("project_form"):
    st.subheader("Project Details")
    
    # Create two columns to make the UI look neat
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
        "Describe any specific architectural separations, environmental data pipelines, or other needs:",
        placeholder="e.g., I need to pull live environmental factors from Met Éireann like rain and visibility to feed a predictive ML model. The architecture needs to cleanly separate the data processing pipeline, the ML engine, and the controller..."
    )
    
    # The submit button
    submitted = st.form_submit_button("Consult AI Architect")

# ==========================================
# AGENT LOGIC (Runs when button is clicked)
# ==========================================
if submitted:
    if not api_key:
        st.error("Please provide an API key in the sidebar first!")
    else:
        # Show a loading spinner while the AI thinks
        with st.spinner("Analyzing architecture constraints..."):
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Pack the UI inputs into our dictionary
            project_data = {
                "name": name, "ai_workload": ai_workload, "system_size": system_size,
                "scalability": scalability, "real_time": real_time, "budget": budget,
                "cloud_expertise": cloud_expertise, "data_sensitivity": data_sensitivity,
                "deployment_preference": deployment_pref, "additional_context": extra_context
            }
            
            prompt = f"""
            You are an expert AI System Architect. Evaluate these requirements and recommend the best technical architecture:
            {json.dumps(project_data, indent=2)}
            
            Select from these exact categories:
            - Architecture: monolithic, layered, microservices, event-driven, or serverless
            - Service Model: SaaS, PaaS, or IaaS
            - Deployment Model: Public, Private, Hybrid, or Community
            
            Respond ONLY in valid JSON with keys: "architecture", "service_model", "deployment_model", and "explanation".
            """
            
            try:
                response = model.generate_content(
                    prompt, 
                    generation_config=genai.GenerationConfig(response_mime_type="application/json")
                )
                result = json.loads(response.text)
                
                # Display the results beautifully using Streamlit Markdown
                st.success("✅ Recommendation Generated Successfully!")
                
                st.markdown("### 📊 Final AI Recommendation")
                st.markdown(f"**Architecture Style:** `{result.get('architecture', 'N/A').title()}`")
                st.markdown(f"**Service Model:** `{result.get('service_model', 'N/A')}`")
                st.markdown(f"**Deployment Model:** `{result.get('deployment_model', 'N/A').title()}`")
                
                st.markdown("### 🧠 Explanation")
                st.info(result.get('explanation', 'No explanation provided.'))
                
            except Exception as e:
                st.error(f"Error consulting the AI Agent. Ensure your API key is correct. Details: {e}")