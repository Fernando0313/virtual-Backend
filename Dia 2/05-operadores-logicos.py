
frutas=['carambola','guayabana','higo','melocoton']
frutas=frutas[0]
fruta='platano'

print(id(fruta))
print(id(frutas))

frutas2=frutas
# frutas2.append('fresa')
print(frutas)
print(id(frutas2))
print(id(frutas))


# hacer copia sin que se ubique en la misma memoria id
frutas_variadas=frutas.copy
print(id(frutas_variadas))
print(id(frutas))