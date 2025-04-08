import tkinter as tk
from tkinter import ttk, END
from pymongo import MongoClient

# Conectando ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["sua_base"]
collection = db["clientes"]

# Cria a janela principal
tela = tk.Tk()
tela.title("Cadastro de Clientes - Fatec de Registro")
tela.geometry("775x300")
tela.resizable(False, False)

# Lista de estados brasileiros
estados = [
    "Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", "Distrito Federal",
    "Espírito Santo", "Goiás", "Maranhão", "Mato Grosso", "Mato Grosso do Sul",
    "Minas Gerais", "Pará", "Paraíba", "Paraná", "Pernambuco", "Piauí",
    "Rio de Janeiro", "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia",
    "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"
]

# ==== CAMPOS DO FORMULÁRIO ====
tk.Label(tela, text="Código").grid(row=0, column=0, padx=10, pady=5, sticky="w")
txt_codigo = tk.Entry(tela, width=30)
txt_codigo.grid(row=0, column=1, padx=10, pady=5)

tk.Label(tela, text="Nome").grid(row=1, column=0, padx=10, pady=5, sticky="w")
txt_nome = tk.Entry(tela, width=30)
txt_nome.grid(row=1, column=1, padx=10, pady=5)

tk.Label(tela, text="CPF").grid(row=1, column=2, padx=10, pady=5, sticky="w")
txt_cpf = tk.Entry(tela, width=20)
txt_cpf.grid(row=1, column=3, padx=10, pady=5)

tk.Label(tela, text="Idade").grid(row=2, column=0, padx=10, pady=5, sticky="w")
txt_idade = tk.Entry(tela, width=30)
txt_idade.grid(row=2, column=1, padx=10, pady=5)

tk.Label(tela, text="Rua").grid(row=2, column=2, padx=10, pady=5, sticky="w")
txt_rua = tk.Entry(tela, width=20)
txt_rua.grid(row=2, column=3, padx=10, pady=5)

tk.Label(tela, text="Bairro").grid(row=3, column=0, padx=10, pady=5, sticky="w")
txt_bairro = tk.Entry(tela, width=30)
txt_bairro.grid(row=3, column=1, padx=10, pady=5)

tk.Label(tela, text="Estado").grid(row=3, column=2, padx=10, pady=5, sticky="w")
combo_estado = ttk.Combobox(tela, values=estados, width=20)
combo_estado.grid(row=3, column=3, padx=10, pady=5)
combo_estado.set("São Paulo")

tk.Label(tela, text="Cidade").grid(row=4, column=0, padx=10, pady=5, sticky="w")
txt_cidade = tk.Entry(tela, width=30)
txt_cidade.grid(row=4, column=1, padx=10, pady=5)

# ==== FUNÇÕES ====
def limpar_campos():
    txt_codigo.delete(0, END)
    txt_nome.delete(0, END)
    txt_cpf.delete(0, END)
    txt_idade.delete(0, END)
    txt_rua.delete(0, END)
    txt_bairro.delete(0, END)
    combo_estado.set("")
    txt_cidade.delete(0, END)

def salvar():
    cliente = {
        "codigo": txt_codigo.get(),
        "nome": txt_nome.get(),
        "cpf": txt_cpf.get(),
        "idade": txt_idade.get(),
        "rua": txt_rua.get(),
        "bairro": txt_bairro.get(),
        "estado": combo_estado.get(),
        "cidade": txt_cidade.get()
    }
    collection.insert_one(cliente)
    print("Cliente inserido:", cliente)
    limpar_campos()

def atualizar():
    codigo = txt_codigo.get()
    rua = txt_rua.get()
    bairro = txt_bairro.get()
    endereco = f"{rua}, {bairro}"
    collection.update_one(
        {"codigo": codigo},
        {"$set": {
            "nome": txt_nome.get(),
            "idade": int(txt_idade.get()),
            "cpf": txt_cpf.get(),
            "endereco": endereco,
            "cidade": txt_cidade.get(),
            "estado": combo_estado.get()
        }}
    )
    print(f"Cliente {codigo} atualizado.")
    limpar_campos()

def apagar():
    codigo = txt_codigo.get()
    collection.delete_one({"codigo": codigo})
    print(f"Cliente {codigo} apagado.")
    limpar_campos()

def consultar():
    codigo = txt_codigo.get()  # Pegue o código antes de limpar
    resultado = collection.find_one({"codigo": codigo})

    if resultado:
        limpar_campos()
        txt_codigo.insert(END, resultado['codigo'])
        txt_nome.insert(END, resultado['nome'])
        txt_cpf.insert(END, resultado['cpf'])
        txt_idade.insert(END, resultado['idade'])
        txt_rua.insert(END, resultado.get('rua', ''))
        txt_bairro.insert(END, resultado.get('bairro', ''))
        combo_estado.set(resultado.get('estado', ''))
        txt_cidade.insert(END, resultado.get('cidade', ''))
    else:
        print("Cliente não encontrado.")


def sair():
    tela.destroy()

# ==== BOTÕES ====
btn_salvar = tk.Button(tela, text="Salvar", width=15, command=salvar)
btn_salvar.grid(row=6, column=0, padx=10, pady=20)

btn_atualizar = tk.Button(tela, text="Atualizar", width=15, command=atualizar)
btn_atualizar.grid(row=6, column=1, padx=10, pady=20)

btn_apagar = tk.Button(tela, text="Apagar", width=15, command=apagar)
btn_apagar.grid(row=6, column=2, padx=10, pady=20)

btn_consultar = tk.Button(tela, text="Consultar", width=15, command=consultar)
btn_consultar.grid(row=6, column=3, padx=10, pady=20)

btn_sair = tk.Button(tela, text="Sair", width=15, command=sair)
btn_sair.grid(row=6, column=4, padx=10, pady=20)

# Executa a janela
tela.mainloop()
