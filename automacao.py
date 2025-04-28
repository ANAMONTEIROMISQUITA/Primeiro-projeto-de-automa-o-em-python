import pyautogui
import time
import pandas as pd
from openpyxl import Workbook


def digitar_texto(texto):
    pyautogui.write(texto, interval=0.05)
    return True


def clicar_em(nome, posicoes):
    if nome in posicoes:
        x, y = posicoes[nome]
        pyautogui.click(x, y)
        return True
    else:
        return False
    
def pressionar_tecla(tecla):
    pyautogui.press(tecla)
    return True


def esperar(segundos):
    time.sleep(float(segundos))
    return True


def executar_tarefa(tarefa, tipo, dado, posicoes):
    try:
        inicio = time.time()
        if tipo == "click":
            sucesso = clicar_em(dado, posicoes)
        elif tipo == "texto":
            sucesso = digitar_texto(dado)
        elif tipo == "tecla":
            sucesso = pressionar_tecla(dado)
        elif tipo == "espera":
            sucesso = esperar(dado)
        else:
            sucesso = False


        fim = time.time()
        tempo = round(fim - inicio, 2)
        status = "Executada com sucesso" if sucesso else "Erro: posição não encontrada"
        return tarefa, status, tempo


    except Exception as e:
        return tarefa, f"Erro: {str(e)}", 0.0


def gerar_relatorio(relatorio, nome_arquivo='relatorio.xlsx'):
    wb = Workbook()
    ws = wb.active
    ws.append(["Tarefa", "Status", "Tempo (s)"])
    for linha in relatorio:
        ws.append(linha)
    wb.save(nome_arquivo)


def main():
    posicoes = {
        "navegador_icone": (679, 270),
        "tema":(1245,347)
    }
   
    df = pd.read_csv('tarefas.csv')


#lista pro rela´torio
    relatorio = []


    print("Pressionando a tecla Windows para abrir o menu iniciar...")
    pyautogui.hotkey('win')  
    time.sleep(1)  
    print("Buscando o Google Chrome no menu iniciar...")
    digitar_texto("Google Chrome")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(3)
    digitar_texto('https://www.terra.com.br/')
    time.sleep(1)
    pressionar_tecla("enter")
    print("Pesquisa realizada!")
    time.sleep(3)




    for _, linha in df.iterrows():
        tarefa, tipo, dado = linha['Tarefa'], linha['Tipo'], linha['Dado']
        resultado = executar_tarefa(tarefa, tipo, dado, posicoes)
        print(f"{resultado[0]} -> {resultado[1]} ({resultado[2]}s)")
        relatorio.append(resultado)


    gerar_relatorio(relatorio)
    print("Relatório gerado com sucesso!")


if __name__ == '__main__':
    main()