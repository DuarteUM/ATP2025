TPC2 Duarte Matos; A110102;
<img width="2316" height="3088" alt="image" src="https://github.com/user-attachments/assets/d91980a5-6755-4c81-8bdd-e6c016b30471" />
Resumo: Tpc1 é criar no VSCode um código para o "Jogo dos 21 fóforos" em duas etapas uma em que nós os jogadores começamos o jogo e uma em que o computador comece, e o objetivo é que o computador ganhe 100% das vezes em que nós formos os primeiros a jogar e que saiba aproveitar os nossos erros quando for o primeiro a jogar. Basicamente no jogo existem 21 fósforos cada jogador escolher um numero de 1 a 4 para retirar os fósforos e quem ficar com o último perde. Tpc2 é criar também um código no VSCode que funcione como o jogo "Adivinha o número", onde existem duas modalidades: na primeira, o computador pensa num número entre 0 e 100 e o utilizador tenta adivinhar; na segunda, o utilizador pensa num número entre 0 e 100 e o computador tenta adivinhar, devendo usar a lógica para descobrir o número corretamente. Em ambos os casos, o programa deve informar se o palpite está certo ou se o número pensado é maior ou menor, e no final mostrar quantas tentativas foram necessárias para acertar.
Jogo dos Fósforos:
<img width="1917" height="1198" alt="fosforo1" src="https://github.com/user-attachments/assets/bcc4c7a2-ccea-4c03-9560-cff551b2f419" />
<img width="1918" height="1198" alt="fosforo2" src="https://github.com/user-attachments/assets/e1915362-34f8-4cf6-a61b-6ea42b555f99" />
[Jogo21final.py](https://github.com/user-attachments/files/22578481/Jogo21final.py)

print("Vamos jogar aos 21 fósforos, quem ficar com o último perde!")

n1 = 21
jogador = int(input("Queres ser o primeiro ou o segundo? 1 ou 2? "))
jogada1 = True

if jogador == 1:
    print("És o primeiro a jogar!")
else:
    print("És o segundo a jogar!")

while n1 > 1:
    if jogador == 1:
        # Jogada do jogador 1
        while True:
            jogar = int(input("Quantos fósforos queres retirar? De 1 a 4? "))
            if jogar < 1 or jogar > 4:
                print("Número inválido! Tens que escolher entre 1 e 4 fósforos.")
            elif jogar > n1 - 1:
                print(f"Número inválido! Só restam {n1-1} fósforos para retirar.")
            else:
                break
        n1 = n1 - jogar
        print(f"Número de fósforos restantes: {n1}")

        if n1 == 1:
            print("Perdeste o jogo!")
            break

        # Jogada do computador
        print("É a vez do computador!")
        computador = (n1 - 1) % 5
        if computador == 0:
            computador = 1
        if computador > n1 - 1:
            computador = n1 - 1
        print(f"Computador retirou {computador} fósforos")
        n1 = n1 - computador
        print(f"Número de fósforos restantes {n1}")

        if n1 == 1:
            print("Perdeste o jogo!")
            break

    elif jogador == 2:
        if jogada1 == True:
            nc = 1
            print(f"O computador retirou {nc} fósforos!")
            n1 = n1 - nc
            print(f"Restam {n1} fósforos!")
            jogada1 = False
            if n1 == 1:
                print("Perdeste o jogo!")
                break
        else:
            # Jogada do jogador 2
            while True:
                jogar = int(input("Quantos fósforos queres retirar? De 1 a 4? "))
                if jogar < 1 or jogar > 4:
                    print("Número inválido! Tens que escolher entre 1 e 4 fósforos.")
                elif jogar > n1 - 1:
                    print(f"Número inválido! Só restam {n1-1} fósforos para retirar.")
                else:
                    break
            n1 = n1 - jogar
            if n1 == 1:
                print(f"Número de fósforos restantes {n1}")
                print("O computador perdeu o jogo!")
                break
            print(f"Número de fósforos restantes {n1}")

            # Jogada do computador
            print("É a vez do computador jogar!")
            computador = (n1 - 1) % 5
            if computador == 0:
                computador = 1
            if computador > n1 - 1:
                computador = n1 - 1
            print(f"Computador retirou {computador} fósforos")
            n1 = n1 - computador
            print(f"Número de fósforos restantes {n1}")

            if n1 == 1:
                print("Perdeste o jogo!")
                break
Jogo 2:





