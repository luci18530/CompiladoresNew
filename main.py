from AnalisadorSintatico import AnalisadorSintatico

def main():
    path = 'Test4.pas'
    try:
        AS = AnalisadorSintatico(path)
        
    except (FileNotFoundError, IOError) as e:
        print(e)

if __name__ == "__main__":
    main()