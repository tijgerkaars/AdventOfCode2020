def plot(t, y, legend, indexes, title='PLOT', show=True):
    import numpy as np
    import matplotlib.pyplot as plt

    
    def onpick(event):
        # on the pick event, find the orig line corresponding to the
        # legend proxy line, and toggle the visibility
        legline = event.artist
        origline = lined[legline][0]
        vis = not origline.get_visible()
        origline.set_visible(vis)
        # Change the alpha on the line in the legend so we can see what lines
        # have been toggled
        if vis:
            legline.set_alpha(1.0)
        else:
            legline.set_alpha(0.2)
        fig.canvas.draw()

    # TODO add axis labels
    fig, ax = plt.subplots()
    ax.set_title(title)
    lines = [ax.plot(t,y[i,:], lw=2, label=legend[i])   for i in indexes]
    #line1, = ax.plot(t, y1, lw=2, color='red', label='1 HZ')
    #line2, = ax.plot(t, y2, lw=2, color='blue', label='2 HZ')
    leg = ax.legend(loc=2, bbox_to_anchor=(1.02, 1), borderaxespad=0. , fancybox=True, shadow=True)
    leg.get_frame().set_alpha(0.4)
    


    # we will set up a dict mapping legend line to orig line, and enable
    # picking on the legend line
    # lines = [line1, line2]
    lined = dict()
    for legline, origline in zip(leg.get_lines(), lines):
        legline.set_picker(5)  # 5 pts tolerance
        lined[legline] = origline


    fig.canvas.mpl_connect('pick_event', onpick)
    fig.canvas.mpl_connect('key_press_event', lambda e, plt=plt, fig=fig: plt.close(fig) if e.key == 'escape' else None) # allows closing the plot with escape key
    
    #plt.subplots_adjust(right=bbox)
    
    

    plt.grid(True)
    plt.tight_layout()
    if show:
        plt.show()
    else:
        return plt


if __name__ == '__main__':
    import run_main