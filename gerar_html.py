import gspread
from oauth2client.service_account import ServiceAccountCredentials
import subprocess
from datetime import datetime

# -------------------------------
# CONFIGURAÇÃO
# -------------------------------
CREDENTIALS_FILE = "credentials.json"
HTML_OUTPUT = "index.html"
SHEET_ID_VISITANTES = "1NylIvo_gFt8CaI_ow_IfMFcB5f_JBG5aMNeXyDP-rhY"
SHEET_ID_IGREJAS = "1PsL6HuXS2LUUhu5o4Z3NRZoyWG5-ebbNXhWexCHzXh4"

# -------------------------------
# FUNÇÃO: GERAR HTML
# -------------------------------
def gerar_html():
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)

    # Pega dados completos das planilhas
    sheet_visitantes = client.open_by_key(SHEET_ID_VISITANTES).sheet1
    visitantes_values = sheet_visitantes.get_all_values()

    sheet_igrejas = client.open_by_key(SHEET_ID_IGREJAS).sheet1
    igrejas_values = sheet_igrejas.get_all_values()

    # Construindo HTML
    html = """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Relatório</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f9f9f9; }
            h1 { color: #333; border-bottom: 2px solid #444; padding-bottom: 5px; }
            .table-container { overflow-x: auto; margin-bottom: 40px; }
            table { width: 100%; min-width: 600px; border-collapse: collapse; }
            th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
            th { background: #444; color: #fff; }
            tr:nth-child(even) { background: #f2f2f2; }
            tr:hover { background: #e9f5ff; }
            @media (max-width: 768px) { body { font-size: 14px; margin: 10px; } th, td { padding: 8px; } }
        </style>
    </head>
    <body>
    """

    # ---------- Visitantes ----------
    html += "<h1>Relatório de Visitantes</h1><div class='table-container'><table>"
    if visitantes_values:
        # Cabeçalhos
        html += "<tr>" + "".join([f"<th>{col}</th>" for col in visitantes_values[0]]) + "</tr>"
        # Dados
        for row in visitantes_values[1:]:
            html += "<tr>" + "".join([f"<td>{cell}</td>" for cell in row]) + "</tr>"
    html += "</table></div>"

    # ---------- Igrejas ----------
    html += "<h1>Relatório de Igrejas</h1><div class='table-container'><table>"
    if igrejas_values:
        # Cabeçalhos
        html += "<tr>" + "".join([f"<th>{col}</th>" for col in igrejas_values[0]]) + "</tr>"
        # Dados
        for row in igrejas_values[1:]:
            html += "<tr>" + "".join([f"<td>{cell}</td>" for cell in row]) + "</tr>"
    html += "</table></div>"

    # Fecha HTML
    html += "</body></html>"

    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Relatório gerado com sucesso: {HTML_OUTPUT}")

# -------------------------------
# FUNÇÃO: ATUALIZAR GITHUB
# -------------------------------
def atualizar_github():
    def rodar(comando):
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"✔ {comando}")
        else:
            print(f"❌ Erro: {comando}")
            print(resultado.stderr)

    rodar("git add index.html gerar_html.py atualiza_git.py .gitignore")
    mensagem = f'Atualização automática {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'
    rodar(f'git commit -m \"{mensagem}\"')
    rodar("git push origin master")

# -------------------------------
# EXECUÇÃO PRINCIPAL
# -------------------------------
if __name__ == "__main__":
    gerar_html()
    atualizar_github()
