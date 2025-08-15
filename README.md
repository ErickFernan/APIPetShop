# 🐶 APIPetShop

<p align="justify">
Uma API RESTful robusta e modular para gerenciamento completo de um petshop, desenvolvida com Django REST Framework e encapsulada em Docker para máxima portabilidade.
</p>

---

## 👋 Introdução

<p align="justify">
APIPetShop é uma solução de back-end projetada para simular um ambiente de software real para um petshop. O projeto nasceu do desejo de aplicar conhecimentos práticos e, ao mesmo tempo, explorar novas tecnologias em um contexto de portfólio.
</p>

<p align="justify">
A API centraliza as principais operações de um petshop, incluindo:
</p>

- **Serviços de Estética:** 🛁 Gestão de agendamentos para banho e tosa.
- **Atendimento Veterinário:** 🩺 Controle de consultas, exames, cirurgias e tratamentos.
- **Loja:** 🛍️ Gerenciamento de estoque e venda de produtos.
- **Hotel Pet:** 🏨 Controle de hospedagem, reservas e disponibilidade.

---

## 🏗️ Arquitetura do Sistema

<p align="justify">
O projeto foi planejado para ser um ambiente de desenvolvimento completo e de fácil reprodução, utilizando Docker-compose. A arquitetura foi dividida em duas fases:
</p>

### Modelo Atual (Simplificado)
<p align="justify">
Atualmente, o projeto opera com uma arquitetura simplificada para focar no desenvolvimento do core da aplicação. Nesta fase, a <strong>PetshopAPI</strong> se comunica diretamente com os outros serviços.
</p>

![Modelo Simplificado](readme_images/petshopapisimplificado.drawio.svg)
<p align="center">Figura 1 - Modelo Simplificado</p>

### Modelo Planejado (Completo)
<p align="justify">
A visão final do projeto inclui o <strong>Kong</strong> como um API Gateway. Ele será responsável por unificar a comunicação, gerenciar o tráfego entre os serviços, e adicionar uma camada extra de segurança e observabilidade.
</p>

![Modelo Completo](readme_images/petshopapicompleto.drawio.svg)
<p align="center">Figura 2 - Modelo Completo</p>

---

## 🛠️ Tecnologias Utilizadas

| Ferramenta | Propósito |
| :--- | :--- |
| **Django REST (DRF)** | Framework principal para a construção da `PetshopAPI`, gerenciando rotas, serializers e views. |
| **PostgreSQL** | Banco de dados relacional principal para persistência dos dados da aplicação. |
| **Keycloak** | Gerenciador de identidade e acesso, responsável pela autenticação e autorização (OAuth 2.0 / OIDC). As regras de segurança, como complexidade de senhas, são centralizadas e configuráveis diretamente nele. |
| **MinIO** | Bucket de armazenamento S3-compatível para imagens, documentos e outros arquivos. |
| **Docker & Docker-compose**| Contentorização de todo o ambiente, garantindo portabilidade e facilidade na configuração. |
| **FakeSMTP** | Servidor SMTP de desenvolvimento para simular e testar o envio de e-mails. (Vai ser substituitdo pelo plano gratuito do Brevo)|
| **Kong (Planejado)** | API Gateway para orquestrar e proteger a comunicação entre os microsserviços. |
| **Flask & BeautifulSoup (Planejado)** | Utilizados no desenvolvimento do `Bot de Preços`. |
| **MongoDB (Planejado)** | Banco de dados NoSQL para armazenar dados não relacionais, como logs, cache e estatísticas. |
| **RabbitMQ + Celery (Planejado)** | Gerenciamento de tarefas assíncronas e filas, como envio de e-mails e geração de relatórios. |

---

## 💡 Detalhes do Design e Funcionalidades

### 🧱 PetshopAPI: Uma Arquitetura Modular

<p align="justify">
O núcleo do projeto, a <strong>PetshopAPI</strong>, foi desenhado com uma abordagem modular para garantir flexibilidade e desacoplamento. O sistema é dividido em sete aplicações Django, cada uma com uma responsabilidade específica:
</p>

- **APP Usuários:** Gerencia usuários, perfis, permissões e dados relacionados.
- **APP Pet:** Armazena e gerencia informações dos pets e seus tutores.
- **APP Produtos:** Centraliza o cadastro de produtos, servindo como fonte única de dados.
- **APP Loja:** Controla o estoque e as vendas de produtos da loja.
- **APP Banho/Tosa:** Gerencia os agendamentos e serviços de banho e tosa.
- **APP Hotel:** Administra as reservas e a ocupação do hotel para pets.
- **APP Saúde:** Focada no atendimento veterinário (consultas, exames, etc.).

<p align="justify">
A separação da <strong>APP Produtos</strong> é uma decisão de design estratégica. Ela permite que módulos como <strong>Loja</strong> e <strong>Banho/Tosa</strong> consumam os mesmos produtos de uma fonte única, evitando redundância e facilitando a gestão.
</p>

![Diagrama UML da API](readme_images/PETSHOPAPIUML.svg)
<p align="center">Figura 3 - Diagrama UML da API</p>

### 🔑 Convenções do Diagrama UML
- `+` **Público:** Atributos que podem ser alterados livremente.
- `-` **Privado/Restrito:** Atributos modificáveis apenas por métodos internos.
- `#` **Protegido:** Atributos que, uma vez definidos, não devem ser alterados.
- `*` **Lista Pré-definida:** O campo aceita apenas valores de uma lista de opções, garantindo a consistência dos dados.

### 🤖 Bot de Preços (Serviço Planejado)
<p align="justify">
Um serviço auxiliar será desenvolvido em <strong>Flask</strong> e <strong>BeautifulSoup</strong> para automatizar a coleta de preços de produtos. Através de uma rota REST, um usuário autorizado poderá solicitar uma busca que resultará em uma planilha Excel, armazenada no <strong>MinIO</strong> ou enviada por e-mail.
</p>

---

## 🚀 Iniciando o Projeto
<p align="justify">
Para executar o projeto em sua máquina local, siga os passos abaixo.
</p>

**Pré-requisitos:**
- Docker
- Docker Compose

---

### Passos para Instalação e Configuração

#### 1. Setup Inicial do Projeto

```bash
# Clone o repositório e acesse a pasta do projeto
git clone [https://github.com/seu-usuario/APIPetShop.git](https://github.com/seu-usuario/APIPetShop.git)
cd APIPetShop

# Selecione a branch de desenvolvimento (Opcional)
# Por padrão, você estará na branch 'main'. Para usar a versão em desenvolvimento:
git checkout apisimplificada

# Crie e configure seu arquivo de variáveis de ambiente
cp .envexample.txt .env

```
💡 Importante: Abra o arquivo .env e preencha todas as variáveis com as suas configurações locais (senhas, portas, etc.).

#### 2. Execução do Ambiente

```bash
# Suba os contêineres com Docker Compose
# O comando --build garante que a imagem da sua API seja reconstruída com as últimas alterações.
docker-compose up --build
```

💡 Importante: Após a conclusão, os serviços estarão disponíveis nos endereços indicados no terminal.

#### 3. Configuração Pós-Inicialização do Keycloak

Para que a integração entre a API e o Keycloak funcione corretamente, alguns passos manuais são necessários na primeira execução. Utilize a coleção do Postman fornecida para facilitar o processo.

```bash
3.1: Criar o "Client Scope"**
    * Na coleção do Postman, localize a pasta `Keycloak`.
    * Execute a requisição **`ADMIN - CREATE django-uuid Scope`**. Certifique-se de estar utilizando um token de administrador do Keycloak para esta chamada.

3.2: Habilitar Atributos Não Gerenciados**
    * Acesse o painel de administração do Keycloak (`http://localhost:8080/`).
    * No canto superior esquerdo, mude do realm `master` para o realm **`dev`**.
    * No menu lateral, vá em **Realm Settings** > **General**.
    * Ative a opção **Unmanaged Attributes** e salve.

3.3: Adicionar o Scope ao Cliente**
    * Ainda no realm `dev`, vá em **Clients** no menu lateral.
    * Selecione o cliente **`rest-client`**.
    * Vá para a aba **Client Scopes**.
    * Clique no botão **Add client scope** e adicione o scope `django_uuid` que você criou no passo 3.1.
```

#### 4. Finalização
<p align="justify">
Pronto! Seu ambiente está totalmente configurado. Agora você já pode utilizar as rotas da <strong>PetshopAPI</strong> para criar usuários, produtos e interagir com todas as funcionalidades do sistema.
</p>

---
## 🎥 Demonstração em Vídeo

> Em breve: um vídeo será disponibilizado aqui mostrando como clonar, configurar e testar o projeto localmente em sua máquina.

O vídeo abordará:

- Clonagem do repositório
- Configuração do ambiente (`.env`)
- Inicialização com `docker-compose`
- Acesso aos serviços (Swagger, Keycloak, MinIO, etc.)
- Exemplos de requisições autenticadas
---

## 📄 Documentação da API

<p align="justify">
Para facilitar a exploração e os testes dos endpoints, foi criada uma coleção completa no Postman. Você pode visualizar a documentação online ou importar a coleção e o ambiente de desenvolvimento para o seu aplicativo clicando no botão abaixo:
</p>

<div align="center">

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/26401442-a9363828-79c6-4216-81f2-6ad70efd50ec?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D26401442-a9363828-79c6-4216-81f2-6ad70efd50ec%26entityType%3Dcollection%26workspaceId%3Dc2450012-cccd-4464-bccc-4e4c5da8ccd1#?env%5Benvpetshopproject%5D=W3sia2V5IjoiYWRtaW5hY2Nlc3NUb2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6InRleHQiLCJzZXNzaW9uVmFsdWUiOiJleUpoYkdjaU9pSlNVekkxTmlJc0luUjVjQ0lnT2lBaVNsZFVJaXdpYTJsa0lpQTZJQ0pNV1Y5Q05sWllSV2M1YWpJd2NqWmFYMGhRVkdGcE0xY3lTbFZrZUVSTFVVZHZWVFJqUWpBNFNDMDBJbjAuZXlKbGVIQWlPakUzTlRRMU1UY3pNVFlzSS4uLiIsImNvbXBsZXRlU2Vzc2lvblZhbHVlIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJZ09pQWlTbGRVSWl3aWEybGtJaUE2SUNKTVdWOUNObFpZUldjNWFqSXdjalphWDBoUVZHRnBNMWN5U2xWa2VFUkxVVWR2VlRSalFqQTRTQzAwSW4wLmV5SmxlSEFpT2pFM05UUTFNVGN6TVRZc0ltbGhkQ0k2TVRjMU5EVXhOVFV4Tml3aWFuUnBJam9pWVRJMFpHSXhNalV0TkdFNE5TMDBNekZrTFdKbU16Y3RObU5tTVRVek5EQTFZVE0xSWl3aWFYTnpJam9pYUhSMGNEb3ZMMnh2WTJGc2FHOXpkRG80TURnd0wzSmxZV3h0Y3k5a1pYWWlMQ0poZFdRaU9sc2ljbVZoYkcwdGJXRnVZV2RsYldWdWRDSXNJbUZqWTI5MWJuUWlYU3dpYzNWaUlqb2laVFUwTXprMk5HSXRZVGd5TmkwME1USTFMV0UzTm1ZdE1EYzJOVFl4TTJGak1tRmxJaXdpZEhsd0lqb2lRbVZoY21WeUlpd2lZWHB3SWpvaWNtVnpkQzFqYkdsbGJuUWlMQ0p6WlhOemFXOXVYM04wWVhSbElqb2lZelk0T1dSbE16SXRPREU0TWkwME5EVXlMV0ZtWmpFdE9XSXlOemN6WXpOa01EY3pJaXdpWVdOeUlqb2lNU0lzSW5KbFlXeHRYMkZqWTJWemN5STZleUp5YjJ4bGN5STZXeUprWldaaGRXeDBMWEp2YkdWekxXUmxkaUlzSW05bVpteHBibVZmWVdOalpYTnpJaXdpZFcxaFgyRjFkR2h2Y21sNllYUnBiMjRpTENKemRYQmxjblZ6WlhJaVhYMHNJbkpsYzI5MWNtTmxYMkZqWTJWemN5STZleUp5WldGc2JTMXRZVzVoWjJWdFpXNTBJanA3SW5KdmJHVnpJanBiSW5acFpYY3RjbVZoYkcwaUxDSjJhV1YzTFdsa1pXNTBhWFI1TFhCeWIzWnBaR1Z5Y3lJc0ltMWhibUZuWlMxcFpHVnVkR2wwZVMxd2NtOTJhV1JsY25NaUxDSnBiWEJsY25OdmJtRjBhVzl1SWl3aWNtVmhiRzB0WVdSdGFXNGlMQ0pqY21WaGRHVXRZMnhwWlc1MElpd2liV0Z1WVdkbExYVnpaWEp6SWl3aWNYVmxjbmt0Y21WaGJHMXpJaXdpZG1sbGR5MWhkWFJvYjNKcGVtRjBhVzl1SWl3aWNYVmxjbmt0WTJ4cFpXNTBjeUlzSW5GMVpYSjVMWFZ6WlhKeklpd2liV0Z1WVdkbExXVjJaVzUwY3lJc0ltMWhibUZuWlMxeVpXRnNiU0lzSW5acFpYY3RaWFpsYm5Seklpd2lkbWxsZHkxMWMyVnljeUlzSW5acFpYY3RZMnhwWlc1MGN5SXNJbTFoYm1GblpTMWhkWFJvYjNKcGVtRjBhVzl1SWl3aWJXRnVZV2RsTFdOc2FXVnVkSE1pTENKeGRXVnllUzFuY205MWNITWlYWDBzSW1GalkyOTFiblFpT25zaWNtOXNaWE1pT2xzaWJXRnVZV2RsTFdGalkyOTFiblFpTENKdFlXNWhaMlV0WVdOamIzVnVkQzFzYVc1cmN5SXNJblpwWlhjdGNISnZabWxzWlNKZGZYMHNJbk5qYjNCbElqb2laVzFoYVd3Z2NISnZabWxzWlNJc0luTnBaQ0k2SW1NMk9EbGtaVE15TFRneE9ESXRORFExTWkxaFptWXhMVGxpTWpjM00yTXpaREEzTXlJc0ltVnRZV2xzWDNabGNtbG1hV1ZrSWpwbVlXeHpaU3dpYm1GdFpTSTZJa0ZrYldsdUlGUmxjM1JsSWl3aWNISmxabVZ5Y21Wa1gzVnpaWEp1WVcxbElqb2lZV1J0YVc0aUxDSm5hWFpsYmw5dVlXMWxJam9pUVdSdGFXNGlMQ0ptWVcxcGJIbGZibUZ0WlNJNklsUmxjM1JsSWl3aVpXMWhhV3dpT2lKaFpHMXBia0IwWlhOMFpTNWpiMjB1WW5JaWZRLmszWllfTzJjMGhRWV9LM2tQQkhvQ1VGMVVhRVdWaTE0U281cHVSR1lqbWdoQzdqeEc5a1Q2SHF6UmUtQUc3UXdxSXRQcGc3Vm5ybl95QVZSNWFLQVV2MDZ6bXBPRmF2czVxMFo1QldSNUpTS19BVjc0dS1nWTlPNVk4TjlMeWlJMnZJc00tcGdzTTY5U0RiVmFEaTNNZWpSck9GTTJHOGVXMGMtTFpWNURSdTlaTGpFWFp4NXNEMndRX253Mlc1S0NzMldLZHk0cUM1aGJoZlVXUVBGSFNuN3JWaWt0bWN6TEZEOTEwSkY3ZVlRUmlzSUhoTVIxQnlmU1paakdxd3RXTHdVOHlWUmRGTng1T3ppdXZjcUdKZ3lFQ1NrTlp3ZFk0M3RJX05Qb0xTVUdJOWxDRVRVb0VOTzN0YU1HZUJXSVl1TFpUdG85OThtVGJYaGlTa2kxdyIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJ1c2VyYWNjZXNzVG9rZW4iLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJkZWZhdWx0Iiwic2Vzc2lvblZhbHVlIjoibnVsbCIsImNvbXBsZXRlU2Vzc2lvblZhbHVlIjoibnVsbCIsInNlc3Npb25JbmRleCI6MX0seyJrZXkiOiJtZWR2ZXRhY2Nlc3NUb2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImRlZmF1bHQiLCJzZXNzaW9uVmFsdWUiOiJleUpoYkdjaU9pSlNVekkxTmlJc0luUjVjQ0lnT2lBaVNsZFVJaXdpYTJsa0lpQTZJQ0pNV1Y5Q05sWllSV2M1YWpJd2NqWmFYMGhRVkdGcE0xY3lTbFZrZUVSTFVVZHZWVFJqUWpBNFNDMDBJbjAuZXlKbGVIQWlPakUzTlRRMU1UY3pNVFlzSS4uLiIsImNvbXBsZXRlU2Vzc2lvblZhbHVlIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJZ09pQWlTbGRVSWl3aWEybGtJaUE2SUNKTVdWOUNObFpZUldjNWFqSXdjalphWDBoUVZHRnBNMWN5U2xWa2VFUkxVVWR2VlRSalFqQTRTQzAwSW4wLmV5SmxlSEFpT2pFM05UUTFNVGN6TVRZc0ltbGhkQ0k2TVRjMU5EVXhOVFV4Tml3aWFuUnBJam9pTjJOaFpEazBNemt0TVRjM09TMDBaak16TFRrMFpUY3RZekl4TURSalpqTmtORGxtSWl3aWFYTnpJam9pYUhSMGNEb3ZMMnh2WTJGc2FHOXpkRG80TURnd0wzSmxZV3h0Y3k5a1pYWWlMQ0poZFdRaU9pSmhZMk52ZFc1MElpd2ljM1ZpSWpvaVlXSmlNMkpoT1RVdE1EVmxNeTAwTVdFM0xUZ3pZakV0WmpFME5UUm1aalEzTWpJNUlpd2lkSGx3SWpvaVFtVmhjbVZ5SWl3aVlYcHdJam9pY21WemRDMWpiR2xsYm5RaUxDSnpaWE56YVc5dVgzTjBZWFJsSWpvaVl6RmlabUV4T0dJdE5UQTVOUzAwWkdZNUxUa3dZV010TldFMVlqVTFNVFZoWW1Oaklpd2lZV055SWpvaU1TSXNJbkpsWVd4dFgyRmpZMlZ6Y3lJNmV5SnliMnhsY3lJNld5SnRaV1JwWTI5ZmRtVjBaWEpwYm1GeWFXOGlMQ0prWldaaGRXeDBMWEp2YkdWekxXUmxkaUlzSW05bVpteHBibVZmWVdOalpYTnpJaXdpZFcxaFgyRjFkR2h2Y21sNllYUnBiMjRpWFgwc0luSmxjMjkxY21ObFgyRmpZMlZ6Y3lJNmV5SmhZMk52ZFc1MElqcDdJbkp2YkdWeklqcGJJbTFoYm1GblpTMWhZMk52ZFc1MElpd2liV0Z1WVdkbExXRmpZMjkxYm5RdGJHbHVhM01pTENKMmFXVjNMWEJ5YjJacGJHVWlYWDE5TENKelkyOXdaU0k2SW1WdFlXbHNJSEJ5YjJacGJHVWlMQ0p6YVdRaU9pSmpNV0ptWVRFNFlpMDFNRGsxTFRSa1pqa3RPVEJoWXkwMVlUVmlOVFV4TldGaVkyTWlMQ0psYldGcGJGOTJaWEpwWm1sbFpDSTZabUZzYzJVc0ltUnFZVzVuYjE5MWRXbGtJam9pWVRBeVptSTBOMlV0WkRJME15MDBaVFprTFRrd05XUXRaR1U1TkRkbU4yWTVZakl5SWl3aWJtRnRaU0k2SWsxbFpHbGpieUJXWlhSbGNtbHVZWEpwYnlJc0luQnlaV1psY25KbFpGOTFjMlZ5Ym1GdFpTSTZJbTFsWkdsamIzWmxkQ0lzSW1kcGRtVnVYMjVoYldVaU9pSk5aV1JwWTI4aUxDSm1ZVzFwYkhsZmJtRnRaU0k2SWxabGRHVnlhVzVoY21sdklpd2laVzFoYVd3aU9pSnRaV1JwWTI5MlpYUkFaVzFoYVd3dVkyOXRJbjAuSjNWVjFrTEozN3ZqdzByLTFWT3ZNYU9WMnVJUnNlWWczMXZvdzRCcWRYbEhPQXN0akdRYTZRSnhkemJOWVhDNkhQLVczS1hBM2pyVi1TRWhUSEJHbjVJbU1tNFd5WEhvMXVmVFhaaC1mUDR6T3JMQnZlcFgtcGNqRG93TjBxcWNPZG5USmhFSk03QkxTLW04R3ZaY0tpTXMybEVTUjk3WXRPTU9Ba0MycFZyb3MxeGZPNUZTQXpKWWZKYkhCNDVjaDgtR1ZFZjFtNENNcGhvUEtybmFKdVd2T3NxNGZlSFhYSEJjNkp0MXVqSTlDQl9QZFlEM1ZHaW5lNnlWemZBeWNpS1YtWUtYUHBxUE1TcHpaRTRfSlRES001X015U1hQMWtWUXhsRVB2UUNudW5RYmxyejZvalFXNlN0Q1JOTUdBS1J2eWlKNVZHbEYxcS0zYXFrN1FRIiwic2Vzc2lvbkluZGV4IjoyfSx7ImtleSI6Imdyb29tZXJhY2Nlc3NUb2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6ImV5SmhiR2NpT2lKU1V6STFOaUlzSW5SNWNDSWdPaUFpU2xkVUlpd2lhMmxrSWlBNklDSk1XVjlDTmxaWVJXYzVhakl3Y2paYVgwaFFWR0ZwTTFjeVNsVmtlRVJMVVVkdlZUUmpRakE0U0MwMEluMC5leUpsZUhBaU9qRTNOVFExTVRjek1UWXNJLi4uIiwiY29tcGxldGVTZXNzaW9uVmFsdWUiOiJleUpoYkdjaU9pSlNVekkxTmlJc0luUjVjQ0lnT2lBaVNsZFVJaXdpYTJsa0lpQTZJQ0pNV1Y5Q05sWllSV2M1YWpJd2NqWmFYMGhRVkdGcE0xY3lTbFZrZUVSTFVVZHZWVFJqUWpBNFNDMDBJbjAuZXlKbGVIQWlPakUzTlRRMU1UY3pNVFlzSW1saGRDSTZNVGMxTkRVeE5UVXhOaXdpYW5ScElqb2lZMlEwTTJRME5XWXRNR1F3WVMwMFlXVTFMV0UxWW1ZdE9HSTRPREV3TUdNMVpqVXlJaXdpYVhOeklqb2lhSFIwY0RvdkwyeHZZMkZzYUc5emREbzRNRGd3TDNKbFlXeHRjeTlrWlhZaUxDSmhkV1FpT2lKaFkyTnZkVzUwSWl3aWMzVmlJam9pTmpsbU1XRTNOVGN0WXpjek9TMDBPV1UyTFdFNFpEVXRZV0kwWVRNd05HRTRNRGxqSWl3aWRIbHdJam9pUW1WaGNtVnlJaXdpWVhwd0lqb2ljbVZ6ZEMxamJHbGxiblFpTENKelpYTnphVzl1WDNOMFlYUmxJam9pTW1VeVlqZ3dZbUV0T1RWbU55MDBPV1l5TFdJd016TXRPRFF4WlRJNFpXWXpZalkySWl3aVlXTnlJam9pTVNJc0luSmxZV3h0WDJGalkyVnpjeUk2ZXlKeWIyeGxjeUk2V3lKa1pXWmhkV3gwTFhKdmJHVnpMV1JsZGlJc0ltZHliMjl0WlhJaUxDSnZabVpzYVc1bFgyRmpZMlZ6Y3lJc0luVnRZVjloZFhSb2IzSnBlbUYwYVc5dUlsMTlMQ0p5WlhOdmRYSmpaVjloWTJObGMzTWlPbnNpWVdOamIzVnVkQ0k2ZXlKeWIyeGxjeUk2V3lKdFlXNWhaMlV0WVdOamIzVnVkQ0lzSW0xaGJtRm5aUzFoWTJOdmRXNTBMV3hwYm10eklpd2lkbWxsZHkxd2NtOW1hV3hsSWwxOWZTd2ljMk52Y0dVaU9pSmxiV0ZwYkNCd2NtOW1hV3hsSWl3aWMybGtJam9pTW1VeVlqZ3dZbUV0T1RWbU55MDBPV1l5TFdJd016TXRPRFF4WlRJNFpXWXpZalkySWl3aVpXMWhhV3hmZG1WeWFXWnBaV1FpT21aaGJITmxMQ0prYW1GdVoyOWZkWFZwWkNJNklqY3pZems0TTJNMUxUSXhNRFF0TkRJMlppMWlaRGRqTFRjd1pEQXlPREV6T1RJd09TSXNJbTVoYldVaU9pSm5jbTl2YldWeUlHSmhibWh2SUhSdmMyRWlMQ0p3Y21WbVpYSnlaV1JmZFhObGNtNWhiV1VpT2lKbmNtOXZiV1Z5SWl3aVoybDJaVzVmYm1GdFpTSTZJbWR5YjI5dFpYSWlMQ0ptWVcxcGJIbGZibUZ0WlNJNkltSmhibWh2SUhSdmMyRWlMQ0psYldGcGJDSTZJbWR5YjI5dFpYSkFaVzFoYVd3dVkyOXRJbjAuT00zaXpQaTRCOHh4X2pXckhaWlNMeGFiTldZRWVsY2pESV96eG1fNDFMQ2lkY2VLMUdJR3pObTNvZFhKY0hEQnM2VGh3QXMtSlJIdEU0NWF4UkVrR3FpTDIxcFFoRWpCVlNoSmpkRVl5OEtSVVk4dFVCU0ZHNlFiUVpySVZBUmRWanpxaVh0OGZtV2hjNEIyeUk0eXMwQzRMQWotVTBJY2pFWWE4TFBrOWFNRFdpcHFKOTlaM2dTUHV5aGYzQ2IwQ1dGZ3hZNEVZY2dhWEU1X2FUTW94cUl2TDlkQS1zcTd2NUh3VDBfTXIwTHhDejhEUU9qZGQwa2daYUd3V0U4VnE1SVFyV1hIY2N1LXVSdHA3Y3l0SXBMRTVrd0pncFZFS2NrYTMzMGo3ZHk0dEpUdWttMEhhX3BhaFNLdWRrQTNSNlhueUxQNE1SNHpOQjhmMjd3YlhBIiwic2Vzc2lvbkluZGV4IjozfSx7ImtleSI6ImF0ZW5kZW50ZWxvamFjY2Vzc1Rva2VuIiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiYW55Iiwic2Vzc2lvblZhbHVlIjoibnVsbCIsImNvbXBsZXRlU2Vzc2lvblZhbHVlIjoibnVsbCIsInNlc3Npb25JbmRleCI6NH0seyJrZXkiOiJhdGVuZGVudGVob3RlbGNjZXNzVG9rZW4iLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJleUpoYkdjaU9pSlNVekkxTmlJc0luUjVjQ0lnT2lBaVNsZFVJaXdpYTJsa0lpQTZJQ0pNV1Y5Q05sWllSV2M1YWpJd2NqWmFYMGhRVkdGcE0xY3lTbFZrZUVSTFVVZHZWVFJqUWpBNFNDMDBJbjAuZXlKbGVIQWlPakUzTlRRMU1UY3pNVGNzSS4uLiIsImNvbXBsZXRlU2Vzc2lvblZhbHVlIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJZ09pQWlTbGRVSWl3aWEybGtJaUE2SUNKTVdWOUNObFpZUldjNWFqSXdjalphWDBoUVZHRnBNMWN5U2xWa2VFUkxVVWR2VlRSalFqQTRTQzAwSW4wLmV5SmxlSEFpT2pFM05UUTFNVGN6TVRjc0ltbGhkQ0k2TVRjMU5EVXhOVFV4Tnl3aWFuUnBJam9pTjJFeE1HWm1aR1V0T1RabE5DMDBZamRqTFdGaE5ERXRPREExTW1WbFpHSXpOREV4SWl3aWFYTnpJam9pYUhSMGNEb3ZMMnh2WTJGc2FHOXpkRG80TURnd0wzSmxZV3h0Y3k5a1pYWWlMQ0poZFdRaU9pSmhZMk52ZFc1MElpd2ljM1ZpSWpvaU5URXdOVFEzWm1VdE9EaGhNeTAwWVRRM0xXSTBZV1l0TW1GaFpUUmlNMlE0WkdVNUlpd2lkSGx3SWpvaVFtVmhjbVZ5SWl3aVlYcHdJam9pY21WemRDMWpiR2xsYm5RaUxDSnpaWE56YVc5dVgzTjBZWFJsSWpvaU0yVTRZVEV5WVdRdE1tWTVNUzAwTm1VMUxUZzJabVV0TlRaa05EQTRNek5rTlRBMUlpd2lZV055SWpvaU1TSXNJbkpsWVd4dFgyRmpZMlZ6Y3lJNmV5SnliMnhsY3lJNld5SmtaV1poZFd4MExYSnZiR1Z6TFdSbGRpSXNJbTltWm14cGJtVmZZV05qWlhOeklpd2lkVzFoWDJGMWRHaHZjbWw2WVhScGIyNGlMQ0poZEdWdVpHVnVkR1ZmYUc5MFpXd2lYWDBzSW5KbGMyOTFjbU5sWDJGalkyVnpjeUk2ZXlKaFkyTnZkVzUwSWpwN0luSnZiR1Z6SWpwYkltMWhibUZuWlMxaFkyTnZkVzUwSWl3aWJXRnVZV2RsTFdGalkyOTFiblF0YkdsdWEzTWlMQ0oyYVdWM0xYQnliMlpwYkdVaVhYMTlMQ0p6WTI5d1pTSTZJbVZ0WVdsc0lIQnliMlpwYkdVaUxDSnphV1FpT2lJelpUaGhNVEpoWkMweVpqa3hMVFEyWlRVdE9EWm1aUzAxTm1RME1EZ3pNMlExTURVaUxDSmxiV0ZwYkY5MlpYSnBabWxsWkNJNlptRnNjMlVzSW1ScVlXNW5iMTkxZFdsa0lqb2lOamxqTTJSbU9Ua3RPR0l3WVMwMFpUTm1MV0U1TURjdE9USmtZekZoTUdSbE5qYzJJaXdpYm1GdFpTSTZJa0YwWlc1a1pXNTBaU0JJYjNSbGJDSXNJbkJ5WldabGNuSmxaRjkxYzJWeWJtRnRaU0k2SW1GMFpXNTBaVzUwWldodmRHVnNJaXdpWjJsMlpXNWZibUZ0WlNJNklrRjBaVzVrWlc1MFpTSXNJbVpoYldsc2VWOXVZVzFsSWpvaVNHOTBaV3dpTENKbGJXRnBiQ0k2SW1GMFpXNWtaVzUwWldodmRHVnNRR1Z0WVdsc0xtTnZiU0o5LnVBdGdqQUdVZk5tOHNacGhhS3RScnVKc2pyNUlYLUJyNWExaU9jdDBmOXRxUkoySE1UVWUwZWpjc1VxNmZOTzl5MkJmNnVJbW1pX0xPd0JJdnZKc1YzTnBoVEs3akxBcUMyMk44QXprbTVGMWNQWTB0aWpYT3VmMDVQODVvbEpYZGh0QUJ4YTNUX2tvdWI3NDd4TVdlOWlqM2MtQmZ0QmxRM2JZMnpVdlBUSlVpektZenlaY0VxRWZyR0RPRFVNRVJZUHlSUFVPa3FlN2ktTUlXNkpUSks5OGE3NXhqSVhacXg5NTFLaGtuaG1GSVdXcjJRMVdKTjlGTFB0d0FPM0hWa1dVaEFpSFdFTlRjeHpFUk5WbjlJd0tGVjhmOFRHMUFnUExsYmtmcUhnelRvRVJadndGTTFYNk5jM1NTeGtvRDZsSFhPNGtNWmJPRXlWRWlnTkJ3ZyIsInNlc3Npb25JbmRleCI6NX0seyJrZXkiOiJhdGVuZGVudGViYW5ob3Rvc2FUb2tlbiIsInZhbHVlIjoiIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImFueSIsInNlc3Npb25WYWx1ZSI6ImV5SmhiR2NpT2lKU1V6STFOaUlzSW5SNWNDSWdPaUFpU2xkVUlpd2lhMmxrSWlBNklDSk1XVjlDTmxaWVJXYzVhakl3Y2paYVgwaFFWR0ZwTTFjeVNsVmtlRVJMVVVkdlZUUmpRakE0U0MwMEluMC5leUpsZUhBaU9qRTNORFl6TURjME9EZ3NJLi4uIiwiY29tcGxldGVTZXNzaW9uVmFsdWUiOiJleUpoYkdjaU9pSlNVekkxTmlJc0luUjVjQ0lnT2lBaVNsZFVJaXdpYTJsa0lpQTZJQ0pNV1Y5Q05sWllSV2M1YWpJd2NqWmFYMGhRVkdGcE0xY3lTbFZrZUVSTFVVZHZWVFJqUWpBNFNDMDBJbjAuZXlKbGVIQWlPakUzTkRZek1EYzBPRGdzSW1saGRDSTZNVGMwTmpNd05UWTRPQ3dpYW5ScElqb2lNMlUwTWpVMlptUXRNVEk1T0MwME5qZGxMV0UwWlRFdFpqWmtNVE5qTURRek5UZ3lJaXdpYVhOeklqb2lhSFIwY0RvdkwyeHZZMkZzYUc5emREbzRNRGd3TDNKbFlXeHRjeTlrWlhZaUxDSmhkV1FpT2lKaFkyTnZkVzUwSWl3aWMzVmlJam9pTmpsak5UQTBNVE10TXpKaFpTMDBNMlptTFRrM1pEZ3RabUZoWkdRd1pEazJNemhqSWl3aWRIbHdJam9pUW1WaGNtVnlJaXdpWVhwd0lqb2ljbVZ6ZEMxamJHbGxiblFpTENKelpYTnphVzl1WDNOMFlYUmxJam9pTUROaU9HTmlPVFF0T0RobU5TMDBPVGxrTFRnMFlXUXROVFU0T0dFNE56WTNaV1l6SWl3aVlXTnlJam9pTVNJc0luSmxZV3h0WDJGalkyVnpjeUk2ZXlKeWIyeGxjeUk2V3lKa1pXWmhkV3gwTFhKdmJHVnpMV1JsZGlJc0ltOW1abXhwYm1WZllXTmpaWE56SWl3aVlYUmxibVJsYm5SbFgySmhibWh2ZEc5ellTSXNJblZ0WVY5aGRYUm9iM0pwZW1GMGFXOXVJbDE5TENKeVpYTnZkWEpqWlY5aFkyTmxjM01pT25zaVlXTmpiM1Z1ZENJNmV5SnliMnhsY3lJNld5SnRZVzVoWjJVdFlXTmpiM1Z1ZENJc0ltMWhibUZuWlMxaFkyTnZkVzUwTFd4cGJtdHpJaXdpZG1sbGR5MXdjbTltYVd4bElsMTlmU3dpYzJOdmNHVWlPaUpsYldGcGJDQndjbTltYVd4bElpd2ljMmxrSWpvaU1ETmlPR05pT1RRdE9EaG1OUzAwT1Rsa0xUZzBZV1F0TlRVNE9HRTROelkzWldZeklpd2laVzFoYVd4ZmRtVnlhV1pwWldRaU9tWmhiSE5sTENKa2FtRnVaMjlmZFhWcFpDSTZJalpoWTJRNU1UQmtMVEV5TnprdE5HVTNOUzA0WTJKakxUbG1NalprTkRFMlpESTJNQ0lzSW01aGJXVWlPaUpCZEdWdVpHVnVkR1VnUW1GdWFHOTBiM05oSWl3aWNISmxabVZ5Y21Wa1gzVnpaWEp1WVcxbElqb2lZWFJsYm5SbGJuUmxZbUZ1YUc5MGIzTmhJaXdpWjJsMlpXNWZibUZ0WlNJNklrRjBaVzVrWlc1MFpTSXNJbVpoYldsc2VWOXVZVzFsSWpvaVFtRnVhRzkwYjNOaElpd2laVzFoYVd3aU9pSmhkR1Z1WkdWdWRHVmlZVzVvYjNSdmMyRkFaVzFoYVd3dVkyOXRJbjAubGEwMEZFbkcxUXZKaXZpVVVBaXQwM2V4UnNubENMcldIMWpmZ0FPRW8zcFc0TUNhWGpldENoX2pZTVhvRXhPSjVFQkxtemtZYzkxN2NTTWlNLVpucHFUelJwbDZNeVdqVGhtZFJERGpSSzJmYUJybV92TlB1SWE4bDNVbFI5a1J1bHpVLTVLUnFFOVBLOWZubXRDMV94Nm11TWxRQi1GVVJyLXZtTXctYTZUZWV0RVA3TVh4M0dzM1hXajFHcFRVcG1OU1d0ajNiRDctTWpBMm9PcUhGcWtWcFcxQ2hUN3VpTVhQQjczUldkWjExaHYyNXQ4UjRNQ3F0bTlIaWk2NGtOaVJMUll2SFN2RlBfOVN5UW5LdXlhOERUS2FLd0lDRk5LWVNDNUVQOGRKcGk1dHk4OEliZzRyamZaekp2M3dvX21POHdxclBXM0N4UDRTWjJETHZRIiwic2Vzc2lvbkluZGV4Ijo2fSx7ImtleSI6ImF0ZW5kZW50ZWJhbmhvdG9zYWNjZXNzVG9rZW4iLCJ2YWx1ZSI6IiIsImVuYWJsZWQiOnRydWUsInR5cGUiOiJhbnkiLCJzZXNzaW9uVmFsdWUiOiJleUpoYkdjaU9pSlNVekkxTmlJc0luUjVjQ0lnT2lBaVNsZFVJaXdpYTJsa0lpQTZJQ0pNV1Y5Q05sWllSV2M1YWpJd2NqWmFYMGhRVkdGcE0xY3lTbFZrZUVSTFVVZHZWVFJqUWpBNFNDMDBJbjAuZXlKbGVIQWlPakUzTlRRMU1UY3pNVGNzSS4uLiIsImNvbXBsZXRlU2Vzc2lvblZhbHVlIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJZ09pQWlTbGRVSWl3aWEybGtJaUE2SUNKTVdWOUNObFpZUldjNWFqSXdjalphWDBoUVZHRnBNMWN5U2xWa2VFUkxVVWR2VlRSalFqQTRTQzAwSW4wLmV5SmxlSEFpT2pFM05UUTFNVGN6TVRjc0ltbGhkQ0k2TVRjMU5EVXhOVFV4Tnl3aWFuUnBJam9pWW1ObE1EbGpNekV0TXpKaU9TMDBOMkZrTFRreFltUXRNalF3TXpJd05HUmpZakJsSWl3aWFYTnpJam9pYUhSMGNEb3ZMMnh2WTJGc2FHOXpkRG80TURnd0wzSmxZV3h0Y3k5a1pYWWlMQ0poZFdRaU9pSmhZMk52ZFc1MElpd2ljM1ZpSWpvaU1tUmhOelZsT0RZdE5UbGtNQzAwT1RNNExXSTVNR0l0Tm1SbU1EWXlZelJoT1dNMUlpd2lkSGx3SWpvaVFtVmhjbVZ5SWl3aVlYcHdJam9pY21WemRDMWpiR2xsYm5RaUxDSnpaWE56YVc5dVgzTjBZWFJsSWpvaU16VXpaakkzTURBdFpqSmlaUzAwTmpFd0xUZzRZalV0TTJZME1tVTNNV1ZrTnpSbElpd2lZV055SWpvaU1TSXNJbkpsWVd4dFgyRmpZMlZ6Y3lJNmV5SnliMnhsY3lJNld5SmtaV1poZFd4MExYSnZiR1Z6TFdSbGRpSXNJbTltWm14cGJtVmZZV05qWlhOeklpd2lZWFJsYm1SbGJuUmxYMkpoYm1odmRHOXpZU0lzSW5WdFlWOWhkWFJvYjNKcGVtRjBhVzl1SWwxOUxDSnlaWE52ZFhKalpWOWhZMk5sYzNNaU9uc2lZV05qYjNWdWRDSTZleUp5YjJ4bGN5STZXeUp0WVc1aFoyVXRZV05qYjNWdWRDSXNJbTFoYm1GblpTMWhZMk52ZFc1MExXeHBibXR6SWl3aWRtbGxkeTF3Y205bWFXeGxJbDE5ZlN3aWMyTnZjR1VpT2lKbGJXRnBiQ0J3Y205bWFXeGxJaXdpYzJsa0lqb2lNelV6WmpJM01EQXRaakppWlMwME5qRXdMVGc0WWpVdE0yWTBNbVUzTVdWa056UmxJaXdpWlcxaGFXeGZkbVZ5YVdacFpXUWlPbVpoYkhObExDSmthbUZ1WjI5ZmRYVnBaQ0k2SW1NeVpqTXhaREZrTFdNNFpESXROR1UzWkMwNU1USXdMV001TlRobFl6Y3laakJqWVNJc0ltNWhiV1VpT2lKQmRHVnVaR1Z1ZEdVZ1FtRnVhRzkwYjNOaElpd2ljSEpsWm1WeWNtVmtYM1Z6WlhKdVlXMWxJam9pWVhSbGJuUmxiblJsWW1GdWFHOTBiM05oSWl3aVoybDJaVzVmYm1GdFpTSTZJa0YwWlc1a1pXNTBaU0lzSW1aaGJXbHNlVjl1WVcxbElqb2lRbUZ1YUc5MGIzTmhJaXdpWlcxaGFXd2lPaUpoZEdWdVpHVnVkR1ZpWVc1b2IzUnZjMkZBWlcxaGFXd3VZMjl0SW4wLms2b3RMLTRYanVQb3VSUEttWHBobDdXY09LX3F0R0R6OVQxTllaM1F6OWxCRDNCQ3Z0R19lSEZmb3Fkc1dmX2d3QTlzWUNPZmYtUnhBeXFIWXhnNHU4MXBBcGRwcXM0UTVTQVBXMEw1WlJlcnNHb2hveEZDRVRyeVRDM3RESC1FWHNWRW12UEIyaU1WcDlQQUp5V202VU0xcWNRZHl1N0IweGo0eEM3akc0T1pVY0R1Rmd6T0VvMUtsdjY4WHZ5cEdQaTNRd3pjdUZVd09kaEVFY3I1ZExrTkhIRXd1QzdnVmkyN2tMMzNxa2ExdjlWTGpCOGs1ZVl5MG8yOVhWSTZ6eFdEXy1qRGZCVXlheXZJYVZLODNGOFhBX3BlUDJMLXJ2ZU84RFJncHdwY2NFTXVTOXJqM3JTZFJzWkZja2Fza19raWpSNkl5ZV85LWphTmpGZkpSQSIsInNlc3Npb25JbmRleCI6N31d)

</div>
<br>

<p align="justify">
Além da coleção do Postman, após iniciar o projeto localmente, a documentação interativa via Swagger UI também estará disponível em <code>http://localhost:'porta'/swagger/</code>.
</p>

---

<div align="justify">

## 🌿 Estratégia de Branches

Este projeto utiliza uma estratégia de branches para organizar o desenvolvimento e manter um histórico limpo e estável:

* **`main`**:
    * Contém a versão estável e mais recente do projeto.
    * É a branch recomendada para testes ou implementações de produção.
    * O histórico de commits é mantido limpo e significativo através do uso de *squash commits*.

* **`apisimplificada`**:
    * Branch de desenvolvimento principal onde o modelo simplificado (Figura 1) está sendo construído.
    * Contém o trabalho em andamento antes de ser considerado estável para a `main`.

* **`Branches de Features`** (ex: `feat/user-auth`, `fix/login-bug`):
    * Novas funcionalidades, melhorias e correções de bugs são desenvolvidas em branches separadas, partindo da `apisimplificada`.
    * Isso permite o desenvolvimento paralelo e isolado de cada tarefa.

> **Nota sobre Squash Commit:**
> Ao finalizar uma feature, os múltiplos commits da sua branch (ex: "WIP", "fix typo", "final adjustments") são agrupados (*squashed*) em um único commit descritivo antes de serem mesclados na branch `apisimplificada` ou `main`. Esta prática é fundamental para manter o histórico do projeto legível e fácil de auditar.

---

## 🛣️ Roadmap e Status do Projeto
<p align="justify">
Este projeto está em desenvolvimento contínuo. Abaixo está uma visão geral das tarefas.
</p>

### ✅ Concluído
* **Estruturação e Configuração do Ambiente:**
    * [x] Modelagem completa dos serviços do projeto e do banco de dados relacional.
    * [x] Configuração do ambiente de desenvolvimento com Docker, incluindo `docker-compose.yml` e `Dockerfile` para o serviço da API.
    * [x] Inicialização do projeto Django com configurações iniciais e gestão de variáveis de ambiente (`.env`).

* **Integração e Autenticação:**
    * [x] Integração com o Keycloak para gerenciamento de autenticação e autorização baseada em `roles`.
    * [x] Configuração inicial do realm do Keycloak via JSON para automação.
    * [x] Sincronização do ID do usuário entre Django e Keycloak para garantir consistência de dados.
    * [x] Integração com o MinIO para armazenamento de objetos, incluindo funções de upload, update e delete de arquivos.

* **Desenvolvimento do Core da API:**
    * [x] Implementação de todos os `models`, `serializers` e `views` (CRUD inicial) para as 7 aplicações.
    * [x] Adição de documentação interativa da API com Swagger/OpenAPI.
    * [x] Personalização completa das rotas em todas as aplicações (`produtos`, `usuarios`, `pet`, `loja`, `hotel`, `banhotosa` e `saude`).
    * [x] Implementação de filtros avançados com `django-filter` nos endpoints de listagem.

* **Regras de Negócio e Validações:**
    * [x] Implementação de validações complexas, como unicidade de documentos por tipo e regras de negócio para criação e exclusão de dados de usuários.
    * [x] Criação de exclusão atômica (`transaction.atomic`), garantindo que os dados no banco e os arquivos no MinIO sejam removidos de forma segura e simultânea.
    * [x] Adição de regras nos `models` para garantir a integridade relacional entre `roles` de usuários e suas áreas de atuação.
    * [x] Adição de proteção na exclusão de serviços com agendamentos futuros.

* **Qualidade, Manutenibilidade e Correções:**
    * [x] Implementação de um sistema de logging e aprimoramento do tratamento de exceções em toda a aplicação. (Precisa ser aprimorado)
    * [x] Criação de funções utilitárias para centralizar as chamadas ao Keycloak, facilitando a manutenção.
    * [x] Resolução de bugs críticos, incluindo a dissociação do username do Keycloak do e-mail, a consistência de UUIDs no token JWT e a prevenção de salvamento de arquivos órfãos no MinIO.
    * [x] Verificação e atualização das imagens e diagramas do projeto.


### ⏳ Em Execução
   * [ ] Revisão e organização final do README para a primeira versão estável.

### 🗺️ Backlog e Melhorias Futuras
- **Testes:** Implementar testes unitários e de integração com `pytest`.
- **Bot de Preços:** Desenvolver e integrar o serviço de coleta de preços.
- **Integração com Kong:** Adicionar o Kong à arquitetura como API Gateway.
- **IA para Geração de Conteúdo:** Integrar a API com um modelo de linguagem (como Llama 3) para gerar automaticamente descrições de raças.
- **Logs de Auditoria de Segurança:** Implementar logs detalhados para registrar sucessos e falhas de autenticação (`KeyCloakAuthentication`) e autorização (`HasRolePermission`), facilitando auditorias e a detecção de atividades suspeitas.
- **Soft Delete:** Criar uma branch para demonstrar a implementação de exclusão lógica.
- **Validação de Competência por Função:** Implementar uma regra de negócio na `APP Saúde` para validar se o usuário designado como responsável por um serviço (como uma cirurgia) possui a função (`role`) apropriada (ex: `Veterinário`), garantindo a integridade e a lógica dos dados.
- **Refatoração de Filtros:** Otimizar os filtros do `django-filter` para uma sintaxe mais declarativa e limpa.
- **Sistema de Filas Assíncronas:** Implementar um sistema de gerenciamento de filas (ex: com **RabbitMQ** + **Celery**) para processar tarefas em segundo plano, como o envio de e-mails ou a geração de relatórios do `Bot de Preços`.
- **Banco NoSQL (MongoDB):** Adicionar suporte a banco de dados NoSQL (ex: MongoDB) para armazenar dados não relacionais, como logs, histórico ou cache.

> 💡 A ideia de usar um banco NoSQL como o MongoDB é complementar o PostgreSQL, armazenando dados que não exigem estrutura relacional rígida. Isso pode incluir logs, dados históricos, documentos grandes ou até estatísticas geradas automaticamente.
- **Vídeo Tutorial:** Gravar e disponibilizar um vídeo demonstrando como clonar, configurar e executar o projeto localmente.

- **Atualização Automática de Estoque (via Signals):** Implementar `signals` do Django para atualizar o estoque de produtos automaticamente ao realizar vendas ou reservas.

> 💡 O uso de `signals` no Django garante que a lógica de atualização de estoque esteja acoplada ao fluxo de negócio da aplicação, mantendo o controle e a rastreabilidade dentro do código.

- **Acesso Seguro a Arquivos com "Presigned URLs":** Refatorar a forma como a API retorna links para arquivos no MinIO. Em vez de links diretos, a API gerará *Presigned URLs* — links temporários e seguros com tempo de expiração limitado. Isso garante que apenas usuários autorizados possam acessar os arquivos, e somente por um curto período, sem a necessidade de tornar os arquivos públicos.

---

## 📝 Decisões de Design e Anotações Técnicas

- **Sincronização de IDs de Usuário (Django & Keycloak):**
<p align="justify">
Inicialmente, o sistema utilizava UUIDs distintos para um mesmo usuário no banco de dados do Django e no Keycloak. Isso exigia uma consulta extra ao banco para validar permissões, gerando um potencial gargalo de desempenho e um risco de segurança em uma aplicação de maior escala. Para resolver isso, o ID do usuário do Django foi adicionado como um atributo customizado (`custom attribute`) ao token JWT gerado pelo Keycloak. Dessa forma, ao decodificar o token na API, temos acesso imediato a ambos os identificadores, eliminando a necessidade de consultas extras e tornando a verificação de permissões mais segura e eficiente.
</p>

- **Proteção de Agendamentos Futuros na Exclusão de Serviços:**
<p align="justify">
Foi implementada uma validação para impedir a exclusão de um tipo de serviço (ex: 'Tosa Higiênica') se ele estiver associado a qualquer agendamento com data futura. Essa regra de negócio é crucial para garantir a integridade da agenda e evitar que clientes tenham seus serviços cancelados inesperadamente. A exclusão só é permitida se não houver compromissos futuros vinculados àquele serviço.
</p>

- **Hard Delete vs. Soft Delete:**
<p align="justify">
Atualmente, o projeto utiliza exclusão física (hard delete). Esta abordagem foi escolhida por ser um projeto de portfólio, permitindo explorar desafios como o rollback de exclusões em conjunto com o Keycloak. Para um projeto comercial, a implementação de soft delete seria a prática recomendada.
</p>

- **Atualização de Serviços com Tempo Fixo:**
> 💡 Para garantir a integridade da agenda, o campo `execution_time` em um serviço de banho/tosa não pode ser alterado após a criação. Para modificar o tempo, um **novo tipo de serviço** deve ser criado. Isso evita conflitos e sobreposição de horários. Para gerenciar a transição, ao criar um novo serviço com um nome já existente, o antigo é renomeado para `"<nome>-desativado"`.

- **Uso de `BaseViewSet`:**
<p align="justify">
Muitas views utilizam `ModelViewSet` para agilizar o desenvolvimento. Em um ambiente de produção, é recomendado o uso de `mixins` mais específicos ou a declaração explícita dos métodos para expor apenas os endpoints estritamente necessários.
</p>

- **Garantia de Consistência na Exclusão de Arquivos:**
<p align="justify">
Para evitar a existência de arquivos órfãos no MinIO (um arquivo que existe no armazenamento, mas sem referência no banco de dados), a lógica de exclusão foi envolvida em um bloco <code>transaction.atomic</code> do Django. Isso garante que o arquivo no bucket só seja removido se, e somente se, o registro correspondente no banco de dados for excluído com sucesso. Se a operação no banco falhar, a transação inteira é revertida (rollback), e o arquivo permanece intacto, mantendo a consistência dos dados.
</p>

---

<p align="justify">
<em>Este README será atualizado continuamente à medida que o projeto evolui. Sinta-se à vontade para explorar, testar e contribuir!</em>
</p>
