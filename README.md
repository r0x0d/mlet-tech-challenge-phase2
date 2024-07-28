[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/r0x0d/mlet_tech_challenge_phase2/main.svg)](https://results.pre-commit.ci/latest/github/r0x0d/mlet_tech_challenge_phase2/main)
[![Coverage](https://github.com/r0x0d/mlet_tech_challenge_phase2/actions/workflows/coverage.yml/badge.svg)](https://github.com/r0x0d/mlet_tech_challenge_phase2/actions/workflows/coverage.yml)
[![codecov](https://codecov.io/gh/r0x0d/mlet_tech_challenge_phase2/branch/main/graph/badge.svg?token=<your-token-for-badges>)](https://codecov.io/gh/r0x0d/mlet_tech_challenge_phase2)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/r0x0d/mlet_tech_challenge_phase2.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/r0x0d/mlet_tech_challenge_phase2/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/r0x0d/mlet_tech_challenge_phase2.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/r0x0d/mlet_tech_challenge_phase2/context:python)
[![Code Scanning - Action](https://github.com/r0x0d/mlet_tech_challenge_phase2/actions/workflows/codeql.yml/badge.svg)](https://github.com/r0x0d/mlet_tech_challenge_phase2/actions/workflows/codeql.yml)

# mlet-tech-challenge-phase2

Tech Challenge FIAP - Big Data Architecture (Fase 2)

# Clonando o projeto

Para dar os primeiros passos, primeiro devemos clonar o projeto da seguinte maneira:

```bash
git clone git@github.com:r0x0d/mlet_tech_challenge_phase2.git
```

Com o projeto clonado, vamos entrar em sua pasta raíz e instalar as dependencias do projeto

```bash
cd mlet_tech_challenge_phase2
virtualenv vev
./bin/Scripts/activate.ps1
pip install -r requirements/requirements.txt
```

É possível que seja necessário a instalação do Visual C++ 2015, uma vez que precisamos escrever o output final no formato `.parquet`. [Visual C++ Redistributable for Visual Studio 2015](https://www.microsoft.com/en-us/download/details.aspx?id=48145)

Após concluir as instalações, podemos iniciar o projeto utilizando o seguinte comando:

```bash
python -m mlet_tech_challenge_phase2
```

# Utilizando o lambda

O projeto conta com um código lambda (escrito em Python) para executar um job no AWS Glue a partir de um novo registro sendo feito upload em um bucket. Para tal, precisamos atualizar o nome do job ETL no script e fazer o upload do mesmo no AWS S3.

É necessário também realizar uma configuração no bucket que receberá os eventos e irá fazer o trigger do lambda, sendo a configuração a seguinte:

- Configuração do Bucket S3 para acionar a Função Lambda
  - Acesse o Console de Gerenciamento da AWS e vá para o serviço S3.
  - Selecione o bucket onde o upload dos arquivos ocorrerá.
  - Vá para a aba "Properties" e, na seção "Event notifications", clique em "Create event notification".
  - Preencha as informações necessárias:
    - Event name: Nome da sua notificação de evento.
    - Event types: Selecione "All object create events" ou eventos específicos de upload.
    - Prefix/Suffix: Opcional, se você quiser restringir a notificação a arquivos específicos.
    - Destination: Escolha "Lambda function" e selecione a função Lambda que você criou.
  - Clique em "Save changes".
