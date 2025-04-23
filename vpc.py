import os
import platform
import socket
import subprocess
import traceback
from datetime import datetime

def obter_ip_local():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return "Desconhecido"

def testar_ping(ip):
    try:
        resposta = subprocess.run(["ping", "-c", "4", ip], capture_output=True, text=True)
        return resposta.stdout, resposta.returncode == 0
    except Exception as e:
        return str(e), False

def testar_traceroute(ip):
    try:
        resultado = subprocess.run(["traceroute", ip], capture_output=True, text=True)
        return resultado.stdout
    except Exception as e:
        return str(e)

def testar_socket(ip, porta, timeout=5):
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, porta))
        return True, ""
    except Exception as e:
        return False, traceback.format_exc()

def gerar_relatorio(ip, porta):
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    relatorio = []

    relatorio.append(f"📅 Data e hora: {agora}")
    relatorio.append(f"📍 IP alvo: {ip}")
    relatorio.append(f"🔌 Porta alvo: {porta}")
    relatorio.append(f"🖥️ Sistema operacional: {platform.system()} {platform.release()}")
    relatorio.append(f"🌐 Nome do host local: {socket.gethostname()}")
    relatorio.append(f"📡 IP local: {obter_ip_local()}")
    relatorio.append("")

    # Teste de ping
    ping_saida, ping_sucesso = testar_ping(ip)
    relatorio.append("📶 Teste de ping:")
    relatorio.append(ping_saida.strip())
    relatorio.append("✅ Ping bem-sucedido!" if ping_sucesso else "❌ Ping falhou.")
    relatorio.append("")

    # Teste de traceroute
    relatorio.append("🧭 Resultado do traceroute:")
    relatorio.append(testar_traceroute(ip).strip())
    relatorio.append("")

    # Teste de conexão TCP
    relatorio.append("🧪 Teste de conexão via socket (TCP):")
    sucesso, detalhes = testar_socket(ip, porta)
    if sucesso:
        relatorio.append(f"✅ Conexão bem-sucedida com {ip}:{porta}")
    else:
        relatorio.append(f"❌ Falha na conexão com {ip}:{porta}")
        relatorio.append("📋 Stacktrace do erro:")
        relatorio.append(detalhes.strip())

    return "\n".join(relatorio)

def salvar_relatorio(relatorio, caminho="relatorio_conexao.log"):
    with open(caminho, "w") as f:
        f.write(relatorio)
    print(f"📁 Relatório salvo em: {caminho}")

if __name__ == "__main__":
    ip_alvo = ""
    porta_alvo = 1111
    relatorio = gerar_relatorio(ip_alvo, porta_alvo)
    salvar_relatorio(relatorio)
