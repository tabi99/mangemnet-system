from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class ChartCanvas(FigureCanvasQTAgg):
    def __init__(self):
        self.fig = Figure(figsize=(5,4))
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)

    def bar_chart(self, labels, values, title, colors=None):
        self.ax.clear()
        # Agar colors provide kiye gaye hain, use kare, warna default matplotlib colors
        if colors:
            self.ax.bar(labels, values, color=colors)
        else:
            self.ax.bar(labels, values)
        self.ax.set_title(title, fontsize=14, fontweight='bold')
        self.ax.set_ylabel("Marks", fontsize=12)
        self.ax.set_xticklabels(labels, rotation=45, ha='right')
        self.fig.tight_layout()
        self.draw()

    def pie_chart(self, labels, values, title, colors=None):
        self.ax.clear()
        if colors:
            self.ax.pie(values, labels=labels, autopct="%1.1f%%", colors=colors)
        else:
            self.ax.pie(values, labels=labels, autopct="%1.1f%%")
        self.ax.set_title(title, fontsize=14, fontweight='bold')
        self.draw()