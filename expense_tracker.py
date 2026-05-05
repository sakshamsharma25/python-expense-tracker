import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "expenses_data.json"

# ── Data Layer ──────────────────────────────────────────────────────────────

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"budget": 0.0, "expenses": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ── Main App ─────────────────────────────────────────────────────────────────

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Expense & Budget Tracker")
        self.root.geometry("780x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1B2A4A")

        self.data = load_data()

        # Fonts
        self.font_title  = ("Segoe UI", 20, "bold")
        self.font_label  = ("Segoe UI", 11)
        self.font_bold   = ("Segoe UI", 11, "bold")
        self.font_small  = ("Segoe UI", 10)
        self.font_big    = ("Segoe UI", 26, "bold")

        # Colors
        self.BG      = "#1B2A4A"
        self.CARD    = "#243355"
        self.GOLD    = "#C49A2A"
        self.WHITE   = "#FFFFFF"
        self.LIGHT   = "#D0D8EC"
        self.GREEN   = "#2ECC71"
        self.RED     = "#E74C3C"
        self.YELLOW  = "#F1C40F"

        self.CATEGORIES = ["Food", "Transport", "Shopping", "Entertainment",
                           "Health", "Education", "Bills", "Other"]

        self._build_ui()
        self._refresh()

# ── UI Construction ───────────────────────────────────────────────────

    def _build_ui(self):
        # ── Title Bar
        title_bar = tk.Frame(self.root, bg=self.BG)
        title_bar.pack(fill="x", padx=20, pady=(18, 0))

        tk.Label(title_bar, text="💰 Expense & Budget Tracker",
                 font=self.font_title, bg=self.BG, fg=self.GOLD).pack(side="left")

        tk.Label(title_bar, text="by Saksham Sharma",
                 font=self.font_small, bg=self.BG, fg=self.LIGHT).pack(side="right", pady=6)

        # ── Summary Cards Row
        cards_frame = tk.Frame(self.root, bg=self.BG)
        cards_frame.pack(fill="x", padx=20, pady=12)

        self.card_budget  = self._make_card(cards_frame, "Monthly Budget", "₹0.00", self.GOLD)
        self.card_spent   = self._make_card(cards_frame, "Total Spent",    "₹0.00", self.RED)
        self.card_balance = self._make_card(cards_frame, "Balance Left",   "₹0.00", self.GREEN)

        for c in [self.card_budget, self.card_spent, self.card_balance]:
            c[0].pack(side="left", expand=True, fill="both", padx=6)

        # ── Main body (left form + right list)
        body = tk.Frame(self.root, bg=self.BG)
        body.pack(fill="both", expand=True, padx=20, pady=0)

        self._build_form(body)
        self._build_list(body)

        # ── Bottom status bar
        self.status_var = tk.StringVar(value="Ready.")
        tk.Label(self.root, textvariable=self.status_var,
                 font=self.font_small, bg=self.GOLD, fg=self.BG,
                 anchor="w", padx=10).pack(fill="x", side="bottom")

    def _make_card(self, parent, label, value, color):
        frame = tk.Frame(parent, bg=self.CARD, relief="flat", bd=0)
        tk.Label(frame, text=label, font=self.font_small,
                 bg=self.CARD, fg=self.LIGHT).pack(pady=(10, 0))
        val_lbl = tk.Label(frame, text=value, font=self.font_big,
                           bg=self.CARD, fg=color)
        val_lbl.pack(pady=(2, 10))
        return (frame, val_lbl)

    def _build_form(self, parent):
        form = tk.Frame(parent, bg=self.CARD, bd=0)
        form.pack(side="left", fill="y", padx=(0, 10), pady=4, ipadx=14, ipady=10)

        tk.Label(form, text="Add / Settings", font=self.font_bold,
                 bg=self.CARD, fg=self.GOLD).grid(row=0, column=0, columnspan=2,
                                                  sticky="w", pady=(8, 12), padx=8)

        # Budget input
        self._lbl(form, "Monthly Budget (₹)", 1)
        self.budget_entry = self._entry(form, 1)
        self.budget_entry.insert(0, str(self.data["budget"]))

        tk.Button(form, text="Set Budget", font=self.font_small,
                  bg=self.GOLD, fg=self.BG, relief="flat", cursor="hand2",
                  command=self._set_budget).grid(row=2, column=0, columnspan=2,
                                                 sticky="ew", padx=8, pady=(2, 14))

        ttk.Separator(form, orient="horizontal").grid(row=3, column=0,
                                                      columnspan=2, sticky="ew", padx=8, pady=6)

        # Expense inputs
        self._lbl(form, "Description", 4)
        self.desc_entry = self._entry(form, 4)

        self._lbl(form, "Amount (₹)", 5)
        self.amount_entry = self._entry(form, 5)

        self._lbl(form, "Category", 6)
        self.cat_var = tk.StringVar(value=self.CATEGORIES[0])
        cat_menu = ttk.Combobox(form, textvariable=self.cat_var,
                                values=self.CATEGORIES, state="readonly",
                                font=self.font_small, width=18)
        cat_menu.grid(row=6, column=1, sticky="ew", padx=8, pady=3)

        self._lbl(form, "Date", 7)
        self.date_entry = self._entry(form, 7)
        self.date_entry.insert(0, datetime.today().strftime("%d-%m-%Y"))

        tk.Button(form, text="➕  Add Expense", font=self.font_bold,
                  bg=self.GREEN, fg=self.BG, relief="flat", cursor="hand2",
                  command=self._add_expense).grid(row=8, column=0, columnspan=2,
                                                  sticky="ew", padx=8, pady=(10, 4))

        tk.Button(form, text="🗑  Delete Selected", font=self.font_small,
                  bg=self.RED, fg=self.WHITE, relief="flat", cursor="hand2",
                  command=self._delete_expense).grid(row=9, column=0, columnspan=2,
                                                     sticky="ew", padx=8, pady=2)

        tk.Button(form, text="🔄  Clear All Data", font=self.font_small,
                  bg="#4A3030", fg=self.LIGHT, relief="flat", cursor="hand2",
                  command=self._clear_all).grid(row=10, column=0, columnspan=2,
                                                sticky="ew", padx=8, pady=2)

    def _build_list(self, parent):
        list_frame = tk.Frame(parent, bg=self.CARD)
        list_frame.pack(side="left", fill="both", expand=True, pady=4)

        tk.Label(list_frame, text="Expense History", font=self.font_bold,
                 bg=self.CARD, fg=self.GOLD).pack(anchor="w", padx=12, pady=(10, 4))

        # Filter bar
        filter_bar = tk.Frame(list_frame, bg=self.CARD)
        filter_bar.pack(fill="x", padx=12, pady=(0, 6))

        tk.Label(filter_bar, text="Filter:", font=self.font_small,
                 bg=self.CARD, fg=self.LIGHT).pack(side="left")

        self.filter_var = tk.StringVar(value="All")
        filter_opts = ["All"] + self.CATEGORIES
        ttk.Combobox(filter_bar, textvariable=self.filter_var,
                     values=filter_opts, state="readonly",
                     font=self.font_small, width=14).pack(side="left", padx=6)

        tk.Button(filter_bar, text="Apply", font=self.font_small,
                  bg=self.GOLD, fg=self.BG, relief="flat", cursor="hand2",
                  command=self._refresh).pack(side="left")

        # Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=self.BG, foreground=self.WHITE,
                        fieldbackground=self.BG, rowheight=26,
                        font=self.font_small)
        style.configure("Treeview.Heading", background=self.CARD,
                        foreground=self.GOLD, font=self.font_bold)
        style.map("Treeview", background=[("selected", self.GOLD)],
                  foreground=[("selected", self.BG)])

        cols = ("Date", "Description", "Category", "Amount")
        self.tree = ttk.Treeview(list_frame, columns=cols,
                                 show="headings", selectmode="browse")

        widths = [90, 180, 110, 90]
        for col, w in zip(cols, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical",
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=(0, 10))
        scrollbar.pack(side="right", fill="y", pady=(0, 10), padx=(0, 6))

# ── Helpers ───────────────────────────────────────────────────────────

    def _lbl(self, parent, text, row):
        tk.Label(parent, text=text, font=self.font_small,
                 bg=self.CARD, fg=self.LIGHT).grid(row=row, column=0,
                                                   sticky="w", padx=8, pady=3)

    def _entry(self, parent, row):
        e = tk.Entry(parent, font=self.font_small, bg=self.BG,
                     fg=self.WHITE, insertbackground=self.WHITE,
                     relief="flat", bd=4, width=20)
        e.grid(row=row, column=1, sticky="ew", padx=8, pady=3)
        return e

    def _set_status(self, msg, color=None):
        self.status_var.set("  " + msg)

# ── Actions ───────────────────────────────────────────────────────────

    def _set_budget(self):
        try:
            b = float(self.budget_entry.get())
            if b < 0:
                raise ValueError
            self.data["budget"] = b
            save_data(self.data)
            self._refresh()
            self._set_status(f"Budget set to ₹{b:,.2f}")
        except ValueError:
            messagebox.showerror("Invalid", "Please enter a valid positive number for budget.")

    def _add_expense(self):
        desc   = self.desc_entry.get().strip()
        amount = self.amount_entry.get().strip()
        cat    = self.cat_var.get()
        date   = self.date_entry.get().strip()

        if not desc:
            messagebox.showerror("Missing", "Please enter a description."); return
        try:
            amount = float(amount)
            if amount <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Invalid", "Please enter a valid positive amount."); return

        self.data["expenses"].append({
            "date": date, "desc": desc, "category": cat, "amount": amount
        })
        save_data(self.data)
        self.desc_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")
        self._refresh()
        self._set_status(f"Added: {desc} — ₹{amount:,.2f}")

    def _delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select", "Please select an expense to delete."); return
        idx = self.tree.index(selected[0])

        # Map back through filter
        cat_filter = self.filter_var.get()
        filtered = [e for e in self.data["expenses"]
                    if cat_filter == "All" or e["category"] == cat_filter]
        expense = filtered[idx]
        self.data["expenses"].remove(expense)
        save_data(self.data)
        self._refresh()
        self._set_status(f"Deleted: {expense['desc']}")

    def _clear_all(self):
        if messagebox.askyesno("Confirm", "Clear ALL expenses and reset budget?"):
            self.data = {"budget": 0.0, "expenses": []}
            save_data(self.data)
            self.budget_entry.delete(0, "end")
            self.budget_entry.insert(0, "0.0")
            self._refresh()
            self._set_status("All data cleared.")

    def _refresh(self):
        # Update tree
        for row in self.tree.get_children():
            self.tree.delete(row)

        cat_filter = self.filter_var.get()
        total_spent = 0.0

        for exp in self.data["expenses"]:
            if cat_filter == "All" or exp["category"] == cat_filter:
                self.tree.insert("", "end", values=(
                    exp["date"],
                    exp["desc"],
                    exp["category"],
                    f"₹{exp['amount']:,.2f}"
                ))
            total_spent += exp["amount"]

        budget  = self.data["budget"]
        balance = budget - total_spent
        bal_color = self.GREEN if balance >= 0 else self.RED

        self.card_budget[1].config(text=f"₹{budget:,.2f}", fg=self.GOLD)
        self.card_spent[1].config(text=f"₹{total_spent:,.2f}", fg=self.RED)
        self.card_balance[1].config(text=f"₹{balance:,.2f}", fg=bal_color)


# ── Run ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
    