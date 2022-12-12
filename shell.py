import Livin 

while True: 
    text = input('Livin > ' )
    if text == '':
        break
    lexer = Livin.Lexer(text)
    tokens, error = lexer.make_tokens()
    if error:
        print(error)
    else:
        print(tokens)
        
#     print(tokens)

