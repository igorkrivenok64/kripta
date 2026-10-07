import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime


class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Курсы криптовалют")
        self.root.geometry("450x400")

        # Переменные интерфейса
        self.selected_coin_var = tk.StringVar()
        self.coin_info_label_var = tk.StringVar()
        self.result_label_var = tk.StringVar()

        # Словарь: отображаемое имя -> id для API
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

        # Метка заголовка
        self.label_choose = tk.Label(root, text="Выберите криптовалюту", font=("Arial", 10))
        self.label_choose.pack(pady=(20, 5))

        # Выпадающий список
        self.coin_combobox = ttk.Combobox(root, textvariable=self.selected_coin_var, state="readonly", width=35)
        self.coin_combobox.pack(pady=5)
        self.coin_combobox['values'] = list(self.coin_map.keys())
        self.coin_combobox.bind("<<ComboboxSelected>>", self.on_coin_selected)

        # Метка с названием выбранной монеты
        self.coin_info_label = tk.Label(root, textvariable=self.coin_info_label_var, font=("Arial", 10, "bold"),
                                        fg="blue")
        self.coin_info_label.pack(pady=5)

        # Метка целевой валюты
        self.label_target = tk.Label(root, text="Целевая валюта - доллар США", font=("Arial", 10))
        self.label_target.pack(pady=15)

        # Фрейм для кнопок
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.btn_request = tk.Button(button_frame, text="Запросить курс", width=15, command=self.request_coin_data)
        self.btn_request.pack(side=tk.LEFT, padx=10)

        self.btn_update = tk.Button(button_frame, text="Обновить курс", width=15, command=self.request_coin_data)
        self.btn_update.pack(side=tk.RIGHT, padx=10)

        # Метка для вывода результата
        self.result_label = tk.Label(root, textvariable=self.result_label_var, font=("Arial", 10), justify=tk.LEFT,
                                     wraplength=400)
        self.result_label.pack(pady=20)

    def fetch_data_from_api(self, endpoint, params=None):
        """Запрос к API CoinGecko. Возвращает JSON или None при ошибке."""
        base_url = "https://api.coingecko.com/api/v3"
        url = f"{base_url}{endpoint}"

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            messagebox.showerror("Ошибка", "Превышено время ожидания ответа от сервера.")
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Ошибка", "Нет подключения к интернету.")
        except requests.exceptions.HTTPError as e:
            messagebox.showerror("Ошибка", f"Сервер вернул ошибку: {e}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка при запросе: {e}")
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный формат ответа от сервера.")

        return None

    def on_coin_selected(self, event):
        """Обновление метки при выборе монеты."""
        selection = self.selected_coin_var.get()
        if selection:
            self.coin_info_label_var.set(f"Выбрано: {selection}")
            self.result_label_var.set("")

    def request_coin_data(self):
        """Получение и отображение курса выбранной монеты."""
        selection = self.selected_coin_var.get()

        if not selection:
            messagebox.showwarning("Внимание", "Сначала выберите криптовалюту из списка.")
            return

        coin_id = self.coin_map.get(selection)
        if not coin_id:
            messagebox.showerror("Ошибка", "Неизвестная криптовалюта.")
            return

        self.result_label_var.set("Загрузка данных...")
        self.root.update()

        # Запрос цены и изменения за 24 часа
        data = self.fetch_data_from_api("/simple/price", params={
            "ids": coin_id,
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        })

        # Если запрос не удался — выходим
        if data is None:
            self.result_label_var.set("Не удалось получить данные.")
            return

        try:
            coin_data = data[coin_id]
            price = coin_data['usd']
            change_24h = coin_data.get('usd_24h_change', 0)
        except KeyError:
            messagebox.showerror("Ошибка", "В ответе сервера отсутствуют нужные данные.")
            self.result_label_var.set("Ошибка данных.")
            return
        except (TypeError, ValueError):
            messagebox.showerror("Ошибка", "Не удалось обработать полученные данные.")
            self.result_label_var.set("Ошибка данных.")
            return

        # Формирование строки результата
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

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