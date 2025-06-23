from dataclasses import dataclass
from typing import List, Optional
import tkinter as tk
from tkinter import ttk, messagebox


@dataclass
class Nutrients:
    """Simple container for nutrient values per 100 g."""
    kcal: float
    protein: float
    fat: float
    carbs: float
    fiber: float = 0.0
    vitamin_c: float = 0.0
    iron: float = 0.0


# Example local data used when an external API is unavailable. In a real
# application this would be replaced by an HTTP request.
LOCAL_FOOD_DB = {
    "banana": Nutrients(kcal=89, protein=1.1, fat=0.3, carbs=23, fiber=2.6, vitamin_c=8.7, iron=0.3),
    "oats": Nutrients(kcal=389, protein=16.9, fat=6.9, carbs=66.3, fiber=10.6, iron=4.7),
    "milk": Nutrients(kcal=42, protein=3.4, fat=1.0, carbs=5.0),
}


def get_nutrients(food_name: str) -> Optional[Nutrients]:
    """Look up nutrient data from the local database."""
    return LOCAL_FOOD_DB.get(food_name.lower())


@dataclass
class Entry:
    name: str
    grams: float
    nutrients: Nutrients


class Tracker:
    def __init__(self) -> None:
        self.entries: List[Entry] = []

    def add(self, name: str, grams: float) -> None:
        base = get_nutrients(name)
        if base is None:
            raise ValueError(f"Unbekanntes Lebensmittel: {name}")
        factor = grams / 100
        nutrients = Nutrients(
            kcal=base.kcal * factor,
            protein=base.protein * factor,
            fat=base.fat * factor,
            carbs=base.carbs * factor,
            fiber=base.fiber * factor,
            vitamin_c=base.vitamin_c * factor,
            iron=base.iron * factor,
        )
        self.entries.append(Entry(name=name, grams=grams, nutrients=nutrients))

    def summary(self) -> Nutrients:
        total = Nutrients(0, 0, 0, 0)
        for e in self.entries:
            total.kcal += e.nutrients.kcal
            total.protein += e.nutrients.protein
            total.fat += e.nutrients.fat
            total.carbs += e.nutrients.carbs
            total.fiber += e.nutrients.fiber
            total.vitamin_c += e.nutrients.vitamin_c
            total.iron += e.nutrients.iron
        return total

    def report(self) -> str:
        t = self.summary()
        lines = ["Tagesbilanz:"]
        lines.append(f"Kalorien: {t.kcal:.1f} kcal")
        lines.append(f"Protein: {t.protein:.1f} g")
        lines.append(f"Fett: {t.fat:.1f} g")
        lines.append(f"Kohlenhydrate: {t.carbs:.1f} g")
        lines.append(f"Ballaststoffe: {t.fiber:.1f} g")
        lines.append(f"Vitamin C: {t.vitamin_c:.1f} mg")
        lines.append(f"Eisen: {t.iron:.1f} mg")
        return "\n".join(lines)


class TrackerGUI:
    def __init__(self, tracker: Tracker) -> None:
        self.tracker = tracker
        self.root = tk.Tk()
        self.root.title("Ernährungstracker")

        self.food_var = tk.StringVar(value=list(LOCAL_FOOD_DB.keys())[0])
        self.grams_var = tk.StringVar()

        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Lebensmittel:").grid(row=0, column=0, sticky="w")
        self.food_combo = ttk.Combobox(frame, textvariable=self.food_var,
                                       values=list(LOCAL_FOOD_DB.keys()), state="readonly")
        self.food_combo.grid(row=0, column=1, sticky="ew")

        ttk.Label(frame, text="Gramm:").grid(row=1, column=0, sticky="w")
        self.grams_entry = ttk.Entry(frame, textvariable=self.grams_var)
        self.grams_entry.grid(row=1, column=1, sticky="ew")

        add_btn = ttk.Button(frame, text="Hinzufügen", command=self.add)
        add_btn.grid(row=2, column=0, columnspan=2, pady=5)

        self.summary_text = tk.Text(frame, width=40, height=7, state="disabled")
        self.summary_text.grid(row=3, column=0, columnspan=2)

        frame.columnconfigure(1, weight=1)

    def add(self) -> None:
        name = self.food_var.get()
        try:
            grams = float(self.grams_var.get())
        except ValueError:
            messagebox.showerror("Fehler", "Bitte Grammzahl eingeben")
            return
        try:
            self.tracker.add(name, grams)
        except ValueError as e:
            messagebox.showerror("Fehler", str(e))
            return
        self.grams_var.set("")
        self.update_summary()

    def update_summary(self) -> None:
        report = self.tracker.report()
        self.summary_text.configure(state="normal")
        self.summary_text.delete("1.0", "end")
        self.summary_text.insert("1.0", report)
        self.summary_text.configure(state="disabled")

    def run(self) -> None:
        self.root.mainloop()


def main() -> None:
    tracker = Tracker()
    gui = TrackerGUI(tracker)
    gui.run()


if __name__ == "__main__":
    main()
