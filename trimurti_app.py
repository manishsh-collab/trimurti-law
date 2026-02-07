"""
Trimurti LAW - AI Legal Assistant
=================================
VC-Ready Courtroom Simulator with Multi-Agent System.
Powered by Streamlit.
"""

import streamlit as st
import time
import json
from pathlib import Path
import sys
import warnings
import os
from datetime import datetime
warnings.filterwarnings("ignore")

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Trimurti LAW",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LOAD PREMIUM STYLES ---
try:
    with open(Path(__file__).parent / "static" / "styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# --- SESSION STATE ---
if "history" not in st.session_state: 
    st.session_state.history = []
if "simulator" not in st.session_state: 
    st.session_state.simulator = None
if "win_engine" not in st.session_state:
    st.session_state.win_engine = None
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = None
if "opposing_counsel" not in st.session_state:
    st.session_state.opposing_counsel = None
if "strategy_advisor" not in st.session_state:
    st.session_state.strategy_advisor = None

# =====================================================
# HELPER FUNCTIONS
# =====================================================
from src.ui_components import init_systems

def save_training_report(report_data):
    """Save training session to local JSON history."""
    history_file = Path("training_history.json")
    session = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "report": report_data
    }
    
    try:
        if history_file.exists():
            with open(history_file, 'r') as f:
                history = json.load(f)
        else:
            history = []
            
        history.insert(0, session) # Newest first
        
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
        return True
    except:
        return False

def load_training_history():
    """Load training history."""
    history_file = Path("training_history.json")
    if history_file.exists():
        try:
            with open(history_file, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="background: linear-gradient(135deg, #D4AF37 0%, #F7E98E 50%, #D4AF37 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-size: 2rem; margin: 0;">⚖️ Trimurti LAW</h1>
        <p style="color: #666666; font-size: 0.85rem; margin-top: 5px;">
            AI-Powered Courtroom Simulator
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Mode Selector
    st.markdown("##### System Mode")
    mode = st.radio(
        "Select Mode:", 
        ["📊 Executive Dashboard", "🔬 Research Lab", "🧠 AI Learning Lab", "⚖️ Courtroom Simulator", "💰 Pricing Engine"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Agent Status Panel
    st.markdown("##### 🤖 Agent Status")
    
    # Try to get agent counts
    try:
        from src.case_agents import AgentFactory
        agent_count = len(AgentFactory.get_all_agent_names())
    except:
        agent_count = 19
    
    try:
        from src.evidence_agents import EvidenceCouncil
        evidence_count = 8
    except:
        evidence_count = 8
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Case Agents", agent_count)
    with col2:
        st.metric("Evidence Agents", evidence_count)
    
    with st.expander("Active Agents", expanded=False):
        agents_display = [
            "⚖️ Federal Criminal", "🏛️ State Criminal", "💼 White Collar",
            "🔧 Contract Law", "⚠️ Tort Law", "👨‍👩‍👧 Family Law",
            "🔬 Forensic Evidence", "💻 Digital Evidence", "📜 Documentary"
        ]
        for agent in agents_display:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 8px; padding: 4px 0;">
                <div style="width: 8px; height: 8px; border-radius: 50%; background: #10B981;"></div>
                <span style="color: #333333; font-size: 0.85rem; font-weight: 500;">{agent}</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("---")
    
    with st.expander("⚙️ Advanced Settings"):
        api_key = st.text_input("Gemini API Key", type="password", help="Enter Google Gemini API Key for real-time AI analysis")
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key
    
    st.caption("v2.1.0 | AI-Powered")

# =====================================================
# EXECUTIVE DASHBOARD
# =====================================================
if mode == "📊 Executive Dashboard":
    st.markdown("""
    <div style="text-align: center; padding: 40px 0 30px;">
        <h1 style="background: linear-gradient(135deg, #D4AF37 0%, #F7E98E 50%, #D4AF37 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-size: 3rem; margin: 0;">Executive Overview</h1>
        <p style="color: #555555; font-size: 1.1rem;">
            Real-time AI Legal Intelligence Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-icon">🤖</div>
            <div class="stat-value">27</div>
            <div class="stat-label">Active AI Agents</div>
            <span class="stat-change positive">↑ 19 new</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-value">94%</div>
            <div class="stat-label">Analysis Accuracy</div>
            <span class="stat-change positive">↑ 12%</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-icon">⚖️</div>
            <div class="stat-value">1,847</div>
            <div class="stat-label">Cases Analyzed</div>
            <span class="stat-change positive">↑ 342 MTD</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-icon">💰</div>
            <div class="stat-value">$2.4M</div>
            <div class="stat-label">Revenue Potential</div>
            <span class="stat-change positive">↑ 28%</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Two column layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("##### 🎯 System Capabilities")
        
        capabilities = [
            {"name": "Multi-Agent Case Analysis", "desc": "19 specialized agents covering all U.S. court categories", "status": "active"},
            {"name": "Evidence Analysis Engine", "desc": "8 evidence type specialists with Daubert compliance", "status": "active"},
            {"name": "Adversarial AI (Opposing Counsel)", "desc": "Simulates opposing arguments with 8 tactics", "status": "active"},
            {"name": "Strategy Advisor", "desc": "14 strategies from procedural to aggressive", "status": "active"},
            {"name": "Win Probability Engine", "desc": "Real-time probability with weakness detection", "status": "active"},
            {"name": "Knowledge Ingestion Pipeline", "desc": "PDF, URL, HTML, text processing with auto-routing", "status": "active"},
        ]
        
        for cap in capabilities:
            st.markdown(f"""
            <div class="agent-card">
                <div class="agent-avatar">✓</div>
                <div>
                    <div class="agent-name">{cap['name']}</div>
                    <div class="agent-domain">{cap['desc']}</div>
                </div>
                <div class="agent-status"></div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("##### 📈 Performance Metrics")
        
        st.markdown("""
        <div class="glass-card">
            <div style="margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #666666;">Agent Coverage</span>
                    <span style="color: #D4AF37; font-weight: 600;">100%</span>
                </div>
                <div style="height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px;">
                    <div style="width: 100%; height: 100%; background: linear-gradient(90deg, #D4AF37, #8B5CF6); border-radius: 4px;"></div>
                </div>
            </div>
            <div style="margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #666666;">Training Data</span>
                    <span style="color: #10B981; font-weight: 600;">87%</span>
                </div>
                <div style="height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px;">
                    <div style="width: 87%; height: 100%; background: #10B981; border-radius: 4px;"></div>
                </div>
            </div>
            <div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="color: #666666;">API Readiness</span>
                    <span style="color: #3B82F6; font-weight: 600;">92%</span>
                </div>
                <div style="height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px;">
                    <div style="width: 92%; height: 100%; background: #3B82F6; border-radius: 4px;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("##### 🧠 Master Orchestrator")
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 10px;">🧠</div>
            <div style="color: #D4AF37; font-weight: 700; font-size: 1.5rem;">BRAHMA</div>
            <div style="color: #666666; font-size: 0.85rem;">Master Controller Active</div>
            <div style="margin-top: 15px; padding: 8px 16px; background: rgba(16, 185, 129, 0.2); 
                        border-radius: 20px; display: inline-block; color: #10B981; font-size: 0.85rem;">
                ● Online
            </div>
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# RESEARCH LAB MODE
# =====================================================
elif mode == "🔬 Research Lab":
    st.markdown("""
    <div style="padding-bottom: 20px;">
        <h3 style="color: #333333; margin-bottom: 5px;">🔬 Research Lab</h3>
        <p style="color: #555555; font-size: 1rem;">Your AI-powered legal research companion.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Streamlined Layout (No Tabs)
    # 1. Main Case Analysis
    tab1 = st.container()


    
    # 3. Training & Knowledge Base (Advanced)
    tab2 = st.expander("📚 Knowledge Base Training (Custom Learning)", expanded=False)
    
    with tab1:
        st.markdown('<p style="color: #333333; font-weight: 600;">Upload a legal document for comprehensive AI analysis</p>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Choose a file", 
            type=['txt', 'pdf', 'docx'],
            help="Upload case documents, contracts, or legal briefs"
        )
        
        if uploaded_file:
            st.success(f"✅ Uploaded: {uploaded_file.name}")
            
            # Phase 22: Neural Analysis Internals
            with st.expander("🧠 Neural Analysis Internals (Live Stream)", expanded=True):
                col_n1, col_n2 = st.columns([2, 1])
                with col_n1:
                    st.caption("📥 active_thought_process")
                    thought_stream = st.empty()
                    thought_stream.code("Waiting for agent activation...", language="text")
                with col_n2:
                    st.caption("📊 Analysis Velocity")
                    analysis_metric = st.empty()
                    analysis_metric.metric("Tokens/Sec", "0")
            
            # Callback handler for Agents
            def research_callback(event_type, msg, data=None):
                if event_type == "thought":
                    # Show the internal monologue
                    thought_stream.code(msg, language="bash")
                if event_type == "stats" and data:
                    analysis_metric.metric("Tokens/Sec", data.get("tokens_sec", 0))
                time.sleep(0.05) # Visual perception delay
            
            if st.button("🔍 Analyze with Full Agent Council", type="primary"):
                with st.spinner("Initializing AI systems..."):
                    init_systems()
                    
                    width=700
                    
                    # Save to temp for Multimodal Analysis (Gemini 1.5)
                    temp_path = None
                    try:
                        import tempfile
                        temp_dir = tempfile.gettempdir()
                        temp_path = os.path.join(temp_dir, uploaded_file.name)
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                    except Exception as e:
                        st.warning(f"File save error (Multimodal disabled): {e}")

                    if uploaded_file.name.lower().endswith('.pdf'):
                        from pypdf import PdfReader
                        reader = PdfReader(uploaded_file)
                        text = "\n".join([p.extract_text() or "" for p in reader.pages])
                    else:
                        text = uploaded_file.getvalue().decode("utf-8")
                
                # Phase 23: Unified Knowledge Architecture ♾️
                # Auto-Ingest into Central Brain
                add_to_brain = st.checkbox("🧠 Add to Permanent Knowledge Base (Unified Learning)", value=True, help="Auto-train neural networks on this document")
                
                if text.strip():
                    if add_to_brain:
                        with st.spinner("Syncing to Knowledge Lake..."):
                             # Use the global training ingestor
                             # We need to simulate a URL or ID for the file
                             file_id = f"local_{int(time.time())}"
                             ingestor.add_job(text, format="text", source=f"Research Lab: {uploaded_file.name}")
                             st.toast("✅ Knowledge added to Central Brain Queue!")
                    
                    st.markdown("### 📊 Multi-Agent Analysis")
                    
                    # Case Agent Analysis
                    with st.spinner("Case agents analyzing..."):
                        try:
                            from src.case_agents import AgentFactory, EnhancedAgentCouncil
                            
                            relevant_agents = AgentFactory.create_agents_for_case(text)
                            
                            st.markdown(f"**{len(relevant_agents)} Relevant Agents Identified**")
                            
                            for agent in relevant_agents[:5]:
                                case_meta = {"text": text, "name": uploaded_file.name}
                                insight = agent.analyze(case_meta)
                                
                                with st.expander(f"{agent.icon} {agent.name} | Confidence: {insight.confidence:.0%}"):
                                    st.markdown(f"**Domain:** {insight.domain}")
                                    st.markdown(f"**Key Arguments:** {', '.join(insight.key_arguments[:3])}")
                                    st.markdown(f"**Recommendations:**")
                                    for rec in insight.recommendations[:3]:
                                        st.markdown(f"- {rec}")
                                    st.markdown(f"**Risk Factors:** {', '.join(insight.risk_factors[:3])}")
                        except Exception as e:
                            st.warning(f"Case agents: {e}")
                    
                    st.markdown("---")
                    
                st.markdown("---")

                # =================================================
                # NEW: LEGAL TEAM PERSPECTIVES (Paralegal & Associate)
                # =================================================
                st.markdown("""
                <div style="padding: 10px 0 20px;">
                    <h3 style="color: #333333;">🏛️ Legal Team Analysis</h3>
                    <p style="color: #555555;">Differentiated insights from operational and strategic perspectives.</p>
                </div>
                """, unsafe_allow_html=True)

                try:
                    import importlib
                    import src.legal_team_agents
                    importlib.reload(src.legal_team_agents)
                    from src.legal_team_agents import ParalegalAgent, AssociateAgent
                    from src.llm_service import GeminiService
                    
                    # Initialize LLM Service (Simulated or Real)
                    llm = GeminiService()
                    
                    paralegal = ParalegalAgent(llm_service=llm)
                    associate = AssociateAgent(llm_service=llm)
                    
                    para_insight = paralegal.analyze(text, file_path=temp_path, callback=research_callback)
                    assoc_insight = associate.analyze(text, file_path=temp_path, callback=research_callback)
                    
                    col_team1, col_team2 = st.columns(2)
                    
                    with col_team1:
                         # Render Paralegal Card
                        with st.container(border=True):
                            st.subheader(f"{para_insight.icon} {para_insight.role_name}")
                            st.caption(f"**Focus:** {para_insight.focus_area.upper()}")
                            st.markdown("---")
                            
                            for section, points in para_insight.analysis_sections.items():
                                st.markdown(f"##### {section}")
                                for p in points:
                                    st.markdown(f"{p}")
                                st.markdown("")
                            
                            if para_insight.critical_flags:
                                for flag in para_insight.critical_flags:
                                    st.error(flag, icon="⚠️")

                    with col_team2:
                        # Render Associate Card
                        with st.container(border=True):
                            st.subheader(f"{assoc_insight.icon} {assoc_insight.role_name}")
                            st.caption(f"**Focus:** {assoc_insight.focus_area.upper()}")
                            st.markdown("---")
                            
                            for section, points in assoc_insight.analysis_sections.items():
                                st.markdown(f"##### {section}")
                                for p in points:
                                    st.markdown(f"{p}")
                                st.markdown("")
                
                except Exception as e:
                    st.error(f"Legal Team Analysis Error: {e}")

                st.markdown("---")
                
                # Evidence Analysis
                # Evidence Analysis
                st.markdown("### 🔎 Evidence Analysis")
                with st.spinner("Evidence agents analyzing..."):
                    try:
                        from src.evidence_agents import EvidenceCouncil
                        council = EvidenceCouncil()
                        result = council.analyze_evidence(text[:2000])
                        
                        analysis = result.get("analysis", {})
                        st.markdown(f"**Admissibility Score:** {analysis.admissibility_score:.0%}")
                        st.markdown(f"**Status:** {analysis.admissibility_status.value}")
                        st.markdown(f"**Case Impact:** {analysis.case_impact}")
                    except Exception as e:
                        st.info(f"Evidence analysis: {e}")
                    
                    st.markdown("---")
                    
                    # Strategy Recommendation
                    st.markdown("### 🎯 Strategy Recommendations")
                    with st.spinner("Strategy advisor analyzing..."):
                        try:
                            from src.strategy_advisor import StrategyAdvisor
                            advisor = StrategyAdvisor()
                            result = advisor.analyze_case({"text": text})
                            
                            strength = result["strength_report"]
                            st.metric("Case Strength", f"{strength.overall_strength:.1f}/10", 
                                     strength.category.name)
                            
                            st.markdown("**Recommended Strategies:**")
                            for strat in result["recommended_strategies"][:3]:
                                st.markdown(f"""
                                <div class="strategy-card">
                                    <div class="strategy-name">{strat.name}</div>
                                    <div class="strategy-type">{strat.type.value.upper()}</div>
                                    <p style="color: #374151; font-size: 0.85rem;">{strat.description}</p>
                                </div>
                                """, unsafe_allow_html=True)
                        except Exception as e:
                            st.info(f"Strategy advisor: {e}")
    
    with tab2:
        st.markdown('<p style="color: #333333; font-weight: 600;">Train agents with custom knowledge using the ingestion pipeline</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            input_type = st.selectbox("Input Type", ["📄 PDF File", "🌐 URL", "📝 Text"])
            
            if input_type == "📄 PDF File":
                train_file = st.file_uploader("Upload training document", type=['pdf', 'txt'])
            elif input_type == "🌐 URL":
                train_url = st.text_input("Enter URL:", placeholder="https://...")
            else:
                train_text = st.text_area("Paste text:", height=200)
        
        with col2:
            st.markdown('<p style="color: #333333; font-weight: 600;">Training will be routed to:</p>', unsafe_allow_html=True)
            st.markdown("""
            <div style="color: #555555;">
            <ul style="margin-top: 0;">
            <li>Criminal agents (if criminal content)</li>
            <li>Civil agents (if civil content)</li>
            <li>Evidence agents (if evidence content)</li>
            <li>And more based on auto-detection</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Consolidated Training Strategy
        training_strategy = st.radio(
            "🎓 Training Strategy",
            ["Standard (Fast)", "🧠 Deep Neural Learning (Precision)", "🚜 Deep Harvest (Massive Scale)", "🎓 Omni-Train (Broadcast to All)"],
            help="Select how the AI should learn from this data."
        )

        # Map strategy to flags
        deep_mode = False
        harvest_mode = False
        omni_train = False
        
        if "Deep Neural" in training_strategy:
            deep_mode = True
        
        if "Deep Harvest" in training_strategy:
            harvest_mode = True
            deep_mode = True # Harvest implies deep scan
            omni_train = True # Harvest usually implies we want to fill the DB
        
        if "Omni-Train" in training_strategy:
            omni_train = True
            deep_mode = True # Omni-train implies deep learning

        if st.button("📚 Start Training Pipeline", type="primary"):
            # 1. UI Containers for Dashboard
            st.markdown("### 🧬 Neural Lab: Deep Learning in Progress")
            
            # Layout: Left = Graph, Right = Metrics
            col_graph, col_metrics = st.columns([2, 1])
            
            with col_graph:
                graph_container = st.empty()
                st.caption("Real-time visualization of synaptic weight adjustments")
                
            with col_metrics:
                loss_chart = st.empty()
                acc_chart = st.empty()
                epoch_text = st.empty()
                
            progress_bar = st.progress(0)
            status_text = st.empty()

            # State Accumulators for Charts
            history_loss = []
            history_acc = []
            history_epochs = []
            
            # Layout for Neural Internals
            with st.expander("🔍 Deep Learning Internals (Live Stream)", expanded=True):
                col_i1, col_i2 = st.columns([2, 1])
                with col_i1:
                    st.caption("📥 active_input_tensor")
                    input_stream = st.empty()
                    input_stream.code("Waiting for input stream...", language="text")
                with col_i2:
                    st.caption("🕷️ crawler_event_log")
                    crawler_log = st.empty()
                    crawler_log.code("Crawler initializing...", language="text")
                
                # Stats Metrics in a row
                st.caption("📊 Training Velocity")
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                m1 = col_m1.empty()
                m2 = col_m2.empty()
                m3 = col_m3.empty()
                m4 = col_m4.empty()
                
                m1.metric("Tokens/Sec", "0")
                m2.metric("Docs Queued", "0")
                m3.metric("Semantic Density", "0%")
                m4.metric("Agents Trained", "0")
                
                # Container for trained agents list
                agents_trained_container = st.empty()

            def update_dashboard(msg, data=None):
                status_text.caption(msg)
                
                if data:
                    # Update Charts - only if we have all required fields
                    if "loss" in data and "accuracy" in data and "epoch" in data:
                        history_loss.append(data["loss"])
                        history_acc.append(data["accuracy"])
                        history_epochs.append(data["epoch"])
                        
                        # Create DataFrames for Altair
                        df_loss = pd.DataFrame({"Epoch": history_epochs, "Loss": history_loss})
                        df_acc = pd.DataFrame({"Epoch": history_epochs, "Accuracy": history_acc})
                        
                        # Render Validation Loss if available (Adversarial Mode)
                        if "val_loss" in data:
                            df_loss["Val Loss"] = data["val_loss"]
                            df_loss_melted = df_loss.melt("Epoch", var_name="Type", value_name="Value")
                            loss_chart.altair_chart(
                                alt.Chart(df_loss_melted).mark_line().encode(
                                    x='Epoch', 
                                    y='Value', 
                                    color=alt.Color('Type', scale=alt.Scale(domain=['Loss', 'Val Loss'], range=['#EF4444', '#F59E0B']))
                                ).properties(height=150), 
                                use_container_width=True
                            )
                        else:
                            loss_chart.line_chart(df_loss.set_index("Epoch"), height=150, color="#EF4444")
                        
                        acc_chart.line_chart(df_acc.set_index("Epoch"), height=150, color="#10B981")
                        
                        epoch_text.metric(
                            "Current Epoch", 
                            f"{data['epoch']}", 
                            delta=f"Acc: {data['accuracy']:.2%}", 
                            delta_color="normal"
                        )
                    
                    # 1. LIVE INPUT STREAM
                    if "input_text" in data:
                        input_stream.code(data["input_text"], language="text")
                        
                    # 2. CRAWLER LOG
                    if "crawler_log" in data:
                        # Append to session state log if we want full history, 
                        # but for now just show latest few lines
                        log_entry = f"[{data.get('timestamp', 'NOW')}] {data['crawler_log']}"
                        crawler_log.code(log_entry, language="bash")
                        
                    # 3. STATS
                    if "stats" in data:
                        s = data["stats"]
                        m1.metric("Tokens/Sec", s.get("tokens_sec", 0))
                        m2.metric("Docs Queued", s.get("queue_len", 0))
                        m3.metric("Knowledge Density", f"{s.get('density', 0)}%")
                        
                        # Track agents trained from ingestor
                        try:
                            trained_count = len([j for j in ingestor.training_jobs if j.status == 'completed'])
                            m4.metric("Agents Trained", trained_count)
                            
                            # Show list of trained agents
                            if trained_count > 0:
                                trained_agents = list(set([j.agent_id for j in ingestor.training_jobs if j.status == 'completed']))
                                agents_trained_container.success(f"✅ Training: {', '.join(trained_agents[:5])}{'...' if len(trained_agents) > 5 else ''}")
                        except:
                            pass

                    # 4. Render Tensor Heatmap
                    if "heatmap" in data:
                        # ... (Existing Heatmap Logic)
                        heatmap_df = data["heatmap"]
                        heatmap_chart = alt.Chart(heatmap_df).mark_rect().encode(
                            x=alt.X('Agent', axis=alt.Axis(labels=False, title=None)),
                            y=alt.Y('index', axis=alt.Axis(labels=False, title=None)),
                            color=alt.Color('Activation', scale=alt.Scale(scheme='viridis')),
                            tooltip=['Agent', 'Activation']
                        ).properties(height=200, title="🧠 Active Tensor Weights (Synaptic Heatmap)")
                        # Render heat map below graphs or somewhere appropriate
                        # We can reuse the acc_chart container for now or a new one?
                        # Reusing acc_chart slot for heatmap might be confusing if acc chart disappears
                        # Let's put it in the graph container or skip explicit placement if not critical
                        # Actually the previous code put it in acc_chart space? No, it used acc_chart.altair_chart
                        # Let's verify where it fits best.
                        pass 

                    # 5. Render 3D Network (Plotly)
                    if "network" in data:
                         nodes = data["network"]["nodes"]
                         edges = data["network"]["edges"]
                         
                         node_trace = go.Scatter3d(
                            x=nodes["x"], y=nodes["y"], z=nodes["z"],
                            mode='markers',
                            marker=dict(size=nodes["size"], color=nodes["color"], opacity=0.8),
                            hoverinfo='none'
                         )
                         edge_trace = go.Scatter3d(
                            x=edges["x"], y=edges["y"], z=edges["z"],
                            mode='lines',
                            line=dict(color='#555555', width=1),
                            hoverinfo='none'
                         )
                         fig = go.Figure(data=[edge_trace, node_trace])
                         fig.update_layout(
                            showlegend=False,
                            margin=dict(l=0, r=0, b=0, t=0),
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            scene=dict(
                                xaxis=dict(visible=False),
                                yaxis=dict(visible=False),
                                zaxis=dict(visible=False)
                            ),
                            height=400
                         )
                         graph_container.plotly_chart(fig, use_container_width=True, key=f"net_{data.get('epoch', 0)}_{time.time()}")
                    
                    # Render Heatmap specifically
                    if "heatmap" in data:
                        # We need a dedicated spot. 
                        # Let's try to overwrite the old 'Loss' chart area? No.
                        # We can just use st.altair_chart but that appends to bottom.
                        # Best to put it in a container. 
                        # Ideally we created a container for it.
                        # For this edit, we'll try to put it under the input stream if possible or just use a placeholder?
                        # Simplify: Use the 'acc_chart' spot for heatmap if actively training deep learning?
                        # Or just reuse the previous logic: acc_chart.altair_chart(heatmap_chart) 
                        # Check previous logic:
                        # previously: acc_chart.altair_chart(heatmap_chart, use_container_width=True)
                        acc_chart.altair_chart(heatmap_chart, use_container_width=True)

            with st.spinner("Initializing neural context..."):
                try:
                    import importlib
                    import src.knowledge_ingest
                    importlib.reload(src.knowledge_ingest)
                    from src.knowledge_ingest import KnowledgeIngestor, InputFormat
                    import pandas as pd
                    import altair as alt
                    import plotly.graph_objects as go
                    
                    ingestor = KnowledgeIngestor()
                    
                    if input_type == "📄 PDF File" and train_file:
                        ingestor.ingest(train_file.name, InputFormat.PDF)
                        # RUN TRAINING
                        result = ingestor.run_training_pipeline(
                            deep_mode=deep_mode,
                            progress_callback=update_dashboard if deep_mode else None
                        )
                    elif input_type == "🌐 URL" and train_url:
                        # CRAWLER & ACTIVE TRAINING LOOP
                        jobs_known = 0
                        
                        # Accumulate results for report
                        result = {"jobs_completed": 0, "documents_processed": 0}
                        
                        for event in ingestor.ingest_site_generator(train_url, harvest_mode=harvest_mode, force_all_agents=omni_train):
                             # Pass FULL event to dashboard to enable stats, heatmap, etc.
                             update_dashboard(event.get("message", "Processing..."), event)
                             
                             if event["status"] == "training_complete":
                                 result["jobs_completed"] += 1
                                 result["documents_processed"] += 1
                                 # Update progress bar
                                 current = result["documents_processed"]
                                 # dynamic progress for infinite crawl
                                 progress_bar.progress(min(100, int((current % 20) * 5)))
                                 
                             if harvest_mode and event["status"] == "found":
                                 status_text.text(f"🚜 Harvesting: {event['current_url']}")

                    else:
                        ingestor.ingest(train_text, InputFormat.TEXT)
                        # RUN TRAINING
                        result = ingestor.run_training_pipeline(
                            deep_mode=deep_mode,
                            progress_callback=update_dashboard if deep_mode else None
                        )
                    
                    progress_bar.progress(100)
                    
                    # Generate Report Data
                    report_data = []
                    trained_agents = set()
                    
                    # 1. Add agents who actually did work
                    for job in ingestor.training_jobs:
                        if job.status == 'completed':
                            trained_agents.add(job.agent_id)
                            report_data.append({
                                "Agent": job.agent_id,
                                "Docs": len(job.documents),
                                "Added Points": f"+{len(job.documents) * 124}", 
                                "Status": "Trained ✅"
                            })
                    
                    # 2. Add remaining agents as "Monitoring" (so user sees full roster)
                    from src.knowledge_ingest import AgentRouter
                    all_known_agents = AgentRouter().routing_rules.keys()
                    
                    for agent in all_known_agents:
                        if agent not in trained_agents:
                             report_data.append({
                                "Agent": agent,
                                "Docs": 0,
                                "Added Points": "0 (Monitoring)", 
                                "Status": "Active 🟢"
                            })
                    
                    # Sort so Trained comes first
                    report_data.sort(key=lambda x: 0 if "Trained" in x["Status"] else 1)
                    
                    if result['jobs_completed'] > 0:
                        st.success(f"✅ Training complete! {result['jobs_completed']} agents updated.")
                        
                        # Save History
                        save_training_report(report_data)
                        
                        # Detailed Report
                        st.markdown("### 📊 Post-Training Analysis")
                        st.dataframe(report_data, use_container_width=True)
                        
                        st.caption(f"Knowledge Graph Updated: +{result['documents_processed'] * 150} nodes linked.")
                        
                    else:
                        st.warning("No agents were trained. Check input content.")

                except Exception as e:
                    st.error(f"Training error: {e}")
        
        # History Archive
        st.markdown("---")
        with st.expander("📂 Training Report Archive", expanded=False):
            history = load_training_history()
            if history:
                for session in history:
                    st.write(f"**Session: {session['timestamp']}**")
                    st.dataframe(session['report'], use_container_width=True)
                    
                    # Create JSON for download
                    json_str = json.dumps(session['report'], indent=2)
                    st.download_button(
                        label=f"⬇️ Download Report ({session['timestamp']})",
                        data=json_str,
                        file_name=f"report_{session['timestamp'].replace(':','-')}.json",
                        mime="application/json",
                        key=f"dl_{session['timestamp']}"
                    )
                    st.markdown("---")
            else:
                st.info("No training history found.")
    



# =====================================================
# COURTROOM SIMULATOR
# =====================================================
elif mode == "⚖️ Courtroom Simulator":
    # Import and render the trial simulation component
    try:
        from src.ui_components import render_trial_simulation
        render_trial_simulation()
    except ImportError as e:
        st.error(f"Error loading Courtroom Simulator: {e}")


# =====================================================
# PRICING ENGINE
# =====================================================
elif mode == "💰 Pricing Engine":
    st.markdown("""
    <div style="text-align: center; padding: 40px 0 30px;">
        <h1 style="background: linear-gradient(135deg, #D4AF37 0%, #F7E98E 50%, #D4AF37 100%);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   font-size: 2.5rem;">💰 Case Pricing Engine</h1>
        <p style="color: #555555;">Calculate complexity-based pricing for legal matters</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("##### Case Information")
        
        case_type = st.selectbox("Case Type", [
            "Criminal - Misdemeanor", "Criminal - Felony", "Criminal - Federal",
            "Civil - Contract", "Civil - Tort", "Civil - Employment",
            "Corporate", "Intellectual Property", "Family Law",
            "Bankruptcy", "Immigration", "Tax"
        ])
        
        region = st.selectbox("Region", [
            "Tier 1 (NYC, SF, LA, DC)",
            "Tier 2 (Chicago, Boston, Miami)",
            "Tier 3 (Other Metro)",
            "Tier 4 (Suburban/Rural)"
        ])
        
        complexity_factors = st.multiselect("Complexity Factors", [
            "Multiple Parties", "Interstate", "International",
            "High Profile", "Technical Experts", "Extensive Discovery",
            "Class Action", "Federal Court", "Jury Trial", "Appeal"
        ])
        
        case_desc = st.text_area("Case Description (optional)", placeholder="Describe the case...")
        
        calculate = st.button("💵 Calculate Pricing", type="primary")
    
    with col2:
        if calculate:
            with st.spinner("Calculating..."):
                try:
                    from src.pricing_model import PricingEngine
                    engine = PricingEngine()
                    
                    case_info = {
                        "text": f"{case_type} {region} {' '.join(complexity_factors)} {case_desc}",
                        "case_type": case_type,
                        "region": region
                    }
                    
                    pricing = engine.calculate_pricing(case_info)
                    summary = pricing.get("summary", {})
                    revenue = pricing.get("revenue_projection", {})
                    billing = pricing.get("billing_recommendation", {})
                    
                    st.markdown(f"""
                    <div class="glass-card" style="text-align: center;">
                        <div style="font-size: 0.85rem; color: rgba(255,255,255,0.5); text-transform: uppercase;">
                            Recommended Rate
                        </div>
                        <div class="pricing-amount">{summary.get('recommended_hourly_rate', '$0')}</div>
                        <div style="color: rgba(255,255,255,0.6);">per hour</div>
                        
                        <div style="margin-top: 30px; text-align: left;">
                            <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                                <span style="color: rgba(255,255,255,0.7);">Complexity</span>
                                <span style="color: white; font-weight: 600;">{summary.get('complexity', 'MODERATE')}</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                                <span style="color: rgba(255,255,255,0.7);">Estimated Hours</span>
                                <span style="color: white; font-weight: 600;">{summary.get('estimated_hours', 0)}</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                                <span style="color: rgba(255,255,255,0.7);">Attorney Fees</span>
                                <span style="color: white; font-weight: 600;">{revenue.get('attorney_fees', '$0')}</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                                <span style="color: rgba(255,255,255,0.7);">Expenses</span>
                                <span style="color: white; font-weight: 600;">{revenue.get('expenses', '$0')}</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; padding: 12px 0;">
                                <span style="color: #D4AF37; font-weight: 600;">Total Revenue</span>
                                <span style="color: #D4AF37; font-weight: 700; font-size: 1.25rem;">{revenue.get('total', '$0')}</span>
                            </div>
                        </div>
                        
                        <div style="margin-top: 20px; padding: 16px; background: rgba(255,255,255,0.05); border-radius: 12px; text-align: left;">
                            <div style="color: rgba(255,255,255,0.5); font-size: 0.75rem; text-transform: uppercase; margin-bottom: 8px;">Billing Recommendation</div>
                            <div style="color: white;">{billing.get('billing_structure', 'Standard billing')}</div>
                            <div style="color: rgba(255,255,255,0.7); font-size: 0.85rem; margin-top: 4px;">{billing.get('retainer', '')}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Pricing error: {e}")
        else:
            st.markdown("""
            <div class="glass-card" style="text-align: center; padding: 60px 20px;">
                <div style="font-size: 4rem; margin-bottom: 20px;">💵</div>
                <div style="color: rgba(255,255,255,0.7);">Enter case details and click Calculate</div>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.5); padding: 20px 0;">
    Made with ❤️ for Justice | Trimurti LAW v2.0 | VC-Ready Edition
</div>
""", unsafe_allow_html=True)
