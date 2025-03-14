'Plotting routines for simulation results'

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.figsize'] = [10, 6]


def plot(*args, fig_kwargs={}, **kwargs):
        '''
        matplotlib plotting wrapper.

            Parameters
            ----------
            *args:
                Inputs to ``pyplot.plot``.
            fig_kwargs : dict, optional
                Keyword arguments for ``pyplot.subplots``.
            xlabel : str, optional
                x-axis label, LaTeX math mode, no $s needed.
            ylabel : str, optional
                y-axis label, LaTeX math mode, no $s needed.
            xrange : tuple, optional
                x range to plot over.
            yrange : tuple, optional
                y range to plot over.
            overplot : bool, optional
                If True, plot on top of the current figure.
            gcf : bool, optional
                If True, do not start a new figure.
            onedhists : bool, optional
                If True, make one-d histograms on the sides.
            onedhistcolor : str, optional
                Histogram color.
            onedhistfc : str, optional
                Histogram fill color.
            onedhistec : str, optional
                Histogram edge color.
            onedhistxnormed : bool, optional
                If True, normalize the x-axis histogram.
            onedhistynormed : bool, optional
                If True, normalize the y-axis histogram.
            onedhistxweights : numpy.ndarray, optional
                Weights for the x-axis histogram.
            onedhistyweights : numpy.ndarray, optional
                Weights for the y-axis histogram.
            bins : int, optional
                Number of bins for the one-d histograms.
            semilogx : bool, optional
                If True, plot the x-axis on a log scale.
            semilogy : bool, optional
                If True, plot the y-axis on a log scale.
            loglog : bool, optional
                If True, plot both axes on a log scale.
            scatter : bool, optional
                If True, use ``pyplot.scatter`` instead of ``pyplot.plot``.
            colorbar : bool, optional
                If True, add a colorbar.
            crange : tuple, optional
                Range for the colorbar.
            clabel : str, optional
                Label for the colorbar.
            **kwargs
                All other keyword arguments are passed to ``pyplot.plot`` or ``pyplot.scatter``.

        '''
        fig, ax = plt.subplots(**fig_kwargs)
        ax.plot(*args, **kwargs)

def scatter(*args, fig_kwargs={}, **kwargs):
        '''
        Scatter plot of the results of the suite.

        Parameters
        ----------
        *args:
            Inputs to ``pyplot.scatter``.
        fig_kwargs : dict, optional
            Keyword arguments for ``pyplot.subplots``.
        xlabel : str, optional
            x-axis label, LaTeX math mode, no $s needed.
        ylabel : str, optional
            y-axis label, LaTeX math mode, no $s needed.
        '''
        fig, ax = plt.subplots(**fig_kwargs)
        ax.scatter(*args, **kwargs)