# MDfy API

Backend Python pronto para um Hugging Face Space gratuito do tipo **Docker**.

## Produção

Space: https://huggingface.co/spaces/fdossi/mdfy-api

1. Defina `ALLOWED_ORIGINS` com o domínio do frontend.
2. No frontend, defina `NEXT_PUBLIC_MDFY_API_URL` com a URL pública do Space.

Os uploads são temporários e removidos após a resposta. Em um Space gratuito, a primeira conversão depois da hibernação pode demorar.
