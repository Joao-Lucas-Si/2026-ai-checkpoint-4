# CKP01 — Chatbot Profissional · [Domínio do grupo]
**Prompt Engineering & AI · FIAP · 2º Semestre 2026**
**Integrantes:** Nome Completo (RM12345) · Nome Completo (RM67890) · Nome Completo (RM24680)
**Peso: 25% · Apresentação: Aula 04 · Entrega: 23:55 do dia da Aula 05 (.zip via Teams — só o líder)**
# Domínio
[Qual domínio, por que foi escolhido, quem são os usuários-alvo]
# Requisitos atendidos
| Requisito | Status | Implementação |
| -| -| -|
| Pipeline LCEL | ✅ | chain.py — prompt \| llm \| PydanticOutputParser() |
| ChatOllama | ✅ | gemma4:cloud via Ollama Cloud (.env) |
| Memória gerenciada | ✅ | ConversationChain + Buffer, justificada em memory_manager.py |
| Pydantic v2 (≥4 campos) | ✅ | AnaliseConsulta com 6 campos em schemas.py |
| Context rot | ✅ | context_rot.py — tabela 0/5/10/15/20 turnos |
| Domínio documentado | ✅ | Este README + system prompt rico em prompts.py |
# Como executar (local — sem Colab)
cp .env.example .env # edite com sua OLLAMA_API_KEY — este arquivo NÃO vai no .zip
pip install -r requirements.txt
python -m app.main # Gradio: http: /localhost:7860
# Justificativa da memória
[Escolha + por quê + efeito no custo de tokens]