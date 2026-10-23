import requests
from datetime import datetime

ESTADO_UF = "RS"  # Pode alterar para o seu estado (ex: SP, MG, RJ, SC, etc.)
TERMOS_BUSCA = ["monitoramento", "cftv", "cameras", "alarme", "vigilancia eletronica", "controle de acesso"]
EXCLUSOES = ["merenda", "medicamento", "limpeza", "pavimentacao", "alimenticios", "pneus"]

def consultar_pncp():
    hoje = datetime.now().strftime("%Y%m%d")
    url = f"https://pncp.gov.br/api/consulta/v1/contratacoes/proposta?dataFinal={hoje}&tamanhoPagina=100"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            print("Erro ao consultar PNCP:", response.status_code)
            return []
            
        dados = response.json().get("resultado", [])
        oportunidades = []

        for item in dados:
            uf_item = item.get("unidadeOrgao", {}).get("ufSigla", "")
            objeto = item.get("objeto", "").lower()
            
            if ESTADO_UF and uf_item != ESTADO_UF:
                continue
                
            if any(excl in objeto for excl in EXCLUSOES):
                continue
                
            if any(kw in objeto for kw in TERMOS_BUSCA):
                numero_pncp = item.get("numeroControlPncp", "")
                oportunidades.append({
                    "orgao": item.get("orgaoNome", "Órgão Público"),
                    "objeto": item.get("objeto"),
                    "valor": item.get("valorTotalEstimado", 0.0),
                    "link": f"https://pncp.gov.br/app/editais/{numero_pncp}" if numero_pncp else "https://pncp.gov.br/app/editais"
                })

        return oportunidades

    except Exception as e:
        print("Erro na execução:", e)
        return []

if __name__ == "__main__":
    ops = consultar_pncp()
    print(f"Encontradas {len(ops)} oportunidades em {ESTADO_UF} hoje.")
    for op in ops:
        print(f"• [{op['orgao']}] R$ {op['valor']:,.2f} -> {op['link']}")
