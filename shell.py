import Livin # Import Livin

##while True: # Infinite loop
  ##  text = input('Enter a command: ') # Get input from user
    ##text = input( 'Livin > ')
    #p##rint (text) # Echo input
    ##result, error = Livin.run('<stdin>', text) # Run code and get result
     ##enter exit to exit program 
    ##if text == 'exit': break # Exit
    ##if error: print(error.as_string())
    ##else : print(result)












##import Livin 

while True: 
    text = input('Livin > ' )
    if text == '':
       break
    lexer = Livin.Lexer(text)
    tokens, error = lexer.make_tokens()
    if error:
        print(error)
    ## enter exit to exit the shell
    elif text == 'exit':
        break
    else:
        print(tokens)
        
    ##print(tokens)

