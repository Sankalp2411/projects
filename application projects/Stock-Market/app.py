import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from main_predict import run_prediction
from main_agent import run_agent


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Market AI")
        self.root.geometry("900x650")

        self.mode = tk.StringVar(value="predict")

        self.canvas = None  # holds graph

        self.build_ui()

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Stock Market AI", font=("Arial", 18)).pack(pady=10)

        # Mode buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Predict Stocks",
                   command=lambda: self.mode.set("predict")).pack(side="left", padx=10)

        ttk.Button(btn_frame, text="See Stocks",
                   command=lambda: self.mode.set("agent")).pack(side="left", padx=10)

        # Inputs
        self.symbol = self.create_input(frame, "Symbol", "AAPL")
        self.period = self.create_input(frame, "Period", "1y")
        self.epochs = self.create_input(frame, "Epochs", "20")
        self.window = self.create_input(frame, "Window", "30")
        self.sims = self.create_input(frame, "Simulations", "3")
        self.initial = self.create_input(frame, "Initial Money", "10000")
        self.skip = self.create_input(frame, "Skip Days", "2")

        ttk.Button(frame, text="RUN", command=self.run).pack(pady=15)

        # Graph container
        self.graph_frame = ttk.Frame(frame)
        self.graph_frame.pack(fill="both", expand=True)

    def create_input(self, parent, label, default):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=3)

        ttk.Label(frame, text=label, width=18).pack(side="left")

        entry = ttk.Entry(frame)
        entry.insert(0, default)
        entry.pack(side="left", fill="x", expand=True)

        return entry

    def clear_graph(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

    def run(self):
        self.clear_graph()

        sym = self.symbol.get()
        per = self.period.get()
        ep = int(self.epochs.get())

        fig, ax = plt.subplots(figsize=(8, 4))

        if self.mode.get() == "predict":
            data = run_prediction(
                sym,
                per,
                ep,
                int(self.window.get()),
                int(self.sims.get())
            )

            ax.plot(data["real"], label="Real Price")
            ax.plot(data["pred"], label="Prediction")

            ax.set_title(f"{sym} Prediction")

        else:
            data = run_agent(
                sym,
                per,
                ep,
                float(self.initial.get()),
                int(self.skip.get()),
                int(self.sims.get())
            )

            ax.plot(data["prices"], label="Price")

            ax.scatter(data["buys"],
                       [data["prices"][i] for i in data["buys"]],
                       marker="^", label="Buy")

            ax.scatter(data["sells"],
                       [data["prices"][i] for i in data["sells"]],
                       marker="v", label="Sell")

            ax.set_title(f"{sym} Trading | Profit: {data['profit']:.2f}")

        ax.legend()

        # 🔥 EMBED GRAPH (NO NEW WINDOW)
        self.canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()