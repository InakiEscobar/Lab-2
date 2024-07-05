from typing import List
'''CÓDIGO WRAP'''

def cuadrado(n):
    return n * n

def ajustarPalabrasUtil(palabras, n, ancho, indicePalabra, longitudRestante, memo):
    # Caso base para la última palabra
    if indicePalabra == n - 1:
        memo[indicePalabra][longitudRestante] = 0 if (palabras[indicePalabra] < longitudRestante) else cuadrado(longitudRestante)
        return memo[indicePalabra][longitudRestante]

    palabraActual = palabras[indicePalabra]
    # Si la palabra cabe en la línea restante
    if palabraActual < longitudRestante:
        memo[indicePalabra][longitudRestante] = min(
            ajustarPalabrasConMemo(
                palabras, n, ancho, indicePalabra + 1,
                longitudRestante - palabraActual if (longitudRestante == ancho) else longitudRestante - palabraActual - 1,
                memo
            ),
            cuadrado(longitudRestante) + ajustarPalabrasConMemo(
                palabras, n, ancho, indicePalabra + 1,
                ancho - palabraActual, memo
            )
        )
    else:
        # Si la palabra se coloca en la siguiente línea
        memo[indicePalabra][longitudRestante] = (cuadrado(longitudRestante) + ajustarPalabrasConMemo(
            palabras, n, ancho, indicePalabra + 1,
            ancho - palabraActual, memo
        ))

    return memo[indicePalabra][longitudRestante]

def ajustarPalabrasConMemo(palabras, n, ancho, indicePalabra, longitudRestante, memo):
    if memo[indicePalabra][longitudRestante] != -1:
        return memo[indicePalabra][longitudRestante]

    memo[indicePalabra][longitudRestante] = ajustarPalabrasUtil(palabras, n, ancho, indicePalabra, longitudRestante, memo)
    return memo[indicePalabra][longitudRestante]

def ajustarPalabras(palabras, n, ancho):
    memo = [[-1] * (ancho + 1) for _ in range(n)]
    ajustarPalabrasConMemo(palabras, n, ancho, 0, ancho, memo)
    return memo

'''FIN CÓDIGO WRAP'''

'''FUNCIÓN AUXILIAR PARA CALCULAR LOS SALTOS DE LÍNEA'''

def calcularSaltosLineas(largos: List[int], anchoMaximo: int, memo: List[List[int]]) -> List[List[int]]:
    """
    Args:
        largos: lista de longitudes de palabras
        anchoMaximo: ancho máximo de la línea
        memo: matriz de memoización de ajustarPalabras

    Returns: lista de saltos de línea
    """
    n = len(largos)
    lineas = []
    i = 0

    while i < n:
        linea = []
        longitudActual = anchoMaximo

        while i < n:
            longitudRestante = longitudActual - largos[i] - 1  # Longitud restante si agregamos la palabra y un espacio

            # Verificar si la palabra cabe en la línea actual y si corresponde al costo mínimo
            if longitudRestante >= 0 and memo[i][longitudRestante] == min(memo[i][longitudRestante],
                                                                         cuadrado(longitudActual) + memo[i][anchoMaximo - largos[i]]):
                linea.append(largos[i])
                longitudActual = longitudRestante  # Actualizar la longitud restante
                i += 1
            else:
                break

        lineas.append(linea)

    return lineas

'''FUNCIÓN AUXILIAR PARA LEER UN ARCHIVO DE TEXTO O UN DOCUMENTO DOCX'''

def leerArchivoTexto(file_path: str) -> str:
    """
    Args:
        file_path: ruta al archivo de texto o documento docx

    Returns: texto del archivo
    """
    try:
        if file_path.endswith('.docx'):
            doc = Document(file_path)
            return '\n'.join([para.text for para in doc.paragraphs])
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
    except OSError as e:
        return f"Error al abrir el archivo: {e}"

'''FUNCIÓN AUXILIAR PARA ACTUALIZAR UN ARCHIVO DE TEXTO'''

def actualizarArchivoTexto(filename: str, textoFormateado: str) -> None:
    """
    Actualiza un archivo de texto existente con el texto formateado.

    Args:
    - filename (str): El nombre del archivo de texto a actualizar.
    - textoFormateado (str): El texto formateado que se añadirá al archivo.

    Returns:
    - None
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(textoFormateado)
    except OSError as e:
        print(f"Error al actualizar el archivo: {e}")

'''FUNCIÓN PRINCIPAL'''

def formatearTexto(texto: str, anchoMaximo: int) -> List[str]:
    """
    Args:
        texto: texto a formatear
        anchoMaximo: ancho máximo de la línea

    Returns: lista de líneas
    """
    # Restricciones
    if len(texto) > 1000 or len(texto) < 1:
        return ["Error: texto fuera del límite de caracteres"]
    if anchoMaximo > 100 or anchoMaximo < 1:
        return ["Error: anchoMaximo fuera del límite de caracteres"]

    # Separación de palabras
    listaTexto = texto.split()
    longitudesPalabras = [len(palabra) for palabra in listaTexto]
    n = len(longitudesPalabras)

    # Cálculo de saltos de línea óptimos
    memo = ajustarPalabras(longitudesPalabras, n, anchoMaximo)
    saltosLinea = calcularSaltosLineas(longitudesPalabras, anchoMaximo, memo)

    # Distribuir equitativamente los espacios
    resultado = []
    indice = 0
    for i, linea in enumerate(saltosLinea):
        if i == len(saltosLinea) - 1:
            textoLinea = ' '.join(listaTexto[indice:indice + len(linea)])
        else:
            textoLinea = listaTexto[indice]
            longitudLinea = len(textoLinea)
            for j in range(1, len(linea)):
                textoLinea += ' ' + listaTexto[indice + j]
                longitudLinea += len(listaTexto[indice + j]) + 1

            espaciosTotales = anchoMaximo - longitudLinea
            espaciosNecesarios = len(linea) - 1
            if espaciosNecesarios > 0:
                espaciosExtra = espaciosTotales // espaciosNecesarios
                espaciosRestantes = espaciosTotales % espaciosNecesarios

                textoLinea = listaTexto[indice]
                for j in range(1, len(linea)):
                    espacios = ' ' * (espaciosExtra + 1)
                    if j <= espaciosRestantes:
                        espacios += ' '
                    textoLinea += espacios + listaTexto[indice + j]

        resultado.append(textoLinea)
        indice += len(linea)

    return resultado

def main():
    # Leer texto del archivo
    print('Inserta la ruta del archivo de texto (incluyendo el nombre del archivo):')
    rutaArchivo = input().strip()
    print(f"Ruta del archivo ingresada: {rutaArchivo}")  # Agregar mensaje de depuración
    texto = leerArchivoTexto(rutaArchivo)

    if texto.startswith("Error"):
        print(texto)
        return

    print('Inserta el ancho máximo:')
    try:
        anchoMaximo = int(input().strip())
    except ValueError:
        print("Error: ancho máximo no válido")
        return

    textoFormateado = formatearTexto(texto, anchoMaximo)
    if textoFormateado[0].startswith("Error"):
        print(textoFormateado[0])
    else:
        # Actualizar el archivo de texto existente con el texto formateado
        actualizarArchivoTexto(rutaArchivo, '\n'.join(textoFormateado))
        print(f'Texto formateado actualizado en "{rutaArchivo}".')

if __name__ == "__main__":
    main()
