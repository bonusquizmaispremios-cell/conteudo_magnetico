import streamlit as st
from groq import Groq
from datetime import datetime
import json
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="CONTEÚDO MAGNÉTICO", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#FDFAF6; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#92400E,#78350F) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#78350F,#5C2D0A) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#3D2B1F !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#FDF8F0,#FAF0E6); padding:20px; border-radius:14px; border:1px solid #D4B896; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#3D2B1F !important; }

    .card-dark { background:linear-gradient(135deg,#FAF0E6,#F5E6D3); padding:20px; border-radius:14px; border:1px solid #C4956A; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#3D2B1F !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #D4B896; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#3D2B1F !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#7C5C3E !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #D4B896; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#3D2B1F !important; }

    .badge { background:#92400E; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#D4B896,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #D4B896; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#3D2B1F !important; }

    .chat-persona { background:#FDFAF6; border:1px solid #D4B896; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#3D2B1F !important; }

    .questao-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#3D2B1F !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#3D2B1F !important; }

    .meta-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#3D2B1F !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#7C5C3E !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE — persiste enquanto servidor não reiniciar
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_conteudo():
    return {"perfis": {}}

_cache = get_cache_conteudo()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_conteudos', 'biblioteca_conteudos',
    'nicho_padrao', 'tom_padrao', 'publico_padrao',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login'}
    _pref = (
        'btn_','sel_','ul_','dl_','cad_','_sub','_sm','_tab','_bsc',
        'ativo_','rem_','sel_pet_','ev_','prof_','hig_','prev_',
        'vac_','sint_','comp_','trad_','subs_','amb_','viag_','chat_',
        'duvida_','emerg_','peso_','data_','obs_','tipo_','vet_','desc_',
        'local_','prox_','alim','sit_emerg_','tc_','oraf','siau','agmag',
        'lv','mv','pt','pi','sh','wc','rv','rp','rc',
    )
    import re as _re
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_\d+$', k): continue
        st.session_state[k] = v

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_conteudo(tipo: str, plataforma: str, nicho: str, conteudo: str):
    st.session_state.historico_conteudos.append({
        'data':       datetime.now().strftime('%d/%m %H:%M'),
        'tipo':       tipo,
        'plataforma': plataforma,
        'nicho':      nicho,
        'conteudo':   conteudo,
        'favoritado': False,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa':                "Login",
    'usuario':              "",
    'api_key':              "",
    'pagina':               "Home",
    'historico_conteudos':  [],
    'biblioteca_conteudos': [],
    'nicho_padrao':         "",
    'tom_padrao':           "Inspirador",
    'publico_padrao':       "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- MOTOR DE IA ---
def gerar_conteudo_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f"""Você é um especialista em criação de conteúdo para redes sociais no Brasil.
Especialidades: Instagram, TikTok, YouTube Shorts, LinkedIn, WhatsApp.
Usuário: {st.session_state.usuario}.
{system_extra}
Crie conteúdo que gera engajamento real — direto, autêntico, sem clichês corporativos.
Use emojis estrategicamente. Escreva em português brasileiro natural."""
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt},
            ],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total = len(st.session_state.historico_conteudos)
    bib   = len(st.session_state.biblioteca_conteudos)

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#F5F3FF;border:1px solid #C4B5FD;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} conteúdos gerados · {bib} salvos na biblioteca</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_btn:
        st.download_button(
            label="💾 SALVAR MEUS DADOS (.json)",
            data=gerar_json_sessao(),
            file_name=f"conteudo_magnetico_{nome_usuario}.json",
            mime="application/json",
            use_container_width=True,
            key="conteudo10"
        )
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    """, unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if 'biblioteca_conteudos' not in st.session_state: st.session_state['biblioteca_conteudos'] = None
if 'historico_conteudos' not in st.session_state: st.session_state['historico_conteudos'] = []
if 'nicho_padrao' not in st.session_state: st.session_state['nicho_padrao'] = None
if 'publico_padrao' not in st.session_state: st.session_state['publico_padrao'] = None
if 'tom_padrao' not in st.session_state: st.session_state['tom_padrao'] = None

if st.session_state.etapa == "Login":
    st.markdown("# 🤖 CONTEÚDO MAGNÉTICO")
    st.markdown("<div class=\'card\'><b>🔒 ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</b><br>🔗 <a href='https://quizcompremios.com.br' target='_blank' style='color:#4F46E5;font-weight:700;text-decoration:underline;'>quizcompremios.com.br</a></div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        arq_j = st.file_uploader("📂 Carregar dados salvos (.json):", type=["json"], key="upload_login")
        dados_login = json.load(arq_j) if arq_j else None
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                if dados_login: carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":

    # BARRA DE SALVAR


    # TABS — navegação nativa
    _tab_Home, _tab_Legenda, _tab_Carrossel, _tab_Reels, _tab_Stories, _tab_LinkedIn, _tab_Calendario, _tab_Biblioteca, _tab_Progresso = st.tabs(['🏠 Painel Principal', '📝 Gerador de Legendas', '🎠 Criador de Carrosséi', '🎬 Roteiro de Reels/Tik', '📖 Stories Sequenciais', '💼 Conteúdo para Linked', '📅 Calendário Editorial', '📚 Biblioteca de Conteú', '📈 Meu Progresso'])

    # ── BARRA SALVAR — aparece em todas as abas ──
    with st.expander("💾 Salvar / Carregar meus dados", expanded=False):
        _bsc1, _bsc2 = st.columns(2)
        with _bsc1:
            import json as _jsv
            _dsv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_') and k not in ('api_key',)}
            st.download_button("💾 Baixar meus dados (.json)",
                data=_jsv.dumps(_dsv, ensure_ascii=False, indent=2, default=str),
                file_name=f"dados_{st.session_state.get('usuario','user')}.json",
                mime="application/json", key="dl_barra_sv_conteudo")
        with _bsc2:
            _fupsv = st.file_uploader("📂 Carregar dados salvos:", type=["json"], key="ul_barra_sv_conteudo", label_visibility="collapsed")
            if _fupsv:
                try:
                    import json as _jld
                    for _k2,_v2 in _jld.loads(_fupsv.read().decode()).items():
                        if _k2 not in ('api_key','etapa'): st.session_state[_k2] = _v2
                    st.success("✅ Dados restaurados!"); st.rerun()
                except: st.error("Arquivo inválido.")


    with _tab_Home:
            col_u, col_r = st.columns([3, 1])
            with col_u:
                st.title(f"Olá, {st.session_state.usuario}! 🚀")
                st.markdown("<span class='badge'>Criador de Conteúdo</span>", unsafe_allow_html=True)
            with col_r:
                if st.button("🚪 Sair", key="conteudo3"):
                    for k in list(st.session_state.keys()):
                        del st.session_state[k]
                    st.rerun()

            # AVISO SE DADOS SUMIRAM
            total_h = len(st.session_state.historico_conteudos)
            if total_h == 0 and len(st.session_state.biblioteca_conteudos) == 0:
                st.markdown("""<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
                padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
                ⚠️ Seus dados não estão mais no servidor.
                </div>""", unsafe_allow_html=True)
                arq_home = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_home")
                if arq_home is not None:
                    try:
                        dados_home = json.load(arq_home)
                        carregar_json_sessao(dados_home)
                        salvar_perfil_cache(st.session_state.usuario)
                        st.success("✅ Dados recuperados!")
                        st.rerun()
                    except Exception:
                        st.error("Arquivo inválido.")

            # CONFIGURAÇÕES PADRÃO
            st.markdown("#### ⚙️ Configure seu perfil de criador")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.session_state.nicho_padrao  = st.text_input("Seu nicho:", value=st.session_state.nicho_padrao, placeholder="ex: emagrecimento, finanças, moda...", key="conteudo4")
            with col_b:
                st.session_state.publico_padrao = st.text_input("Público-alvo:", value=st.session_state.publico_padrao, placeholder="ex: mulheres de 25-40 anos...", key="conteudo5")
            with col_c:
                st.session_state.tom_padrao = st.selectbox("Tom de voz:", ["Inspirador","Educativo","Divertido","Provocativo","Direto","Empático"], index=["Inspirador","Educativo","Divertido","Provocativo","Direto","Empático"].index(st.session_state.tom_padrao) if st.session_state.tom_padrao in ["Inspirador","Educativo","Divertido","Provocativo","Direto","Empático"] else 0, key="conteudo6")


            # MÉTRICAS
            bib_total = len(st.session_state.biblioteca_conteudos)
            tipos_gerados = {}
            for c in st.session_state.historico_conteudos:
                tipos_gerados[c['tipo']] = tipos_gerados.get(c['tipo'], 0) + 1

            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total_h}</div><div>Conteúdos gerados</div></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{bib_total}</div><div>Salvos na biblioteca</div></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos_gerados.get('Legenda',0)}</div><div>Legendas criadas</div></div>", unsafe_allow_html=True)
            c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos_gerados.get('Reels',0)}</div><div>Roteiros de Reels</div></div>", unsafe_allow_html=True)

            st.markdown("<div class='card'>💡 <em>'Quem posta com consistência e estratégia não depende de sorte — depende de método.'</em></div>", unsafe_allow_html=True)

            st.markdown("### 🗺️ O que cada aba faz")
            guia = {
                "📝 Legenda":    "Gera legendas completas com gancho, corpo, CTA e hashtags",
                "🎠 Carrossel":  "Cria roteiros de carrosséis slide a slide — do gancho ao CTA",
                "🎬 Reels":      "Roteiro completo de Reels e TikToks com hook, script e legenda",
                "📖 Stories":    "Sequência estratégica de stories para engajar e vender",
                "💼 LinkedIn":   "Posts profissionais com storytelling e posicionamento de autoridade",
                "📅 Calendário": "Plano editorial de 30 dias com temas, formatos e frequência",
                "📚 Biblioteca": "Seus melhores conteúdos salvos organizados por tipo",
                "📈 Progresso":  "Histórico completo de tudo que você gerou",
            }
            for aba, desc in guia.items():
                st.markdown(f"**{aba}** — {desc}")

            if st.session_state.historico_conteudos:
                st.markdown("### 🕐 Últimos Conteúdos Gerados")
                for item in reversed(st.session_state.historico_conteudos[-4:]):
                    st.markdown(
                        f"<div class='hist-item'>"
                        f"<span class='badge'>{item['tipo']}</span> "
                        f"<span class='badge-rosa'>{item.get('plataforma', '')}</span> "
                        f"<small style='color:#888'>{item['data']}</small><br>"
                        f"<small style='color:#555'>{item.get('nicho', '')}</small></div>",
                        unsafe_allow_html=True
                    )

        # ========================
        # LEGENDA
        # ========================

    with _tab_Legenda:
            st.header("📝 Gerador de Legendas")
            st.markdown("Legendas com gancho poderoso, corpo, CTA e hashtags — prontas para copiar e postar.")

            col1, col2 = st.columns(2)
            with col1:
                nicho    = st.text_input("Nicho/tema:", value=st.session_state.nicho_padrao, placeholder="ex: emagrecimento, finanças...", key="conteudo7")
                publico  = st.text_input("Público-alvo:", value=st.session_state.publico_padrao, placeholder="ex: mulheres de 30-45 anos...", key="conteudo8")
                assunto  = st.text_input("Assunto do post:", placeholder="ex: 3 erros que impedem o emagrecimento", key="conteudo9")
            with col2:
                plataforma = st.selectbox("Plataforma:", ["Instagram", "TikTok", "Facebook", "LinkedIn"], key="conteudo10_d2")
                tom        = st.selectbox("Tom de voz:", ["Inspirador","Educativo","Divertido","Provocativo","Direto","Empático"], index=["Inspirador","Educativo","Divertido","Provocativo","Direto","Empático"].index(st.session_state.tom_padrao) if st.session_state.tom_padrao in ["Inspirador","Educativo","Divertido","Provocativo","Direto","Empático"] else 0, key="conteudo11")
                qtd_opcoes = st.radio("Gerar:", ["1 legenda", "3 opções"], horizontal=True, key="conteudo12")
                incluir_hashtags = st.checkbox("Incluir hashtags", value=True, key="conteudo13")
                incluir_cta      = st.checkbox("Incluir CTA (chamada para ação)", value=True, key="conteudo14")

            if st.button("📝 GERAR LEGENDA AGORA", key="conteudo15"):
                if assunto.strip():
                    with st.spinner("Criando legenda magnética..."):
                        qtd = "3 opções de legendas diferentes" if "3" in qtd_opcoes else "1 legenda completa"
                        prompt = (
                            f"Crie {qtd} para {plataforma} sobre '{assunto}'.\n"
                            f"Nicho: {nicho}. Público: {publico}. Tom: {tom}.\n\n"
                            f"Para cada legenda, siga EXATAMENTE esta estrutura:\n"
                            f"🎣 GANCHO (1-2 linhas que param o scroll)\n"
                            f"📖 CORPO (desenvolvimento em parágrafos curtos, fácil de ler)\n"
                            f"{'📢 CTA (chamada clara para ação: comentar, salvar, compartilhar, clicar no link)' if incluir_cta else ''}\n"
                            f"{'#️⃣ HASHTAGS (mistura de grandes, médias e pequenas, max 15)' if incluir_hashtags else ''}\n\n"
                            f"REGRAS:\n"
                            f"- Gancho deve gerar curiosidade ou identificação imediata\n"
                            f"- Parágrafos curtos (máx 3 linhas cada)\n"
                            f"- Emojis estratégicos, não excessivos\n"
                            f"- Tom {tom} do início ao fim\n"
                            f"- Linguagem natural, como uma pessoa real escreveria"
                        )
                        res = gerar_conteudo_ia(prompt)
                        if res: st.session_state['res_legenda_conteu1'] = str(res)
                        salvar_conteudo("Legenda", plataforma, nicho or assunto, res)
                        st.session_state['legenda_temp'] = res
                        st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Preencha o assunto do post antes de continuar.")

            if st.session_state.get('legenda_temp'):
                col_copy, col_salvar, col_novo = st.columns(3)
                with col_copy:
                    st.download_button("📋 Baixar legenda (.txt)", data=st.session_state['legenda_temp'],
                        file_name="legenda.txt", mime="text/plain", use_container_width=True, key="conteudo9_d2")
                with col_salvar:
                    if st.button("💾 Salvar na Biblioteca", use_container_width=True, key="conteudo16"):
                        st.session_state.biblioteca_conteudos.append({
                            'tipo': 'Legenda', 'plataforma': plataforma,
                            'nicho': nicho or assunto, 'conteudo': st.session_state['legenda_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("✅ Salvo na Biblioteca!")
                with col_novo:
                    if st.button("🔄 Gerar outra", use_container_width=True, key="conteudo17"):
                        st.session_state.pop('legenda_temp', None)
                        st.rerun()

        # ========================
        # CARROSSEL
        # ========================

    with _tab_Carrossel:
            st.header("🎠 Criador de Carrosséis")
            st.markdown("Roteiros slide a slide — do gancho irresistível ao CTA que converte.")

            col1, col2 = st.columns(2)
            with col1:
                nicho   = st.text_input("Nicho/tema:", value=st.session_state.nicho_padrao, placeholder="ex: produtividade, beleza...", key="conteudo18")
                publico = st.text_input("Público-alvo:", value=st.session_state.publico_padrao, key="conteudo19")
                assunto = st.text_input("Tema do carrossel:", placeholder="ex: 5 erros que estão sabotando seu emagrecimento", key="conteudo20")
            with col2:
                num_slides = st.slider("Número de slides:", min_value=5, max_value=12, value=7, key="conteudo1")
                objetivo   = st.selectbox("Objetivo do carrossel:", ["Educar","Engajar","Vender","Gerar salvamentos","Atrair seguidores"], key="conteudo21")
                tom        = st.selectbox("Tom:", ["Educativo","Inspirador","Provocativo","Direto","Divertido"], key="conteudo22")

            if st.button("🎠 CRIAR ROTEIRO DO CARROSSEL", key="conteudo23"):
                if assunto.strip():
                    with st.spinner("Montando carrossel slide a slide..."):
                        prompt = (
                            f"Crie um roteiro completo de carrossel para Instagram sobre '{assunto}'.\n"
                            f"Nicho: {nicho}. Público: {publico}. Tom: {tom}. Objetivo: {objetivo}.\n"
                            f"Total de slides: {num_slides}.\n\n"
                            f"Para CADA slide, use este formato:\n\n"
                            f"📌 SLIDE 1 — CAPA\n"
                            f"Título: [texto principal — máx 8 palavras]\n"
                            f"Subtítulo: [texto secundário — máx 12 palavras]\n"
                            f"Visual sugerido: [descrição da imagem/cor/elemento]\n\n"
                            f"📌 SLIDE 2 a {num_slides-1} — CONTEÚDO\n"
                            f"Título do slide: [max 6 palavras]\n"
                            f"Texto: [conteúdo do slide — máx 3 linhas]\n"
                            f"Destaque: [frase ou dado que deve aparecer em destaque]\n\n"
                            f"📌 SLIDE {num_slides} — CTA\n"
                            f"Texto principal: [chamada para ação direta]\n"
                            f"Ação: [o que a pessoa deve fazer: salvar, comentar, seguir, clicar...]\n\n"
                            f"Ao final: sugira uma legenda curta para o carrossel (máx 3 linhas) + 10 hashtags."
                        )
                        res = gerar_conteudo_ia(prompt)
                        if res: st.session_state['res_carrossel_conteu2'] = str(res)
                        salvar_conteudo("Carrossel", "Instagram", nicho or assunto, res)
                        st.session_state['carrossel_temp'] = res
                        st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Preencha o tema do carrossel.")

            if st.session_state.get('carrossel_temp'):
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar roteiro (.txt)", data=st.session_state['carrossel_temp'],
                        file_name="carrossel.txt", mime="text/plain", use_container_width=True, key="conteudo8_d2")
                with col_sv:
                    if st.button("💾 Salvar na Biblioteca", key="sv_carr", use_container_width=True):
                        st.session_state.biblioteca_conteudos.append({
                            'tipo': 'Carrossel', 'plataforma': 'Instagram',
                            'nicho': nicho or assunto, 'conteudo': st.session_state['carrossel_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("✅ Salvo na Biblioteca!")

        # ========================
        # REELS / TIKTOK
        # ========================

    with _tab_Reels:
            st.header("🎬 Roteiro de Reels e TikTok")
            st.markdown("Scripts cronometrados com hook, desenvolvimento e CTA — só gravar e postar.")

            col1, col2 = st.columns(2)
            with col1:
                nicho    = st.text_input("Nicho:", value=st.session_state.nicho_padrao, key="conteudo24")
                publico  = st.text_input("Público:", value=st.session_state.publico_padrao, key="conteudo25")
                assunto  = st.text_input("Tema do vídeo:", placeholder="ex: por que você não consegue emagrecer", key="conteudo26")
            with col2:
                duracao    = st.selectbox("Duração:", ["15 segundos","30 segundos","60 segundos","90 segundos"], key="conteudo27")
                plataforma = st.selectbox("Plataforma:", ["Instagram Reels","TikTok","YouTube Shorts"], key="conteudo28")
                estilo     = st.selectbox("Estilo:", ["Educativo rápido","Storytelling pessoal","Provação/Desafio","Revelar segredo","Lista rápida","POV"], key="conteudo29")

            if st.button("🎬 GERAR ROTEIRO COMPLETO", key="conteudo30"):
                if assunto.strip():
                    with st.spinner("Escrevendo o roteiro..."):
                        prompt = (
                            f"Crie um roteiro completo de {plataforma} sobre '{assunto}'.\n"
                            f"Nicho: {nicho}. Público: {publico}. Duração: {duracao}. Estilo: {estilo}.\n\n"
                            f"ESTRUTURA OBRIGATÓRIA:\n\n"
                            f"⏱️ HOOK (0-3 segundos):\n"
                            f"[Frase de abertura que prende em 3 segundos — a mais importante do vídeo]\n"
                            f"Ação visual: [o que aparece na tela]\n\n"
                            f"📹 DESENVOLVIMENTO (segundo a segundo):\n"
                            f"[Script cronometrado — cada linha = ±3 segundos de fala]\n"
                            f"[Inclua sugestões de cortes, transições e elementos visuais]\n\n"
                            f"🎯 CTA FINAL (últimos 3 segundos):\n"
                            f"[Chamada clara e direta]\n\n"
                            f"📝 LEGENDA SUGERIDA:\n"
                            f"[Legenda curta com gancho e hashtags]\n\n"
                            f"🎵 SUGESTÃO DE ÁUDIO/TRILHA:\n"
                            f"[Tipo de música ou som que combina]\n\n"
                            f"💡 DICA DE EDIÇÃO:\n"
                            f"[1 dica específica para esse tipo de vídeo performar melhor]"
                        )
                        res = gerar_conteudo_ia(prompt)
                        if res: st.session_state['res_reels_conteu3'] = str(res)
                        salvar_conteudo("Reels", plataforma, nicho or assunto, res)
                        st.session_state['reels_temp'] = res
                        st.markdown(f"<div class='card-dark'>{res}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Preencha o tema do vídeo.")

            if st.session_state.get('reels_temp'):
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar roteiro (.txt)", data=st.session_state['reels_temp'],
                        file_name="roteiro_reels.txt", mime="text/plain", use_container_width=True, key="conteudo7_d2")
                with col_sv:
                    if st.button("💾 Salvar na Biblioteca", key="sv_reels", use_container_width=True):
                        st.session_state.biblioteca_conteudos.append({
                            'tipo': 'Reels', 'plataforma': plataforma,
                            'nicho': nicho or assunto, 'conteudo': st.session_state['reels_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("✅ Salvo na Biblioteca!")

        # ========================
        # STORIES
        # ========================

    with _tab_Stories:
            st.header("📖 Stories Sequenciais")
            st.markdown("Sequências estratégicas de stories para engajar, aquecer e converter.")

            col1, col2 = st.columns(2)
            with col1:
                nicho   = st.text_input("Nicho:", value=st.session_state.nicho_padrao, key="conteudo31")
                publico = st.text_input("Público:", value=st.session_state.publico_padrao, key="conteudo32")
                assunto = st.text_input("Objetivo da sequência:", placeholder="ex: lançar produto, gerar curiosidade, aquecimento...", key="conteudo33")
            with col2:
                num_stories = st.slider("Quantidade de stories:", min_value=3, max_value=10, value=5, key="conteudo2")
                tipo_story  = st.selectbox("Tipo:", [
                    "Aquecimento (curiosidade/antecipação)",
                    "Vendas (lançamento de produto)",
                    "Engajamento (enquete/interação)",
                    "Storytelling pessoal",
                    "Conteúdo educativo",
                    "Bastidores",
                ], key="conteudo6_d2")

            if st.button("📖 CRIAR SEQUÊNCIA DE STORIES", key="conteudo34"):
                if assunto.strip():
                    with st.spinner("Criando sequência estratégica..."):
                        prompt = (
                            f"Crie uma sequência de {num_stories} stories para Instagram.\n"
                            f"Nicho: {nicho}. Público: {publico}. Objetivo: {assunto}. Tipo: {tipo_story}.\n\n"
                            f"Para CADA story use este formato:\n\n"
                            f"📸 STORY [N] de {num_stories}\n"
                            f"Texto principal: [o que aparece escrito no story]\n"
                            f"Elemento interativo: [enquete / caixinha de perguntas / link / nenhum]\n"
                            f"Visual sugerido: [fundo, foto, vídeo, cor — 1 linha]\n"
                            f"Objetivo deste story: [o que ele deve fazer pelo espectador]\n\n"
                            f"REGRAS:\n"
                            f"- Cada story tem 1 só ideia\n"
                            f"- Texto curto — max 2 linhas visíveis\n"
                            f"- Crie progressão: cada story leva ao próximo\n"
                            f"- Último story sempre tem CTA claro\n"
                            f"- Use emojis para chamar atenção em pontos chave"
                        )
                        res = gerar_conteudo_ia(prompt)
                        if res: st.session_state['res_stories_conteu4'] = str(res)
                        salvar_conteudo("Stories", "Instagram", nicho or assunto, res)
                        st.session_state['stories_temp'] = res
                        st.markdown(f"<div class='card-pink'>{res}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Preencha o objetivo da sequência.")

            if st.session_state.get('stories_temp'):
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar sequência (.txt)", data=st.session_state['stories_temp'],
                        file_name="stories.txt", mime="text/plain", use_container_width=True, key="conteudo5_d2")
                with col_sv:
                    if st.button("💾 Salvar na Biblioteca", key="sv_stories", use_container_width=True):
                        st.session_state.biblioteca_conteudos.append({
                            'tipo': 'Stories', 'plataforma': 'Instagram',
                            'nicho': nicho or assunto, 'conteudo': st.session_state['stories_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("✅ Salvo na Biblioteca!")

        # ========================
        # LINKEDIN
        # ========================

    with _tab_LinkedIn:
            st.header("💼 Conteúdo para LinkedIn")
            st.markdown("Posts com storytelling profissional, posicionamento de autoridade e alcance orgânico.")

            col1, col2 = st.columns(2)
            with col1:
                profissao = st.text_input("Sua profissão/área:", placeholder="ex: coach, nutricionista, empreendedor...", key="conteudo35")
                assunto   = st.text_input("Tema do post:", placeholder="ex: como triplicar minha renda em 6 meses", key="conteudo36")
                contexto  = st.text_area("Contexto ou história real (opcional):", height=80, placeholder="ex: quando eu perdi meu emprego em 2022...", key="conteudo37")
            with col2:
                formato = st.selectbox("Formato:", [
                    "Post de texto (storytelling)",
                    "Lista de dicas (5-7 pontos)",
                    "Opinião polêmica",
                    "Lição aprendida",
                    "Conquista com aprendizado",
                    "Pergunta para debate",
                ], key="conteudo4_d2")
                tom = st.selectbox("Tom:", ["Profissional e direto","Vulnerável e humano","Provocativo","Inspirador"], key="conteudo38")

            if st.button("💼 GERAR POST LINKEDIN", key="conteudo39"):
                if assunto.strip():
                    with st.spinner("Escrevendo post de autoridade..."):
                        prompt = (
                            f"Crie um post para LinkedIn sobre '{assunto}'.\n"
                            f"Profissão: {profissao}. Formato: {formato}. Tom: {tom}.\n"
                            f"{'Contexto/história: ' + contexto if contexto.strip() else ''}\n\n"
                            f"ESTRUTURA:\n"
                            f"📌 PRIMEIRA LINHA (gancho): frase que para o scroll — sem começar com 'Eu' ou 'Hoje'\n"
                            f"📖 DESENVOLVIMENTO: storytelling ou lista — parágrafos de 1-2 linhas cada\n"
                            f"💡 APRENDIZADO/VIRADA: a lição ou insight principal\n"
                            f"🎯 CTA: pergunta para debate ou chamada para comentar\n\n"
                            f"REGRAS LinkedIn:\n"
                            f"- Primeira linha decide tudo — deve gerar clique em 'ver mais'\n"
                            f"- Parágrafos curtos com linha em branco entre eles\n"
                            f"- Emojis com moderação (máx 5 no post todo)\n"
                            f"- Sem hashtags em excesso (máx 5, ao final)\n"
                            f"- Tom humano e autêntico, não corporativo"
                        )
                        res = gerar_conteudo_ia(prompt)
                        if res: st.session_state['res_linkedin_conteu5'] = str(res)
                        salvar_conteudo("LinkedIn", "LinkedIn", profissao or assunto, res)
                        st.session_state['linkedin_temp'] = res
                        st.markdown(f"<div class='card-green'>{res}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Preencha o tema do post.")

            if st.session_state.get('linkedin_temp'):
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar post (.txt)", data=st.session_state['linkedin_temp'],
                        file_name="post_linkedin.txt", mime="text/plain", use_container_width=True, key="conteudo3_d2")
                with col_sv:
                    if st.button("💾 Salvar na Biblioteca", key="sv_li", use_container_width=True):
                        st.session_state.biblioteca_conteudos.append({
                            'tipo': 'LinkedIn', 'plataforma': 'LinkedIn',
                            'nicho': profissao or assunto, 'conteudo': st.session_state['linkedin_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("✅ Salvo na Biblioteca!")

        # ========================
        # CALENDÁRIO EDITORIAL
        # ========================

    with _tab_Calendario:
            st.header("📅 Calendário Editorial — 30 Dias")
            st.markdown("Plano completo de postagens para um mês inteiro — com temas, formatos e frequência.")

            col1, col2 = st.columns(2)
            with col1:
                nicho          = st.text_input("Nicho:", value=st.session_state.nicho_padrao, key="conteudo40")
                publico        = st.text_input("Público:", value=st.session_state.publico_padrao, key="conteudo41")
                objetivo_mes   = st.text_input("Objetivo do mês:", placeholder="ex: lançar infoproduto, crescer 500 seguidores, gerar leads...", key="conteudo42")
            with col2:
                freq_semana    = st.slider("Posts por semana:", min_value=2, max_value=7, value=4, key="conteudo3_x2")
                plataformas_cal= st.multiselect("Plataformas:", ["Instagram Feed","Instagram Stories","Reels","TikTok","LinkedIn","YouTube Shorts"], default=["Instagram Feed","Reels"], key="conteudo4_x2")
                tem_produto    = st.checkbox("Tenho produto/serviço para vender", key="conteudo43")

            if st.button("📅 GERAR CALENDÁRIO DE 30 DIAS", key="conteudo44"):
                if nicho.strip():
                    with st.spinner("Montando seu calendário editorial..."):
                        plats = ', '.join(plataformas_cal) if plataformas_cal else 'Instagram'
                        prompt = (
                            f"Crie um calendário editorial de 30 dias para criador de conteúdo.\n"
                            f"Nicho: {nicho}. Público: {publico}. Objetivo do mês: {objetivo_mes}.\n"
                            f"Frequência: {freq_semana}x por semana. Plataformas: {plats}.\n"
                            f"{'Tem produto/serviço para vender.' if tem_produto else 'Foco em crescimento e autoridade.'}\n\n"
                            f"FORMATO DE SAÍDA:\n"
                            f"Organize por SEMANAS (1 a 4), com cada post assim:\n\n"
                            f"📅 Semana 1 — [tema âncora da semana]\n"
                            f"Post 1: [dia] | [plataforma] | [formato] | [tema/título]\n"
                            f"Post 2: [dia] | [plataforma] | [formato] | [tema/título]\n"
                            f"...\n\n"
                            f"Após as 4 semanas:\n"
                            f"📊 ESTRATÉGIA DO MÊS: explica a lógica por trás da sequência\n"
                            f"🎯 PILARES DE CONTEÚDO: os 3-4 temas principais do nicho\n"
                            f"⚡ DICAS DE CONSISTÊNCIA: como manter a frequência sem burnout\n\n"
                            f"Formatos disponíveis: Carrossel, Reels, Legenda, Stories, Live, Bastidores"
                        )
                        res = gerar_conteudo_ia(prompt)
                        if res: st.session_state['res_calendario_conteu6'] = str(res)
                        salvar_conteudo("Calendário", plats, nicho, res)
                        st.session_state['calendario_temp'] = res
                        st.markdown(f"<div class='card-orange'>{res}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Preencha o nicho antes de gerar o calendário.")

            if st.session_state.get('calendario_temp'):
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar calendário (.txt)", data=st.session_state['calendario_temp'],
                        file_name="calendario_editorial.txt", mime="text/plain", use_container_width=True, key="conteudo2_d2")
                with col_sv:
                    if st.button("💾 Salvar na Biblioteca", key="sv_cal", use_container_width=True):
                        st.session_state.biblioteca_conteudos.append({
                            'tipo': 'Calendário', 'plataforma': 'Múltiplas',
                            'nicho': nicho, 'conteudo': st.session_state['calendario_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("✅ Salvo na Biblioteca!")

        # ========================
        # BIBLIOTECA
        # ========================

    with _tab_Biblioteca:
            st.header("📚 Biblioteca de Conteúdos")
            st.markdown("Seus melhores conteúdos salvos — organizados e prontos para usar.")

            if not st.session_state.biblioteca_conteudos:
                st.info("Biblioteca vazia. Gere conteúdos nas outras abas e salve os melhores aqui!")
            else:
                # Filtros
                tipos_bib = list(set(c['tipo'] for c in st.session_state.biblioteca_conteudos))
                filtro    = st.selectbox("Filtrar por tipo:", ["Todos"] + tipos_bib, key="conteudo45")

                conteudos_filtrados = [
                    c for c in st.session_state.biblioteca_conteudos
                    if filtro == "Todos" or c['tipo'] == filtro
                ]

                st.markdown(f"**{len(conteudos_filtrados)} conteúdo(s) encontrado(s)**")

                for i, item in enumerate(reversed(conteudos_filtrados)):
                    idx_real = len(st.session_state.biblioteca_conteudos) - 1 - i
                    with st.expander(f"[{item['tipo']}] [{item.get('plataforma', '')}] {item.get('nicho', '')} — {item['data']}"):
                        st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                        col_dl, col_del = st.columns([3, 1])
                        with col_dl:
                            st.download_button(
                                "📋 Baixar", data=item['conteudo'],
                                file_name=f"{item['tipo'].lower()}_{item['data'][:5].replace('/','')}.txt",
                                mime="text/plain", key=f"dl_bib_{i}"
                            )
                        with col_del:
                            if st.button("🗑️ Remover", key=f"del_bib_{i}"):
                                st.session_state.biblioteca_conteudos.pop(idx_real)
                                st.rerun()

        # ========================
        # PROGRESSO
        # ========================

    with _tab_Progresso:
            st.header("📈 Meu Progresso")

            total = len(st.session_state.historico_conteudos)
            bib   = len(st.session_state.biblioteca_conteudos)

            # Contagem por tipo
            tipos = {}
            for c in st.session_state.historico_conteudos:
                tipos[c['tipo']] = tipos.get(c['tipo'], 0) + 1

            c1, c2, c3, c4, c5 = st.columns(5)
            c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total}</div><div>Total gerado</div></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{bib}</div><div>Na biblioteca</div></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Legenda',0)}</div><div>Legendas</div></div>", unsafe_allow_html=True)
            c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Reels',0)}</div><div>Reels</div></div>", unsafe_allow_html=True)
            c5.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Carrossel',0)}</div><div>Carrosséis</div></div>", unsafe_allow_html=True)

            if st.session_state.historico_conteudos:
                col_f, col_ex = st.columns([3, 1])
                with col_f:
                    filtro = st.selectbox("Filtrar:", ["Todos","Legenda","Carrossel","Reels","Stories","LinkedIn","Calendário"], key="conteudo46")
                with col_ex:
                    historico_txt = "\n\n".join(
                        f"[{c['data']}] {c['tipo']} | {c['plataforma']} | {c['nicho']}\n{c['conteudo']}\n{'─'*40}"
                        for c in st.session_state.historico_conteudos
                    )
                    st.download_button("⬇️ Exportar TXT", data=historico_txt,
                        file_name="historico_conteudos.txt", mime="text/plain", key="conteudo1_d2")

                for i, item in enumerate(reversed(st.session_state.historico_conteudos)):
                    if filtro != "Todos" and item['tipo'] != filtro:
                        continue
                    idx_real = len(st.session_state.historico_conteudos) - 1 - i
                    with st.expander(f"[{item['tipo']}] [{item.get('plataforma', '')}] {item.get('nicho', '')} — {item['data']}"):
                        st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                        col_sv, col_del = st.columns([3, 1])
                        with col_sv:
                            if st.button("💾 Salvar na Biblioteca", key=f"sv_hist_{i}"):
                                st.session_state.biblioteca_conteudos.append(item.copy())
                                st.success("Salvo!")
                        with col_del:
                            if st.button("🗑️", key=f"del_hist_{i}"):
                                st.session_state.historico_conteudos.pop(idx_real)
                                st.rerun()

                if st.button("🗑️ Limpar Todo o Histórico", key="conteudo47"):
                    st.session_state.historico_conteudos = []
                    st.rerun()
            else:
                st.info("Nenhum conteúdo gerado ainda. Use as ferramentas para começar!")

    # --- RODAPÉ ---
    st.markdown(
        "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
        "© 2026 Conteúdo Magnético — Criador de Conteúdo com IA · Quiz Com Prêmios"
        "</div>", unsafe_allow_html=True
    )

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "</div>", unsafe_allow_html=True
)
