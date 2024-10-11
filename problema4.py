path = '/workspaces/PythonPC4/temperaturas.txt'

with open(path, mode = 'r') as file:
    lineas = file.readlines()
lineas

temperaturas = []
for linea in lineas:
    
    _, temperatura = linea.strip().split(',')
    temperatura = float(temperatura)
    temperatura.append(temperatura)
temperaturas

temperatura_max = max(temperaturas)
temperatura_min = min(temperaturas)
temperatura_promedio = sum(temperaturas)/len(temperaturas)


print('temperatura maxima: {temperatura_max}')
print('temperatura minima: {temperatura_min}')
print('temperatura_promedio: {temperatura_promedio}')

with open('resumen_temperaturas.txt',mode ='w') as file:
    file.write(f'temperatura maxima: {temperatura_max}')
    file.write(f'temperatura minima: {temperatura_min}')
    file.write(f'temperatura_promedio: {temperatura_promedio}')