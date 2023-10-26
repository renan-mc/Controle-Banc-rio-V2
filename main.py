import os

def escolher_operacao():
    menu = '''========================================================

            Aplicativo de controle bancário.

    Digite a operação desejada e pressione 'Enter':

    [1] Extrato
    [2] Saque
    [3] Depósito
    
    [4] Criar Usuário
    [5] Excluir Usuário
    [6] Listar Usuários Cadastrados

    [7] Criar Conta Corrente
    [8] Excluir Conta Corrente
    [9] Listar Contas Corrente

    [0] Sair

========================================================

'''

    operacao = input(menu)

    if operacao.isdigit() and (0 <= int(operacao) <= 9):
        return int(operacao)
    else:
        os.system('clear')
        print('Opção selecionada inválida... Retornando ao menu')
        return None

def verificar_ponto_flutuante(valor):
    try:
        float(valor)
        return True
    except:
        return False

def depositar_valor(saldo, /, extrato):
    os.system('clear')
    print('============ Operação selecionada: Depósito ============\n')
    valor = input('Insira o valor que deseja depositar (Formato R$ XXX,XX): ')
    e_float = verificar_ponto_flutuante(valor)
    if e_float == True:
        valor = float(valor)    
        if valor > 0.0:
            saldo += valor
            print(f'\n\nOperação realizada! \nValor depositado: R$ {valor:.2f} \nSaldo após depósito: R$ {saldo:.2f}\n')
            atualiza_extrato = f'Depósito realizado. Valor: R$ {valor:.2f}'
            extrato = f'{atualiza_extrato}\n{extrato}'
        else:
            print('Não é possível depositar valores negativos! Retornando ao menu...\n')
    else:
        print('Não foi inserido um valor para ser depositado! Retornando ao menu...\n')
    
    return saldo, extrato

def sacar_valor(*, saldo, extrato, saques_realizados, limite_de_saques, limite_por_saque):
    os.system('clear')
    print('============= Operação selecionada: Saque =============\n\n')
    if saques_realizados < limite_de_saques:
        valor = input('Insira o valor que deseja sacar (Formato R$ XXX,XX): ')
        e_float = verificar_ponto_flutuante(valor)
        if e_float == True:
            valor = float(valor)
            if 0.01 < valor <= limite_por_saque:
                if valor <= saldo:
                    saldo -= valor
                    saques_realizados += 1
                    print(f'\nOperação realizada! \nValor sacado: R$ {valor:.2f} \nSaldo após saque: R$ {saldo:.2f} \nSaques feitos hoje: {saques_realizados} (Limite de {limite_de_saques} saques por dia) \nRetornando ao menu...\n')
                    atualiza_extrato = f'Saque realizado. Valor: R$ {valor:.2f}'
                    extrato = f'{atualiza_extrato}\n{extrato}'
                else:
                    print(f'\nVocê não possui esta quantia em conta atualmente. Saldo atual: R$ {saldo:.2f} \nRetornando ao menu...')
            else:
                print(f'\nNão é possível sacar valores menores do que R$ 0,01 ou maiores do que R$ {limite_por_saque:.2f}! \n\nRetornando ao menu...')
        else:
            print('Não foi inserido um valor para ser depositado! Retornando ao menu...\n')
    else:
        print(f'\nLimite máximo de saques por dia alcançado ({limite_de_saques} saques) \nRetornando ao menu...')

    return saldo, extrato, saques_realizados

def exibir_extrato(saldo, /, *, extrato):
    os.system('clear')
    print('============= Operação selecionada: Extrato =============')
    print(f'\nSaldo Atual: R$ {saldo:.2f}')
    print('Não foram realizadas movimentações hoje') if len(extrato) == 0 else print('Movimentações feitas hoje (da mais recente até a mais antiga):\n',extrato)
    print('\nRetornando ao menu...\n')

def criar_usuario(usuarios):
    os.system('clear')
    print('============= Operação selecionada: Criar Usuário =============\n\n')
    cpf = input('Insira o seu CPF (sem traços e pontos): ')
    esta_cadastrado, usuario = verificar_usuario_cadastrado(usuarios, cpf)
    if esta_cadastrado:
        print('\nUsuário %s já cadastrado, retornando ao menu...' %(usuario['Nome']))
        return
    nome = input('Insira o seu nome completo: ')
    nascimento = input('Insira a sua data de nascimento (DD-MM-AAAA): ')
    endereco = input('Insira o seu endereço (Logradouro, N - Bairro - Cidade - Estado/Sigla): ')
    usuarios.append({'Nome': nome, 'Nascimento': nascimento, 'CPF':cpf, 'Endereço':endereco})
    print(f'\nUsuário {nome} cadastrado! Retornando ao menu...\n')
        
def verificar_usuario_cadastrado(usuarios, cpf):
    for usuario in usuarios:
        if cpf == usuario.get('CPF', None):
            return True, usuario
    return False, None

def listar_usuarios(usuarios):
    os.system('clear')
    print('============= Operação selecionada: Listar Usuários Cadastrados =============\n')
    if len(usuarios) > 0:
        print('Seguem abaixo os usuários cadastrados no sistema:\n')
        for usuario in usuarios:
            print(usuario)
        print('\nRetornando ao menu...\n')
    else:
        print('Não existem usuários cadastrados! Retornando ao menu...\n')

def excluir_usuario(usuarios, contas_corrente):
    os.system('clear')
    print('============= Operação selecionada: Excluir Usuário =============\n\n')
    cpf = input('Insira o CPF do usuário que deseja remover do sistema (sem traços e pontos): ')
    esta_cadastrado, usuario = verificar_usuario_cadastrado(usuarios, cpf)
    if esta_cadastrado:
        if len(contas_corrente) > 0:
            usuario_possui_conta_corrente = False
            for conta in contas_corrente:
                if conta['Nome do Usuário'] == usuario['Nome']:
                    usuario_possui_conta_corrente = True
            if usuario_possui_conta_corrente:
                print('\nEste usuário possui conta(s) corrente cadastrada(s)... remova a(s) conta(s) antes para de excluir o usuário\n\nRetornando ao menu...\n')
            else:
                print('\nUsuário %s removido com sucesso!\n' %(usuario['Nome']))
                usuarios.remove(usuario)
        else:
            print('\nUsuário %s removido com sucesso!\n' %(usuario['Nome']))
            usuarios.remove(usuario)
    else:
        print('\nUsuário não encontrado, retornando ao menu...\n')

def criar_conta_corrente(contas_corrente, usuarios):
    os.system('clear')
    print('============= Operação selecionada: Criar Conta Corrente =============\n\n')
    agencia = '0001'
    numero_da_conta = 1
    cpf = input('Digite o CPF do usuário em que deseja criar a conta corrente (sem traços e pontos): ')
    esta_cadastrado, usuario = verificar_usuario_cadastrado(usuarios, cpf)
    if esta_cadastrado:
        for conta in contas_corrente:
            if numero_da_conta <= conta.get('Número da Conta', 0):
                numero_da_conta = conta['Número da Conta'] + 1 
        nome = usuario['Nome']
        contas_corrente.append({'Número da Conta': numero_da_conta, 'Nome do Usuário': nome, 'Agência': agencia,})
        print('\nConta de número %d criada para o usuário %s na agência %s' %(numero_da_conta, nome, agencia))
        print('\nRetornando ao menu.\n')
    else:
        print('\nUsuário não encontrado no número de CPF informado!\n\nRetornando ao menu...\n')

def listar_contas_corrente(contas_corrente):
    os.system('clear')
    print('============= Operação selecionada: Listar Usuários Cadastrados =============\n')
    if len(contas_corrente) > 0:
        print('Seguem abaixo as contas corrente cadastrados no sistema:\n')
        for conta in contas_corrente:
            print(conta)
        print('\nRetornando ao menu...\n')
    else:
        print('Não existem contas corrente cadastradas! Retornando ao menu...\n')

def excluir_conta_corrente(contas_corrente):
    os.system('clear')
    print('============= Operação selecionada: Excluir Conta Corrente =============\n\n')
    numero_da_conta = input('Insira o numero da conta corrente que deseja remover do sistema (menor número de conta possível -> 1): ')
    excluiu = False
    if numero_da_conta.isdigit() and int(numero_da_conta) >= 1:
        numero_da_conta = int(numero_da_conta)
        for conta in contas_corrente:
            if conta.get('Número da Conta', 0) == numero_da_conta:
                print('\nConta de número %d referente ao usuário %s excluída...\n\nRetornando ao Menu...\n ' %(numero_da_conta, conta['Nome do Usuário']))
                contas_corrente.remove(conta)
                excluiu = True
        if not excluiu:
            print(f'\nConta de número {numero_da_conta} não encontrada\n\nRetornando ao menu...\n')
                
    else:
        print('\nEntrada Inválida Inserida\n\nRetornando ao menu...\n')

def main():
    saldo = 1000

    saques_realizados = 0
    LIMITE_DE_SAQUES = 3
    LIMITE_POR_SAQUE = 500.00

    extrato = ''

    usuarios = []
    contas_corrente = []

    os.system('clear')

    while True:

        operacao = escolher_operacao()
        
        if operacao == 0: #Sair
            os.system('clear')
            break


        elif operacao == 1: #Extrato
            exibir_extrato(saldo, extrato=extrato)
        
        elif operacao == 2: #Saque
            saldo, extrato, saques_realizados = sacar_valor(saldo=saldo, extrato=extrato, saques_realizados=saques_realizados, limite_por_saque=LIMITE_POR_SAQUE, limite_de_saques=LIMITE_DE_SAQUES)

        elif operacao == 3: #Depósito
            saldo, extrato = depositar_valor(saldo, extrato)


        elif operacao == 4: #Criar Usuário
            criar_usuario(usuarios)

        elif operacao == 5: #Excluir Usuário
            excluir_usuario(usuarios, contas_corrente)

        elif operacao == 6: #Listar Usuários
            listar_usuarios(usuarios)


        elif operacao == 7: #Criar Conta Corrente
            criar_conta_corrente(contas_corrente, usuarios)

        elif operacao == 8: #Excluir Conta Corrente           
            excluir_conta_corrente(contas_corrente)

        elif operacao == 9: #Listar Contas Corrente
            listar_contas_corrente(contas_corrente)

main()