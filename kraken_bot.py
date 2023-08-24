import ccxt
import time

# Configuración de la estrategia y parámetros
ema_length = 20
rsi_length = 14
overbought_level = 70
oversold_level = 30

# Configura tu clave API y secreto
api_key = '7KHDMJfdVZObK4v7a9wxnnCi20LQWnMgCm1FjY7wovtI7/r+zgsGgR+z'
api_secret = 'Gq2Bxt+xcC2SmPokJ7DXmosOgHOfejwKDEIRVvV4oZWfqs+XFvSyjaTR41tzCmwgv3h+xkUKgq7qLhGDPBaTmQ=='

# Inversión y riesgo
initial_investment = 1000  # Tu inversión en dólares
risk_percentage = 1  # Porcentaje de riesgo por operación (1% en este caso)

# Cálculo del tamaño de posición
def calculate_position_size(entry_price, stop_loss_price):
    risk_amount = initial_investment * (risk_percentage / 100)
    position_size = risk_amount / (entry_price - stop_loss_price)
    
# Crea una instancia del intercambio Kraken
exchange = ccxt.kraken({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
})

def calculate_ema(data, length):
    return sum(data[-length:]) / length

def calculate_rsi(data, length):
    deltas = [data[i] - data[i - 1] for i in range(1, len(data))]
    gains = [delta if delta > 0 else 0 for delta in deltas]
    losses = [-delta if delta < 0 else 0 for delta in deltas]
    avg_gain = sum(gains[-length:]) / length
    avg_loss = sum(losses[-length:]) / length
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    return 100 - (100 / (1 + rs))

while True:
    try:
        # Obtén datos del par de trading en Kraken (ajusta según tu par)
        ohlcv = exchange.fetch_ohlcv('BTC/USD', timeframe='1h', limit=ema_length + rsi_length)
        close_prices = [ohlcv[i][4] for i in range(len(ohlcv))]
        
        # Calcular EMA y RSI
        ema = calculate_ema(close_prices, ema_length)
        rsi = calculate_rsi(close_prices, rsi_length)
        
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
