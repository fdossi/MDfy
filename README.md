# MDfy

Aplicação web para converter documentos, planilhas, e-books, imagens e pacotes em Markdown.

## Aplicação

- Frontend responsivo em React/Next (Vinext)
- Backend Python com FastAPI e Microsoft MarkItDown
- Upload múltiplo, progresso por arquivo e download imediato
- Exclusão dos arquivos temporários após cada resposta
- Proteção contra *path traversal* em ZIP, TAR e TGZ

Formatos: PDF, DOCX, DOC, XLSX, XLS, CSV, EPUB, MOBI, PNG, JPG/JPEG, TIFF, DjVu, ZIP, TAR e TGZ.

## Desenvolvimento do frontend

```bash
npm ci
npm run dev
```

Defina `NEXT_PUBLIC_MDFY_API_URL` com a URL do backend, sem barra final.

## Desenvolvimento do backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --port 7860
```

O contêiner em `backend/Dockerfile` está preparado para um Hugging Face Space gratuito do tipo Docker.

## Implantação no Hugging Face

1. Crie um Space Docker público.
2. Crie um token do Hugging Face com permissão de escrita.
3. No GitHub, adicione o secret `HF_TOKEN` e a variável `HF_SPACE_ID` no formato `usuario/nome-do-space`.
4. Execute o workflow **Sync backend to Hugging Face**.

Não publique o token em arquivos, commits ou issues.

## Privacidade

O backend remove os diretórios temporários após entregar a resposta. Em produção, configure `ALLOWED_ORIGINS` com o domínio exato do frontend.

## Licença

MIT.
