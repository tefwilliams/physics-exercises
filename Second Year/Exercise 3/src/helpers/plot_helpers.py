from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from .methods import IterationData


def plot_fall(data: dict[str, IterationData]):
    fig, axes = plt.subplots(3, 1, figsize=(8, 12), sharex=True)
    ax1: Axes = axes[0]
    ax2: Axes = axes[1]
    ax3: Axes = axes[2]

    for records in data.values():
        ax1.plot(records["time"], records["height"])
        ax2.plot(records["time"], records["velocity"])
        ax3.plot(records["time"], records["acceleration"])

    ax1.set_ylabel("Height ($m$)")
    ax2.set_ylabel("Velocity ($ms^{-1}$)")
    ax3.set_ylabel("Acceleration ($ms^{-2}$)")
    ax3.set_xlabel("Time ($s$)")

    fig.legend(data.keys())
    fig.show()
