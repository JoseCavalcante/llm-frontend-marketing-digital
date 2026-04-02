import streamlit as st
import requests

# =============================
# Configurações da página
# =============================
st.set_page_config(
    page_title="Assistente de Geração de Conteúdo",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Assistente de Geração de Conteúdo Automatizado")

# =============================
# Configurações técnicas
# =============================
API_URL = "http://127.0.0.1:8000/chat_chain"
TIMEOUT_SECONDS = 30
MAX_PROMPT_LENGTH = 1000

# =============================
# Estado da sessão (histórico)
# =============================
if "history" not in st.session_state:
    st.session_state.history = []

# =============================
# Input do usuário
# =============================
prompt = st.text_area(
    "Digite o que deseja gerar:",
    height=80,
    max_chars=MAX_PROMPT_LENGTH,
    value="Gere um post para LinkedIn sobre IA aplicada a negócios",
    placeholder="Ex: Gere um post para LinkedIn sobre IA aplicada a negócios..."
)

# =============================
# Botão de geração
# =============================
if st.button("Gerar conteúdo"):
    if not prompt.strip():
        st.warning("Digite um prompt válido.")
    else:
        with st.spinner("Gerando resposta da IA..."):
            try:
                response = requests.get(
                    API_URL,
                    params={"msg": prompt},
                    timeout=TIMEOUT_SECONDS
                )

                dados = response.json()
                resposta = dados.get("answer")

                st.success("Conteúdo gerado:")
                st.write(resposta)

                st.session_state.history.append(
                    {"role": "user", "content": prompt}
                )

                st.session_state.history.append(
                    {"role": "assistant", "content": resposta}
                )



            except requests.exceptions.Timeout:
                st.error("⏱️ A IA demorou muito para responder.")
            except requests.exceptions.ConnectionError:
                st.error("🚫 Não foi possível conectar ao backend.")
            except Exception as e:
                st.error("Erro inesperado.")
                st.text(str(e))

# =============================
# Exibição do histórico
# =============================
st.divider()
st.subheader("🧠 Histórico da Conversa")

for msg in st.session_state.history:
    if msg["role"] == "user":
        st.markdown(f"**👤 Você:** {msg['content']}")
    else:
        st.markdown(f"**🤖 IA:** {msg['content']}")
