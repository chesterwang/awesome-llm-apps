from agno.agent import Agent
from agno.models.google import Gemini
from agno.media import Image as AgnoImage
from agno.tools.duckduckgo import DuckDuckGoTools
import streamlit as st
from typing import List, Optional
import logging
from pathlib import Path
import tempfile
import os

# Configure logging for errors only
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

import os
os.environ['HTTP_PROXY'] = "http://127.0.0.1:7890"
os.environ['HTTPS_PROXY'] = "http://127.0.0.1:7890"

def initialize_agents(api_key: str) -> tuple[Agent, Agent, Agent, Agent]:
    try:
        model = Gemini(id="gemini-2.0-flash", api_key=api_key)
        
        therapist_agent = Agent(
            model=model,
            name="治疗师代理",
            instructions=[
                "你是一位富有同情心的治疗师，你会：",
                "1. 富有同理心地倾听并认同感受",
                "2. 使用温和的幽默来缓和气氛",
                "3. 分享相关的分手经历",
                "4. 提供安慰的话语和鼓励",
                "5. 分析文本和图片输入以了解情感背景",
                "在你的回应中要充满支持和理解"
            ],
            markdown=True
        )

        closure_agent = Agent(
            model=model,
            name="情感终结代理",
            instructions=[
                "你是一位帮助用户获得情感终结的专家，你会：",
                "1. 为未发送的情感创建信息",
                "2. 帮助表达原始、诚实的情感",
                "3. 使用标题清晰地格式化信息",
                "4. 确保语气真诚可信",
                "专注于情感释放和获得终结"
            ],
            markdown=True
        )

        routine_planner_agent = Agent(
            model=model,
            name="日常计划代理",
            instructions=[
                "你是一位恢复日常计划的规划师，你会：",
                "1. 设计为期7天的恢复挑战",
                "2. 包含有趣的活动和自我关怀任务",
                "3. 建议社交媒体戒断策略",
                "4. 创建能赋予力量的播放列表",
                "专注于实际的恢复步骤"
            ],
            markdown=True
        )

        brutal_honesty_agent = Agent(
            model=model,
            name="绝对坦诚代理",
            tools=[DuckDuckGoTools()],
            instructions=[
                "你是一位提供直接反馈的专家，你会：",
                "1. 针对分手提供原始、客观的反馈",
                "2. 清晰地解释关系失败的原因",
                "3. 使用直白、基于事实的语言",
                "4. 提供向前看的理由",
                "专注于提供诚实的见解，不加糖衣"
            ],
            markdown=True
        )
        
        return therapist_agent, closure_agent, routine_planner_agent, brutal_honesty_agent
    except Exception as e:
        st.error(f"初始化代理时出错: {str(e)}")
        return None, None, None, None

# Set page config and UI elements
st.set_page_config(
    page_title="💔 分手恢复小队",
    page_icon="💔",
    layout="wide"
)



# Sidebar for API key input
with st.sidebar:
    st.header("🔑 API 配置")

    if "api_key_input" not in st.session_state:
        st.session_state.api_key_input = ""
        
    api_key = st.text_input(
        "输入您的 Gemini API 密钥",
        value=st.session_state.api_key_input,
        type="password",
        help="从 Google AI Studio 获取您的 API 密钥",
        key="api_key_widget"  
    )

    if api_key != st.session_state.api_key_input:
        st.session_state.api_key_input = api_key
    
    if api_key:
        st.success("已提供 API 密钥! ✅")
    else:
        st.warning("请输入您的 API 密钥以继续")
        st.markdown("""
        要获取您的 API 密钥：
        1. 前往 [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. 在您的 [Google Cloud Console](https://console.developers.google.com/apis/api/generativelanguage.googleapis.com) 中启用 Generative Language API
        """)

# Main content
st.title("💔 分手恢复小队")
st.markdown("""
    ### 您的人工智能分手恢复团队随时为您提供帮助！
    分享您的感受和聊天截图，我们将帮助您度过这段艰难时期。
""")

# Input section
col1, col2 = st.columns(2)

with col1:
    st.subheader("分享您的感受")
    user_input = st.text_area(
        "您感觉怎么样？发生了什么事？",
        height=150,
        placeholder="告诉我们您的故事..."
    )
    
with col2:
    st.subheader("上传聊天截图")
    uploaded_files = st.file_uploader(
        "上传您的聊天截图（可选）",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="screenshots"
    )
    
    if uploaded_files:
        for file in uploaded_files:
            st.image(file, caption=file.name, use_container_width=True)

# Process button and API key check
if st.button("获取恢复计划 💝", type="primary"):
    if not st.session_state.api_key_input:
        st.warning("请先在侧边栏输入您的 API 密钥！")
    else:
        therapist_agent, closure_agent, routine_planner_agent, brutal_honesty_agent = initialize_agents(st.session_state.api_key_input)
        
        if all([therapist_agent, closure_agent, routine_planner_agent, brutal_honesty_agent]):
            if user_input or uploaded_files:
                try:
                    st.header("您的个性化恢复计划")
                    
                    def process_images(files):
                        processed_images = []
                        for file in files:
                            try:
                                temp_dir = tempfile.gettempdir()
                                temp_path = os.path.join(temp_dir, f"temp_{file.name}")
                                
                                with open(temp_path, "wb") as f:
                                    f.write(file.getvalue())
                                
                                agno_image = AgnoImage(filepath=Path(temp_path))
                                processed_images.append(agno_image)
                                
                            except Exception as e:
                                logger.error(f"处理图片 {file.name} 时出错: {str(e)}")
                                continue
                        return processed_images
                    
                    all_images = process_images(uploaded_files) if uploaded_files else []
                    
                    # Therapist Analysis
                    with st.spinner("🤗 正在获取同理心支持..."):
                        therapist_prompt = f"""
                        Analyze the emotional state and provide empathetic support based on:
                        User's message: {user_input}
                        
                        Please provide a compassionate response with:
                        1. Validation of feelings
                        2. Gentle words of comfort
                        3. Relatable experiences
                        4. Words of encouragement
                        """
                        
                        response = therapist_agent.run(
                            therapist_prompt,
                            images=all_images
                        )
                        
                        st.subheader("🤗 情感支持")
                        st.markdown(response.content)
                    
                    # Closure Messages
                    with st.spinner("✍️ 正在撰写结束语..."):
                        closure_prompt = f"""
                        Help create emotional closure based on:
                        User's feelings: {user_input}
                        
                        Please provide:
                        1. Template for unsent messages
                        2. Emotional release exercises
                        3. Closure rituals
                        4. Moving forward strategies
                        """
                        
                        response = closure_agent.run(
                            closure_prompt,
                            images=all_images
                        )
                        
                        st.subheader("✍️ 寻求释怀")
                        st.markdown(response.content)
                    
                    # Recovery Plan
                    with st.spinner("📅 正在创建您的恢复计划..."):
                        routine_prompt = f"""
                        Design a 7-day recovery plan based on:
                        Current state: {user_input}
                        
                        Include:
                        1. Daily activities and challenges
                        2. Self-care routines
                        3. Social media guidelines
                        4. Mood-lifting music suggestions
                        """
                        
                        response = routine_planner_agent.run(
                            routine_prompt,
                            images=all_images
                        )
                        
                        st.subheader("📅 您的恢复计划")
                        st.markdown(response.content)
                    
                    # Honest Feedback
                    with st.spinner("💪 正在获取坦诚的观点..."):
                        honesty_prompt = f"""
                        Provide honest, constructive feedback about:
                        Situation: {user_input}
                        
                        Include:
                        1. Objective analysis
                        2. Growth opportunities
                        3. Future outlook
                        4. Actionable steps
                        """
                        
                        response = brutal_honesty_agent.run(
                            honesty_prompt,
                            images=all_images
                        )
                        
                        st.subheader("💪 坦诚的观点")
                        st.markdown(response.content)
                            
                except Exception as e:
                    logger.error(f"分析期间出错: {str(e)}")
                    st.error("分析期间发生错误。请查看日志以获取详细信息。")
            else:
                st.warning("请分享您的感受或上传截图以获取帮助。")
        else:
            st.error("初始化代理失败。请检查您的 API 密钥。")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>由分手恢复小队 ❤️ 制作</p>
        <p>使用 #BreakupRecoverySquad 分享您的恢复之旅</p>
    </div>
""", unsafe_allow_html=True)