# MDfy

Aplicação web para converter arquivos em Markdown com processamento local no navegador e ambientes gratuitos para formatos avançados.

## Arquitetura

1. **Conversão local e privada** para formatos comuns, diretamente no navegador.
2. **MyBinder + Voilà** para conversões avançadas, sem login.
3. **Google Colab** como contingência quando o Binder estiver indisponível.

O ambiente avançado é mantido separadamente em [fdossi/mdfy-runtime](https://github.com/fdossi/mdfy-runtime).

## Formatos

O frontend converte localmente PDF, DOCX, TXT, MD, CSV, JSON, HTML e XML. Outros formatos compatíveis são encaminhados ao ambiente avançado.

## Desenvolvimento

```bash
npm ci
npm run dev
```

Para validar uma versão de produção:

```bash
npm run lint
npx next build
```

## Publicação

O workflow `.github/workflows/pages.yml` gera o site estático e publica o diretório `out/` no GitHub Pages.

- GitHub Pages: [fdossi.github.io/MDfy](https://fdossi.github.io/MDfy/)
- Domínio solicitado: [mdfy.js.org](https://mdfy.js.org)
- Registro do domínio: `public/CNAME`

## Privacidade

Arquivos compatíveis são processados localmente pelo navegador. Arquivos enviados ao Binder ou Colab seguem as políticas e os limites desses serviços.

## Licença

MIT.
