from PIL.Image import Image
import numpy as np

class UnicodeConverter:
    def convert_image_to_unicode(self, image: Image) -> str:
        upper_block = "▀"
        lower_block = "▄"
        empty_block = " "

        unicode_sprite = ""
        unicode_sprite2 = ""

        # Función auxiliar para mostrar un bloque de color en la consola (para debug)
        # np.array([246, 213, 49, 255])

        def color_swatch(pixel: np.ndarray) -> str:
            # Solo cogemos los 3 primeros RGB que nos interesan para vomitar por pantalla
            r, g, b = pixel[:3]
            # Cadena ANSI
            return f"\x1b[48;2;{r};{g};{b}m  \x1b[0m"
        
        def convert_to_rgba(image: Image) -> Image:
            if image.mode != "RGBA":
                rgba_image = image.convert("RGBA")
                return rgba_image
            return image
        


        print("[UnicodeConverter] Iniciando conversion a unicode")
        print(f"[UnicodeConverter] image.mode={image.mode}, image.size={image.size}")

        image = convert_to_rgba(image)

        image_array = np.array(image)
        height, width, channels = image_array.shape
        print(
            f"[UnicodeConverter] array.shape={image_array.shape} "
            f"(height={height}, width={width}, channels={channels})"
        )

        # as we're mapping two pixels to one character, we need an even number
        # of pixels as height. So adding an empty row at the bottom for odd heights
        if height % 2:
            print("[UnicodeConverter] Altura impar detectada, anadiendo fila vacia al final")
            empty_row = np.zeros((1, width, channels), dtype=np.uint8)
            image_array = np.vstack((image_array, empty_row))
            height, width, channels = image_array.shape
            print(
                f"[UnicodeConverter] Nueva array.shape={image_array.shape} "
                f"(height={height}, width={width}, channels={channels})"
            )
        # Eliminamos el padding transparente alrededor de la imagen para optimizar el resultado

        # Ejemplo para una imagen de 4x4 píxeles:
        # (y,x): (0,0) (0,1) (0,2) (0,3) R G B
        #        (1,0) (1,1) (1,2) (1,3)
        #        (2,0) (2,1) (2,2) (2,3)
        #        (3,0) (3,1) (3,2) (3,3)

        # y recorremos de 2 en 2 filas porque un carácter representa 2 píxeles verticales

        for y in range(0, height, 2):
            print(f"[UnicodeConverter] Procesando filas y={y} y y+1={y + 1}")
            row_output = ""
            # y: recorrido de filas, x: recorrido de columnas 
            for x in range(width):
                # Pillamos el pixel de arriba y luego el de abajo 
                top_pixel = image_array[y, x]
                bottom_pixel = image_array[y + 1, x]
                
                #print(
                #    f"[UnicodeConverter] Pixel superior (y={y}, x={x}): "
                #    f"{top_pixel} {color_swatch(top_pixel)}"
                #)
                #print(
                #    f"[UnicodeConverter] Pixel inferior (y={y + 1}, x={x}): "
                #    f"{bottom_pixel} {color_swatch(bottom_pixel)}"
                #)

                if top_pixel[3] == 0 and bottom_pixel[3] == 0:
                    unicode_sprite += empty_block
                    print(f"[UnicodeConverter] Ambos píxeles transparentes, añadiendo bloque vacío)")
                    
                # Caso: arrriba no haya nada: "▄"
                elif top_pixel[3] == 0:
                    r , g , b = bottom_pixel[:3]
                    ansi_code = f"\x1b[38;2;{r};{g};{b}m"+lower_block+"\x1b[0m"
                    unicode_sprite += ansi_code
                    print(f"[UnicodeConverter]   Píxel superior transparente, añadiendo bloque inferior ansi_code={ansi_code}")
                # Caso: abajo no haya nada: "▀"
                elif bottom_pixel[3] == 0:
                    r , g , b = top_pixel[:3]
                    ansi_code = f"\x1b[38;2;{r};{g};{b}m"+upper_block+"\x1b[0m"
                    unicode_sprite += ansi_code
                    print(f"[UnicodeConverter] Píxel inferior transparente, añadiendo bloque superior ansi_code={ansi_code}")

                # Caso: ambos píxeles tienen color. Usamos "▀" con el color del pixel superior
                # pero el background sera del pixel inferior
                else:
                    rtop, gtop, btop = top_pixel[:3]
                    rbot, gbot, bbot = bottom_pixel[:3]
                    # Añadimos 38: color de texto de arriba y 48: color de fondo de abajo
                    ansi_code = f"\x1b[38;2;{rtop};{gtop};{btop}m\x1b[48;2;{rbot};{gbot};{bbot}m"+upper_block+"\x1b[0m"
                    unicode_sprite += ansi_code
                    print(f"[UnicodeConverter] ansi_code={ansi_code}")
                    print(f"[UnicodeConverter] Ambos píxeles tienen color, añadiendo bloque con colores combinados)")

            unicode_sprite += "\n" # Nueva línea al final de cada fila procesada
        unicode_sprite += "\x1b[0m" # Reset al final para evitar que el color se escape a lo que venga después    
        return unicode_sprite
