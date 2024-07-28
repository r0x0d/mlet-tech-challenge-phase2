import json

import boto3


def lambda_handler(event, context):
    # Exemplo de evento S3
    s3_event = event["Records"][0]["s3"]
    bucket = s3_event["bucket"]["name"]
    key = s3_event["object"]["key"]

    print(f"Arquivo {key} foi carregado no bucket {bucket}")

    # Inicia o job do AWS Glue
    glue_client = boto3.client("glue")

    try:
        response = glue_client.start_job_run(
            JobName="<nome-do-job-no-aws-glue>",
            Arguments={"--S3_BUCKET": bucket, "--S3_KEY": key},
        )
        print(f'Job do AWS Glue iniciado: {response["JobRunId"]}')
    except Exception as e:
        print(f"Erro ao iniciar o job do AWS Glue: {e}")

    return {"statusCode": 200, "body": json.dumps("Sucesso!")}
