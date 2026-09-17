#app.py
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from main_predict import run_prediction
from main_agent import run_agent
import threading


class App:
    # ── Color Palette ──────────────────────────────────────────────
    BG_DARK     = "#0d1117"
    BG_CARD     = "#161b22"
    BG_INPUT    = "#0d1117"
    BG_HOVER    = "#1c2333"
    ACCENT      = "#4f8ff7"
    ACCENT_GLOW = "#5c9cff"
    ACCENT_2    = "#a371f7"
    TEXT_PRI    = "#e6edf3"
    TEXT_SEC    = "#8b949e"
    TEXT_MUTED  = "#484f58"
    BORDER      = "#21262d"
    BORDER_HL   = "#388bfd"
    SUCCESS     = "#3fb950"
    WARNING     = "#d29922"
    DANGER      = "#f85149"
    CHART_LINE  = "#58a6ff"
    CHART_PRED  = "#3fb950"

    def __init__(self, root):
        self.root = root
        self.root.title("Stock Market AI")
        self.root.geometry("1150x740")
        self.root.configure(bg=self.BG_DARK)
        self.root.minsize(960, 620)

        self.mode = tk.StringVar(value="predict")
        self.canvas = None
        self.fig = None
        self.is_running = False

        self._setup_fonts()
        self._build_ui()

    # ── Fonts ──────────────────────────────────────────────────────
    def _setup_fonts(self):
        self.f_title    = ("Segoe UI", 22, "bold")
        self.f_sub      = ("Segoe UI", 10)
        self.f_section  = ("Segoe UI", 9, "bold")
        self.f_label    = ("Segoe UI", 10)
        self.f_hint     = ("Segoe UI", 8)
        self.f_input    = ("Segoe UI", 10)
        self.f_btn      = ("Segoe UI", 11, "bold")
        self.f_run      = ("Segoe UI", 12, "bold")
        self.f_status   = ("Segoe UI", 9)
        self.f_ph_icon  = ("Segoe UI", 44)
        self.f_ph_text  = ("Segoe UI", 13)

    # ── Main Layout ───────────────────────────────────────────────
    def _build_ui(self):
        outer = tk.Frame(self.root, bg=self.BG_DARK)
        outer.pack(fill="both", expand=True, padx=24, pady=20)

        self._build_header(outer)

        content = tk.Frame(outer, bg=self.BG_DARK)
        content.pack(fill="both", expand=True, pady=(16, 0))

        self._build_sidebar(content)
        self._build_graph_area(content)

    # ── Header ────────────────────────────────────────────────────
    def _build_header(self, parent):
        hdr = tk.Frame(parent, bg=self.BG_DARK)
        hdr.pack(fill="x")

        row = tk.Frame(hdr, bg=self.BG_DARK)
        row.pack(fill="x")

        icon = tk.Label(row, text="📈", font=("Segoe UI Emoji", 26),
                        bg=self.BG_DARK, fg=self.TEXT_PRI)
        icon.pack(side="left", padx=(0, 14))

        txt = tk.Frame(row, bg=self.BG_DARK)
        txt.pack(side="left")
        tk.Label(txt, text="Stock Market AI", font=self.f_title,
                 bg=self.BG_DARK, fg=self.TEXT_PRI).pack(anchor="w")
        tk.Label(txt, text="LSTM Prediction  ·  Evolution Strategy Trading",
                 font=self.f_sub, bg=self.BG_DARK, fg=self.TEXT_SEC).pack(anchor="w")

        tk.Frame(hdr, bg=self.BORDER, height=1).pack(fill="x", pady=(14, 0))

    # ── Sidebar ───────────────────────────────────────────────────
    def _build_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=self.BG_CARD, width=310,
                           highlightbackground=self.BORDER, highlightthickness=1)
        sidebar.pack(side="left", fill="y", padx=(0, 16))
        sidebar.pack_propagate(False)

        inner = tk.Frame(sidebar, bg=self.BG_CARD)
        inner.pack(fill="both", expand=True, padx=20, pady=20)

        # ─── Mode toggle ─────────────────────────────────────────
        tk.Label(inner, text="MODE", font=self.f_section,
                 bg=self.BG_CARD, fg=self.TEXT_SEC).pack(anchor="w", pady=(0, 8))

        mode_fr = tk.Frame(inner, bg=self.BORDER)
        mode_fr.pack(fill="x", pady=(0, 18))

        self.btn_predict = tk.Button(
            mode_fr, text="📊  Predict", font=self.f_btn,
            bg=self.ACCENT, fg="white",
            activebackground=self.ACCENT_GLOW, activeforeground="white",
            bd=0, padx=16, pady=10, cursor="hand2",
            command=lambda: self._set_mode("predict"))
        self.btn_predict.pack(side="left", fill="x", expand=True)

        self.btn_agent = tk.Button(
            mode_fr, text="🤖  Trade", font=self.f_btn,
            bg=self.BG_INPUT, fg=self.TEXT_SEC,
            activebackground=self.BG_HOVER, activeforeground=self.TEXT_PRI,
            bd=0, padx=16, pady=10, cursor="hand2",
            command=lambda: self._set_mode("agent"))
        self.btn_agent.pack(side="left", fill="x", expand=True)

        # ─── Separator ───────────────────────────────────────────
        tk.Frame(inner, bg=self.BORDER, height=1).pack(fill="x", pady=(0, 14))

        # ─── Parameters ──────────────────────────────────────────
        tk.Label(inner, text="PARAMETERS", font=self.f_section,
                 bg=self.BG_CARD, fg=self.TEXT_SEC).pack(anchor="w", pady=(0, 10))

        self.symbol  = self._input(inner, "Symbol",       "AAPL",  "Ticker, e.g. AAPL, MSFT")
        self.period  = self._input(inner, "Period",       "1y",    "1d · 5d · 1mo · 1y · 5y")
        self.epochs  = self._input(inner, "Epochs",       "20",    "Training iterations")
        self.window  = self._input(inner, "Window",       "30",    "Lookback window size")
        self.sims    = self._input(inner, "Simulations",  "3",     "Population size")
        self.initial = self._input(inner, "Initial ($)",  "10000", "Starting capital")
        self.skip    = self._input(inner, "Skip Days",    "2",     "Trading interval")

        # ─── Spacer ──────────────────────────────────────────────
        tk.Frame(inner, bg=self.BG_CARD).pack(fill="both", expand=True)

        # ─── Status ──────────────────────────────────────────────
        self.status_var = tk.StringVar(value="● Ready")
        self.status_lbl = tk.Label(inner, textvariable=self.status_var,
                                   font=self.f_status, bg=self.BG_CARD,
                                   fg=self.SUCCESS, anchor="w")
        self.status_lbl.pack(fill="x", pady=(0, 12))

        # ─── Run button ──────────────────────────────────────────
        self.run_btn = tk.Button(
            inner, text="▶   RUN  ANALYSIS", font=self.f_run,
            bg=self.ACCENT, fg="white",
            activebackground=self.ACCENT_GLOW, activeforeground="white",
            bd=0, pady=14, cursor="hand2",
            command=self._run_threaded)
        self.run_btn.pack(fill="x", ipady=2)
        self._hover(self.run_btn, self.ACCENT, self.ACCENT_GLOW)

    # ── Graph area ────────────────────────────────────────────────
    def _build_graph_area(self, parent):
        self.graph_outer = tk.Frame(parent, bg=self.BG_CARD,
                                    highlightbackground=self.BORDER,
                                    highlightthickness=1)
        self.graph_outer.pack(side="left", fill="both", expand=True)

        # Placeholder
        self.ph = tk.Frame(self.graph_outer, bg=self.BG_CARD)
        self.ph.pack(fill="both", expand=True)
        tk.Label(self.ph, text="📊", font=self.f_ph_icon,
                 bg=self.BG_CARD, fg=self.TEXT_MUTED).pack(expand=True, anchor="s", pady=(0, 4))
        tk.Label(self.ph, text="Run an analysis to see results here",
                 font=self.f_ph_text, bg=self.BG_CARD,
                 fg=self.TEXT_MUTED).pack(expand=True, anchor="n")

        # Graph (hidden)
        self.graph_frame = tk.Frame(self.graph_outer, bg=self.BG_CARD)

    # ── Reusable input field ──────────────────────────────────────
    def _input(self, parent, label, default, hint=""):
        box = tk.Frame(parent, bg=self.BG_CARD)
        box.pack(fill="x", pady=(0, 9))

        top = tk.Frame(box, bg=self.BG_CARD)
        top.pack(fill="x")
        tk.Label(top, text=label, font=self.f_label,
                 bg=self.BG_CARD, fg=self.TEXT_PRI).pack(side="left")
        if hint:
            tk.Label(top, text=hint, font=self.f_hint,
                     bg=self.BG_CARD, fg=self.TEXT_MUTED).pack(side="right")

        entry = tk.Entry(box, font=self.f_input,
                         bg=self.BG_INPUT, fg=self.TEXT_PRI,
                         insertbackground=self.ACCENT,
                         selectbackground=self.ACCENT,
                         selectforeground="white",
                         bd=0, relief="flat")
        entry.insert(0, default)
        entry.pack(fill="x", ipady=7, pady=(4, 0))

        line = tk.Frame(box, bg=self.BORDER, height=1)
        line.pack(fill="x")

        entry.bind("<FocusIn>",  lambda e: line.configure(bg=self.ACCENT))
        entry.bind("<FocusOut>", lambda e: line.configure(bg=self.BORDER))
        return entry

    # ── Mode toggle ───────────────────────────────────────────────
    def _set_mode(self, mode):
        self.mode.set(mode)
        if mode == "predict":
            self.btn_predict.configure(bg=self.ACCENT, fg="white")
            self.btn_agent.configure(bg=self.BG_INPUT, fg=self.TEXT_SEC)
        else:
            self.btn_agent.configure(bg=self.ACCENT, fg="white")
            self.btn_predict.configure(bg=self.BG_INPUT, fg=self.TEXT_SEC)

    # ── Hover helper ──────────────────────────────────────────────
    def _hover(self, w, normal, hover):
        w.bind("<Enter>", lambda e: w.configure(bg=hover) if not self.is_running else None)
        w.bind("<Leave>", lambda e: w.configure(bg=normal) if not self.is_running else None)

    # ── Graph helpers ─────────────────────────────────────────────
    def _clear_graph(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        if self.fig:
            plt.close(self.fig)
            self.fig = None

    def _style_ax(self, ax, title, title_color=None):
        """Apply the dark theme to a matplotlib Axes."""
        tc = title_color or self.TEXT_PRI
        ax.set_facecolor(self.BG_DARK)
        ax.set_title(title, color=tc, fontsize=14, fontweight="bold", pad=16,
                     fontfamily="Segoe UI")
        ax.set_xlabel("Days", color=self.TEXT_SEC, fontsize=10, fontfamily="Segoe UI")
        ax.set_ylabel("Price ($)", color=self.TEXT_SEC, fontsize=10, fontfamily="Segoe UI")
        ax.tick_params(colors=self.TEXT_MUTED, labelsize=9)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)
        for spine in ("bottom", "left"):
            ax.spines[spine].set_color(self.BORDER)
        ax.legend(facecolor=self.BG_CARD, edgecolor=self.BORDER,
                  labelcolor=self.TEXT_PRI, fontsize=9, framealpha=.9)
        ax.grid(True, alpha=0.08, color=self.TEXT_MUTED)

    # ── Run logic ─────────────────────────────────────────────────
    def _run_threaded(self):
        if self.is_running:
            return
        self.is_running = True
        self.run_btn.configure(text="⏳  RUNNING …", bg=self.TEXT_MUTED, state="disabled")
        self.status_var.set("⟳ Processing…")
        self.status_lbl.configure(fg=self.WARNING)
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        try:
            sym = self.symbol.get().strip().upper()
            per = self.period.get().strip()
            ep  = int(self.epochs.get())

            if self.mode.get() == "predict":
                data = run_prediction(sym, per, ep,
                                      int(self.window.get()),
                                      int(self.sims.get()))
                self.root.after(0, lambda: self._plot_predict(data, sym))
            else:
                data = run_agent(sym, per, ep,
                                float(self.initial.get()),
                                int(self.skip.get()),
                                int(self.sims.get()))
                self.root.after(0, lambda: self._plot_agent(data, sym))
        except Exception as exc:
            self.root.after(0, lambda: self._on_error(str(exc)))

    # ── Prediction chart ──────────────────────────────────────────
    def _plot_predict(self, data, sym):
        self._clear_graph()
        self.ph.pack_forget()
        self.graph_frame.pack(fill="both", expand=True)

        self.fig = Figure(figsize=(8, 5), dpi=100, facecolor=self.BG_CARD)
        ax = self.fig.add_subplot(111)

        ax.plot(data["real"], color=self.CHART_LINE, lw=1.6,
                label="Real Price", alpha=.92)
        ax.plot(data["pred"], color=self.CHART_PRED, lw=1.6,
                label="Prediction", alpha=.88, linestyle="--")

        self._style_ax(ax, f"{sym}  —  Price Prediction")
        self.fig.tight_layout(pad=2.5)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self._on_done(f"✓ Prediction complete for {sym}")

    # ── Agent / trading chart ─────────────────────────────────────
    def _plot_agent(self, data, sym):
        self._clear_graph()
        self.ph.pack_forget()
        self.graph_frame.pack(fill="both", expand=True)

        self.fig = Figure(figsize=(8, 5), dpi=100, facecolor=self.BG_CARD)
        ax = self.fig.add_subplot(111)

        prices = data["prices"]
        ax.plot(prices, color=self.CHART_LINE, lw=1.6, label="Price", alpha=.92)

        if data["buys"]:
            bi = [i for i in data["buys"] if i < len(prices)]
            ax.scatter(bi, [prices[i] for i in bi],
                       color=self.SUCCESS, marker="^", s=56,
                       zorder=5, label="Buy", alpha=.9)
        if data["sells"]:
            si = [i for i in data["sells"] if i < len(prices)]
            ax.scatter(si, [prices[i] for i in si],
                       color=self.DANGER, marker="v", s=56,
                       zorder=5, label="Sell", alpha=.9)

        profit = data["profit"]
        sign   = "+" if profit >= 0 else ""
        pcol   = self.SUCCESS if profit >= 0 else self.DANGER
        self._style_ax(ax,
                       f"{sym}  —  Trading   |   Profit: {sign}${profit:,.2f}",
                       title_color=pcol)
        self.fig.tight_layout(pad=2.5)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self._on_done(f"✓ Trading done for {sym}  |  Profit: {sign}${profit:,.2f}")

    # ── Status helpers ────────────────────────────────────────────
    def _on_done(self, msg):
        self.is_running = False
        self.run_btn.configure(text="▶   RUN  ANALYSIS", bg=self.ACCENT, state="normal")
        self.status_var.set(msg)
        self.status_lbl.configure(fg=self.SUCCESS)

    def _on_error(self, msg):
        self.is_running = False
        self.run_btn.configure(text="▶   RUN  ANALYSIS", bg=self.ACCENT, state="normal")
        self.status_var.set(f"✗ {msg}")
        self.status_lbl.configure(fg=self.DANGER)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()