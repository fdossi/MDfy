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

O contêiner em `backend/Dockerfile` está preparado para um Web Service gratuito no Render.

## Implantação no Render

1. No Render, selecione **New → Blueprint**.
2. Conecte o repositório `fdossi/MDfy`.
3. O arquivo `render.yaml` criará o serviço Docker gratuito `mdfy-api`.
4. Aguarde o health check `/health` ficar disponível.

## Privacidade

O backend remove os diretórios temporários após entregar a resposta. Em produção, configure `ALLOWED_ORIGINS` com o domínio exato do frontend.

## Licença

MIT.
