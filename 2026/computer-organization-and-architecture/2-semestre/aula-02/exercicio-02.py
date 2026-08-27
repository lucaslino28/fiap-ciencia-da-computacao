# 2 - Desenvolva um programa que receba uma mensagem e
# apresente sua representação em bytes e bits.
# 1. Solicite uma mensagem;
# 2. Converta cada caractere em seu código;
# 3. Converta cada código para binário;
# 4. Mostre os resultados no terminal;
# 5. Informe a quantidade de caracteres;
# 6. Informe a quantidade de bytes;
# 7. Informe a quantidade total de bits.

mensagem = input("Digite sua mensagem: ")

print("Digite sua mensagem: {}".format(mensagem))

for caractere in mensagem:
    codigo = ord(caractere)
    binario = "{:08b}".format(codigo)
    print("{} -> {} -> {}".format(caractere, codigo, binario))

print("Caracteres: {}".format(len(mensagem)))
print("Bytes: {}".format(len(mensagem)))
print("Bits: {}".format(len(mensagem) * 8))
