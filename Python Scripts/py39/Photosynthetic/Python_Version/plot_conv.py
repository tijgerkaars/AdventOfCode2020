import datetime
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

def plot_conv(sol, p, title=None, title_marker=None):
    # print(p.small_legend)
    t,y = sol.t, sol.y
    fig, ax = plt.subplots() # pylint: disable=unused-variable

    fig.canvas.mpl_connect('key_press_event', lambda e, plt=plt, fig=fig: plt.close(fig) if e.key == 'escape' else None) # allows closing the plot with escape key

    ax.set_title(title)


    mon_i = 15
    bond_i = 11
    bond1 = ax.plot(t,(y[bond_i,:]/2)/y[mon_i,0], label="Conversion") # pylint: disable=unused-variable

    plt.grid(True)
    plt.legend()
    ax.set_xlabel('Times (/s)')
    ax.set_ylabel('Conversion %')
    ax.set_title(f"{title}")
    plt.tight_layout()

    date = str(datetime.datetime.today()).split()[0]
    fname = f'{date}_conc_{p.figures}_init_{"" if title_marker == None else title_marker +"_"}{p.init_intensity}_inhib_{p.inhi_intensity}'; p.figures += 1
    plt.savefig(rf'{p.file_loc}{fname}')
    
    if p.show_figs['all'] or p.show_figs['tests']:
        plt.show()








if __name__ == '__main__':
    import run_main