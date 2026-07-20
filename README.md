## Implementação do Upload de XML

### Funcionalidade: Upload de XML

1. **Upload de XML**
   - **Descrição:** Permitir que os usuários façam upload de arquivos XML individuais ou múltiplos para o sistema.
   - **Responsável:** `ralplast-xml-upload`
   - **Endpoints:** 
     - `POST /xml/upload`

2. **Upload Múltiplo**
   - **Descrição:** O sistema deve suportar o upload de vários arquivos XML ao mesmo tempo.
   - **Implementação:**
     - Modificar o endpoint `/xml/upload` para aceitar uma array de arquivos.
     - Garantir que todos os arquivos sejam processados em sequência.

3. **Validar Extensão**
   - **Descrição:** Validar a extensão dos arquivos enviados para garantir que sejam XML.
   - **Implementação:**
     - Após o upload, verificar cada arquivo:
       - Se a extensão do arquivo for `.xml`.
       - Retornar erro se a extensão for inválida.
   - **Código Exemplo:**
     ```python
     def validar_extensao(arquivo):
         if not arquivo.endswith('.xml'):
             raise ValueError("Extensão inválida: apenas arquivos .xml são suportados")
     ```

4. **Salvar XML no Amazon S3**
   - **Descrição:** Após a validação, o arquivo XML deve ser salvo no Amazon S3.
   - **Implementação:**
     - Conectar-se ao serviço S3.
     - Salvar o arquivo em um bucket específico.
     - Retornar a URL do arquivo salvo.
   - **Código Exemplo:**
     ```python
     import boto3

     def salvar_no_s3(arquivo, bucket):
         s3 = boto3.client('s3')
         s3.upload_file(arquivo, bucket, arquivo)  # Nome do arquivo como chave
         return f"s3://{bucket}/{arquivo}"
     ```

5. **Registrar Importação**
   - **Descrição:** Registrar detalhes da importação no banco de dados.
   - **Implementação:**
     - Criar uma entrada no banco de dados que inclui:
       - Nome do arquivo
       - Timestamp da importação
       - Usuário que realizou a importação
     - Garantir que a entrada seja criada apenas após a confirmação do upload e validação do arquivo.
   - **Código Exemplo:**
     ```python
     def registrar_importacao(nome_arquivo, usuario):
         # Exemplo de conexão com o banco de dados
         conn = conectar_ao_banco()
         cursor = conn.cursor()
         cursor.execute("INSERT INTO importacoes (nome_arquivo, usuario, timestamp) VALUES (%s, %s, NOW())", (nome_arquivo, usuario))
         conn.commit()
     ```

---

### Considerações Finais
- **Tratamento de Erros:** Implementar tratamento de erros adequado para gerenciar falhas durante o upload e validação dos arquivos.
- **Testes:** Criar testes unitários para garantir que cada parte do processo funcione corretamente.
- **Documentação:** Documentar as APIs e as funcionalidades para referência futura.
