import tkinter as tk
from tkinter import messagebox
import mysql.connector as mysql

# Conexão com o banco de dados
db = mysql.connect(host="localhost", user="root", password="", database="consulta")
mycursor = db.cursor()

# Função para realizar a pesquisa de médico ou paciente por CPF
def realizar_pesquisa():
    cpf = e1_pesquisa.get()  # Obtém o CPF inserido pelo usuário
    tipo = var_tipo.get()  # Obtém o tipo de registro escolhido (médico ou paciente)

    if not cpf:  # Se o CPF não for fornecido, exibe um aviso
        messagebox.showwarning("Erro", "Por favor, insira um CPF para pesquisa.")
        return
    
    if tipo == "Médico":
        sql = "SELECT * FROM medico WHERE cpf = %s"
    elif tipo == "Paciente":
        sql = "SELECT * FROM paciente WHERE cpf = %s"
    else:
        messagebox.showwarning("Erro", "Por favor, escolha Médico ou Paciente.")
        return

    try:
        mycursor.execute(sql, (cpf,))
        resultado = mycursor.fetchall()

        # Exibe o resultado da pesquisa
        if resultado:
            messagebox.showinfo("Resultado", f"Registro encontrado: {resultado}")
        else:
            messagebox.showinfo("Resultado", "Nenhum registro encontrado.")
    except mysql.Error as err:
        messagebox.showerror("Erro", f"Erro na pesquisa: {err}")

# Função para abrir a janela de pesquisa
def abrir_janela_pesquisa():
    root.withdraw()
    pesquisa_window = tk.Toplevel(root)
    pesquisa_window.title("Pesquisa de Médico ou Paciente por CPF")
    pesquisa_window.geometry("600x400")

    tk.Label(pesquisa_window, text="Pesquisar Médico ou Paciente por CPF", font=('Times New Roman', 20, 'bold')).pack(pady=20)

    # Label e campo de pesquisa (CPF)
    tk.Label(pesquisa_window, text="Digite o CPF para pesquisa:").pack(pady=10)
    global e1_pesquisa
    e1_pesquisa = tk.Entry(pesquisa_window)
    e1_pesquisa.pack(pady=10)

    # Opções para escolher entre Médico ou Paciente
    tk.Label(pesquisa_window, text="Escolha o tipo de registro para pesquisa:").pack(pady=10)
    global var_tipo
    var_tipo = tk.StringVar()
    var_tipo.set("Médico")  # valor inicial

    tipo_opcao = tk.OptionMenu(pesquisa_window, var_tipo, "Médico", "Paciente")
    tipo_opcao.pack(pady=10)

    # Botões
    tk.Button(pesquisa_window, text="Pesquisar", command=realizar_pesquisa, height=3, width=20).pack(pady=20)
    tk.Button(pesquisa_window, text="Voltar", command=lambda: voltar_para_menu(pesquisa_window), height=3, width=20).pack(pady=20)

# Função para deletar médico ou paciente
def Delete(tipo):
    cpf = e1_delete.get()  # Obtém o CPF inserido pelo usuário na janela de deletação

    if not cpf:  # Se o CPF não for fornecido, não faz nada
        messagebox.showwarning("Erro", "Por favor, insira um CPF válido.")
        return

    # A escolha do tipo determina a tabela a ser deletada
    if tipo == "medico":
        sql = "DELETE FROM medico WHERE cpf = %s"
    elif tipo == "paciente":
        sql = "DELETE FROM paciente WHERE cpf = %s"
    
    val = (cpf,)
    try:
        mycursor.execute(sql, val)
        db.commit()

        # Verifica se o registro foi realmente excluído
        if mycursor.rowcount > 0:
            messagebox.showinfo("Sucesso", "Registro deletado com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Registro não encontrado.")

        e1_delete.delete(0, tk.END)  # Limpar o campo de entrada após a exclusão
    except mysql.Error as err:
        messagebox.showerror("Erro", f"Erro ao excluir o registro: {err}")

# Função para abrir a janela de deletação com escolha de médico ou paciente
def abrir_janela_deletar():
    root.withdraw()
    delete_window = tk.Toplevel(root)
    delete_window.title("Deletar Registro")
    delete_window.geometry("400x300")

    # Labels e campos de entrada
    tk.Label(delete_window, text="Deletar Registro", font=('Times New Roman', 20, 'bold')).pack()
    tk.Label(delete_window, text="Digite o CPF do registro a ser deletado:").pack()

    global e1_delete
    e1_delete = tk.Entry(delete_window)
    e1_delete.pack(pady=10)

    # Botões
    tk.Button(delete_window, text="Deletar Médico", command=lambda: Delete("medico"), height=2, width=15).pack(pady=5)
    tk.Button(delete_window, text="Deletar Paciente", command=lambda: Delete("paciente"), height=2, width=15).pack(pady=5)
    tk.Button(delete_window, text="Voltar", command=lambda: voltar_para_menu(delete_window), height=2, width=15).pack(pady=5)

# Função para voltar ao menu principal
def voltar_para_menu(window):
    window.destroy()
    root.deiconify()

# Função para adicionar médico
def Add_medico():
    codigo = e1.get()
    nome = e2.get()
    cpf = e3.get() 
    idade = e4.get()
    cidade = e5.get()
    endereco = e6.get()
    estado = e7.get()


    if not all([codigo, nome, cpf, idade, cidade, endereco, estado]):
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")
        return

    sql = "INSERT INTO medico (codigo, nome, cpf, idade, cidade, endereco, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (codigo, nome, cpf, idade, cidade, endereco, estado)
    mycursor.execute(sql, val)
    db.commit()
    messagebox.showinfo("Sucesso", "Médico adicionado com sucesso!")

    # Limpar os campos após o cadastro
    e1.delete(0, tk.END)
    e2.delete(0, tk.END)
    e3.delete(0, tk.END)
    e4.delete(0, tk.END)
    e5.delete(0, tk.END)
    e6.delete(0, tk.END)
    e7.delete(0, tk.END)

 

# Função para adicionar paciente
def Add_paciente():
    id = e1_paciente.get()
    nome = e2_paciente.get()
    horario = e3_paciente.get()
    cpf = e4_paciente.get()
    nome_medico = e5_paciente.get()
    idade = e6_paciente.get()
    endereco = e7_paciente.get()
    cidade = e8_paciente.get()
    estado = e9_paciente.get()


    if not all([id, nome, horario, cpf, nome_medico, idade, endereco, cidade, estado]):
        messagebox.showwarning("Erro", "Por favor, preencha todos os campos.")
        return

    sql = "INSERT INTO paciente (id, nome, horario, cpf, nome_medico, idade, endereco, cidade, estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (id, nome, horario, cpf, nome_medico, idade, endereco, cidade, estado)
    mycursor.execute(sql, val)
    db.commit()
    messagebox.showinfo("Sucesso", "Paciente adicionado com sucesso!")

    # Limpar os campos após o cadastro
    e1_paciente.delete(0, tk.END)
    e2_paciente.delete(0, tk.END)
    e3_paciente.delete(0, tk.END)
    e4_paciente.delete(0, tk.END)
    e5_paciente.delete(0, tk.END)
    e6_paciente.delete(0, tk.END)
    e7_paciente.delete(0, tk.END)
    e8_paciente.delete(0, tk.END)
    e9_paciente.delete(0, tk.END)

 

# Função para abrir a janela de cadastro de médicos
def abrir_janela_cadastro_medico():
    root.withdraw()
    cadastro_window = tk.Toplevel(root)
    cadastro_window.title("Cadastro do Médico")
    cadastro_window.geometry("500x350")

    # Labels e campos de entrada
    tk.Label(cadastro_window, text="Cadastro de Médico", font=('Times New Roman', 30, 'bold')).grid(row=0, column=3)
    tk.Label(cadastro_window, text="CÓDIGO").grid(row=1, column=2)
    tk.Label(cadastro_window, text="NOME").grid(row=2, column=2)
    tk.Label(cadastro_window, text="CPF").grid(row=3, column=2)
    tk.Label(cadastro_window, text="IDADE").grid(row=4, column=2)
    tk.Label(cadastro_window, text="CIDADE").grid(row=5, column=2)
    tk.Label(cadastro_window, text="ENDEREÇO").grid(row=6, column=2)
    tk.Label(cadastro_window, text="ESTADO").grid(row=7, column=2)

    global e1, e2, e3, e4, e5, e6, e7
    e1 = tk.Entry(cadastro_window)
    e2 = tk.Entry(cadastro_window)
    e3 = tk.Entry(cadastro_window)
    e4 = tk.Entry(cadastro_window)
    e5 = tk.Entry(cadastro_window)
    e6 = tk.Entry(cadastro_window)
    e7 = tk.Entry(cadastro_window)

    e1.grid(row=1, column=3)
    e2.grid(row=2, column=3)
    e3.grid(row=3, column=3)
    e4.grid(row=4, column=3)
    e5.grid(row=5, column=3)
    e6.grid(row=6, column=3)
    e7.grid(row=7, column=3)

    # Botões
    tk.Button(cadastro_window, text="Adicionar", command=Add_medico, height=3, width=10).place(x=150, y=250)
    tk.Button(cadastro_window, text="Voltar", command=lambda: voltar_para_menu(cadastro_window), height=3, width=10).place(x=250, y=250)

# Função para abrir a janela de cadastro de pacientes
def abrir_janela_cadastro_paciente():
    root.withdraw()
    cadastro_window = tk.Toplevel(root)
    cadastro_window.title("Cadastro de Pacientes")
    cadastro_window.geometry("500x400")

    # Labels e campos de entrada
    tk.Label(cadastro_window, text="Cadastro de Pacientes", font=('Times New Roman', 30, 'bold')).grid(row=0, column=3)
    tk.Label(cadastro_window, text="ID").grid(row=1, column=2)
    tk.Label(cadastro_window, text="NOME").grid(row=2, column=2)
    tk.Label(cadastro_window, text="HORÁRIO").grid(row=3, column=2)
    tk.Label(cadastro_window, text="CPF").grid(row=4, column=2)
    tk.Label(cadastro_window, text="NOME DO MÉDICO").grid(row=5, column=2)
    tk.Label(cadastro_window, text="IDADE").grid(row=6, column=2)
    tk.Label(cadastro_window, text="ENDEREÇO").grid(row=7, column=2)
    tk.Label(cadastro_window, text="CIDADE").grid(row=8, column=2)
    tk.Label(cadastro_window, text="ESTADO").grid(row=9, column=2)

    global e1_paciente, e2_paciente, e3_paciente, e4_paciente, e5_paciente, e6_paciente, e7_paciente, e8_paciente, e9_paciente, e10_paciente
    e1_paciente = tk.Entry(cadastro_window)
    e2_paciente = tk.Entry(cadastro_window)
    e3_paciente = tk.Entry(cadastro_window)
    e4_paciente = tk.Entry(cadastro_window)
    e5_paciente = tk.Entry(cadastro_window)
    e6_paciente = tk.Entry(cadastro_window)
    e7_paciente = tk.Entry(cadastro_window)
    e8_paciente = tk.Entry(cadastro_window)
    e9_paciente = tk.Entry(cadastro_window)
 

    e1_paciente.grid(row=1, column=3)
    e2_paciente.grid(row=2, column=3)
    e3_paciente.grid(row=3, column=3)
    e4_paciente.grid(row=4, column=3)
    e5_paciente.grid(row=5, column=3)
    e6_paciente.grid(row=6, column=3)
    e7_paciente.grid(row=7, column=3)
    e8_paciente.grid(row=8, column=3)
    e9_paciente.grid(row=9, column=3)
    

    # Botões
    tk.Button(cadastro_window, text="Adicionar", command=Add_paciente, height=3, width=10).place(x=125, y=300)
    tk.Button(cadastro_window, text="Voltar", command=lambda: voltar_para_menu(cadastro_window), height=3, width=10).place(x=250, y=300)

# Janela principal (menu)
root = tk.Tk()
root.title("Sistema de Cadastro")
root.geometry("1920x1080")

# Botões no menu principal
tk.Button(root, text="Cadastro de Médicos", command=abrir_janela_cadastro_medico, height=3, width=20).pack(pady=20)
tk.Button(root, text="Cadastro de Pacientes", command=abrir_janela_cadastro_paciente, height=3, width=20).pack(pady=20)
tk.Button(root, text="Pesquisar Médico/Paciente", command=abrir_janela_pesquisa, height=3, width=20).pack(pady=20)
tk.Button(root, text="Deletar Médico ou Paciente", command=abrir_janela_deletar, height=3, width=20).pack(pady=20)

# Botão para fechar o programa
tk.Button(root, text="Fechar", command=root.quit, height=3, width=20).pack(pady=20)

# Iniciar o Tkinter
root.mainloop()
