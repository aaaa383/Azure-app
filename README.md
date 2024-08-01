# 前提

Azure App Service へのローカル Git からのデプロイに関する詳細は以下のドキュメントを参照してください:  
[App Service へのローカル Git からのデプロイ](https://learn.microsoft.com/ja-jp/azure/app-service/deploy-local-git?tabs=cli)

## 認証情報のセットアップ

デプロイメントユーザーの資格情報を設定または更新するには、以下の`az`コマンドを使用します。  
az login コマンドで既にログイン済みでも下記は実行してください。  
azure 上に作成するリポジトリに対する認証情報になります。

```bash
az webapp deployment user set --user-name [username] --password [password]

ex)
az webapp deployment user set --user-name takayoshi.maruki.bt --password  r2tH3sw!
```

# Azure Developer CLI

## リソースグループの作成

リソースグループを作成するには、以下のコマンドを実行します。

```bash
az group create --name <your-resource-group-name> --location japaneast
```

## App Service Plan の作成

App Service Plan を作成するには、次のコマンドを使用します。

```bash
az appservice plan create --name <your-serviceplan-name> --resource-group <your-resource-group-name> --sku B1 --is-linux
```

## App Service の作成

App Service を作成し、ローカル Git デプロイメントを設定するには、以下のコマンドを実行します。

```bash
az webapp create --resource-group <your-resource-group-name> --plan <your-serviceplan-name> --name <your-app-name> --runtime "PYTHON|3.9" --deployment-local-git
```

Web アプリが作成されると、Azure CLI によって次の例のような出力が表示されます。

```
 {
   "availabilityState": "Normal",
   "clientAffinityEnabled": true,
   "clientCertEnabled": false,
   "cloningInfo": null,
   "containerSize": 0,
   "dailyMemoryTimeQuota": 0,
   "defaultHostName": "<app-name>.azurewebsites.net",
   "deploymentLocalGitUrl": "https://<username>@<app-name>.scm.azurewebsites.net/<app-name>.git",
   "enabled": true,
   < JSON data removed for brevity. >
 }
```

> [!IMPORTANT]
> Git リモートの URL は deploymentLocalGitUrl プロパティに https://<username>@<app-name>.scm.azurewebsites.net/<app-name>.git 形式で出力されます。 この URL は後で必要になるので保存しておいてください。

## スタートアップコマンドの設定

環境変数、スタートアップコマンドを設定するには、次のコマンドを利用します。

```bash
az webapp config appsettings set --resource-group <your-resource-group-name> --name <your-app-name> --settings KEY1=VALUE1 KEY2=VALUE2 --startup-file "cmd script"

ex)
az webapp config set -g  rg-edv-streamlit -n edv-streamlit-web --startup-file "python -m streamlit run app/app.py --server.port 8000 --server.address 0.0.0.0"
```

詳細はこちらを参照[リンク](https://learn.microsoft.com/ja-jp/cli/azure/webapp/config?view=azure-cli-latest)

## ローカルリポジトリの設定

## デプロイのためのリモートリポジトリの設定

`az webapp create` コマンドの出力から `deploymentLocalGitUrl` を取得し、以下のコマンドでリモートとして Git に追加します。  
deploymentLocalGitUrl が不明な場合は app serivce の Git クローン URL から取得できます。

リモートリポジトリの設定例:

```bash
git remote add azure <your-repo-url>

ex)
git remote add azure https://takayoshi.maruki.bt@edv-streamlit-web.scm.azurewebsites.net/edv-streamlit-web.git
```

## Azure へのデプロイ

変更内容を Azure にデプロイするには、以下のコマンドを使用します。

```bash
git push azure main:master
```

### 認証設定
AMBL Group ドメインのみのアクセスにする
https://learn.microsoft.com/ja-jp/azure/app-service/scenario-secure-app-authentication-app-service
### DefaultAzureCredential　IDシステム割り当て
コード中でDefaultAzureCredentialを利用し、Azure Open AIへのアクセスを認可しています。
ID＞システム割り当て済み
ロールの割り当て
