import sys

from AnalisadorLexico import AnalisadorLexico

class IdentificadorTipado:
    def __init__(self, identificador, tipo):
        self.identificador = identificador
        self.tipo = tipo
        

class AnalisadorSintatico:
    
    def __init__(self, path):
        self.tokens = []
        self.index = 0
        # Pilhas para controle de fluxo e análise de tipos {SEMÂNTICO}
        self.pilhaIdentificadores = [] 
        self.tokenBuffer = [] # Buffer para armazenar identificadores {SEMÂNTICO}
        self.idsTipados = [] # Lista de identificadores tipados {SEMÂNTICO}
        self.pilhaControleTipo = [] # Pilha para controle de tipos {SEMÂNTICO}
        self.AnalisadorSintatico(path)

    def debugpilhas(self):
        print(self.pilhaIdentificadores)
        print(self.pilhaControleTipo)
        
    def proximoToken(self):
        """Incrementa o índice e imprime o token atual para debug."""
        if self.index < len(self.tokens) - 1:
            self.index += 1
            token_atual = self.tokens[self.index]
            print(f"Token atual: {token_atual.lexema} (Tipo: {token_atual.tipo})")
            print(self.pilhaControleTipo)
        else:
            print("Aviso: Tentativa de acessar um token além do limite da lista.")

    def lexemaAtual(self):
        """Retorna o lexema do token atual."""
        return self.tokens[self.index].lexema
    
    def lexemaAnterior(self):
        """Retorna o lexema do token anterior."""
        return self.tokens[self.index - 1].lexema
    
    def tipoAtual(self):
        """Retorna o tipo do token atual."""
        return self.tokens[self.index].tipo
    
    def linhaAtual(self):
        """Retorna a linha do token atual."""
        return self.tokens[self.index].linha
    
    def linhaAnterior(self):
        """Retorna a linha do token anterior."""
        return self.tokens[self.index - 1].linha

    def AnalisadorSintatico(self, path):
        # Cria uma instância do Analisador Lexico, executa a análise léxica e inicia a análise sintática se não houver erros léxicos.
        AL = AnalisadorLexico()
        self.tokens = AL.executar(path)
        if AL.erroInvalido or AL.erroComentario:
            print("Houve erro léxico! Análise sintática não será efetuada.")
            sys.exit(0)
        self.index = 0
        if self.tokens:
            print(f"Token inicial: {self.lexemaAtual()} (Tipo: {self.tipoAtual()})")
        try:
            self.programa()
        except IndexError:
            print("Estrutura do programa não foi devidamente construída.")

    def programa(self):
        # Verifica a estrutura do programa, começando com a palavra-chave 'program'.
        # tem que ter no minimo <program> <identificador> ; <decs_var> ou <decs_subp> ou <comando_composto> . 
        print(f"Analisando programa: {self.lexemaAtual()}")
        if self.lexemaAtual() == "program":
            self.pilhaIdentificadores.append("$")
            self.idsTipados.append(IdentificadorTipado("$", "mark"))
            self.proximoToken()
            if self.tipoAtual() == "Identificador":
                self.pilhaIdentificadores.append(self.lexemaAtual())
                self.proximoToken()
                if self.lexemaAtual() == ";":
                    self.proximoToken()
                    self.decs_var()
                    self.decs_subp()
                    self.comando_composto()
                    if self.lexemaAtual() == ".":
                        print("Programa analisado com sucesso. Sem erros sintáticos.")
                    else:
                        print("Esperava . e recebeu " + self.lexemaAtual())
                else:
                    print("Esperava ; e recebeu " + self.lexemaAtual())
            else:
                print("Esperava identificador e recebeu " + self.tipoAtual())
        else:
            print("Esperava program e recebeu " + self.lexemaAtual())

    def decs_var(self):
        # Analisa declarações de variáveis iniciando com a palavra-chave 'var'.
        if self.lexemaAtual() == "var":
            escopovar = True
            self.proximoToken()
            self.lista_dec_var()

    def lista_dec_var(self):
        # Processa uma lista de declarações de variáveis.
        self.lista_de_identificadores()
        if self.lexemaAtual() == ":":
            # opa vamos ver se tem um tipo dessa variavel
            self.proximoToken()
            tipo = self.tipo()
            if self.lexemaAtual() == ";":
                for identificador in self.tokenBuffer:
                    self.idsTipados.append(IdentificadorTipado(identificador, tipo))
                self.tokenBuffer.clear()               
                self.proximoToken()
                self.lista_dec_var2() # pula a linha e verifica se tem mais variaveis
            else:
                print("Esperava ; e recebeu " + self.lexemaAtual())
                sys.exit(0)
        else:
            print("Esperava : e recebeu " + self.lexemaAtual())
            sys.exit(0)

    def lista_dec_var2(self):

        if self.tipoAtual() == "Identificador":
            self.lista_de_identificadores()
            if self.lexemaAtual() == ":": 
                # opa vamos ver se tem um tipo dessa variavel
                self.proximoToken()
                tipo = self.tipo()
                if self.lexemaAtual() == ";":
                    for identificador in self.tokenBuffer:
                        self.idsTipados.append(IdentificadorTipado(identificador, tipo))
                    self.tokenBuffer.clear()
                    self.proximoToken()
                    self.lista_dec_var2() # pula a linha e verifica se tem mais variaveis
                else:
                    print("Esperava ; e recebeu " + self.lexemaAtual())
                    sys.exit(0)
            else:
                print("Esperava : e recebeu " + self.lexemaAtual())
                sys.exit(0)

    def lista_de_identificadores(self):
        # Processa uma lista de identificadores
        if self.tipoAtual() == "Identificador":
            declarou = False
            for identificador in reversed(self.pilhaIdentificadores):
                if not identificador == "$":
                    if identificador == self.lexemaAtual():
                        declarou = True
                        break
                else:
                    break
            
            if declarou:
                print(f"Erro de escopo: variável {self.lexemaAtual()} já declarada.")
                exit(0)
            else:
                self.pilhaIdentificadores.append(self.lexemaAtual())
                self.tokenBuffer.append(self.lexemaAtual())
                self.proximoToken()
                self.lista_de_identificadores2()

        else:
            print("Esperava Identificador e recebeu " + self.tipoAtual())
            sys.exit(0)

    def lista_de_identificadores2(self):
        if self.lexemaAtual() == ",":
            self.proximoToken() # opa tem alguma coisa depois
            if self.tipoAtual() == "Identificador":
                declarou = False
                for identificador in reversed(self.pilhaIdentificadores):
                    if not identificador == "$":
                        if identificador == self.lexemaAtual():
                            declarou = True
                            break
                    else:
                        break
                
                if declarou:
                    print(f"Erro de escopo: variável {self.lexemaAtual()} já declarada.")
                    exit(0)
                else:
                    self.pilhaIdentificadores.append(self.lexemaAtual())
                    self.tokenBuffer.append(self.lexemaAtual())
                    self.proximoToken()
                    self.lista_de_identificadores2()
            else:
                print("Esperava Identificador e recebeu " + self.tipoAtual())
                sys.exit(0)

    def tipo(self):
        # Verifica se o token atual representa um tipo válido (integer, real, boolean).
        if self.lexemaAtual() not in ["integer", "real", "boolean"]:
            print("Esperava Tipo e recebeu " + self.lexemaAtual())
            sys.exit(0) 
        else:
            self.proximoToken()
            return self.lexemaAnterior()
        
    def decs_subp(self):
        # Analisa declarações de subprogramas, iniciando com a palavra-chave 'procedure'.
        if self.lexemaAtual() == "procedure":
            self.dec_subp() # se tiver um subprograma, chama a função para analisar
            if self.lexemaAtual() == ";":
                for identificador in self.pilhaIdentificadores:
                    if not identificador == "$":
                        self.pilhaIdentificadores.pop()
                    else:
                        self.pilhaIdentificadores.pop()
                        break

                for identificador in self.idsTipados:
                    if not identificador.identificador == "$":
                        self.idsTipados.pop()
                    else:
                        self.idsTipados.pop()
                        break

                self.proximoToken()
                self.decs_subp() # se tiver mais subprogramas, chama a função para analisar
            else:
                print("Esperava ; e recebeu " + self.lexemaAtual())
                sys.exit(0)

    def dec_subp(self):
        if self.lexemaAtual() == "procedure":
            self.proximoToken()
            if self.tipoAtual() == "Identificador": # ok tem procedura e tem um identificador, vamos ver se tem argumentos
                declarou = False

                for identificador in self.pilhaIdentificadores:
                    if not identificador == "$":
                        if identificador == self.lexemaAtual():
                            declarou = True
                            break
                    else:
                        break

                if declarou:
                    print(f"Erro de escopo: variável {self.lexemaAtual()} já declarada.")
                    exit(0)
                else:
                    self.pilhaIdentificadores.append(self.lexemaAtual())
                    self.pilhaIdentificadores.append("$")
                    self.idsTipados.append(IdentificadorTipado("$", "mark"))


                self.proximoToken()
                self.argumentos() # vamos ver se tem argumentos
                if self.lexemaAtual() == ";":
                    self.proximoToken()
                    self.decs_var() # vamos ver se tem variaveis desse subprograma
                    self.decs_subp()
                    self.comando_composto()
                else:
                    print("Esperava ; e recebeu " + self.lexemaAtual())
                    sys.exit(0)
            else:
                print("Esperava identificador e recebeu " + self.tipoAtual())
                sys.exit(0)
        else:
            print("Esperava procedure e recebeu " + self.lexemaAtual())
            sys.exit(0)

    def argumentos(self):
        # Processa a lista de argumentos de um subprograma.
        # tem que estar entre parenteses
        if self.lexemaAtual() == "(":
            self.proximoToken()
            self.lista_de_parametros()
            if self.lexemaAtual() == ")":
                self.proximoToken()
            else:
                print("Esperava ) e recebeu " + self.lexemaAtual())
                sys.exit(0)

    def lista_de_parametros(self):
        # Processa uma lista de parâmetros de um subprograma.
        self.lista_de_identificadores() # vamos ver se tem identificadores
        if self.lexemaAtual() == ":": # vamos ver se tem um tipo
            self.proximoToken()
            tipo = self.tipo()

            for identificador in self.tokenBuffer:
                self.idsTipados.append(IdentificadorTipado(identificador, tipo))

            self.tokenBuffer.clear()
            self.lista_de_parametros2() # vamos ver se tem mais parametros
        else:
            print("Esperava : e recebeu " + self.lexemaAtual())
            sys.exit(0)

    def lista_de_parametros2(self):
        """Processa o restante dos parâmetros após um ponto-e-vírgula."""
        if self.lexemaAtual() == ";":
            self.proximoToken()
            self.lista_de_identificadores()
            if self.lexemaAtual() == ":":
                self.proximoToken()
                tipo = self.tipo()

                for identificador in self.tokenBuffer:
                    self.idsTipados.append(IdentificadorTipado(identificador, tipo))

                self.tokenBuffer.clear()
                self.lista_de_parametros2()
            else:
                print("Esperava : e recebeu " + self.lexemaAtual())
                sys.exit(0)
        
    def comando_composto(self):
        """Processa um bloco de comandos, iniciando com 'begin' e terminando com 'end'."""
        if self.lexemaAtual() == "begin":
            self.proximoToken()
            self.comandos_opcionais()  # Chamada atualizada para tratar todos os comandos opcionais corretamente.
            
            # se o token for um end, e o seguinte for um . (ponto), não há comandos a serem processados
            if self.lexemaAtual() != "end":             
                print("Esperava 'end' e recebeu " + self.lexemaAtual())           
                sys.exit(0)
            else:
                self.proximoToken()
        else:
            print(f"Esperava 'begin' e recebeu '{self.lexemaAtual()}'")
            sys.exit(0)


    def comandos_opcionais(self):
        if (self.tipoAtual() == "Identificador" or
            self.lexemaAtual() == "begin" or
            self.lexemaAtual() == "if" or
            self.lexemaAtual()== "while" or
            self.lexemaAtual() == "for"):
            self.lista_de_comandos()

    def lista_de_comandos(self):
        self.comando()
        self.lista_de_comandos2()

    def lista_de_comandos2(self):
        if self.lexemaAtual() == ";":
            self.proximoToken()
            self.comando()
            self.lista_de_comandos2()

    def comando(self):
        
        # Analisa um único comando, podendo ser uma atribuição, uma ativação de procedimento, estruturas de controle, etc.
        if self.tipoAtual() == "Identificador" and self.tokens[self.index + 1].tipo == "Operador de Atribuicao":
            self.variavel() # só pra checar se ta tudo certo
            if self.tipoAtual() == "Operador de Atribuicao":
                self.proximoToken()
                self.expressao() # vamos ver se tem uma expressão
            self.verificacaoAtribuicao()

        elif self.tipoAtual() == "Identificador":
            self.ativacao_de_procedimento()
        elif self.lexemaAtual() == "begin":
            self.comando_composto()
        elif self.lexemaAtual() == "if":
            self.proximoToken()
            self.expressao()
            if self.lexemaAtual() == "then":
                self.proximoToken()
                self.comando()
                self.parte_else()
            else:
                print("Esperava then e recebeu " + self.lexemaAtual())
                sys.exit(0)
        elif self.lexemaAtual() == "while":
            self.proximoToken()
            self.expressao()
            if self.lexemaAtual() == "do":
                self.proximoToken()
                self.comando_composto()
            else:
                print("Esperava do e recebeu " + self.lexemaAtual())
                sys.exit(0)
        elif self.lexemaAtual() == "for":
            self.proximoToken()
            self.variavel()
            if self.tipoAtual() == "Operador de Atribuicao":
                self.proximoToken()
                self.expressao()
                self.verificacaoAtribuicao()
                if self.lexemaAtual() == "to":
                    self.proximoToken()
                    self.expressao()
                    if self.lexemaAtual() == "do":
                        self.proximoToken()
                        self.comando_composto()
                    else:
                        print("Esperava do e recebeu " + self.lexemaAtual())
                        sys.exit(0)
                else:
                    print("Esperava to e recebeu " + self.lexemaAtual())
                    sys.exit(0)
            else:
                print("Esperava := e recebeu " + self.lexemaAtual())
                sys.exit(0)
        else:
            # se o token for um end, e o seguinte for um . (ponto), não há comandos a serem processados
            if self.lexemaAtual() == "end" and self.tokens[self.index + 1].lexema == ".":
                return "sucesso"
            print("Esperava comando e recebeu " + self.lexemaAtual())
            print("Tipo: " + self.lexemaAtual())
            sys.exit(0)

    def parte_else(self):
        # Processa a parte 'else' de uma estrutura condicional 'if'.
        if self.lexemaAtual() == "else":
            self.proximoToken()
            self.comando()

    def variavel(self):
        # Verifica se o token atual é um identificador válido para uma variável.
        if self.tipoAtual() == "Identificador":
            if self.lexemaAtual() not in self.pilhaIdentificadores:
                print(f"O identificador {self.lexemaAtual()} não foi declarado anteriormente.")
                exit(0)

            for identificador in self.idsTipados:
                if identificador.identificador == self.lexemaAtual():
                    self.pilhaControleTipo.append(identificador.tipo)
                    break

            self.proximoToken()
        else:
            print("Esperava variável e recebeu " + self.lexemaAtual())
            sys.exit(0)

    def ativacao_de_procedimento(self):
        if self.tipoAtual() == "Identificador":
            if self.lexemaAtual() not in self.pilhaIdentificadores:
                print(f"O identificador {self.lexemaAtual()} não foi declarado anteriormente.")
                exit(0)

            
            for identificador in self.idsTipados:
                if identificador.identificador == self.lexemaAtual():
                    self.pilhaControleTipo.append(identificador.tipo)
                    break

            self.proximoToken()
            self.ativacao_de_procedimento2()
        else:
            print("Esperava identificador e recebeu " + self.lexemaAtual())
            sys.exit(0)

    def ativacao_de_procedimento2(self):
        if self.lexemaAtual() == "(":
            self.proximoToken()
            self.lista_de_expressoes()
            if self.lexemaAtual() == ")":
                self.proximoToken()
            else:
                print("Esperava ) e recebeu " + self.lexemaAtual())
                sys.exit(0)

    def lista_de_expressoes(self):
        self.expressao()
        self.lista_de_expressoes2()

    def lista_de_expressoes2(self):
        if self.lexemaAtual() == ",":
            self.proximoToken()
            self.expressao()
            self.lista_de_expressoes2()

    def expressao(self):
        self.expressao_simples()
        self.expressao2()

    def expressao2(self):
        if self.tipoAtual() == "Operador Relacional":
            self.op_relacional()
            self.expressao_simples()
            self.expressao2()
            self.verificacaoRelacional()

    def expressao_simples(self):
        if self.lexemaAtual() in ["+", "-"]:
            # Se o token atual for um sinal de adição ou subtração, processa-o e chama a expressão simples.
            self.proximoToken()
            self.termo()
            self.expressao_simples2()
        else:
            self.termo()
            self.expressao_simples2()

    def expressao_simples2(self):
        if self.tipoAtual() == "Operador Aditivo":
            if self.lexemaAtual() == "+" or self.lexemaAtual() == "-":
                self.op_aditivo()
                self.termo()
                self.expressao_simples2()
                self.verificacaoAritmetica()
            elif self.lexemaAtual() == "or":
                self.op_aditivo()
                self.termo()
                self.expressao_simples2()
                self.verificacaoLogica()

    def termo(self):
        # Processa um termo, que pode ser parte de uma expressão, contendo operadores multiplicativos.
        self.fator()
        self.termo2()

    def termo2(self):
        if self.tipoAtual() == "Operador Multiplicativo":
            if self.lexemaAtual() == "/" or self.lexemaAtual() == "*":
                self.op_multiplicativo()
                self.fator()
                self.termo2()
                self.verificacaoAritmetica()
            elif self.lexemaAtual() == "and":
                self.op_multiplicativo()
                self.fator()
                self.termo2()
                self.verificacaoLogica()

    def fator(self):
        # # Analisa um fator, a unidade básica de uma expressão, podendo ser um identificador, número, expressão entre parênteses, etc.
        if self.tipoAtual() == "Identificador":
            self.ativacao_de_procedimento()
        elif self.tipoAtual() in ["Numero Inteiro"]:
            self.pilhaControleTipo.append("integer")
            self.proximoToken()
            
            
        elif self.tipoAtual() in ["Numero Real"]:
            self.pilhaControleTipo.append("real")
            self.proximoToken()
            
        elif self.lexemaAtual() in ["true", "false"]:
            self.pilhaControleTipo.append("boolean")
            self.proximoToken()
                      
        elif self.lexemaAtual() == "(":
            self.proximoToken()
            self.expressao()
            if self.lexemaAtual() != ")":
                print("Esperava ) e recebeu " + self.lexemaAtual())
                sys.exit(0)
            else:
                self.proximoToken()
        elif self.lexemaAtual() == "not":
            self.pilhaControleTipo.append("boolean")
            self.proximoToken()
            self.fator()
            self.verificacaoLogica()
        else:
            print("Esperava fator e recebeu " + self.lexemaAtual())
            sys.exit(0)

    def op_relacional(self):
        if self.tipoAtual() == "Operador Relacional":
            self.proximoToken()
        else:
            print("Esperava operador relacional e recebeu " + self.lexemaAtual())
            sys.exit(0)

    def op_aditivo(self):
        if self.tipoAtual() == "Operador Aditivo":
            self.proximoToken()
        else:
            print("Esperava operador aditivo e recebeu " + self.lexemaAtual())
            sys.exit(0)

    def op_multiplicativo(self):
        if self.tipoAtual() == "Operador Multiplicativo":
            self.proximoToken()
        else:
            print("Esperava operador multiplicativo e recebeu " + self.lexemaAtual())
            sys.exit(0)

    def verificacaoAritmetica(self):
        top = self.pilhaControleTipo.pop()
        subtop = self.pilhaControleTipo.pop()

        if top == "integer" and subtop == "integer":
            self.pilhaControleTipo.append("integer")
        elif top == "real" and subtop == "real":
            self.pilhaControleTipo.append("real")
        elif top == "integer" and subtop == "real":
            self.pilhaControleTipo.append("real")
        elif top == "real" and subtop == "integer":
            self.pilhaControleTipo.append("real")
        else:
            if self.lexemaAtual() == "end":
                print(f"Erro: tipos incompatíveis em operação aritmética na linha {self.linhaAnterior()}")
            else:
                print(f"Erro: tipos incompatíveis em operação aritmética na linha {self.linhaAtual()}")
            exit(0)

    def verificacaoRelacional(self):
        top = self.pilhaControleTipo.pop()
        subtop = self.pilhaControleTipo.pop()

        if top == "integer" and subtop == "integer":      
            self.pilhaControleTipo.append("boolean")
            
        elif top == "real" and subtop == "real":
            
            self.pilhaControleTipo.append("boolean")
        elif top == "integer" and subtop == "real":
            
            self.pilhaControleTipo.append("boolean")
        elif top == "real" and subtop == "integer":
            
            self.pilhaControleTipo.append("boolean")
        else:
            if self.lexemaAtual() == "end":
                print(f"Erro: tipos incompatíveis em operação relacional na linha {self.linhaAnterior()}")
            else:
                print(f"Erro: tipos incompatíveis em operação relacional na linha {self.linhaAtual()}")
            exit(0)


    def verificacaoLogica(self):
        top = self.pilhaControleTipo.pop()
        subtop = self.pilhaControleTipo.pop()

        if top == subtop:        
            self.pilhaControleTipo.append("boolean")
        else:
            if self.lexemaAtual() == "end":
                print(f"Erro: tipos incompatíveis em operação lógica na linha {self.linhaAnterior()}")
            else:
                print(f"Erro: tipos incompatíveis em operação lógica na linha {self.linhaAtual()}")
            exit(0)

    def verificacaoAtribuicao(self):
        top = self.pilhaControleTipo.pop()
        subtop = self.pilhaControleTipo.pop()

        if subtop == "real" and top == "integer":
            self.pilhaControleTipo.append("real")
        elif subtop == top:
            self.pilhaControleTipo.append(subtop)
        else:
            if self.lexemaAtual() == "end":
                print(f"Erro: tipos incompatíveis em atribuição na linha {self.linhaAnterior()}")
            else:
                print(f"Erro: tipos incompatíveis em atribuição na linha {self.linhaAtual()}")
            exit(0)

