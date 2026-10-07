import tkinter as tk
from tkinter import ttk
import requests  # Библиотека для запросов к API (нужно установить: pip install requests)


class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Курсы криптовалют")
        self.root.geometry("400x350")

        # Переменные для хранения данных
        self.selected_coin_var = tk.StringVar()
        self.coin_info_label_var = tk.StringVar()
        self.result_label_var = tk.StringVar()

        # --- 1. Метка "Выберите криптовалюту" ---
        self.label_choose = tk.Label(root, text="Выберите криптовалюту", font=("Arial", 10))
        self.label_choose.pack(pady=(20, 5))

        # --- 2. Выпадающий список  ---
        self.coin_combobox = ttk.Combobox(root, textvariable=self.selected_coin_var, state="readonly", width=30)
        self.coin_combobox.pack(pady=5)

        # --- 3. Появляющаяся метка (название и обозначение выбранной криптовалюты) ---
        self.coin_info_label = tk.Label(root, textvariable=self.coin_info_label_var, font=("Arial", 10, "bold"))
        self.coin_info_label.pack(pady=5)

        # --- 4. Метка "Целевая валюта - доллар США" ---
        self.label_target = tk.Label(root, text="Целевая валюта - доллар США", font=("Arial", 10))
        self.label_target.pack(pady=15)

        # --- 5. Кнопки (Слева и Справа) ---
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.btn_request = tk.Button(button_frame, text="Запросить курс", width=15, command=self.on_request_click)
        self.btn_request.pack(side=tk.LEFT, padx=10)

        self.btn_update = tk.Button(button_frame, text="Обновить курс", width=15, command=self.on_update_click)
        self.btn_update.pack(side=tk.RIGHT, padx=10)

        # --- 6. Метка для вывода результата ---
        self.result_label = tk.Label(root, textvariable=self.result_label_var, font=("Arial", 9), justify=tk.LEFT)
        self.result_label.pack(pady=20)

    def fetch_data_from_api(self, endpoint):
        """
        Для обращения к API CoinGecko.
        """
        base_url = "https://api.coingecko.com/api/v3"
        url = f"{base_url}{endpoint}"

        print(f"Запрос к API: {url}")
        return None

    def on_request_click(self):
        """Обработчик нажатия кнопки 'Запросить курс'"""
        # Пока просто заглушка
        print("Нажата кнопка 'Запросить курс'")
        self.result_label_var.set("Ожидание запроса...")

        # Пример вызова будущей функции API
        # data = self.fetch_data_from_api("/simple/price?ids=bitcoin&vs_currencies=usd")

    def on_update_click(self):
        """Обработчик нажатия кнопки 'Обновить курс'"""
        print("Нажата кнопка 'Обновить курс'")
        # Логика обновления будет добавлена позже


if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoApp(root)
    root.mainloop()