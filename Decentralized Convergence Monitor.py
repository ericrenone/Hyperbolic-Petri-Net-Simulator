import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Configuration
N_NODES = 1000
ALPHA = 0.15
ROUNDS = 500 # Increased for longer monitoring
NOISE_STD = 0.05
HIST_BINS = np.linspace(0, 5, 40)

class KineticEngine:
    def __init__(self, n_nodes: int = N_NODES):
        self.nodes = np.random.uniform(-10, 10, (n_nodes, 2))
        self.history_mean_vel: list[float] = []

    def update(self) -> tuple[np.ndarray, float]:
        mean_pos = np.mean(self.nodes, axis=0)
        drift = ALPHA * (mean_pos - self.nodes)
        noise = np.random.normal(0, NOISE_STD, self.nodes.shape)
        movement = drift + noise
        self.nodes += movement
        velocity = np.linalg.norm(movement, axis=1)
        mean_velocity = np.mean(velocity)
        self.history_mean_vel.append(mean_velocity)
        return velocity, mean_velocity

def update_histogram(bar_container, counts: np.ndarray):
    total = counts.sum()
    if total > 0:
        # Normalize to density
        density = counts / total / np.diff(HIST_BINS)
        for rect, h in zip(bar_container, density):
            rect.set_height(h)

def animate(frame: int, engine: KineticEngine, bar_container, line_vel, ax_time):
    velocity, _ = engine.update()
    
    # 1. Update Histogram
    counts, _ = np.histogram(velocity, bins=HIST_BINS)
    update_histogram(bar_container, counts)

    # 2. Update Time Series
    y_data = engine.history_mean_vel
    x_data = np.arange(len(y_data))
    line_vel.set_data(x_data, y_data)
    
    # 3. Dynamic Scaling (Crucial for "Real-Time" feel)
    ax_time.set_xlim(0, max(100, frame + 10))
    if y_data:
        # Dynamic Y-limits for Log Scale
        current_min = max(min(y_data) * 0.5, 1e-5)
        current_max = max(y_data) * 2.0
        ax_time.set_ylim(current_min, current_max)

    return [line_vel] + list(bar_container)

if __name__ == "__main__":
    plt.style.use('dark_background')
    fig, (ax_hist, ax_time) = plt.subplots(1, 2, figsize=(15, 6), facecolor='#050505')
    engine = KineticEngine()

    # Style Histogram
    ax_hist.set_facecolor('#080808')
    ax_hist.set_title("I. VELOCITY DISTRIBUTION", color='#00ffcc', pad=15)
    hist_data = np.zeros(len(HIST_BINS) - 1)
    bar_container = ax_hist.bar(HIST_BINS[:-1], hist_data, width=np.diff(HIST_BINS), 
                                color='#00ffcc', alpha=0.6, align='edge')
    ax_hist.set_ylim(0, 2.5) # Fixed density height for stability
    ax_hist.grid(True, color='#222', alpha=0.3)
    ax_hist.set_xlabel("Velocity")
    ax_hist.set_ylabel("Density")
    
    # Style Time Series
    ax_time.set_facecolor('#080808')
    ax_time.set_title("II. CONVERGENCE TREND (LOG)", color='#00ffcc', pad=15)
    line_vel, = ax_time.plot([], [], color='#00ffcc', lw=2)
    ax_time.set_yscale('log')
    ax_time.grid(True, which="both", color='#222', alpha=0.3)
    ax_time.set_xlabel("Time step")
    ax_time.set_ylabel("Mean velocity")

    # The Animation Controller
    ani = animation.FuncAnimation(
        fig, animate, frames=None, interval=30, 
        blit=False,  # Set to False to allow dynamic axis rescaling
        fargs=(engine, bar_container, line_vel, ax_time),
        cache_frame_data=False
    )

    plt.tight_layout()
    print(f"[*] MONITOR ONLINE: Tracking {N_NODES} nodes.")
    plt.show()