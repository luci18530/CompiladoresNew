class Token:
    def __init__(self, lexema, tipo, linha):
        self.lexema = lexema
        self.tipo = tipo
        self.linha = linha

class AnalisadorLexico:
    PALAVRAS_RESERVADAS = {
        "program", "var", "integer", "real", "boolean", "procedure",
        "begin", "end", "if", "then", "else", "while", "do", "not", "for", "to"
    }

    def __init__(self):
        self.tokens = [] # Lista para armazenar tokens identificados.
        self.erroInvalido = False # Flag para verificar se um caractere inválido foi encontrado.
        self.erroComentario = False # Flag para verificar se um comentário foi aberto e não fechado.
        self.msgErro = ""

    def adiciona_token(self, lexema, tipo, linha):
        token = Token(lexema, tipo, linha)
        self.tokens.append(token)

    def analisar_linha(self, linha, numLinha):
        i = 0
        while i < len(linha):
            if self.erroComentario:
                # Verifica se o comentário é fechado
                if linha[i] == '}':
                    self.erroComentario = False
            # Marca o início de um comentário.
            elif linha[i] == '{':
                self.erroComentario = True
            elif linha[i].isalpha():
                # Identifica lexemas que começam com letra (palavras reservadas ou identificadores).
                lexema, i = self.extrair_lexema(linha, i)
                tipo = self.determinar_tipo_lexema(lexema)
                self.adiciona_token(lexema, tipo, numLinha)
            elif linha[i].isdigit():
                # Identifica lexemas que começam com dígito (números inteiros ou reais).
                lexema, i, tipo = self.extrair_numero(linha, i)
                self.adiciona_token(lexema, tipo, numLinha)
            elif linha[i] in ';.,()':
                # Identifica delimitadores.
                self.adiciona_token(linha[i], "Delimitador", numLinha)
            elif linha[i] in ':=<>':
                # Identifica operadores de atribuição e relacionais.
                lexema, i = self.extrair_simbolo(linha, i)
                if lexema == "=":
                    # Aqui é onde detectamos o uso incorreto do "=" como operador de atribuição.
                    self.registrar_erro(lexema, numLinha)
                else:
                    tipo = "Operador de Atribuicao" if lexema == ":=" else "Operador Relacional"
                    self.adiciona_token(lexema, tipo, numLinha)
            elif linha[i] in '+-':
                # Identifica operadores aditivos.
                self.adiciona_token(linha[i], "Operador Aditivo", numLinha)
            elif linha[i] in '*/':
                # Identifica operadores multiplicativos.
                self.adiciona_token(linha[i], "Operador Multiplicativo", numLinha)
            elif linha[i] not in ' \n\t':
                # Identifica caracteres inválidos.
                self.registrar_erro(linha[i], numLinha)
                break
            i += 1

    def extrair_lexema(self, linha, i):
        lexema = ""
        while i < len(linha) and (linha[i].isalpha() or linha[i].isdigit() or linha[i] == '_'):
            lexema += linha[i]
            i += 1
        return lexema, i - 1

    def determinar_tipo_lexema(self, lexema):
        if lexema in self.PALAVRAS_RESERVADAS:
            return "Palavra Reservada"
        elif lexema == "or":
            return "Operador Aditivo"
        elif lexema == "and":
            return "Operador Multiplicativo"
        elif lexema == "true" or lexema == "false":
            return "Booleano"   
        else:
            return "Identificador"

    def extrair_numero(self, linha, i):
        lexema = ""
        primeiroPonto = True
        while i < len(linha) and (linha[i].isdigit() or (linha[i] == '.' and primeiroPonto)):
            if linha[i] == '.':
                primeiroPonto = False
            lexema += linha[i]
            i += 1
        tipo = "Numero Inteiro" if primeiroPonto else "Numero Real"
        return lexema, i - 1, tipo

    def extrair_simbolo(self, linha, i):
        lexema = linha[i]
        if i + 1 < len(linha) and linha[i + 1] in ('=', '>'):
            i += 1
            lexema += linha[i]
        return lexema, i

    def registrar_erro(self, caracter, numLinha):
        self.erroInvalido = True
        self.msgErro = f"Erro encontrado: Caracter inválido ou uso incorreto '{caracter}', na linha {numLinha}."

    def executar(self, path):
        self.__init__()
        with open(path, 'r') as file:
            for numLinha, linha in enumerate(file, start=1):
                self.analisar_linha(linha, numLinha)

        with open("saida.txt", 'w') as fw:
            fw.write("{:<12} | {:<23} | {:<3}\n".format("Token", "Tipo", "Linha"))
            fw.write("----------------------------------------------\n")
            for t in self.tokens:
                fw.write("{:<12} | {:<23} | {:<3}\n".format(t.lexema, t.tipo, t.linha))
            if self.erroInvalido:
                fw.write(self.msgErro + "\n")
                print(self.msgErro)
            if self.erroComentario:
                fw.write("Erro encontrado: Comentário não fechado.\n")
                print("Erro encontrado: Comentário não fechado.")

        return self.tokens
