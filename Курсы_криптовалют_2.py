import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime


class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Курсы криптовалют")
        self.root.geometry("450x400")

        # Переменные для хранения данных
        self.selected_coin_var = tk.StringVar()
        self.coin_info_label_var = tk.StringVar()
        self.result_label_var = tk.StringVar()

        # Словарь для хранения соответствия "Название (Символ)" -> "id" (для API)
        # Создаем список из 10 самых популярных монет вручную
        self.coin_map = {
            "Bitcoin (BTC)": "bitcoin",
            "Ethereum (ETH)": "ethereum",
            "Tether (USDT)": "tether",
            "BNB (BNB)": "binancecoin",
            "Solana (SOL)": "solana",
            "XRP (XRP)": "ripple",
            "USD Coin (USDC)": "usd-coin",
            "Cardano (ADA)": "cardano",
            "Dogecoin (DOGE)": "dogecoin",
            "TRON (TRX)": "tron"
        }

        # --- 1. Метка "Выберите криптовалюту" ---
        self.label_choose = tk.Label(root, text="Выберите криптовалюту", font=("Arial", 10))
        self.label_choose.pack(pady=(20, 5))

        # --- 2. Выпадающий список  ---
        self.coin_combobox = ttk.Combobox(root, textvariable=self.selected_coin_var, state="readonly", width=35)
        self.coin_combobox.pack(pady=5)
        # Заполняем список ключами из словаря
        self.coin_combobox['values'] = list(self.coin_map.keys())
        # Привязываем событие выбора элемента
        self.coin_combobox.bind("<<ComboboxSelected>>", self.on_coin_selected)

        # --- 3. Появляющаяся метка  ---
        self.coin_info_label = tk.Label(root, textvariable=self.coin_info_label_var, font=("Arial", 10, "bold"),
                                        fg="blue")
        self.coin_info_label.pack(pady=5)

        # --- 4. Метка "Целевая валюта - доллар США" ---
        self.label_target = tk.Label(root, text="Целевая валюта - доллар США", font=("Arial", 10))
        self.label_target.pack(pady=15)

        # --- 5. Кнопки  ---
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.btn_request = tk.Button(button_frame, text="Запросить курс", width=15, command=self.request_coin_data)
        self.btn_request.pack(side=tk.LEFT, padx=10)

        self.btn_update = tk.Button(button_frame, text="Обновить курс", width=15, command=self.request_coin_data)
        self.btn_update.pack(side=tk.RIGHT, padx=10)

        # --- 6. Метка для вывода результата ---
        self.result_label = tk.Label(root, textvariable=self.result_label_var, font=("Arial", 10), justify=tk.LEFT,
                                     wraplength=400)
        self.result_label.pack(pady=20)

    def fetch_data_from_api(self, endpoint, params=None):
        """
        Функция обращения к API CoinGecko без обработки ошибок.
        """
        base_url = "https://api.coingecko.com/api/v3"
        url = f"{base_url}{endpoint}"

        response = requests.get(url, params=params, timeout=10)
        return response.json()

    def on_coin_selected(self, event):
        """
        Обработчик выбора валюты из списка.
        Обновляет появляющуюся метку с названием и тикером.
        """
        selection = self.selected_coin_var.get()
        if selection:
            self.coin_info_label_var.set(f"Выбрано: {selection}")
            # Сбрасываем старый результат при выборе новой монеты
            self.result_label_var.set("")

    def request_coin_data(self):
        """
        Логика получения и вывода курса.
        Вызывается кнопками 'Запросить курс' и 'Обновить курс'.
        """
        selection = self.selected_coin_var.get()

        # Проверка, что монета выбрана
        if not selection:
            self.result_label_var.set("Сначала выберите криптовалюту из списка.")
            return

        coin_id = self.coin_map[selection]

        # Показываю пользователю, что идет загрузка
        self.result_label_var.set("Загрузка данных...")
        self.root.update()

        # Запрос к API для получения цены и изменения за 24 часа
        data = self.fetch_data_from_api("/simple/price", params={
            "ids": coin_id,
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        })

        # Прямое обращение к данным (без проверки на ошибки)
        coin_data = data[coin_id]
        price = coin_data['usd']
        change_24h = coin_data.get('usd_24h_change', 0)

        # Форматируем вывод
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        # Определяем направление изменения
        if change_24h > 0:
            trend = "▲"
        elif change_24h < 0:
            trend = "▼"
        else:
            trend = "="

        result_text = (
            f"Валюта: {selection}\n"
            f"Текущий курс: {price} USD\n"
            f"Изменение за 24ч: {change_24h:.2f}% {trend}\n"
            f"Дата и время: {current_time}"
        )

        self.result_label_var.set(result_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()