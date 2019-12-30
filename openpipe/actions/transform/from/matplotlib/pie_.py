"""
Create figure using matplotlib
"""
from openpipe.pipeline.engine import ActionRuntime
from PIL import Image
import matplotlib
import io

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # NOQA: E402


class Action(ActionRuntime):

    required_config = """
    path:   # Filename of the file to be generated
    """

    optional_config = """
    label_key:  "label" # Key to be used for the labels
    value_key:  "value" # Key to be used for the values
    """

    def on_input(self, item):
        if isinstance(item, dict):
            self.labels = item.keys()
            self.values = item.values()
        elif isinstance(item, list):
            self.labels = list(map(lambda x: x.get(self.config["label_key"]), item))
            self.values = list(map(lambda x: x.get(self.config["value_key"]), item))

    def on_finish(self, reason):
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = self.labels
        values = self.values
        fig1, ax1 = plt.subplots()
        ax1.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
        ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()

        output_filename = self.config["path"]
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=400)
        buf.seek(0)
        im = Image.open(buf)
        im.save(output_filename)
        buf.close()
        im.close()
