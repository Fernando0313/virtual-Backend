

colores =['morado','azul','rosado','amarillo','azul']
mezclada=['otoño',14,False,15.2,[1,2,3]]
print(colores[0])
print(colores)
colores.remove('azul')
print(colores)



persona = {
    'nombre': 'Eduardo',
    'nombre': 'Ramiro',
    'apellido': 'de Rivero',
    'correo': 'correo@correo.com',
    'edad': 28,
    'donacion_organos': True,
    'hobbies': [
        {
            'nombre': 'Volar drones',
            'conocimiento': 'avanzado',
        },
        {
            'nombre': 'Montar bici',
            'conocimiento': 'Intermedio'
        }
    ]
}
print(persona['hobbies'][0]['nombre'])