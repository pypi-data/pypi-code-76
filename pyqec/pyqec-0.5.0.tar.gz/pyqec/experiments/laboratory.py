import multiprocess as mup
import matplotlib.pyplot as plt


class Laboratory:
    def __init__(self, number_of_processes=None):
        self.experiments = list()
        self.number_of_processes = number_of_processes
        self.stopping_condition = None

    def add_experiment(self, experiment):
        self.experiments.append(experiment)

    def run_all_experiments_while(self, condition):
        return self.__run_all(
            lambda experiment: experiment.run_while(condition)
        )

    def run_all_experiments_n_times(self, number_of_iterations):
        def runner(experiment):
            return experiment.run_n_times(number_of_iterations)
        return self.__run_all(runner)

    def error_probabilities(self):
        return [experiment.error_probability() for experiment in self.experiments]

    def tags(self):
        return [experiment.tag() for experiment in self.experiments]

    def __number_of_processes(self):
        if self.number_of_processes:
            return self.number_of_processes
        else:
            return 1

    def __run_all(self, runner):
        with mup.Pool(self.__number_of_processes()) as pool:
            statistics = pool.map(runner, self.experiments)
            return Results(self.tags(), self.error_probabilities(), statistics)

class Results:
    def __init__(self, tags=None, probabilities=None, statistics=None):
        if tags:
            self.tags = tags
        else:
            self.tags = list()
        if probabilities:
            self.probabilities = probabilities
        else:
            self.probabilities = list()
        if statistics:
            self.statistics = statistics
        else:
            self.statistics = list()

    def group_by_tag(self):
        tags_to_results = dict()
        for (tag, prob, stat) in zip(self.tags, self.probabilities, self.statistics):
            if tag not in tags_to_results:
                tags_to_results[tag] = Results()
            tags_to_results[tag].tags.append(tag)
            tags_to_results[tag].probabilities.append(prob)
            tags_to_results[tag].statistics.append(stat)
        return tags_to_results

    def failure_rates(self):
        return [stat.failure_rate() for stat in self.statistics]

    def uncertainties(self):
        return [stat.uncertainty() for stat in self.statistics]

    def plot(self, savepath=None):
        fig, ax = self.__setup_plot() 
        results_by_tags = self.group_by_tag()
        for tag, results in results_by_tags.items():
            if tag == "":
                results.__plot_curve(ax)
            else: 
                results.__plot_curve(ax, tag)
        self.__render_plot(ax, fig, self.__has_legend(results_by_tags), savepath)

    def __setup_plot(self):
        fig, ax = plt.subplots()
        ax.set_xlabel("Error probability")
        ax.set_ylabel("Failure rate")
        return fig, ax

    def __plot_curve(self, ax, label=None):
        if label:
            ax.errorbar(
                self.probabilities,
                self.failure_rates(),
                yerr=self.uncertainties(),
                marker="o",
                markersize=4,
                label=label
            )
        else:
            ax.errorbar(
                self.probabilities,
                self.failure_rates(),
                yerr=self.uncertainties(),
                marker="o",
                markersize=4,
            )

    def __has_legend(self, results_by_tags):
        if len(results_by_tags) > 2:
            return True
        elif len(results_by_tags) == 1 and "" not in results_by_tags:
            return True
        else:
            return False

    def __render_plot(self, ax, fig, legend, savepath=None):
        if legend:
            ax.legend(frameon=False)
        if savepath:
            fig.savefig(savepath)

