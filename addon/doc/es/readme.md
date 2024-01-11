# Complemento ayudante de Webcam para NVDA
Este complemento para [NVDA], un lector de pantalla gratuito y de código abierto para Microsoft Windows, ayuda a que se te vea mejor en videollamadas al indicarte instrucciones acerca de cómo posicionartte al frente de la cámara. Usa el reconocimiento facial y el procesamiento de imagen para detectar si estás de lado o verticalmente, así como determinar si la iluminación es suficiente.

# Instalación
Este complemento contiene dependencias binarias que requieren los componentes redistribuíbles de Visual C++ para 32 bits, [descargar directamente desde Microsoft](https://aka.ms/vs/17/release/vc_redist.x86.exe)

# Uso
Después de instalar el complemento, presiona NVDA+shift+W y sigue las instrucciones. Después de que escuches el mensaje "la cara está posicionada correctamente", puedes presionar escape para detener la función y liberar la cámara.

# Convenciones de desarrollo
Como esto es un complemento de NVDA, el código se ejecuta dentro del proceso del lector de pantalla, por lo que tiene que trabajar en un entorno de desarrollo en específico (Python 3.7 32bit) y brindar consigo sus dependencias. Además, el código establecido en NVDA es diferente que el de pep8 por razones históricas, pero es aplicado aquí por consistencia.

[NVDA]: https://github.com/nvaccess/nvda
