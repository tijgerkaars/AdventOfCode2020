import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
import datetime
def plot_system(sol, p, plot_title=None,title_marker=None):
    
    def add_plot(plot, group, title = None):
        for each in indexes[group]:
            # l = legend[each] if legend[each] not in l_set else None
            # l_set.add(l)
            l = legend[each] if legend[each] not in l_dict.keys() else None
            plot.plot(sol.t,sol.y[each,:], lw=2, label=l, color=colors[each])
            plot.grid(True)
            plot.set_xlabel('Times (/s)')
            plot.set_ylabel('Moles')
            l_dict[legend[each]] = plot
        title = group if title == None else title
        plot.set_title(f"{title}")

    def add_big_plot(y1,x1,y2,x2,group, plot = None):
        if plot == None:
            plot = axs[y1, x1].get_gridspec()
            for ax in np.reshape(axs[y1:y2+1,x1:x2+1], -1):
                ax.remove()
            axbig = fig.add_subplot(plot[y1:y2+1,x1:x2+1])
        add_plot(axbig, group)
        return axbig

    indexes = p.indexes
    legend  = p.small_legend
    colors  = cm.hsv(np.linspace(0, 1, len(sol.y[:]))) # pylint: disable=no-member

    fig, axs = plt.subplots(4,3)
    
    for ax in np.reshape(axs[:,-1], -1):
        ax.remove()


    # l_set = set()
    l_dict  = {}
    # print(sol.y)
    add_plot(axs[0,0],'initiator')
    add_plot(axs[1,0],'co_initiator')
    add_plot(axs[2,0],'inhibitor')
    add_plot(axs[3,0],'initiator')
    add_plot(axs[3,0],'co_initiator')
    add_plot(axs[3,0], 'inhibitor', 'init+inhib')
    add_big_plot(0,1,3,1, 'small_system')

    plot_title = p.prefix if plot_title == None else plot_title
    fig.suptitle(f'{plot_title}')
    fig.legend(loc='upper right', borderaxespad=0.1, bbox_to_anchor=(1.01, 1))

    fig.canvas.mpl_connect('key_press_event', lambda e, plt=plt, fig=fig: plt.close(fig) if e.key == 'escape' else None) # allows closing the plot with escape key

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    fig.tight_layout()

    date = str(datetime.datetime.today()).split()[0]
    fname = f'{date}_conv_{p.figures}_init_{"" if title_marker == None else title_marker +"_"}{p.init_intensity}_inhib_{p.inhi_intensity}'; p.figures += 1
    plt.savefig(rf'{p.file_loc}{fname}')

    if p.show_figs['all'] or p.show_figs['tests']:
        plt.show()




if __name__ == "__main__":
    import run_main