# Dashboard de Vendas 2024 - Guia de Implantação no Streamlit Cloud

Este pacote contém um dashboard interativo desenvolvido com Streamlit para análise de vendas de 2024, pronto para ser implantado no Streamlit Cloud e compartilhado através de um link público.

## Conteúdo do Pacote

- `app.py`: Aplicação principal do dashboard Streamlit
- `requirements.txt`: Lista de dependências Python necessárias
- `Vendas2024.xlsx`: Arquivo de dados original
- `Vendas2024_Processado.csv`: Arquivo de dados processado
- Arquivos CSV de análises específicas:
  - `analise_vendas_mensais.csv`
  - `analise_vendedores.csv`
  - `analise_vendedores_mensal.csv`
  - `analise_top10_clientes.csv`
  - `analise_comportamento_clientes.csv`
  - `analise_resumo_moedas.csv`

## Instruções para Implantação no Streamlit Cloud

### Passo 1: Criar uma conta no Streamlit Cloud

1. Acesse [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Clique em "Sign up" para criar uma nova conta
3. Você pode se cadastrar usando sua conta GitHub, Google ou e-mail

### Passo 2: Preparar o repositório no GitHub

1. Crie um novo repositório no GitHub:
   - Acesse [https://github.com/new](https://github.com/new)
   - Dê um nome ao repositório (ex: `dashboard-vendas-2024`)
   - Escolha a opção "Public" para que o Streamlit Cloud possa acessá-lo
   - Clique em "Create repository"

2. Faça upload dos arquivos deste pacote para o repositório:
   - Clique no botão "uploading an existing file"
   - Arraste todos os arquivos deste pacote ou selecione-os do seu computador
   - Clique em "Commit changes"

### Passo 3: Implantar no Streamlit Cloud

1. Acesse o [Streamlit Cloud](https://streamlit.io/cloud) e faça login
2. Clique no botão "New app" no canto superior direito
3. Preencha os campos:
   - **Repository**: Selecione o repositório que você acabou de criar
   - **Branch**: main (ou master, dependendo do seu repositório)
   - **Main file path**: app.py
   - **App name**: dashboard-vendas-2024 (ou outro nome de sua preferência)
4. Clique em "Deploy!"

O Streamlit Cloud irá automaticamente:
- Detectar o arquivo requirements.txt e instalar as dependências
- Executar o app.py e iniciar o dashboard
- Fornecer um URL público para acesso ao dashboard

### Passo 4: Compartilhar o Dashboard

Após a implantação bem-sucedida, você receberá um URL público no formato:
```
https://username-dashboard-vendas-2024-app-xyz123.streamlit.app
```

Este link pode ser compartilhado com qualquer pessoa, permitindo que eles acessem o dashboard sem necessidade de login ou instalação.

## Opções de Personalização no Streamlit Cloud

### Configurações de Privacidade

1. No painel do Streamlit Cloud, selecione seu app
2. Clique na guia "Settings"
3. Em "Sharing", você pode escolher:
   - **Public**: Qualquer pessoa com o link pode acessar
   - **Private**: Apenas usuários autorizados podem acessar (requer plano pago)

### Configurações de Recursos

No mesmo painel de configurações, você pode ajustar:
- Memória alocada para o app
- Tempo máximo de inatividade antes do app hibernar
- Opções de tema e aparência

## Manutenção e Atualizações

Para atualizar o dashboard:
1. Faça as alterações necessárias nos arquivos locais
2. Faça upload das versões atualizadas para o repositório GitHub
3. O Streamlit Cloud detectará automaticamente as mudanças e reimplantará o app

## Solução de Problemas

Se o dashboard não carregar corretamente:
1. Verifique os logs de erro no painel do Streamlit Cloud
2. Confirme que todos os arquivos de dados estão presentes no repositório
3. Verifique se o requirements.txt contém todas as dependências necessárias

## Recursos Adicionais

- [Documentação do Streamlit](https://docs.streamlit.io/)
- [Fórum da Comunidade Streamlit](https://discuss.streamlit.io/)
- [Exemplos de Apps Streamlit](https://streamlit.io/gallery)

---

© 2025 Dashboard de Vendas
