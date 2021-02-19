import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

def plot_series(sols, p, labels = None, title=None, title_marker=None):
    fig, ax = plt.subplots() # pylint: disable=unused-variable
    fig.canvas.mpl_connect('key_press_event', lambda e, plt=plt, fig=fig: plt.close(fig) if e.key == 'escape' else None) # allows closing the plot with escape key

    ax.set_title(title)

    mon_i = 15
    bond_i = 11
    plots = []
    for i,sol in enumerate(sols):
        line = ax.plot(sol.t,(sol.y[bond_i,:]/2)/sol.y[mon_i,0], label=labels[i]) # pylint: disable=unused-variable
        plots.append(line)
    plt.grid(True)
    plt.legend()
    y_padding = 0.1; plt.ylim(top=1+y_padding, bottom = -y_padding)
    ax.set_xlabel('Times (/s)')
    ax.set_ylabel('Conversion %')
    ax.set_title(f"{title}")
    plt.tight_layout()

    date = str(datetime.datetime.today()).split()[0]
    fname = f'{date}_conv_serie_{p.figures}_{"" if title_marker == None else title_marker +"_"}init_{p.init_intensity}_inhib_{p.inhi_intensity}'; p.figures += 1
    plt.savefig(rf'{p.file_loc}{fname}')
    
    if p.show_figs['all'] or p.show_figs['tests']:
        plt.show()








if __name__ == '__main__':
    import run_main