import streamlit as st
import requests

st.markdown("""
<style>
.body {
    position: fixed;
    top: 70px;
    width: 100%;
}   
.header {
    position: fixed;
    top: 60px;
    width: 100%;
    
    z-index: 999;
}
</style>

<div class="header">
    <h4>🤖 Marketing IA - Assistente de Geração de Conteúdo Automatizado</h4>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
    <style>
        div[data-baseweb="select"] {
            max-width: 250px;
        }
    </style>
""", unsafe_allow_html=True)

# =============================
# Configurações da página
# =============================
st.set_page_config(
    page_title="Assistente de Geração de Conteúdo",
    page_icon="🤖",
    layout="wide"
)

# =============================
# Configurações técnicas
# =============================
API_URL = "http://127.0.0.1:8000/chat_full/message"
TIMEOUT_SECONDS = 30
MAX_PROMPT_LENGTH = 1000

# =============================
# Estado da sessão (histórico)
# =============================
if "history" not in st.session_state:
    st.session_state.history = []

# Campos do formulário

topic = st.text_input("Tema:", placeholder="Ex: saúde mental, alimentação saudável, prevenção, etc.")

col1, col2, col3, col4 = st.columns(4)

with col1:
    platform = st.selectbox("Plataforma:", ['Instagram', 'Facebook', 'LinkedIn', 'Blog', 'E-mail'])
with col2:
    tone = st.selectbox("Tom:", ['Normal', 'Informativo', 'Inspirador', 'Urgente', 'Informal'])
with col3:
    length = st.selectbox("Tamanho:", ['Curto', 'Médio', 'Longo'])
with col4:
    audience = st.selectbox("Público-alvo:", ['Geral', 'Jovens adultos', 'Famílias', 'Idosos', 'Adolescentes'])

cta = st.checkbox("Incluir CTA")
hashtags = st.checkbox("Retornar Hashtags")
keywords = st.text_area("Palavras-chave (SEO):", placeholder="Ex: bem-estar, medicina preventiva...")


prompt = f"""
Escreva um texto com SEO otimizado sobre o tema '{topic}'.
Retorne em sua resposta apenas o texto final e não inclua ela dentro de aspas.
- Onde será publicado: {platform}.
- Tom: {tone}.
- Público-alvo: {audience}.
- Comprimento: {length}.
- {"Inclua uma chamada para ação clara." if cta else "Não inclua chamada para ação"}
- {"Retorne ao final do texto hashtags relevantes." if hashtags else "Não inclua hashtags."}
 {"- Palavras-chave que devem estar presentes nesse texto (para SEO): " + keywords if keywords else ""}
"""
# =============================
# Botão de geração
# =============================
if st.button("Gerar conteúdo"):


    with st.spinner("Gerando resposta da IA..."):
        try:
            payload = {
                "message": prompt,
                "session_id": "usuario_padrao"
            }
            response = requests.post(
                API_URL,
                json=payload,
                timeout=TIMEOUT_SECONDS
            )

            if response.status_code == 200:
                dados = response.json()
                resposta = dados.get("response")
                st.success("Conteúdo gerado:")
                st.write(resposta)

                st.session_state.history.append({"role": "user", "content": prompt})
                st.session_state.history.append({"role": "assistant", "content": resposta})
            else:
                st.error(f"Erro na API ({response.status_code}): {response.text}")

        except requests.exceptions.Timeout:
            st.error("⏱️ A IA demorou muito para responder.")
        except requests.exceptions.ConnectionError:
            st.error("🚫 Não foi possível conectar ao backend.")
        except Exception as e:
            st.error("Erro inesperado.")
            st.text(str(e))
  