import sys

from AnalisadorLexico import AnalisadorLexico

class AnalisadorSintatico:
    def __init__(self, path):
        self.tokens = []
        self.index = 0
        self.AnalisadorSintatico(path)

    def proximoToken(self):
        """Incrementa o índice e imprime o token atual para debug."""
        if self.index < len(self.tokens) - 1:
            self.index += 1
            token_atual = self.tokens[self.index]
            print(f"Token atual: {token_atual.lexema} (Tipo: {token_atual.tipo})")
        else:
            print("Aviso: Tentativa de acessar um token além do limite da lista.")

    def lexemaAtual(self):
        """Retorna o lexema do token atual."""
        return self.tokens[self.index].lexema
    
    def tipoAtual(self):
        """Retorna o tipo do token atual."""
        return self.tokens[self.index].tipo

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
        #  # Verifica a estrutura do programa, começando com a palavra-chave 'program'.
        print(f"Analisando programa: {self.lexemaAtual()}")
        if self.lexemaAtual() == "program":
            self.proximoToken()
            if self.tipoAtual() == "Identificador":
                self.proximoToken()
                if self.lexemaAtual() == ";":
                    self.proximoToken()
                    self.decs_var()
                    self.decs_subp()
                    self.comando_composto()
                    if self.lexemaAtual() == ".":
                        print("Programa analisado com sucesso.")
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
            self.proximoToken()
            self.lista_dec_var()

    def lista_dec_var(self):
        # Processa uma lista de declarações de variáveis.
        self.lista_de_identificadores()
        if self.lexemaAtual() == ":":
            self.proximoToken()
            self.tipo()
            if self.lexemaAtual() == ";":
                self.proximoToken()
                self.lista_dec_var2()
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
                self.proximoToken()
                self.tipo()
                if self.lexemaAtual() == ";":
                    self.proximoToken()
                    self.lista_dec_var2()
                else:
                    print("Esperava ; e recebeu " + self.lexemaAtual())
                    sys.exit(0)
            else:
                print("Esperava : e recebeu " + self.lexemaAtual())
                sys.exit(0)

    def lista_de_identificadores(self):
        # Processa uma lista de identificadores
        if self.tipoAtual() == "Identificador":
            self.proximoToken()
            self.lista_de_identificadores2()
        else:
            print("Esperava Identificador e recebeu " + self.tipoAtual())
            sys.exit(0)

    def lista_de_identificadores2(self):
        if self.lexemaAtual() == ",":
            self.proximoToken()
            if self.tipoAtual() == "Identificador":
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

    def decs_subp(self):
        # Analisa declarações de subprogramas, iniciando com a palavra-chave 'procedure'.
        if self.lexemaAtual() == "procedure":
            self.dec_subp()
            if self.lexemaAtual() == ";":
                self.proximoToken()
                self.decs_subp()
            else:
                print("Esperava ; e recebeu " + self.lexemaAtual())
                sys.exit(0)

    def dec_subp(self):
        if self.lexemaAtual() == "procedure":
            self.proximoToken()
            if self.tipoAtual() == "Identificador":
                self.proximoToken()
                self.argumentos()
                if self.lexemaAtual() == ";":
                    self.proximoToken()
                    self.decs_var()
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
        self.lista_de_identificadores()
        if self.lexemaAtual() == ":":
            self.proximoToken()
            self.tipo()
            self.lista_de_parametros2()
        else:
            print("Esperava : e recebeu " + self.lexemaAtual())
            sys.exit(0)

    def lista_de_parametros2(self):
        if self.lexemaAtual() == ";":
            self.proximoToken()
            self.lista_de_identificadores()
            if self.lexemaAtual() == ":":
                self.proximoToken()
                self.tipo()
                self.lista_de_parametros2()
            else:
                print("Esperava : e recebeu " + self.lexemaAtual())
                sys.exit(0)

    def comando_composto(self):
        # Processa um bloco de comandos, iniciando com 'begin' e terminando com 'end'.
        if self.lexemaAtual() == "begin":
            self.proximoToken()
            # Verifica se o próximo token não é 'end', indicando que há comandos para processar
            if self.lexemaAtual() != "end":
                self.comandos_opcionais()
            if self.lexemaAtual() == "end":
                self.proximoToken()
            else:
                if self.lexemaAtual() == "=":
                    return "Esperava := e recebeu " + self.lexemaAtual()
                print("Esperava end e recebeu " + self.lexemaAtual())
                sys.exit(0)
        else:
            print("Esperava begin e recebeu " + self.lexemaAtual())
            sys.exit(0)


    def comandos_opcionais(self):
        # Processa uma lista de comandos opcionais.
        if self.tipoAtual() in ["Identificador", "begin", "if", "while", "for"]:
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
        if self.tipoAtual() == "Identificador" and self.tokens[self.index + 1].tipo == "Operador de Atribuição":
            self.variavel()
            if self.tipoAtual() == "Operador de Atribuição":
                self.proximoToken()
                self.expressao()
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
                self.comando()
            else:
                print("Esperava do e recebeu " + self.lexemaAtual())
                sys.exit(0)
        elif self.lexemaAtual() == "for":
            self.proximoToken()
            self.variavel()
            if self.tipoAtual() == "Operador de Atribuição":
                self.proximoToken()
                self.expressao()
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
                return "s"
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
            self.proximoToken()
        else:
            print("Esperava variável e recebeu " + self.lexemaAtual())
            sys.exit(0)

    def ativacao_de_procedimento(self):
        if self.tipoAtual() == "Identificador":
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
            self.proximoToken()
            self.expressao_simples()

    def expressao_simples(self):
        if self.lexemaAtual() in ["+", "-"]:
            self.proximoToken()
            self.termo()
            self.expressao_simples2()
        else:
            self.termo()
            self.expressao_simples2()

    def expressao_simples2(self):
        if self.tipoAtual() == "Operador Aditivo":
            self.op_aditivo()
            self.termo()
            self.expressao_simples2()

    def termo(self):
        # Processa um termo, que pode ser parte de uma expressão, contendo operadores multiplicativos.
        self.fator()
        self.termo2()

    def termo2(self):
        if self.tipoAtual() == "Operador Multiplicativo":
            self.proximoToken()
            self.fator()
            self.termo2()

    def fator(self):
        # # Analisa um fator, a unidade básica de uma expressão, podendo ser um identificador, número, expressão entre parênteses, etc.
        if self.tipoAtual() == "Identificador":
            self.ativacao_de_procedimento()
        elif self.tipoAtual() in ["Número Inteiro", "Número Real"]:
            self.proximoToken()
        elif self.lexemaAtual() in ["true", "false"]:
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
            self.proximoToken()
            self.fator()
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


