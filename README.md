# 🔁 Simulador y Optimizador de Trading entre Exchanges

Este proyecto permite simular la ejecución de órdenes de compra o venta en múltiples exchanges (Binance y KuCoin), usando libros de órdenes reales en tiempo real. Además, implementa un modelo matemático de optimización para determinar la mejor distribución de la orden entre los exchanges disponibles, maximizando la eficiencia de la operación.

## 🧠 ¿Qué hace?

- Consulta los order books reales de Binance y KuCoin.
- Simula el resultado de ejecutar toda la orden en cada exchange.
- Calcula el precio promedio, slippage y comisión (`taker fee`).
- Optimiza la distribución entre exchanges usando programación numérica con restricciones.
- Muestra una tabla comparativa final clara y explicativa.

## 📦 Requisitos

- Python 3.9 o superior
- pip
- Entorno virtual recomendado

## 📁 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tu-usuario/nombre-del-repo.git
cd nombre-del-repo
```

2. Crea un entorno virtual y actívalo:

```bash
python -m venv venv
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## 🚀 Cómo usarlo

Ejecuta el simulador desde consola:

```bash
python main.py
```

Sigue las instrucciones interactivas para:

- Seleccionar el tipo de operación (`buy` o `sell`).
- Ingresar el par de trading (`ETHUSDT`, `BTCETH`, etc.).
- Especificar la cantidad a operar.
- Elegir si la cantidad corresponde a la moneda base o quote.

Al finalizar, se mostrará una tabla comparativa entre los exchanges y la mejor distribución óptima calculada por el modelo matemático.

## ⚙️ Estructura del Proyecto

```
optimizador_PDG_JESLAVA_ASEGURAT202501-/
├── main.py
├── config.py
├── requirements.txt
├── exchanges/
│   ├── binance.py
│   ├── kucoin.py
├── utils/
│   ├── simulation.py
│   ├── optimization.py
```

## 📈 Extensibilidad

- Puedes añadir más exchanges agregando sus módulos dentro de la carpeta `exchanges/`.
- El modelo de optimización se adapta automáticamente a cualquier número de exchanges.

## 📚 Documentación

Consulta el archivo `documentacion/` para ver el documento del proyecto de grado.

## 🧑‍💻 Autor

**Juan Andrés Eslava Tovar**  
**Alejandro José Segura Torres**  
Proyecto de grado – Ingeniería de Sistemas y Computación  
Universidad de los Andes
