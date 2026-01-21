# Lógica de Machine Learning: Procesamiento de Lenguaje
def cerebro_ia_mercadolibre(comentario):
    # Diccionario de entrenamiento (Patrones de datos)
    palabras_positivas = ["excelente", "bueno", "increible", "comprar"]
    palabras_negativas = ["malo", "estafa", "basura", "caro"]
    
    puntuacion = 0
    palabras = comentario.lower().split()
    
    for p in palabras:
        if p in palabras_positivas: puntuacion += 1
        if p in palabras_negativas: puntuacion -= 1
        
    # Resultado de la IA
    if puntuacion > 0: return "IA: El cliente está feliz. (Recomendación: Escalar negocio)"
    elif puntuacion < 0: return "IA: El cliente está enojado. (Recomendación: Revisar soporte)"
    else: return "IA: Comentario neutral."

# Prueba de tu cerebro artificial
print(cerebro_ia_mercadolibre("Este software es excelente y bueno para ganar dinero"))