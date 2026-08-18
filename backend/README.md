---
title: MDfy API
emoji: 📝
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
license: mit
---

# MDfy API

API temporária de conversão de documentos para Markdown, usada pelo frontend MDfy.

- Health check: `GET /health`
- Conversão: `POST /convert` com campo multipart `file`
- Limite: 100 MB por arquivo

Os uploads são removidos automaticamente após a resposta.
