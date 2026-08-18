# MDfy API

Backend Python pronto para um Hugging Face Space gratuito do tipo **Docker**.

1. Envie o conteúdo desta pasta para a raiz do Space.
2. Defina `ALLOWED_ORIGINS` com o domínio do frontend.
3. No frontend, defina `NEXT_PUBLIC_MDFY_API_URL` com a URL pública do Space.

Os uploads são temporários e removidos após a resposta. Em um Space gratuito, a primeira conversão depois da hibernação pode demorar.
