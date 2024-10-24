# APIPetShop

## Introdução:
<p align="justify"> 
Recentemente, decidi aplicar os conhecimentos que adquiri ao longo de dois anos de trabalho e, ao mesmo tempo, utilizar este projeto para estudar novas ferramentas, criando algo para meu portfólio. Para isso, imaginei uma situação do mundo real e desenvolvi uma solução. Assim, surgiu a ideia de criar uma API para um petshop.
</p>

<p align="justify"> 
O projeto abrange as principais funções relacionadas a pets, reunidas em um único serviço: banho e tosa, atendimento veterinário, venda de produtos pet e hotel para pets.
</p>

<p align="justify"> 
Após definir o escopo do projeto, escolhi as tecnologias que utilizaria, conforme ilustrado na Figura 1 abaixo. A proposta é que este sistema funcione como um ambiente de desenvolvimento completo, encapsulado em um Docker-compose, para facilitar o download, as melhorias e os testes.
</p>

![Modelo desejado](readme_images/petshopapicompleto.drawio.svg)
<p align="center"> 
figura 1 - Modelo completo
</p>

## Especificações:

* Keycloak: 
<p align="justify"> 
- O Keycloak é uma excelente ferramenta de autenticação e autorização, oferecendo diversos recursos nessa área. Neste projeto, sua principal função será gerenciar a autenticação e autorização dos serviços, além de aproveitar funcionalidades relacionadas a usuários, como envio de e-mails, autenticação em dois fatores e controle de contas.
</p>

* FakeSMTP: 
<p align="justify"> 
- Como este é um ambiente de desenvolvimento, optei por usar o FakeSMTP para simular as funções que dependem de e-mail. Ele será um auxiliar nos testes, mas, em um ambiente de produção, poderá ser facilmente substituído por um serviço de SMTP da empresa.
</p>

* PostgreSQL (PSQL): 
<p align="justify"> 
- Será o banco de dados principal do sistema.
</p>

* MinIO: 
<p align="justify"> 
- Funcionará como o bucket de armazenamento para imagens, documentos e outros dados importantes.
</p>

* PetshopAPI: 
<p align="justify"> 
- Este será o núcleo do projeto. Todas as aplicações definidas estarão concentradas aqui, sendo responsável pelas rotas REST, utilizando o Django REST Framework (DRF).
</p>

* Kong: 
<p align="justify"> 
- O Kong é uma ferramenta que ainda estou explorando, sendo um dos motivos pelos quais iniciei este projeto. A ideia é que ele funcione como um API Gateway, unificando o projeto e gerenciando a comunicação entre os serviços. No entanto, como ainda não tenho familiaridade suficiente, decidi simplificar o modelo original (Figura 1) para o apresentado na Figura 2, removendo o Kong temporariamente. Assim, posso concluir o projeto com as habilidades que já possuo e, posteriormente, estudar e implementar o Kong.
</p>

<p align="justify"> 
Essa alteração foi feita por praticidade, sem impactos negativos no desenvolvimento. Além disso, me permitirá explorar práticas como o uso de branches e testar o squash commit, outra técnica que tenho interesse em aplicar.
</p>

![Modelo Simplificado](readme_images/petshopapisimplificado.drawio.svg)
<p align="center"> 
figura 2 - Modelo simplificado
</p>

## Detalhamento
<p align="justify">
Definido como o projeto será iniciado, vou detalhar algumas funções e particularidades dos serviços "PetshopAPI" e "Bot de Preços".
</p> 

* Bot de Preços:

<p align="justify">
O funcionamento do bot ainda não está completamente definido, mas a ideia básica é que ele será desenvolvido como um serviço em Flask juntamente com o BeautifulSoup. Ele terá uma rota REST onde o usuário, que precisa estar autenticado e autorizado, enviará as especificações e detalhes do que deseja buscar em formato JSON. O bot processará essas informações, executará a busca e gerará uma planilha Excel com os dados coletados.
</p>

<p align="justify">
Essas informações serão armazenadas no bucket MinIO e/ou enviadas por e-mail ao usuário quando prontas. Alternativamente, o bot poderá enviar um link para download ou o próprio arquivo diretamente. Ainda preciso definir melhor alguns detalhes, mas essa é a ideia geral de como o bot deverá funcionar.
</p> 

* PetshopAPI:

<p align="justify">
Como mencionado anteriormente, o PetshopAPI será uma API desenvolvida utilizando o Django REST Framework (DRF), que centralizará as principais funcionalidades que um petshop poderia necessitar. Durante a modelagem do projeto, optei por um design modular, visando a fácil integração e desacoplamento de funcionalidades. Para isso, o sistema será dividido em sete aplicações, cada uma focada em um aspecto específico do negócio:
</p>

1. APP Usuários: 
<p align="justify">
- Gerencia toda a parte relacionada aos usuários do sistema, como registro, autenticação e controle de permissões.
</p> 

2. APP Saúde: 
<p align="justify">
- Focada no atendimento médico dos pets, incluindo exames, consultas, cirurgias e tratamentos.
</p> 

3. APP Pet: 
<p align="justify">
- Responsável por armazenar e gerenciar informações sobre os pets, como tutor, características e perfil.
</p> 

4. APP Banho/Tosa: 
<p align="justify">
- Cuida da parte de serviços de banho e tosa, com gestão de agendamentos e execução desses serviços.

5. APP Hotel: 
<p align="justify">
- Garante o controle da hospedagem de pets, incluindo disponibilidade de quartos, reservas e check-ins.
</p> 

6. APP Loja: 
<p align="justify">
- Gerencia o estoque e a venda de produtos pet, abrangendo desde o cadastro de produtos até a conclusão das vendas.
</p> 

7. APP Produtos: 
<p align="justify">
- Centraliza as informações dos produtos vendidos ou utilizados nos serviços, funcionando como um banco de dados compartilhado entre as outras aplicações.
</p> 

![UML API](readme_images/PETSHOPAPIUML.svg)
<p align="center"> 
figura 3 - Diagrama UML
</p> 

<p align="justify">
Você pode estar se perguntando por que existe uma aplicação dedicada apenas para os produtos. A razão é que, para garantir a modularidade e a flexibilidade do sistema, as aplicações que compartilham serviços comuns, como Banho/Tosa e Loja, precisam de um intermediário central. Ao separar os dados dos produtos em uma aplicação própria, é possível integrar diferentes serviços que utilizam essas mesmas informações, evitando redundâncias e facilitando a manutenção.
</p> 

<p align="justify">
Se observar o diagrama UML na Figura 3, verá que tanto a aplicação de Banho/Tosa quanto a de Loja utilizam as mesmas informações sobre produtos. Isso justifica a necessidade de uma aplicação separada para produtos, permitindo que, por exemplo, uma clínica veterinária que não ofereça serviços de banho e tosa ainda possa utilizar o sistema sem complicações. Nesse caso, bastaria não incluir a APP Banho/Tosa na implementação, e o restante do sistema continuaria funcionando normalmente.
</p> 

<p align="justify">
Esse design também facilita a personalização e expansão do sistema. Um petshop que não ofereça um serviço específico, como saúde ou hospedagem, pode adquirir apenas os módulos necessários. Se futuramente decidir expandir seus serviços, basta adicionar os módulos correspondentes sem necessidade de grandes adaptações ou retrabalho. Essa flexibilidade oferece uma solução prática tanto para o presente quanto para futuras expansões do negócio.
</p> 

<p align="justify">
Para concluir a análise do diagrama UML apresentado na Figura 3, vou comentar algumas definições importantes adotadas neste projeto. Utilizei os caracteres #, + e - para definir o tipo de acesso aos dados, sendo:
</p> 

#: Variáveis privadas que, após serem modificadas, não podem ser alteradas novamente.

+: Variáveis públicas, que podem ser alteradas a qualquer momento.

-: Informações restritas, que só podem ser modificadas por métodos internos ou agentes específicos.

<p align="justify">
Se você observar o UML, notará que algumas variáveis possuem um *. Esse asterisco indica que as opções para essas variáveis serão uma lista pré-definida, permitindo ao usuário apenas selecionar valores dentre os já estabelecidos. Adotei essa abordagem para garantir maior consistência nos dados, evitando duplicidades ou erros de digitação. Todas as variáveis com * são relativamente estáveis e não exigem mudanças frequentes, então definir listas prévias não será um problema. No entanto, caso seja necessário, essas listas poderão ser transformadas em tabelas editáveis, permitindo aos usuários adicionar ou remover valores. Inicialmente, optei por essa abordagem mais rígida por considerar que ela é suficiente para o contexto. 
</p> 

<p align="justify">
A única exceção a essa regra será no app de pet shop, pois a quantidade de espécies e raças de animais atendidos pode ser extensa. Tentando criar uma lista pré-definida, correria-se o risco de omitir muitas opções importantes. Por isso, adotei uma abordagem mais flexível, criando tabelas editáveis. Dessa forma, é possível começar com uma base inicial e, ao longo do tempo, os usuários podem complementar e expandir as informações conforme necessário, garantindo mais precisão e abrangência.
</p> 

<p align="justify">
Outro ponto importante é que a APP Usuários contém tabelas relacionadas a fotos e áudios dos usuários. Esses dados serão utilizados futuramente para implementar funcionalidades de acesso por reconhecimento de voz e imagem. No entanto, essa parte será desenvolvida somente após a conclusão do sistema completo, incluindo a integração com o Kong. Quando chegar a essa etapa, bem como em outras melhorias futuras, descreverei detalhadamente o que foi feito e como. Já adicionei esse modelo ao banco de dados para evitar a necessidade de modificar o diagrama UML posteriormente.
</p> 

<p align="justify">
Em relação à autenticação e autorização, será utilizado o Keycloak para gerenciar as credenciais dos usuários de maneira eficiente e segura. Quando um usuário é criado, ele é registrado tanto no Keycloak quanto no banco de dados próprio do projeto. No Keycloak, são armazenadas apenas informações básicas, como nome, e-mail e funções (roles). Todas as demais informações relacionadas ao usuário são armazenadas no banco de dados da API, garantindo uma separação clara entre os dados de autenticação e os dados específicos da aplicação.
</p> 

<p align="justify">
Uma outra melhoria planejada é a integração da API com o Llama 3 no LMStudio para gerar textos automaticamente com IA. A ideia é criar uma rota com um prompt predefinido, onde o usuário insere apenas informações-chave. Assim, os dados sobre as características de cada raça serão gerados automaticamente, permitindo o preenchimento dessas informações de forma mais rápida e eficiente. Se a resposta da IA não for satisfatória, o administrador poderá ajustá-la manualmente para garantir a qualidade das informações. Além disso, outra funcionalidade será oferecer ao usuário comum a possibilidade de acessar informações e dicas relacionadas ao seu pet, tornando a experiência mais personalizada e acolhedora.
</p> 

## TO DO:
<p align="justify">
Como mencionei anteriormente, este projeto de portfólio será utilizado para explorar e estudar novas ferramentas. Por esse motivo, ele será constantemente aprimorado e receberá novas funcionalidades com frequência. Para manter a organização do desenvolvimento, adotarei um TO DO separado em algumas categorias categorias: Tarefas concluidas, Tarefas em execução, Backlog e Upgrades.
</p> 

<p align="justify">
Esse TO DO funcionará como uma versão simplificada de sprint e backlog. Como estou desenvolvendo este projeto de forma independente e não pretendo utilizar ferramentas de SCRUM, optei por essa abordagem prática para garantir a organização e não perder de vista as ideias que surgirem ao longo do processo.
</p> 

### Tarefas concluidas:
- [x] Modelar serviços do projeto
- [x] Modelar banco de dados
- [x] Criar o readme
- [x] Inicializar projeto DJANGO da API
- [x] Criar o docker-compose do projeto geral e Dockerfile do serviço DRF.
- [x] Criar json com configurações iniciais do keycloak
- [x] Criar .env e envexample.txt
- [x] Criar configuração do minIO
- [x] Função upload_file minIO
- [x] Configurações iniciais do projeto DRF
- [x] Criar validação de imagem
- [x] Implementar os modelos de banco de dados no projeto
- [x] Implementar os serializers
- [x] Implementar as views - básicas, sem a personalização de rotas ainda (CRUD - padrão do DJANGO)
- [x] Adiconar o swagger
- [x] Criar função para mudar o nome do arquivo salvo no banco para um uuid
- [x] Função delete_file minIO + view delete em produtos

### Tarefas em execução:
- [x] Função update_file minIO + view update em produtos

### Backlog:
- [ ] Implementar autenticação e autorização com o keycloak

### Upgrades:
Em upgrades vou separar tarefas grande que precisarão ser dividas em outras subtarefas.
- [ ] Criação do bot
- [ ] Adicionar o Kong ao projeto
- [ ] Criar uma aplicação extra completa (front e back) com um serviço de chat por texto e voz.
- [ ] Criar um sistema que irá preencher caracteristicas (hábitos, alimentação, etc) das raças dos pets usando o llama3 com o lmstudio, detalhes pensar futuramente.

### IMPORTANTE:
<p align="justify">
Para facilitar a organização e testar o uso de squash commits, o projeto seguirá a estrutura de branches descrita abaixo. A branch main será onde a versão mais recente e estável do projeto será mergeada e ficará disponível publicamente no GitHub.
</p> 

<p align="justify">
No entanto, cada atualização ou melhoria será feita em branches separadas, permitindo manter um histórico das versões anteriores. Se você deseja testar uma versão estável, use a branch main ou uma branch já concluida. Para executar melhorias em andamento ou acessar uma versão anterior estável, será necessário selecionar a branch correspondente. Abaixo estão as branches disponíveis e suas descrições:
</p> 

#### Branchs:
- main: No momento possui apenas arquivos básicos e o readme sem nenhuma configuração
- apisimplificada: Onde estou desenvolvendo o projeto simplificado da figura 2.

### Executando o projeto:
Para testar e executar o projeto em sua máquina local, siga o passo a passo abaixo:

```
Código explicativo aqui:
faça o clone deste repositório
selecione a branch que deseja executar
...
```

Quando pronto colocar um vídeo demonstrativo

Além disso pretendo adicionar algumas documentações do projeto, como o link das rotas testadas pelo postman assim como o swagger

<p align="justify">
Apenas para fins de anotações, vou deixar uma lista de tecnologias que desejo estudar, embora nem todas se encaixem necessariamente neste projeto. Mantendo essa lista aqui, servirá como um lembrete, uma vez que pretendo revisitar este projeto com certa frequência:
</p> 

- [ ] Kafka
- [ ] RabbitMQ
- [ ] Spark
- [ ] FastAPI



Na parte de grupos vou definir a seguinte logica: → Pensar melhor depois

basic - Pode ver informaçãoes do banco relacionados a si mesmo

partial - Pode ver todas as informações do banco

total - Pode ver e editar todas as informações do banco

OBS.: É MUITO IMPORTANTE FALAR NO README SOBRE AS BRANCHS, POIS NÃO VOU TRABALHAR NA MAIN POR ENQUANTO ENTÃO ELA VAI FICAR DESATUALIZADA E É A QUE APARECE NO GITHUB, MUDAR A PADRÃO NÃO COMPENSA POR ENQUANTO, ENTÃO É MELHOR ESCREVER ATÉ QUE A PRIMEIRA PARTE DO PROJETO ESTEJA PRONTA!!!!!!!!!


ANOTAÇÕES:
- verificar seta para o bot(vai depender de como vou salvar os arquivos no minIO)
- ver se consigo obrigar que o usuário só seja criado se um documento for adicionado junto, mesmo sendo tabelas separadas, tem a operação atomica, mas queria fazer no próprio models.
- fazer validação de formato com o regex nos outros documentos

### Melhorias
- no app saúde verificar se o responsivel de um serviço é válido, por exemplo, um zelador não pode ser o resnponsável por uma cirurgia, então quando for criado o dado deve-se verificar isso
- automatizar o tetment_cycle status de acordo com o serviço, por exemplo, uma vacina é aplicada e o ciclo já é finalizado
- na hora de salvar a imagem colocar um uuid no lugar do nome original.
- as funções para lidar com o time no agendamento estão pronta e estão em functions e validations da app utils, quando for fazer a views lembrar de usar.
- editar para que o path do arquivo não seja retornado na resposta, uma vez que não é necessario na resposta