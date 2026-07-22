### N8N Agents 

source: [Link-Repo: github.com/n8n-io](https://github.com/n8n-io/n8n)

Try n8n instantly with npx (requires Node.js):

```npx n8n```

AWO: läuft bei mir nicht wegen Abhängigkeiten! 
```
npm warn ERESOLVE overriding peer dependency
npm warn While resolving: @ai-sdk/anthropic@3.0.99
...
Could not resolve dependency:
npm warn peer zod@"^3.25.76 || ^4.1.8" from @ai-sdk/anthropic@3.0.99
...
```

Or deploy with Docker:


```shell
docker volume create n8n_data
docker run -it --rm --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n docker.n8n.io/n8nio/n8n
```

AWO: Läuft nicht wegen docker.n8n.io pull-request-limit or login??