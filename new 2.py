import ccxt
import time

# Configuración de la estrategia y parámetros
ema_length = 20
rsi_length = 14
overbought_level = 70
oversold_level = 30

# Configura tu clave API y secreto
api_key = 'NUEVA_API_KEY'
api_secret = 'NUEVO_API_SECRET'

# Inversión y riesgo
initial_investment = 1000  # Tu inversión en dólares
risk_percentage = 1  # Porcentaje de riesgo por operación (1% en este caso)

# Cálculo del tamaño de posición
def calculate_position_size(entry_price, stop_loss_price):
    risk_amount = initial_investment * (risk_percentage / 100)
    position_size = risk_amount / (entry_price - stop_loss_price)
    return position_size

# Crea una instancia del intercambio Kraken
exchange = ccxt.kraken({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
})

# Resto del código (calcula EMA, RSI, condiciones de entrada y salida, etc.)

while True:
    try:
        # Obtén datos del par de trading en Kraken (ajusta según tu par)
        ohlcv = exchange.fetch_ohlcv('BTC/USD', timeframe='1h', limit=ema_length + rsi_length)
        close_prices = [ohlcv[i][4] for i in range(len(ohlcv))]
        
        # Resto del código (calcula EMA, RSI, condiciones de entrada y salida, etc.)
        
        # Condiciones de entrada y salida
        if rsi < oversold_level and close_prices[-1] > ema:
            print("Señal de entrada larga")
            
            # Calcular tamaño de posición y stop loss
            entry_price = close_prices[-1]
            stop_loss_price = entry_price - (entry_price * risk_percentage / 100)
            position_size = calculate_position_size(entry_price, stop_loss_price)
            
            # Realizar la operación de compra usando exchange.create_limit_buy_order() o similar
            
        elif rsi > overbought_level and close_prices[-1] < ema:
            print("Señal de entrada corta")
            
            # Calcular tamaño de posición y stop loss
            entry_price = close_prices[-1]
            stop_loss_price = entry_price + (entry_price * risk_percentage / 100)
            position_size = calculate_position_size(entry_price, stop_loss_price)
            
            # Realizar la operación de venta usando exchange.create_limit_sell_order() o similar
        
        time.sleep(3600)  # Esperar una hora antes de verificar de nuevo
    except Exception as e:
        print("Error:", e)
